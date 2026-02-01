# Metrifox SDK Test Apps

Two ways to test the Metrifox Python SDK locally without publishing it.

## Option 1: Simple Standalone Test (Recommended)

A standalone Python script that tests all SDK features.

### Run the test:

```bash
# Set your API key
export METRIFOX_API_KEY=your_metrifox_api_key

# Run the test
python3 simple_test.py
```

### What it tests:
- ✓ SDK initialization
- ✓ Customer creation, update, get, list, delete
- ✓ Usage tracking (check access, record usage)
- ✓ Checkout URL generation
- ✓ Type-safe dataclasses

## Option 2: Flask Web App

A simple Flask web API that wraps the SDK.

### Install dependencies:

```bash
pip3 install flask requests
```

### Run the app:

```bash
# Set your API key
export METRIFOX_API_KEY=your_metrifox_api_key

# Run the Flask app
python3 app.py
```

The app will start at `http://localhost:5000`

### Test the endpoints:

```bash
# Check health
curl http://localhost:5000/health

# List customers
curl http://localhost:5000/customers

# Create a customer
curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "customer_key": "test_123",
    "customer_type": "INDIVIDUAL",
    "primary_email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }'

# Get a customer
curl http://localhost:5000/customers/test_123

# Check feature access
curl http://localhost:5000/access/test_123/premium_feature

# Record usage
curl -X POST http://localhost:5000/usage \
  -H "Content-Type: application/json" \
  -d '{
    "customer_key": "test_123",
    "event_name": "api_call",
    "event_id": "evt_unique_123",
    "amount": 1
  }'

# Generate checkout URL
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "offering_key": "premium_plan",
    "customer_key": "test_123"
  }'
```

## How It Works

Both test apps import the SDK directly from the parent directory without needing to publish or install it:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metrifox_sdk import MetrifoxClient
```

This means you can:
- ✓ Test the SDK locally
- ✓ Make changes to the SDK and test immediately
- ✓ Verify everything works before publishing

## Getting Your API Key

1. Go to https://app.metrifox.com
2. Navigate to Settings → API Keys
3. Copy your API key
4. Set it as an environment variable:
   ```bash
   export METRIFOX_API_KEY=your_api_key_here
   ```

## Next Steps

Once you've verified the SDK works correctly with these test apps:
1. Make any needed adjustments to the SDK
2. Update the version number in `setup.py` and `pyproject.toml`
3. Publish to PyPI (see main README.md for instructions)
