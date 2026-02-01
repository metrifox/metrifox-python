"""
Checkout module for Metrifox SDK
"""

from typing import Dict, Any, Union
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
