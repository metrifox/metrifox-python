"""
Checkout module for Metrifox SDK
"""

from typing import Dict, Any, Optional, Union
from .base import BaseClient
from .types import CheckoutConfig


class CheckoutModule:
    """Module for checkout and billing"""

    def __init__(self, client: BaseClient):
        self._client = client

    def url(self, config: Union[CheckoutConfig, Dict[str, Any]]) -> str:
        """
        Generate a checkout URL for a customer

        Args:
            config: Checkout configuration (CheckoutConfig or dict)

        Returns:
            Checkout URL string

        Example:
            >>> # Basic checkout URL
            >>> url = client.checkout.url({
            ...     "offering_key": "premium_plan"
            ... })
            >>>
            >>> # With billing interval
            >>> url = client.checkout.url({
            ...     "offering_key": "premium_plan",
            ...     "billing_interval": "monthly"
            ... })
            >>>
            >>> # With customer key for pre-filled checkout
            >>> url = client.checkout.url({
            ...     "offering_key": "premium_plan",
            ...     "billing_interval": "monthly",
            ...     "customer_key": "cust_123"
            ... })
        """
        params = config.to_dict() if hasattr(config, 'to_dict') else config
        response = self._client.get("products/offerings/generate-checkout-url", params=params)
        return response.get('data', {}).get('checkout_url', '')

    def card_collection_url(
        self,
        subscription_id: Optional[str] = None,
        order_id: Optional[str] = None,
    ) -> str:
        """
        Generate a card collection URL for an existing subscription or order

        Either subscription_id or order_id must be provided.

        Args:
            subscription_id: The subscription's unique ID (UUID)
            order_id: The order's unique ID (UUID)

        Returns:
            Card collection URL string

        Example:
            >>> url = client.checkout.card_collection_url(subscription_id="sub_uuid_123")
            >>> print(url)
        """
        params: Dict[str, Any] = {}
        if subscription_id is not None:
            params["subscription_id"] = subscription_id
        if order_id is not None:
            params["order_id"] = order_id
        response = self._client.get("checkout/generate-card-collection-url", params=params)
        return response.get('data', {}).get('checkout_url', '')
