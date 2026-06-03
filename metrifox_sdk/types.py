"""
Type definitions for Metrifox SDK
"""

from typing import TypedDict, Optional, Literal, Dict, Any, List
from dataclasses import dataclass, asdict


# ─── Customer Request Types ─────────────────────────────────────────────────────

CustomerType = Literal["INDIVIDUAL", "BUSINESS"]


@dataclass
class CustomerCreateRequest:
    """Request to create a new customer"""

    customer_key: str
    customer_type: CustomerType
    primary_email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    legal_name: Optional[str] = None
    display_name: Optional[str] = None
    primary_phone: Optional[str] = None
    billing_email: Optional[str] = None
    website_url: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    currency: Optional[str] = None
    account_manager: Optional[str] = None
    tax_identification_number: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class CustomerUpdateRequest:
    """Request to update an existing customer"""

    primary_email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    legal_name: Optional[str] = None
    display_name: Optional[str] = None
    primary_phone: Optional[str] = None
    billing_email: Optional[str] = None
    website_url: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    currency: Optional[str] = None
    account_manager: Optional[str] = None
    tax_identification_number: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class CustomerListRequest:
    """Request to list customers with optional filters"""

    page: Optional[int] = None
    per_page: Optional[int] = None
    search_term: Optional[str] = None
    customer_type: Optional[CustomerType] = None
    date_created: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


# ─── Usage Request Types ────────────────────────────────────────────────────────


@dataclass
class UsageEventRequest:
    """Request to record a usage event"""

    customer_key: str
    event_id: str
    event_name: Optional[str] = None
    feature_key: Optional[str] = None
    quantity: int = 1
    amount: Optional[int] = None  # deprecated alias for `quantity`
    credit_used: Optional[int] = None
    timestamp: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        data = asdict(self)
        # Back-compat: the API expects `quantity`; honor the old
        # `amount` name if a caller still passes it.
        legacy = data.pop("amount", None)
        if legacy is not None:
            data["quantity"] = legacy
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class AccessCheckRequest:
    """Request to check feature access"""

    feature_key: str
    customer_key: str
    quantity: int = 1
    requested_quantity: Optional[int] = None  # deprecated alias for `quantity`

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        # Back-compat: the API expects `quantity`; honor the old
        # `requested_quantity` name if a caller still passes it.
        legacy = data.pop("requested_quantity", None)
        if legacy is not None:
            data["quantity"] = legacy
        return data


# ─── Checkout Request Types ─────────────────────────────────────────────────────


@dataclass
class CheckoutConfig:
    """Configuration for checkout URL generation"""

    offering_key: str
    billing_interval: Optional[str] = None
    customer_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


# ─── Customer Response Types ────────────────────────────────────────────────────


class BillingConfig(TypedDict, total=False):
    """Customer billing configuration"""

    preferred_payment_gateway: Optional[str]
    preferred_payment_method: Optional[str]
    billing_email: Optional[str]
    billing_address: Optional[str]
    payment_reminder_days: Optional[int]


class TaxIdentification(TypedDict, total=False):
    """Tax identification entry"""

    type: Optional[str]
    number: Optional[str]
    country: Optional[str]


class ContactPerson(TypedDict, total=False):
    """Contact person for a customer"""

    first_name: Optional[str]
    last_name: Optional[str]
    email_address: Optional[str]
    designation: Optional[str]
    department: Optional[str]
    is_primary: bool
    phone_number: Optional[str]


class PaymentTerm(TypedDict, total=False):
    """Payment term configuration"""

    type: Optional[str]
    value: Optional[int]


class CustomerResponse(TypedDict, total=False):
    """Response from creating, updating, or getting a customer"""

    id: str
    customer_key: str
    customer_type: str
    primary_email: Optional[str]
    primary_phone: Optional[str]
    legal_name: Optional[str]
    display_name: Optional[str]
    legal_number: Optional[str]
    tax_identification_number: Optional[str]
    logo_url: Optional[str]
    website_url: Optional[str]
    account_manager: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    billing_email: Optional[str]
    timezone: Optional[str]
    language: Optional[str]
    currency: Optional[str]
    tax_status: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]
    shipping_address_line1: Optional[str]
    shipping_address_line2: Optional[str]
    shipping_city: Optional[str]
    shipping_state: Optional[str]
    shipping_country: Optional[str]
    shipping_zip_code: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    archived_at: Optional[str]
    phone_numbers: Optional[List[Dict[str, Any]]]
    email_addresses: Optional[List[Dict[str, Any]]]
    billing_configuration: Optional[BillingConfig]
    tax_identifications: Optional[List[TaxIdentification]]
    contact_people: Optional[List[ContactPerson]]
    payment_terms: Optional[List[PaymentTerm]]
    metadata: Optional[Dict[str, Any]]
    date_of_birth: Optional[str]
    documents: Any
    mid_cycle_invoice_consolidation: bool


# ─── Customer Details Response Types ────────────────────────────────────────────


class PaymentMethodResponse(TypedDict, total=False):
    """Payment method attached to a subscription"""

    id: str
    type: str
    last_four: Optional[str]
    brand: Optional[str]
    exp_month: Optional[int]
    exp_year: Optional[int]


class SubscriptionViewResponse(TypedDict, total=False):
    """A subscription within customer details"""

    id: str
    status: str
    starts_at: str
    ends_at: Optional[str]
    cancelled_at: Optional[str]
    renews_at: Optional[str]
    trial_end_date: Optional[str]
    post_trial_action: Optional[str]
    plan_name: Optional[str]
    plan_version: Optional[int]
    default_plan_id: Optional[str]
    default_plan_name: Optional[str]
    product_name: str
    product_key: str
    offering_key: str
    currency_code: str
    created_at: str
    next_billing_date: Optional[str]
    next_billing_amount: Optional[float]
    current_billing_period_start: Optional[str]
    current_billing_period_end: Optional[str]
    subscription_items: Optional[List[Dict[str, Any]]]
    upcoming_invoice: Optional[Dict[str, Any]]
    can_update_quantities: bool
    update_quantity_link: Optional[str]
    manage_addons_link: Optional[str]
    scheduled_change: Optional[str]


class CustomerProductSubscriptionResponse(TypedDict, total=False):
    """A product subscription within customer details"""

    product_key: str
    product_name: str
    status: str
    subscription: Optional[SubscriptionViewResponse]
    subscriptions_history: Optional[List[SubscriptionViewResponse]]
    payment_method: Optional[PaymentMethodResponse]


class WalletResponse(TypedDict, total=False):
    """A credit wallet"""

    id: str
    name: str
    credit_unit_singular: str
    credit_unit_plural: str
    credit_system_id: str
    balance: float
    allocations: Optional[List[Dict[str, Any]]]
    credit_key: str
    customer_key: Optional[str]
    low_balance_threshold: Optional[float]
    credit_attachment_id: Optional[str]
    topup_link: Optional[str]


class CustomerDetailsResponse(TypedDict, total=False):
    """Response from getting customer details"""

    metrifox_id: str
    customer_key: str
    customer_type: str
    primary_email: Optional[str]
    display_name: Optional[str]
    full_name: Optional[str]
    billing_email: Optional[str]
    billing_address: Optional[Dict[str, Any]]
    currency: Optional[str]
    timezone: Optional[str]
    language: Optional[str]
    tenant_checkout_username: str
    subscriptions: List[CustomerProductSubscriptionResponse]
    wallets: List[WalletResponse]
    archived_at: Optional[str]


# ─── Billing History Response ───────────────────────────────────────────────────


class BillingHistoryItemResponse(TypedDict, total=False):
    """A single billing history entry"""

    invoice_id: str
    invoice_number: Optional[str]
    issued_date: Optional[str]
    due_date: Optional[str]
    total_amount: float
    amount_paid: float
    balance_due: float
    currency: str
    status: str
    payment_method: Optional[Dict[str, Any]]
    source_type: str
    created_at: str


# ─── Bulk Operation Response Types ──────────────────────────────────────────────


class BulkAssignSuccessEntry(TypedDict, total=False):
    """A successful entry in bulk assign plan"""

    customer_key: str
    subscription_id: str


class BulkAssignFailedEntry(TypedDict, total=False):
    """A failed entry in bulk assign plan"""

    customer_key: str
    error: str


class BulkAssignPlanResponse(TypedDict, total=False):
    """Response from bulk assigning a plan"""

    succeeded: List[BulkAssignSuccessEntry]
    failed: List[BulkAssignFailedEntry]


class BulkCreateCustomersResponse(TypedDict, total=False):
    """Response from bulk creating customers"""

    total: int
    successful_count: int
    failed_count: int
    customers_created: List[Dict[str, Any]]
    customers_failed: List[Dict[str, Any]]


# ─── Usage Response Types ───────────────────────────────────────────────────────


class AccessResponse(TypedDict, total=False):
    """Response from access check"""

    customer_key: str
    feature_key: str
    requested_quantity: int
    can_access: bool
    unlimited: bool
    balance: float
    used_quantity: float
    entitlement_active: bool
    prepaid: bool
    wallet_balance: Optional[float]
    promotional: bool
    promotional_mode: Optional[str]
    message: str


class UsageEventResponse(TypedDict, total=False):
    """Response from usage event recording"""

    customer_key: str
    quantity: int
    event_name: Optional[str]
    feature_key: Optional[str]


# ─── Entitlements Types (from event service) ────────────────────────────────────


class EntitlementSummaryItem(TypedDict, total=False):
    """A single entitlement in the summary (from entitlements-summary endpoint)"""

    id: str
    subscription_id: str
    customer_id: str
    tenant_id: str
    customer_key: str
    active: bool
    subscription_item_id: Optional[str]
    purchased_qty: Optional[int]
    billing_interval: Optional[str]
    billing_interval_value: Optional[int]
    feature_key: str
    feature_name: str
    feature_type: Optional[str]
    soft_limit_enabled: bool
    included_allowance: Optional[float]
    included_allowance_reset_interval: Optional[str]
    included_allowance_reset_anchor: Optional[str]
    usage_limit: Optional[float]
    usage_limit_reset_interval: Optional[str]
    usage_limit_reset_anchor: Optional[str]
    max_carryover_amount: Optional[float]
    carryover_action: Optional[str]
    carryover_enabled: bool
    carryover_expiry_interval: Optional[str]
    carryover_expiry_value: Optional[int]
    event_names: Optional[List[str]]
    aggregation_method: Optional[str]
    price_type: str
    usage_model: Optional[str]
    entitlement_id: str
    prepaid: bool
    prepaid_credit_system_id: Optional[str]
    credit_cost: Optional[float]
    credit_source_id: Optional[str]
    provisioning_cadence: Optional[str]
    renew_date_anchor: Optional[int]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]]


class EntitlementPool(TypedDict, total=False):
    """A pool within an entitlement usage item (included, purchased, pay-as-you-go, rollover)"""

    balance: Optional[str]
    used: str
    amount: Optional[str]
    next_reset_at: Optional[str]
    billing_end_date: Optional[str]
    active: bool


class EntitlementUsageItem(TypedDict, total=False):
    """A single entitlement usage/pool entry (from entitlements-usage endpoint)"""

    id: str
    feature_key: str
    feature_name: str
    type: str
    active: bool
    included_pool: Optional[EntitlementPool]
    purchased_pool: Optional[EntitlementPool]
    pay_as_you_go_pool: Optional[EntitlementPool]
    rollover_quantity_pool: Optional[EntitlementPool]
    overage_pool: Optional[EntitlementPool]
    pool_type: Optional[str]
    mode: Optional[str]
    unlimited: Optional[bool]
    expires_at: Optional[str]


# ─── Wallet Response Types ──────────────────────────────────────────────────────


class CreditTransactionResponse(TypedDict, total=False):
    """A credit transaction within an allocation"""

    id: str
    amount: float
    created_at: str
    quantity: Optional[float]
    event_name: Optional[str]
    usage_event_id: Optional[str]


class CreditAllocationResponse(TypedDict, total=False):
    """A credit allocation within a wallet"""

    id: str
    amount: float
    consumed: float
    created_at: str
    allocation_type: str
    order_id: Optional[str]
    invoice_id: Optional[str]
    order_number: Optional[str]
    valid_until: Optional[str]
    transactions: List[CreditTransactionResponse]


# ─── Usage Event List Response ──────────────────────────────────────────────────


class UsageEventItem(TypedDict, total=False):
    """A single usage event from the events list"""

    id: str
    event_id: str
    customer_key: str
    feature_key: Optional[str]
    quantity: float
    timestamp: int
    credit_used: Optional[int]
    event_name: Optional[str]
    metadata: Dict[str, Any]


class PaginationMeta(TypedDict, total=False):
    """Pagination metadata returned with list endpoints"""

    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    total_count: int
    total_pages: int
    per_page: int


# ─── Generic API Response ───────────────────────────────────────────────────────


class APIResponse(TypedDict, total=False):
    """Generic API response wrapper"""

    data: Any
    message: str
    meta: Dict[str, Any]
