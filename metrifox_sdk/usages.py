"""
Usages module for Metrifox SDK
"""

from typing import Dict, Any, Union
from .base import BaseClient
from .types import UsageEventRequest, AccessCheckRequest, AccessResponse


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
