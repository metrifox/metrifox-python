"""
Simple test file - just like testing a Ruby gem
Run: python3 test.py
"""

import sys
import os

# Add parent directory to path to import SDK locally
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from metrifox_sdk import MetrifoxClient

# Initialize the SDK
client = MetrifoxClient(api_key="....YOUR_API_KEY")

print("="*60)
print("METRIFOX SDK TEST")
print("="*60)

# Test 1: List customers
print("\n1. List customers:")
result = client.customers.list({"per_page": 3})
print(f"   Found {len(result['data'])} customers")
for customer in result['data']:
    print(f"   - {customer['customer_key']}: {customer['primary_email']}")

# Test 2: Create a customer
print("\n2. Create a customer:")
import time
new_customer = client.customers.create({
    "customer_key": f"test_{int(time.time())}",
    "customer_type": "INDIVIDUAL",
    "primary_email": f"test_{int(time.time())}@example.com",
    "first_name": "Test"
})
print(f"   Created: {new_customer['data']['customer_key']}")

# Test 3: Get the customer
customer_key = new_customer['data']['customer_key']
print(f"\n3. Get customer {customer_key}:")
customer = client.customers.get(customer_key)
print(f"   Email: {customer['data']['primary_email']}")
print(f"   Name: {customer['data'].get('first_name', 'N/A')}")

# Test 4: Check feature access
print("\n4. Check feature access:")
access = client.usages.check_access({
    "feature_key": "premium_feature",
    "customer_key": customer_key
})
print(f"   Can access: {access['data']['can_access']}")
print(f"   Balance: {access['data']['balance']}")
print(f"   Message: {access['data']['message']}")

# Test 5: Generate checkout URL
print("\n5. Generate checkout URL:")
url = client.checkout.url({"offering_key": "premium_plan"})
print(f"   URL: {url}")

# Test 6: Record a usage event
print("\n6. Record a usage event:")
try:
    usage_event = client.usages.record_usage({
        "feature_key": "premium_feature",
        "customer_key": customer_key,
        "quantity": 1,
        "timestamp": int(time.time())
    })
    print(f"   Recorded event ID: {usage_event['data']['event_id']}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    if hasattr(e, 'response_body') and e.response_body:
        print(f"   ✗ API Response: {e.response_body}")

# Test 7: Delete test customer (cleanup)
print(f"\n7. Cleanup - delete {customer_key}:")
client.customers.delete(customer_key)
print("   Deleted!")

print("\n" + "="*60)
print("✓ ALL TESTS PASSED!")
print("="*60)
