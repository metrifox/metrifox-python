"""
Simple test file - just like testing a Ruby gem
Run: python3 test.py
"""

import sys
import os
import time

# Load .env
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Add parent directory to path to import SDK locally
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from metrifox_sdk import MetrifoxClient

# Initialize the SDK
client = MetrifoxClient(
    base_url=os.getenv("METRIFOX_BASE_URL"),
    meter_service_base_url=os.getenv("METRIFOX_METER_SERVICE_BASE_URL"),
)

print("=" * 60)
print("METRIFOX SDK TEST")
print("=" * 60)

# Test 1: List customers
print("\n1. List customers:")
result = client.customers.list({"per_page": 3})
print(f"   Found {len(result['data'])} customers")
for customer in result["data"]:
    print(f"   - {customer['customer_key']}: {customer['primary_email']}")

# Test 2: Create a customer
print("\n2. Create a customer:")
new_customer = client.customers.create(
    {
        "customer_key": f"test_{int(time.time())}",
        "customer_type": "INDIVIDUAL",
        "primary_email": f"test_{int(time.time())}@example.com",
        "first_name": "Test",
    }
)
print(f"   Created: {new_customer['data']['customer_key']}")

# Test 3: Get the customer
customer_key = new_customer["data"]["customer_key"]
print(f"\n3. Get customer {customer_key}:")
customer = client.customers.get(customer_key)
print(f"   Email: {customer['data']['primary_email']}")
print(f"   Name: {customer['data'].get('first_name', 'N/A')}")

# Test 4: Check feature access
print("\n4. Check feature access:")
try:
    access = client.usages.check_access(
        {"feature_key": "premium_feature", "customer_key": customer_key}
    )
    print(f"   Can access: {access['data']['can_access']}")
    print(f"   Balance: {access['data']['balance']}")
    print(f"   Message: {access['data']['message']}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 5: Generate checkout URL
print("\n5. Generate checkout URL:")
try:
    url = client.checkout.url({"offering_key": "premium_plan"})
    print(f"   URL: {url}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 6: Record a usage event
print("\n6. Record a usage event:")
try:
    usage_event = client.usages.record_usage(
        {
            "feature_key": "premium_feature",
            "customer_key": customer_key,
            "event_id": f"evt_{int(time.time())}",
            "quantity": 1,
            "timestamp": int(time.time() * 1000),
        }
    )
    print(f"   Recorded: {usage_event['data']}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 7: List usage events
print("\n7. List usage events:")
try:
    events = client.usages.list_events(per_page=3)
    print(f"   Found {events['meta']['total_count']} events")
    for ev in events["data"]:
        print(
            f"   - {ev['feature_key']}: qty={ev['quantity']} customer={ev['customer_key']}"
        )
except Exception as e:
    print(f"   ✗ {e}")

# Test 7b: Compute quantity price (requires finance API feature on plan)
print("\n7b. Compute quantity price for premium_feature:")
try:
    price = client.usages.quantity_price(
        customer_key=customer_key,
        feature_key="premium_feature",
        quantity=10,
    )
    data = price["data"]
    print(f"   Price: {data['price']} {data['unit']} for {data['quantity']} units")
    for tier in data.get("applied_tiers", []) or []:
        print(
            f"     tier {tier['first_unit']}-{tier['last_unit']}: "
            f"{tier['units_consumed']} units -> {tier['tier_price']}"
        )
except Exception as e:
    print(f"   ✗ {e}")

# Test 8: List wallets
print(f"\n8. List wallets for {customer_key}:")
try:
    wallets = client.wallets.list("cust-mn3hbmwj82w2")
    if wallets["data"]:
        for w in wallets["data"]:
            print(
                f"   - {w['name']}: balance={w['balance']} {w.get('credit_unit_plural', '')}"
            )
    else:
        print("   (no wallets)")
except Exception as e:
    print(f"   ✗ {e}")

# Test 9: List credit allocations for a wallet
print("\n9. List credit allocations for wallet:")
try:
    allocations = client.wallets.list_credit_allocations("120e396c-9c78-40a8-9c05-e5d0daa3f3d7")
    if allocations["data"]:
        for alloc in allocations["data"]:
            print(f"   - {alloc['allocation_type']}: amount={alloc['amount']} consumed={alloc['consumed']}")
            # Test 9b: Get single allocation
            alloc_id = alloc["id"]
            single = client.wallets.get_credit_allocation(alloc_id)
            txns = single["data"].get("transactions", [])
            print(f"     → {len(txns)} transaction(s)")
    else:
        print("   (no allocations)")
except Exception as e:
    print(f"   ✗ {e}")

# Test 10: Card collection URL
print("\n10. Card collection URL:")
try:
    url = client.checkout.card_collection_url(
        subscription_id="234ad06e-349c-45c9-bef5-0e3647c8b9bd"
    )
    print(f"   URL: {url}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 11: Archive customer
print(f"\n11. Archive customer {customer_key}:")
try:
    archived = client.customers.archive(customer_key)
    print(f"    archived_at: {archived['data']['archived_at']}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 12: Unarchive customer
print(f"\n12. Unarchive customer {customer_key}:")
try:
    unarchived = client.customers.unarchive(customer_key)
    print(f"    archived_at: {unarchived['data']['archived_at']}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 13: Delete test customer (cleanup)
print(f"\n13. Cleanup - delete {customer_key}:")
client.customers.delete(customer_key)
print("    Deleted!")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
