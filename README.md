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
# Check access
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": "customer_123"
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

# Simple usage recording (amount defaults to 1)
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
    "amount": 5,
    "credit_used": 25,
    "timestamp": int(time.time() * 1000),  # milliseconds
    "metadata": {
        "source": "web_app",
        "session_id": "sess_xyz"
    }
})

print(response['message'])  # "Event received"
```

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
                "amount": result.get('units_used', 1),
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

# Get detailed customer information (includes usage stats, billing info, etc.)
details = client.customers.get_details("customer_123")
print(details['data']['usage_summary'])

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

### Deleting Customers

Remove customers from your account:

```python
response = client.customers.delete("customer_123")
print(response['message'])
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
print(history['data'])
```

### Entitlements Summary

Get a summary of entitlements for a subscription:

```python
summary = client.subscriptions.get_entitlements_summary("subscription_uuid")
print(summary['data'])
```

### Entitlements Usage

Get detailed entitlements usage for a subscription:

```python
usage = client.subscriptions.get_entitlements_usage("subscription_uuid")
print(usage['data'])
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

The SDK is fully typed with type hints for better IDE support and type checking:

```python
from metrifox_sdk import (
    MetrifoxClient,
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerListRequest,
    UsageEventRequest,
    AccessCheckRequest,
    CheckoutConfig
)

# Your IDE will provide autocomplete and type checking
client: MetrifoxClient = MetrifoxClient(api_key="your_key")
```

## Examples

### Complete Customer Lifecycle

```python
from metrifox_sdk import MetrifoxClient

client = MetrifoxClient(api_key="your_api_key")

# 1. Create a customer
customer = client.customers.create({
    "customer_key": "cust_demo_123",
    "customer_type": "INDIVIDUAL",
    "primary_email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User"
})

print(f"Created customer: {customer['data']['customer_key']}")

# 2. Check feature access
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": "cust_demo_123"
})

if access['data']['can_access']:
    # 3. Record usage
    client.usages.record_usage({
        "customer_key": "cust_demo_123",
        "event_name": "feature_used",
        "event_id": "evt_demo_001",
        "amount": 1
    })
    print("Usage recorded successfully")

# 4. Generate checkout URL
checkout_url = client.checkout.url({
    "offering_key": "premium_plan",
    "customer_key": "cust_demo_123"
})

print(f"Checkout URL: {checkout_url}")

# 5. Get customer details
details = client.customers.get_details("cust_demo_123")
print(f"Customer details: {details['data']}")
```

### Django Integration

```python
# settings.py
METRIFOX_API_KEY = os.getenv('METRIFOX_API_KEY')

# utils/metrifox.py
from metrifox_sdk import MetrifoxClient
from django.conf import settings

metrifox_client = MetrifoxClient(api_key=settings.METRIFOX_API_KEY)

# views.py
from utils.metrifox import metrifox_client

def premium_feature_view(request):
    customer_key = request.user.customer_key

    access = metrifox_client.usages.check_access({
        "feature_key": "premium_feature",
        "customer_key": customer_key
    })

    if not access['data']['can_access']:
        return JsonResponse({
            "error": "Access denied",
            "balance": access['data']['balance']
        }, status=403)

    # Process the feature...

    # Record usage
    metrifox_client.usages.record_usage({
        "customer_key": customer_key,
        "event_name": "premium_feature_used",
        "event_id": f"evt_{request.id}"
    })

    return JsonResponse({"success": True})
```

### Flask Integration

```python
from flask import Flask, jsonify, request
from metrifox_sdk import MetrifoxClient
import os

app = Flask(__name__)
metrifox_client = MetrifoxClient(api_key=os.getenv('METRIFOX_API_KEY'))

@app.route('/api/premium/<customer_id>', methods=['GET'])
def premium_endpoint(customer_id):
    # Check access
    access = metrifox_client.usages.check_access({
        "feature_key": "premium_api",
        "customer_key": customer_id
    })

    if not access['data']['can_access']:
        return jsonify({
            "error": "Access denied",
            "balance": access['data']['balance']
        }), 403

    # Process request...

    # Record usage
    metrifox_client.usages.record_usage({
        "customer_key": customer_id,
        "event_name": "premium_api_call",
        "event_id": f"evt_{request.headers.get('X-Request-ID')}"
    })

    return jsonify({"data": "premium content"})

if __name__ == '__main__':
    app.run()
```

## API Reference

### Client Methods

**Initialization:**
- `MetrifoxClient(api_key, base_url, web_app_base_url)` - Initialize the client
- `init(config)` - Convenience function to initialize the client

**Customers Module (`client.customers`):**
- `create(request)` - Create a customer
- `update(customer_key, request)` - Update a customer
- `get(customer_key)` - Get a customer
- `get_details(customer_key)` - Get detailed customer information
- `list(params)` - List customers with pagination and filters
- `delete(customer_key)` - Delete a customer
- `has_active_subscription(customer_key)` - Check for active subscription
- `upload_csv(file_path)` - Upload customers via CSV

**Usages Module (`client.usages`):**
- `check_access(request)` - Check feature access
- `record_usage(request)` - Record a usage event

**Subscriptions Module (`client.subscriptions`):**
- `get_billing_history(subscription_id)` - Get billing history for a subscription
- `get_entitlements_summary(subscription_id)` - Get entitlements summary
- `get_entitlements_usage(subscription_id)` - Get entitlements usage

**Checkout Module (`client.checkout`):**
- `url(config)` - Generate a checkout URL

## Configuration

### Environment Variables

- `METRIFOX_API_KEY` - Your Metrifox API key

### Custom URLs

```python
client = MetrifoxClient(
    api_key="your_api_key",
    base_url="https://custom-api.metrifox.com/api/v1/",
    web_app_base_url="https://custom-app.metrifox.com"
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
