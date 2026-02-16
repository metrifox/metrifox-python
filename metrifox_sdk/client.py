"""
Main Metrifox SDK client
"""

import os
from typing import Optional, Dict, Any
from .base import BaseClient
from .customers import CustomersModule
from .usages import UsagesModule
from .checkout import CheckoutModule
from .subscriptions import SubscriptionsModule
from .exceptions import ConfigurationError


class MetrifoxClient:
    """
    Main Metrifox SDK client

    Provides access to all Metrifox API modules:
    - customers: Customer management
    - usages: Usage tracking and access control
    - checkout: Checkout URL generation

    Example:
        >>> from metrifox_sdk import MetrifoxClient
        >>>
        >>> # Initialize with API key
        >>> client = MetrifoxClient(api_key="your_api_key")
        >>>
        >>> # Or use environment variable
        >>> # METRIFOX_API_KEY=your_api_key
        >>> client = MetrifoxClient()
        >>>
        >>> # Use the modules
        >>> customer = client.customers.create({
        ...     "customer_key": "cust_123",
        ...     "customer_type": "INDIVIDUAL",
        ...     "primary_email": "user@example.com"
        ... })
        >>>
        >>> access = client.usages.check_access({
        ...     "feature_key": "premium_feature",
        ...     "customer_key": "cust_123"
        ... })
        >>>
        >>> checkout_url = client.checkout.url({
        ...     "offering_key": "premium_plan"
        ... })
    """

    DEFAULT_BASE_URL = "https://api.metrifox.com/api/v1/"
    DEFAULT_WEB_APP_BASE_URL = "https://app.metrifox.com"
    METER_SERVICE_BASE_URL = "https://api-meter.metrifox.com/"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        web_app_base_url: Optional[str] = None,
    ):
        """
        Initialize the Metrifox client

        Args:
            api_key: Your Metrifox API key. If not provided, will look for METRIFOX_API_KEY env var
            base_url: Custom API base URL (optional)
            web_app_base_url: Custom web app base URL (optional)

        Raises:
            ConfigurationError: If API key is not provided or found in environment
        """
        self.api_key = api_key or self._get_api_key_from_environment()
        if not self.api_key:
            raise ConfigurationError(
                "API key is required. Provide it via the api_key parameter "
                "or set the METRIFOX_API_KEY environment variable."
            )

        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.web_app_base_url = web_app_base_url or self.DEFAULT_WEB_APP_BASE_URL
        self.meter_service_base_url = self.METER_SERVICE_BASE_URL

        # Initialize base HTTP clients
        self._main_client = BaseClient(self.api_key, self.base_url)
        self._meter_client = BaseClient(self.api_key, self.meter_service_base_url)

        # Initialize modules
        self._customers_module = CustomersModule(self._main_client)
        self._usages_module = UsagesModule(self._main_client, self._meter_client)
        self._checkout_module = CheckoutModule(self._main_client)
        self._subscriptions_module = SubscriptionsModule(self._main_client)

    @staticmethod
    def _get_api_key_from_environment() -> Optional[str]:
        """Get API key from environment variable"""
        return os.getenv("METRIFOX_API_KEY")

    @property
    def customers(self) -> CustomersModule:
        """Access the customers module"""
        return self._customers_module

    @property
    def usages(self) -> UsagesModule:
        """Access the usages module"""
        return self._usages_module

    @property
    def checkout(self) -> CheckoutModule:
        """Access the checkout module"""
        return self._checkout_module

    @property
    def subscriptions(self) -> SubscriptionsModule:
        """Access the subscriptions module"""
        return self._subscriptions_module


def init(config: Optional[Dict[str, Any]] = None) -> MetrifoxClient:
    """
    Initialize and return a Metrifox client instance

    This is a convenience function for initializing the client.

    Args:
        config: Optional configuration dictionary with keys:
            - api_key: Your Metrifox API key
            - base_url: Custom API base URL
            - web_app_base_url: Custom web app base URL

    Returns:
        Initialized MetrifoxClient instance

    Example:
        >>> from metrifox_sdk import init
        >>>
        >>> # Initialize with config
        >>> client = init({"api_key": "your_api_key"})
        >>>
        >>> # Or with environment variable
        >>> client = init()
    """
    config = config or {}
    return MetrifoxClient(
        api_key=config.get('api_key'),
        base_url=config.get('base_url'),
        web_app_base_url=config.get('web_app_base_url')
    )
