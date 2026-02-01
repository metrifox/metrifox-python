# Metrifox Python SDK - Quick Start Guide

Get started with the Metrifox Python SDK in 5 minutes!

## 1. Installation

```bash
pip install metrifox-sdk
```

## 2. Get Your API Key

1. Log in to your Metrifox dashboard at https://app.metrifox.com
2. Navigate to Settings → API Keys
3. Copy your API key

## 3. Initialize the SDK

### Option A: Using Environment Variable (Recommended)

```bash
export METRIFOX_API_KEY=your_api_key_here
```

```python
from metrifox_sdk import MetrifoxClient

client = MetrifoxClient()
```

### Option B: Direct Initialization

```python
from metrifox_sdk import MetrifoxClient

client = MetrifoxClient(api_key="your_api_key_here")
```

## 4. Create Your First Customer

```python
customer = client.customers.create({
    "customer_key": "user_001",
    "customer_type": "INDIVIDUAL",
    "primary_email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
})

print(f"Created customer: {customer['data']['customer_key']}")
```

## 5. Check Feature Access

```python
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": "user_001"
})

if access['data']['can_access']:
    print(f"Access granted! Balance: {access['data']['balance']}")
else:
    print("Access denied - upgrade needed")
```

## 6. Record Usage

```python
import time

response = client.usages.record_usage({
    "customer_key": "user_001",
    "event_name": "api_call",
    "event_id": f"evt_{int(time.time())}",
    "amount": 1
})

print(f"Usage recorded: {response['message']}")
```

## 7. Generate Checkout URL

```python
checkout_url = client.checkout.url({
    "offering_key": "premium_plan",
    "customer_key": "user_001"
})

print(f"Send customer to: {checkout_url}")
```

## Complete Example

```python
from metrifox_sdk import MetrifoxClient
import time

# Initialize
client = MetrifoxClient(api_key="your_api_key")

# Create customer
customer = client.customers.create({
    "customer_key": "demo_user_001",
    "customer_type": "INDIVIDUAL",
    "primary_email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User"
})

# Check access
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": "demo_user_001"
})

# If they have access, record usage
if access['data']['can_access']:
    client.usages.record_usage({
        "customer_key": "demo_user_001",
        "event_name": "feature_used",
        "event_id": f"evt_{int(time.time())}",
        "amount": 1
    })
    print("Feature used successfully!")
else:
    # Generate checkout URL for upgrade
    checkout_url = client.checkout.url({
        "offering_key": "premium_plan",
        "customer_key": "demo_user_001"
    })
    print(f"Upgrade at: {checkout_url}")
```

## What's Next?

- Read the full [README.md](README.md) for all features
- Check out [example.py](example.py) for more examples
- Visit [https://docs.metrifox.com](https://docs.metrifox.com) for detailed documentation

## Common Patterns

### Django Integration

```python
# settings.py
from metrifox_sdk import MetrifoxClient

METRIFOX_CLIENT = MetrifoxClient(api_key=os.getenv('METRIFOX_API_KEY'))

# views.py
from django.conf import settings

def my_view(request):
    access = settings.METRIFOX_CLIENT.usages.check_access({
        "feature_key": "my_feature",
        "customer_key": request.user.customer_key
    })
    # ...
```

### Flask Integration

```python
# app.py
from flask import Flask
from metrifox_sdk import MetrifoxClient
import os

app = Flask(__name__)
metrifox = MetrifoxClient(api_key=os.getenv('METRIFOX_API_KEY'))

@app.route('/api/feature')
def feature():
    access = metrifox.usages.check_access({
        "feature_key": "api_feature",
        "customer_key": "user_123"
    })
    # ...
```

## Error Handling

```python
from metrifox_sdk import APIError, ConfigurationError

try:
    customer = client.customers.get("user_123")
except APIError as e:
    print(f"API Error: {e}")
    print(f"Status: {e.status_code}")
except ConfigurationError as e:
    print(f"Config Error: {e}")
```

## Need Help?

- Email: support@metrifox.com
- Documentation: https://docs.metrifox.com
- GitHub Issues: https://github.com/metrifox/metrifox-python/issues
