"""
Subscriptions module for Metrifox SDK
"""

from typing import Dict, Any
from .base import BaseClient


class SubscriptionsModule:
    """Module for managing subscriptions"""

    def __init__(self, client: BaseClient):
        self._client = client

    def get_billing_history(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get billing history for a subscription

        Args:
            subscription_id: The subscription's unique ID (UUID)

        Returns:
            API response with billing history data

        Example:
            >>> history = client.subscriptions.get_billing_history("sub_uuid_123")
        """
        return self._client.get(f"subscriptions/{subscription_id}/billing-history")

    def get_entitlements_summary(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get entitlements summary for a subscription

        Args:
            subscription_id: The subscription's unique ID (UUID)

        Returns:
            API response with entitlements summary data

        Example:
            >>> summary = client.subscriptions.get_entitlements_summary("sub_uuid_123")
        """
        return self._client.get(f"subscriptions/{subscription_id}/v2/entitlements-summary")

    def get_entitlements_usage(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get entitlements usage for a subscription

        Args:
            subscription_id: The subscription's unique ID (UUID)

        Returns:
            API response with entitlements usage data

        Example:
            >>> usage = client.subscriptions.get_entitlements_usage("sub_uuid_123")
        """
        return self._client.get(f"subscriptions/{subscription_id}/v2/entitlements-usage")
