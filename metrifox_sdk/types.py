"""
Type definitions for Metrifox SDK
"""

from typing import TypedDict, Optional, Literal, Dict, Any
from dataclasses import dataclass, field, asdict


# Customer Types
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
    customer_type: Optional[CustomerType] = None
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


# Usage Types
@dataclass
class UsageEventRequest:
    """Request to record a usage event"""
    customer_key: str
    event_id: str
    event_name: Optional[str] = None
    feature_key: Optional[str] = None
    amount: int = 1
    credit_used: Optional[int] = None
    timestamp: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        data = asdict(self)
        # Rename 'amount' to 'quantity' as per API requirement
        if 'amount' in data:
            data['quantity'] = data.pop('amount')
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class AccessCheckRequest:
    """Request to check feature access"""
    feature_key: str
    customer_key: str
    requested_quantity: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


# Checkout Types
@dataclass
class CheckoutConfig:
    """Configuration for checkout URL generation"""
    offering_key: str
    billing_interval: Optional[str] = None
    customer_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, removing None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


# Response Types (as TypedDict for flexibility)
class APIResponse(TypedDict, total=False):
    """Generic API response"""
    data: Any
    message: str
    meta: Dict[str, Any]


class AccessResponse(TypedDict):
    """Response from access check"""
    customer_key: str
    feature_key: str
    requested_quantity: int
    can_access: bool
    unlimited: bool
    balance: int
    used_quantity: int
    entitlement_active: bool
    prepaid: bool
    wallet_balance: int
    message: str


class UsageEventResponse(TypedDict):
    """Response from usage event recording"""
    customer_key: str
    quantity: int
    feature_key: str
