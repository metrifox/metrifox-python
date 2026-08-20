# Metrifox Python SDK

A Python SDK for interacting with the Metrifox platform API. Build and scale usage-based SaaS applications with comprehensive tools for customer management, usage tracking, access control, and billing.

## Installation

```bash
pip install metrifox-sdk
```

Or install from source:

```bash
git clone https://github.com/metrifox/metrifox-python.git
cd metrifox-python
pip install -e .
```

## Quick Start

### Configuration

```python
from metrifox_sdk import MetrifoxClient

# Option 1: Initialize with API key
client = MetrifoxClient(api_key="your_api_key")

# Option 2: Use environment variable
# Set METRIFOX_API_KEY=your_api_key in your environment
client = MetrifoxClient()

# Option 3: Use the init function
from metrifox_sdk import init
client = init({"api_key": "your_api_key"})
```

## Usage Tracking & Access Control

### Checking Feature Access

Check if a customer has access to a specific feature before allowing them to use it:

```python
# Check access (quantity defaults to 1)
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": "customer_123",
    "quantity": 1  # how many units to check access for
})

if access['data']['can_access']:
    print(f"Access granted. Balance: {access['data']['balance']}")
else:
    print(f"Access denied. Used: {access['data']['used_quantity']}")
```

### Recording Usage Events

Record when customers use features to track consumption against their quotas:

```python
import time

# Simple usage recording (quantity defaults to 1)
response = client.usages.record_usage({
    "customer_key": "customer_123",
    "event_name": "api_call",
    "event_id": "evt_unique_123"  # Required for idempotency
})

# Advanced usage with metadata
response = client.usages.record_usage({
    "customer_key": "customer_123",
    "feature_key": "premium_feature",
    "event_id": "evt_unique_456",
    "quantity": 5,
    "credit_used": 25,
    "timestamp": int(time.time() * 1000),  # milliseconds
    "metadata": {
        "source": "web_app",
        "session_id": "sess_xyz"
    }
})

print(response['message'])  # "Event received"
```

For a `count_unique` feature, send a `properties` mapping containing every
field configured in the feature's `aggregation_properties`:

```python
response = client.usages.record_usage({
    "customer_key": "customer_123",
    "feature_key": "feature_active_users",
    "event_id": "evt_active_user_123",
    "metadata": {
        "source": "web_app"
    },
    "properties": {
        "workspace_id": "workspace_42",
        "user_id": "user_7"
    }
})
```

### Listing Usage Events

Retrieve usage events with optional filters and pagination:

```python
# List all events
events = client.usages.list_events()

# Filter by customer and feature
events = client.usages.list_events(
    customer_key="customer_123",
    feature_key="premium_feature",
    page=1,
    per_page=25
)

for event in events['data']:
    print(f"{event['feature_key']}: qty={event['quantity']} at {event['timestamp']}")

# Pagination info
print(f"Page {events['meta']['current_page']} of {events['meta']['total_pages']}")
```

### Compute Quantity Price

Compute the price of a given quantity of a feature for a customer based on their plan. Useful for previewing upgrade costs or showing customers the cost of additional usage before they commit.

```python
price = client.usages.quantity_price(
    customer_key="customer_123",
    feature_key="feature_interview_booking",
    quantity=500
)

print(f"{price['data']['price']} {price['data']['unit']}")

# For tiered pricing, inspect the per-tier breakdown
for tier in price['data'].get('applied_tiers', []):
    print(
        f"  Tier {tier['first_unit']}-{tier['last_unit']}: "
        f"{tier['units_consumed']} units -> {tier['tier_price']}"
    )
```

> Only available to tenants whose plan includes the finance API feature.

### Complete Usage Example

Here's a complete example showing the typical access control + usage recording pattern:

```python
def use_feature(customer_key, feature_key, event_name):
    try:
        # 1. Check if customer has access
        access = client.usages.check_access({
            "feature_key": feature_key,
            "customer_key": customer_key
        })

        if access['data']['can_access']:
            # 2. Perform the actual feature logic here
            result = perform_feature_logic()

            # 3. Record usage after successful completion
            client.usages.record_usage({
                "customer_key": customer_key,
                "event_name": event_name,
                "event_id": f"evt_{result['transaction_id']}",
                "quantity": result.get('units_used', 1),
                "metadata": {
                    "execution_time_ms": result.get('duration')
                }
            })

            return {"success": True, "data": result}
        else:
            return {
                "success": False,
                "error": "Quota exceeded",
                "balance": access['data']['balance']
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Customer Management

### Creating Customers

Add new customers to your Metrifox account:

```python
# Individual customer
customer = client.customers.create({
    "customer_key": "user_12345",  # Required: unique identifier
    "customer_type": "INDIVIDUAL",  # Required: "INDIVIDUAL" or "BUSINESS"
    "primary_email": "john.doe@example.com",  # Required
    "first_name": "John",
    "last_name": "Doe",
    "primary_phone": "+1234567890",
    "billing_email": "billing@example.com",
    "timezone": "America/New_York",
    "language": "en",
    "currency": "USD"
})

# Business customer
customer = client.customers.create({
    "customer_key": "company_abc123",
    "customer_type": "BUSINESS",
    "primary_email": "contact@acmecorp.com",
    "legal_name": "ACME Corporation LLC",
    "display_name": "ACME Corp",
    "website_url": "https://acmecorp.com",
    "account_manager": "Sarah Johnson"
})

print(customer['data'])
```

### Using Type-Safe Dataclasses

For better type safety and IDE support, use the provided dataclasses:

```python
from metrifox_sdk import CustomerCreateRequest

customer_request = CustomerCreateRequest(
    customer_key="user_12345",
    customer_type="INDIVIDUAL",
    primary_email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    currency="USD"
)

customer = client.customers.create(customer_request)
```

### Updating Customers

Modify existing customer information:

```python
# Update customer (customer_key cannot be changed)
response = client.customers.update("user_12345", {
    "primary_email": "newemail@example.com",
    "first_name": "Jane",
    "currency": "EUR"
})
```

### Getting Customer Data

Retrieve customer information:

```python
# Get basic customer data
customer = client.customers.get("customer_123")
print(customer['data'])

# Get detailed customer information (includes subscriptions, wallets, etc.)
details = client.customers.get_details("customer_123")
print(details['data']['subscriptions'])

# List all customers with pagination
customers = client.customers.list({
    "page": 1,
    "per_page": 50
})

for customer in customers['data']:
    print(customer['customer_key'], customer['primary_email'])

# List with filters
customers = client.customers.list({
    "search_term": "john@example.com",
    "customer_type": "INDIVIDUAL",
    "date_created": "2025-09-01"
})

# Check if customer has active subscription
is_active = client.customers.has_active_subscription("customer_123")
if is_active:
    print("Customer has active subscription")
```

### Archiving & Unarchiving Customers

Archive customers to soft-delete them, or unarchive to restore:

```python
# Archive a customer
result = client.customers.archive("customer_123")
print(result['data']['archived_at'])  # "2025-09-01T12:00:00.000Z"

# Unarchive a customer
result = client.customers.unarchive("customer_123")
print(result['data']['archived_at'])  # None
```

### Deleting Customers

Remove customers from your account:

```python
response = client.customers.delete("customer_123")
print(response['message'])
```

### Bulk Create Customers

Create multiple customers in a single API call:

```python
result = client.customers.bulk_create([
    {
        "customer_key": "customer_001",
        "customer_type": "BUSINESS",
        "primary_email": "contact@acme.com",
        "legal_name": "Acme Corp",
        "display_name": "Acme"
    },
    {
        "customer_key": "customer_002",
        "customer_type": "INDIVIDUAL",
        "primary_email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    }
])

print(f"Total: {result['data']['total']}")
print(f"Successful: {result['data']['successful_count']}")
print(f"Failed: {result['data']['failed_count']}")
```

### Bulk Customer Import (CSV)

Upload multiple customers at once using a CSV file:

```python
result = client.customers.upload_csv("/path/to/customers.csv")

print(f"Total customers: {result['data']['total_customers']}")
print(f"Successful: {result['data']['successful_upload_count']}")
print(f"Failed: {result['data']['failed_upload_count']}")

# Handle failed imports
if result['data']['failed_upload_count'] > 0:
    for failure in result['data']['customers_failed']:
        print(f"Row {failure['row']}: {failure['error']}")
```

## Checkout & Billing

### Generate Checkout URL

Generate checkout URLs for your customers:

```python
# Basic checkout URL
checkout_url = client.checkout.url({
    "offering_key": "premium_plan"
})

# With billing interval
checkout_url = client.checkout.url({
    "offering_key": "premium_plan",
    "billing_interval": "monthly"
})

# With customer key for pre-filled checkout
checkout_url = client.checkout.url({
    "offering_key": "premium_plan",
    "billing_interval": "monthly",
    "customer_key": "customer_123"
})

print(f"Checkout URL: {checkout_url}")
```

### Generate Card Collection URL

Generate a URL to collect card details for an existing subscription or order:

```python
# For a subscription
url = client.checkout.card_collection_url(subscription_id="sub_uuid_123")

# For an order
url = client.checkout.card_collection_url(order_id="order_uuid_456")

print(f"Card collection URL: {url}")
```

### Using Type-Safe Dataclasses

```python
from metrifox_sdk import CheckoutConfig

config = CheckoutConfig(
    offering_key="premium_plan",
    billing_interval="monthly",
    customer_key="customer_123"
)

checkout_url = client.checkout.url(config)
```

## Subscriptions

### Billing History

Retrieve the billing history for a subscription:

```python
history = client.subscriptions.get_billing_history("subscription_uuid")
for item in history['data']:
    print(f"{item['invoice_number']}: {item['total_amount']} {item['currency']} - {item['status']}")
```

### Entitlements Summary

Get a summary of entitlements for a subscription:

```python
summary = client.subscriptions.get_entitlements_summary("subscription_uuid")
for item in summary['data']:
    print(f"{item['feature_name']}: allowance={item['included_allowance']} model={item['usage_model']}")
```

### Entitlements Usage

Get detailed entitlements usage with pool breakdowns for a subscription:

```python
usage = client.subscriptions.get_entitlements_usage("subscription_uuid")
for item in usage['data']:
    print(f"{item['feature_name']} ({item['type']}):")
    if item.get('included_pool'):
        pool = item['included_pool']
        print(f"  Included: {pool['used']}/{pool['amount']} used (balance: {pool['balance']})")
    if item.get('pay_as_you_go_pool'):
        pool = item['pay_as_you_go_pool']
        print(f"  Pay-as-you-go: {pool['used']} used")
```

### Bulk Assign Plan

Assign a plan to multiple customers at once:

```python
result = client.subscriptions.bulk_assign_plan(
    customer_keys=["customer_001", "customer_002"],
    plan_key="pro-plan",
    billing_interval="monthly",          # optional
    currency_code="USD",                 # optional
    items=[                              # optional: credit/feature quantities
        {"credit_key": "api_credits", "quantity": 500}
    ],
    skip_invoice=False                   # optional
)

print(f"Succeeded: {len(result['data']['succeeded'])}")
print(f"Failed: {len(result['data']['failed'])}")
```

## Wallets

### List Customer Wallets

Retrieve all credit wallets for a customer:

```python
wallets = client.wallets.list("customer_123")
for wallet in wallets['data']:
    print(f"{wallet['name']}: {wallet['balance']} {wallet['credit_unit_plural']}")
    if wallet.get('topup_link'):
        print(f"  Top-up: {wallet['topup_link']}")
```

### List Credit Allocations

Get credit allocations for a specific wallet:

```python
allocations = client.wallets.list_credit_allocations("wallet_uuid_123")
for alloc in allocations['data']:
    print(f"{alloc['allocation_type']}: {alloc['amount']} (consumed: {alloc['consumed']})")
    if alloc.get('valid_until'):
        print(f"  Expires: {alloc['valid_until']}")

# Filter by status
active = client.wallets.list_credit_allocations("wallet_uuid_123", status="active")
```

### Get a Credit Allocation

Get a single credit allocation with its transaction history:

```python
allocation = client.wallets.get_credit_allocation("allocation_uuid_123")
data = allocation['data']

print(f"Amount: {data['amount']}, Consumed: {data['consumed']}")
for txn in data['transactions']:
    print(f"  {txn['created_at']}: {txn['amount']} (event: {txn.get('usage_event_id', 'N/A')})")
```

## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from metrifox_sdk import MetrifoxClient, APIError, ConfigurationError

try:
    client = MetrifoxClient()  # Will raise ConfigurationError if no API key

    customer = client.customers.get("nonexistent_customer")

except ConfigurationError as e:
    print(f"Configuration error: {e}")

except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response_body}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Type Hints and IDE Support

The SDK includes TypedDict definitions for all API responses, giving you IDE autocompletion and type checking:

```python
from metrifox_sdk import (
    MetrifoxClient,
    # Request types (dataclasses)
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerListRequest,
    UsageEventRequest,
    AccessCheckRequest,
    CheckoutConfig,
    # Response types (TypedDicts) for annotation
    CustomerResponse,
    CustomerDetailsResponse,
    AccessResponse,
    EntitlementUsageItem,
    WalletResponse,
    BillingHistoryItemResponse,
)

# Annotate for autocompletion
customer: CustomerResponse = result['data']
print(customer['customer_key'])  # IDE knows this field exists
```

## API Reference

### Client Methods

**Initialization:**
- `MetrifoxClient(api_key, base_url, web_app_base_url, meter_service_base_url)` - Initialize the client
- `init(config)` - Convenience function to initialize the client

**Customers Module (`client.customers`):**
- `create(request)` - Create a customer
- `update(customer_key, request)` - Update a customer
- `get(customer_key)` - Get a customer
- `get_details(customer_key)` - Get detailed customer information
- `list(params)` - List customers with pagination and filters
- `delete(customer_key)` - Delete a customer
- `archive(customer_key)` - Archive a customer
- `unarchive(customer_key)` - Unarchive a customer
- `has_active_subscription(customer_key)` - Check for active subscription
- `upload_csv(file_path)` - Upload customers via CSV
- `bulk_create(customers)` - Create multiple customers at once

**Usages Module (`client.usages`):**
- `check_access(request)` - Check feature access
- `record_usage(request)` - Record a usage event
- `list_events(customer_key, feature_key, page, per_page)` - List usage events
- `quantity_price(customer_key, feature_key, quantity)` - Compute the price for a given usage quantity

**Subscriptions Module (`client.subscriptions`):**
- `get_billing_history(subscription_id)` - Get billing history for a subscription
- `get_entitlements_summary(subscription_id)` - Get entitlements summary
- `get_entitlements_usage(subscription_id)` - Get entitlements usage
- `bulk_assign_plan(customer_keys, plan_key, **options)` - Assign a plan to multiple customers

**Checkout Module (`client.checkout`):**
- `url(config)` - Generate a checkout URL
- `card_collection_url(subscription_id, order_id)` - Generate a card collection URL

**Wallets Module (`client.wallets`):**
- `list(customer_key)` - List all wallets for a customer
- `list_credit_allocations(wallet_id, status)` - List credit allocations for a wallet
- `get_credit_allocation(allocation_id)` - Get a credit allocation with transactions

## Configuration

### Environment Variables

- `METRIFOX_API_KEY` - Your Metrifox API key
- `METRIFOX_METER_SERVICE_BASE_URL` - Custom meter service URL (optional)

### Custom URLs

```python
client = MetrifoxClient(
    api_key="your_api_key",
    base_url="https://custom-api.metrifox.com/api/v1/",
    web_app_base_url="https://custom-app.metrifox.com",
    meter_service_base_url="https://custom-meter.metrifox.com/"
)
```

### Default URLs

- **Production API:** `https://api.metrifox.com/api/v1/`
- **Meter Service:** `https://api-meter.metrifox.com/`
- **Web App:** `https://app.metrifox.com`

## Development

### Running Tests

```bash
pip install pytest pytest-cov
pytest
```

### Code Style

This project uses:
- Type hints for all public APIs
- Docstrings for all public methods
- PEP 8 style guidelines

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/metrifox/metrifox-python.

## License

The SDK is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Support

For support, contact [support@metrifox.com](mailto:support@metrifox.com) or visit our [documentation](https://docs.metrifox.com).
