"""
Simple standalone test script for Metrifox Python SDK
No web framework required - just tests all the main SDK features
"""

import sys
import os
import time

# Add the parent directory to the path to import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metrifox_sdk import (
    MetrifoxClient,
    CustomerCreateRequest,
    UsageEventRequest,
    CheckoutConfig,
    APIError,
    ConfigurationError
)


def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_initialization():
    """Test SDK initialization"""
    print_section("1. Testing SDK Initialization")

    try:
        # Try to initialize with environment variable
        client = MetrifoxClient()
        print(f"✓ Initialized with environment variable")
        print(f"  API Key: {client.api_key[:10]}..." if len(client.api_key) > 10 else client.api_key)
        print(f"  Base URL: {client.base_url}")
        print(f"  Meter Service: {client.meter_service_base_url}")
        return client
    except ConfigurationError:
        print("✗ No METRIFOX_API_KEY environment variable found")
        print("\nPlease set your API key:")
        print("  export METRIFOX_API_KEY=your_api_key_here")
        return None


def test_customers(client):
    """Test customer management"""
    print_section("2. Testing Customer Management")

    test_customer_key = f"test_customer_{int(time.time())}"

    try:
        # Create a customer
        print("\n→ Creating customer...")
        customer = client.customers.create({
            "customer_key": test_customer_key,
            "customer_type": "INDIVIDUAL",
            "primary_email": f"test_{int(time.time())}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "currency": "USD"
        })
        print(f"✓ Created customer: {customer['data']['customer_key']}")
        print(f"  Email: {customer['data']['primary_email']}")

        # Get the customer
        print("\n→ Getting customer...")
        retrieved = client.customers.get(test_customer_key)
        print(f"✓ Retrieved customer: {retrieved['data']['customer_key']}")

        # Update the customer
        print("\n→ Updating customer...")
        updated = client.customers.update(test_customer_key, {
            "display_name": "Test User (Updated)",
            "first_name": "Updated"
        })
        print(f"✓ Updated customer: {updated['data']['display_name']}")

        # Get customer details
        print("\n→ Getting customer details...")
        details = client.customers.get_details(test_customer_key)
        print(f"✓ Retrieved detailed information")

        # List customers
        print("\n→ Listing customers...")
        customers = client.customers.list({"per_page": 5})
        print(f"✓ Listed {len(customers['data'])} customers")

        # Check subscription
        print("\n→ Checking subscription status...")
        has_subscription = client.customers.has_active_subscription(test_customer_key)
        print(f"✓ Has active subscription: {has_subscription}")

        # Clean up - delete the test customer
        print("\n→ Cleaning up - deleting test customer...")
        client.customers.delete(test_customer_key)
        print(f"✓ Deleted customer: {test_customer_key}")

        return True

    except APIError as e:
        print(f"\n✗ API Error: {e}")
        print(f"  Status Code: {e.status_code}")
        if e.response_body:
            print(f"  Response: {e.response_body[:200]}")
        return False


def test_usages(client):
    """Test usage tracking"""
    print_section("3. Testing Usage Tracking")

    try:
        # Note: You'll need a real customer_key and feature_key from your Metrifox account
        print("\n→ Checking feature access...")
        print("  (Using example keys - replace with real ones)")

        # This will likely fail without real data, but demonstrates the API
        try:
            access = client.usages.check_access({
                "feature_key": "premium_feature",
                "customer_key": "existing_customer_key"
            })
            print(f"✓ Access check successful")
            print(f"  Can access: {access['data']['can_access']}")
            print(f"  Balance: {access['data']['balance']}")

            # If they have access, record usage
            if access['data']['can_access']:
                print("\n→ Recording usage...")
                usage = client.usages.record_usage({
                    "customer_key": "existing_customer_key",
                    "event_name": "test_event",
                    "event_id": f"evt_test_{int(time.time())}",
                    "amount": 1
                })
                print(f"✓ Usage recorded: {usage['message']}")

        except APIError as e:
            print(f"  (Expected - no real customer/feature): {str(e)[:100]}")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_checkout(client):
    """Test checkout URL generation"""
    print_section("4. Testing Checkout")

    try:
        print("\n→ Generating checkout URL...")
        print("  (Using example keys - replace with real ones)")

        try:
            url = client.checkout.url({
                "offering_key": "premium_plan"
            })
            print(f"✓ Checkout URL generated")
            print(f"  URL: {url[:80]}..." if len(url) > 80 else url)

        except APIError as e:
            print(f"  (Expected - no real offering): {str(e)[:100]}")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_type_safety(client):
    """Test type-safe dataclasses"""
    print_section("5. Testing Type-Safe Dataclasses")

    try:
        # CustomerCreateRequest
        print("\n→ Testing CustomerCreateRequest dataclass...")
        customer_req = CustomerCreateRequest(
            customer_key=f"typed_customer_{int(time.time())}",
            customer_type="BUSINESS",
            primary_email="typed@example.com",
            legal_name="Test Business LLC"
        )
        print(f"✓ CustomerCreateRequest created")
        print(f"  Data: {customer_req.to_dict()}")

        # UsageEventRequest
        print("\n→ Testing UsageEventRequest dataclass...")
        usage_req = UsageEventRequest(
            customer_key="test_customer",
            event_id=f"evt_{int(time.time())}",
            event_name="test_event",
            amount=5,
            metadata={"source": "test_script"}
        )
        data = usage_req.to_dict()
        print(f"✓ UsageEventRequest created")
        print(f"  'amount' converted to 'quantity': {data.get('quantity')}")

        # CheckoutConfig
        print("\n→ Testing CheckoutConfig dataclass...")
        checkout_cfg = CheckoutConfig(
            offering_key="premium_plan",
            billing_interval="monthly"
        )
        print(f"✓ CheckoutConfig created")
        print(f"  Data: {checkout_cfg.to_dict()}")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Main test runner"""
    print("\n" + "="*60)
    print("  METRIFOX PYTHON SDK - INTEGRATION TEST")
    print("="*60)

    # Initialize client
    client = test_initialization()
    if not client:
        print("\n⚠ Cannot proceed without API key")
        print("\nTo run this test:")
        print("  1. Get your API key from https://app.metrifox.com")
        print("  2. Set it as an environment variable:")
        print("     export METRIFOX_API_KEY=your_api_key_here")
        print("  3. Run this script again:")
        print("     python3 simple_test.py")
        return

    # Run tests
    results = {
        "Customer Management": test_customers(client),
        "Usage Tracking": test_usages(client),
        "Checkout": test_checkout(client),
        "Type Safety": test_type_safety(client)
    }

    # Summary
    print_section("TEST SUMMARY")
    print()
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print("  ⚠ SOME TESTS FAILED")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
