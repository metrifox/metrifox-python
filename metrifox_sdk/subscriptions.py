"""
Subscriptions module for Metrifox SDK
"""

from typing import Dict, Any, List, Optional
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

    def bulk_assign_plan(
        self,
        customer_keys: List[str],
        plan_key: str,
        billing_interval: Optional[str] = None,
        currency_code: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None,
        skip_invoice: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Bulk assign a plan to multiple customers

        Args:
            customer_keys: List of customer keys to assign the plan to
            plan_key: The plan's offering key
            billing_interval: Optional billing interval (e.g. "monthly", "yearly")
            currency_code: Optional ISO 4217 currency code for localized pricing
            items: Optional list of entitlement/credit items
            skip_invoice: If True, creates subscriptions without generating invoices

        Returns:
            API response with succeeded and failed arrays

        Example:
            >>> result = client.subscriptions.bulk_assign_plan(
            ...     customer_keys=["cust_001", "cust_002"],
            ...     plan_key="pro-plan",
            ...     billing_interval="monthly"
            ... )
            >>> print(f"Succeeded: {len(result['data']['succeeded'])}")
            >>> print(f"Failed: {len(result['data']['failed'])}")
        """
        data = {
            "customer_keys": customer_keys,
            "plan_key": plan_key
        }
        if billing_interval is not None:
            data["billing_interval"] = billing_interval
        if currency_code is not None:
            data["currency_code"] = currency_code
        if items is not None:
            data["items"] = items
        if skip_invoice is not None:
            data["skip_invoice"] = skip_invoice
        return self._client.post("subscriptions/bulk-assign-plan", json=data)
