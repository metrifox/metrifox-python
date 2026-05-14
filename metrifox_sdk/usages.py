"""
Usages module for Metrifox SDK
"""

from typing import Dict, Any, Optional, Union
from .base import BaseClient
from .types import UsageEventRequest, AccessCheckRequest


class UsagesModule:
    """Module for usage tracking and access control"""

    def __init__(self, client: BaseClient, meter_service_client: BaseClient):
        self._client = client
        self._meter_client = meter_service_client

    def check_access(self, request: Union[AccessCheckRequest, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check if a customer has access to a feature

        Args:
            request: Access check request (AccessCheckRequest or dict)

        Returns:
            API response with access information

        Example:
            >>> access = client.usages.check_access({
            ...     "feature_key": "premium_feature",
            ...     "customer_key": "cust_123"
            ... })
            >>> if access['data']['can_access']:
            ...     print(f"Access granted. Balance: {access['data']['balance']}")
            ... else:
            ...     print("Access denied")
        """
        params = request.to_dict() if hasattr(request, 'to_dict') else request
        return self._meter_client.get("usage/access", params=params)

    def record_usage(self, request: Union[UsageEventRequest, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Record a usage event

        Args:
            request: Usage event data (UsageEventRequest or dict)

        Returns:
            API response confirming event recording

        Example:
            >>> # Simple usage recording
            >>> response = client.usages.record_usage({
            ...     "customer_key": "cust_123",
            ...     "event_name": "api_call",
            ...     "event_id": "evt_unique_123",
            ...     "amount": 1
            ... })
            >>>
            >>> # Advanced usage with metadata
            >>> response = client.usages.record_usage({
            ...     "customer_key": "cust_123",
            ...     "feature_key": "premium_feature",
            ...     "event_id": "evt_unique_456",
            ...     "amount": 5,
            ...     "credit_used": 25,
            ...     "timestamp": int(time.time() * 1000),
            ...     "metadata": {
            ...         "source": "web_app",
            ...         "session_id": "sess_xyz"
            ...     }
            ... })
        """
        data = request.to_dict() if hasattr(request, 'to_dict') else request

        # Ensure 'quantity' is used instead of 'amount' for API compatibility
        if 'amount' in data and 'quantity' not in data:
            data['quantity'] = data.pop('amount')

        return self._meter_client.post("usage/events", json=data)

    def list_events(
        self,
        customer_key: Optional[str] = None,
        feature_key: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List usage events with optional filters and pagination

        Args:
            customer_key: Filter events by customer key
            feature_key: Filter events by feature key
            page: Page number (starts from 1)
            per_page: Number of records per page (default 25)

        Returns:
            API response with list of usage events and pagination metadata

        Example:
            >>> events = client.usages.list_events(customer_key="cust_123")
            >>> for event in events['data']:
            ...     print(f"{event['feature_key']}: {event['quantity']} at {event['timestamp']}")
            >>> print(f"Page {events['meta']['current_page']} of {events['meta']['total_pages']}")
        """
        params: Dict[str, Any] = {}
        if customer_key is not None:
            params["customer_key"] = customer_key
        if feature_key is not None:
            params["feature_key"] = feature_key
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._meter_client.get("usage/events", params=params)

    def quantity_price(
        self,
        customer_key: str,
        feature_key: str,
        quantity: int,
    ) -> Dict[str, Any]:
        """
        Compute the price of a usage quantity for a feature

        Returns the price for a given quantity of a feature for a customer based
        on their plan. Useful for displaying upgrade/upsell costs before a customer
        commits, or for back-of-house cost estimation.

        Only available to tenants whose plan includes the finance API feature.

        Args:
            customer_key: The customer's unique key
            feature_key: The feature's unique key
            quantity: The quantity to price

        Returns:
            API response with computed price, unit, and per-tier breakdown

        Example:
            >>> price = client.usages.quantity_price(
            ...     customer_key="cust_123",
            ...     feature_key="feature_interview_booking",
            ...     quantity=500,
            ... )
            >>> print(f"{price['data']['price']} {price['data']['unit']}")
            >>> for tier in price['data'].get('applied_tiers', []):
            ...     print(f"  {tier['units_consumed']} units @ tier {tier['first_unit']}-{tier['last_unit']}")
        """
        params = {
            "customer_key": customer_key,
            "feature_key": feature_key,
            "quantity": quantity,
        }
        return self._client.get("usage/quantity-price", params=params)
