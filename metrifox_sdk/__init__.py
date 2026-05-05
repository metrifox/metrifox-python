"""
Metrifox SDK for Python
A Python SDK for interacting with the Metrifox platform API.
"""

from .client import MetrifoxClient, init
from .exceptions import MetrifoxError, APIError, ConfigurationError
from .subscriptions import SubscriptionsModule
from .wallets import WalletsModule
from .types import (
    # Request types
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerListRequest,
    UsageEventRequest,
    AccessCheckRequest,
    CheckoutConfig,
    # Response types
    APIResponse,
    CustomerResponse,
    CustomerDetailsResponse,
    CustomerProductSubscriptionResponse,
    SubscriptionViewResponse,
    WalletResponse,
    BillingHistoryItemResponse,
    BulkAssignPlanResponse,
    BulkAssignSuccessEntry,
    BulkAssignFailedEntry,
    BulkCreateCustomersResponse,
    AccessResponse,
    UsageEventResponse,
    EntitlementSummaryItem,
    EntitlementPool,
    EntitlementUsageItem,
    CreditTransactionResponse,
    CreditAllocationResponse,
    UsageEventItem,
    PaginationMeta,
    BillingConfig,
    TaxIdentification,
    ContactPerson,
    PaymentTerm,
    PaymentMethodResponse,
)

__version__ = "1.2.0"
__all__ = [
    "MetrifoxClient",
    "init",
    "MetrifoxError",
    "APIError",
    "ConfigurationError",
    "SubscriptionsModule",
    "WalletsModule",
    # Request types
    "CustomerCreateRequest",
    "CustomerUpdateRequest",
    "CustomerListRequest",
    "UsageEventRequest",
    "AccessCheckRequest",
    "CheckoutConfig",
    # Response types
    "APIResponse",
    "CustomerResponse",
    "CustomerDetailsResponse",
    "CustomerProductSubscriptionResponse",
    "SubscriptionViewResponse",
    "WalletResponse",
    "BillingHistoryItemResponse",
    "BulkAssignPlanResponse",
    "BulkAssignSuccessEntry",
    "BulkAssignFailedEntry",
    "BulkCreateCustomersResponse",
    "AccessResponse",
    "UsageEventResponse",
    "EntitlementSummaryItem",
    "EntitlementPool",
    "EntitlementUsageItem",
    "CreditTransactionResponse",
    "CreditAllocationResponse",
    "UsageEventItem",
    "PaginationMeta",
    "BillingConfig",
    "TaxIdentification",
    "ContactPerson",
    "PaymentTerm",
    "PaymentMethodResponse",
]
