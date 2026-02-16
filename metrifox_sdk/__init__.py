"""
Metrifox SDK for Python
A Python SDK for interacting with the Metrifox platform API.
"""

from .client import MetrifoxClient, init
from .exceptions import MetrifoxError, APIError, ConfigurationError
from .subscriptions import SubscriptionsModule
from .types import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerListRequest,
    UsageEventRequest,
    AccessCheckRequest,
    CheckoutConfig,
)

__version__ = "1.0.0"
__all__ = [
    "MetrifoxClient",
    "init",
    "MetrifoxError",
    "APIError",
    "ConfigurationError",
    "CustomerCreateRequest",
    "CustomerUpdateRequest",
    "CustomerListRequest",
    "UsageEventRequest",
    "AccessCheckRequest",
    "CheckoutConfig",
    "SubscriptionsModule",
]
