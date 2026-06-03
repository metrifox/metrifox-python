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
        params = request.to_dict() if hasattr(request, 'to_dict') else dict(request)

        # Back-compat: the API expects `quantity`; honor the old
        # `requested_quantity` name if a caller still passes it as a dict.
        if 'requested_quantity' in params and 'quantity' not in params:
            params['quantity'] = params.pop('requested_quantity')

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
            ...     "quantity": 1
            ... })
            >>>
            >>> # Advanced usage with metadata
            >>> response = client.usages.record_usage({
            ...     "customer_key": "cust_123",
            ...     "feature_key": "premium_feature",
            ...     "event_id": "evt_unique_456",
            ...     "quantity": 5,
            ...     "credit_used": 25,
            ...     "timestamp": int(time.time() * 1000),
            ...     "metadata": {
            ...         "source": "web_app",
            ...         "session_id": "sess_xyz"
            ...     }
            ... })
        """
        data = request.to_dict() if hasattr(request, 'to_dict') else dict(request)

        # Back-compat: the API expects `quantity`; honor the old
        # `amount` name if a caller still passes it as a dict.
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
