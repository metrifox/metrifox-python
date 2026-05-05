"""
Wallets module for Metrifox SDK
"""

from typing import Dict, Any, Optional
from .base import BaseClient


class WalletsModule:
    """Module for managing credit wallets"""

    def __init__(self, client: BaseClient):
        self._client = client

    def list(self, customer_key: str) -> Dict[str, Any]:
        """
        List all credit wallets for a customer

        Args:
            customer_key: The customer's unique key

        Returns:
            API response with list of wallets

        Example:
            >>> wallets = client.wallets.list("cust_123")
            >>> for wallet in wallets['data']:
            ...     print(f"{wallet['name']}: {wallet['balance']} {wallet['credit_unit_plural']}")
        """
        return self._client.get("credit_systems/v2/wallets", params={"customer_key": customer_key})

    def list_credit_allocations(
        self,
        wallet_id: str,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List credit allocations for a wallet

        Args:
            wallet_id: The wallet's unique ID (UUID)
            status: Optional filter by allocation status (e.g. "active", "expired")

        Returns:
            API response with list of credit allocations and pagination metadata

        Example:
            >>> allocations = client.wallets.list_credit_allocations("wallet_uuid_123")
            >>> for alloc in allocations['data']:
            ...     print(f"{alloc['allocation_type']}: {alloc['amount']} (consumed: {alloc['consumed']})")
        """
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        return self._client.get(f"credit_systems/v2/wallets/{wallet_id}/credit-allocations", params=params)

    def get_credit_allocation(self, allocation_id: str) -> Dict[str, Any]:
        """
        Get a single credit allocation with its transactions

        Args:
            allocation_id: The credit allocation's unique ID (UUID)

        Returns:
            API response with credit allocation data including transactions

        Example:
            >>> allocation = client.wallets.get_credit_allocation("alloc_uuid_123")
            >>> print(f"Amount: {allocation['data']['amount']}")
            >>> for txn in allocation['data']['transactions']:
            ...     print(f"  {txn['amount']} at {txn['created_at']}")
        """
        return self._client.get(f"credit_systems/v2/credit-allocations/{allocation_id}")
