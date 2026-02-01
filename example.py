"""
Example usage of the Metrifox Python SDK

This example demonstrates the basic functionality of the SDK including:
- Customer creation
- Access checking
- Usage recording
- Checkout URL generation
"""

from metrifox_sdk import MetrifoxClient, init

# Example 1: Initialize with explicit API key
def example_with_api_key():
    client = MetrifoxClient(api_key="your_api_key_here")
    return client


# Example 2: Initialize with environment variable
# Set METRIFOX_API_KEY in your environment
def example_with_env():
    client = MetrifoxClient()
    return client


# Example 3: Initialize using init function
def example_with_init():
    client = init({"api_key": "your_api_key_here"})
    return client


# Example 4: Complete customer lifecycle
def complete_customer_example(client):
    """Demonstrates creating and managing a customer"""

    # Create a customer
    customer = client.customers.create({
        "customer_key": "cust_example_001",
        "customer_type": "INDIVIDUAL",
        "primary_email": "demo@example.com",
        "first_name": "Demo",
        "last_name": "User",
        "currency": "USD"
    })
    print(f"✓ Created customer: {customer['data']['customer_key']}")

    # Update the customer
    updated = client.customers.update("cust_example_001", {
        "display_name": "Demo User (Updated)",
        "timezone": "America/New_York"
    })
    print(f"✓ Updated customer: {updated['data']['display_name']}")

    # Get customer details
    details = client.customers.get_details("cust_example_001")
    print(f"✓ Retrieved customer details")

    # List customers
    customers = client.customers.list({"page": 1, "per_page": 10})
    print(f"✓ Listed {len(customers['data'])} customers")

    # Check for active subscription
    is_active = client.customers.has_active_subscription("cust_example_001")
    print(f"✓ Active subscription: {is_active}")


# Example 5: Usage tracking and access control
def usage_tracking_example(client):
    """Demonstrates usage tracking and access control"""

    customer_key = "cust_example_001"
    feature_key = "premium_feature"

    # Check if customer has access
    access = client.usages.check_access({
        "feature_key": feature_key,
        "customer_key": customer_key
    })

    print(f"\nAccess Check:")
    print(f"  Can access: {access['data']['can_access']}")
    print(f"  Balance: {access['data']['balance']}")
    print(f"  Used: {access['data']['used_quantity']}")

    if access['data']['can_access']:
        # Record usage
        import time
        response = client.usages.record_usage({
            "customer_key": customer_key,
            "event_name": "premium_feature_used",
            "event_id": f"evt_{int(time.time())}",
            "amount": 1,
            "metadata": {
                "source": "example_script",
                "action": "demo"
            }
        })
        print(f"✓ Usage recorded: {response['message']}")
    else:
        print("✗ Access denied - quota exceeded")


# Example 6: Generate checkout URL
def checkout_example(client):
    """Demonstrates checkout URL generation"""

    # Basic checkout URL
    url = client.checkout.url({
        "offering_key": "premium_plan"
    })
    print(f"\n✓ Checkout URL generated: {url}")

    # Checkout URL with customer
    url_with_customer = client.checkout.url({
        "offering_key": "premium_plan",
        "billing_interval": "monthly",
        "customer_key": "cust_example_001"
    })
    print(f"✓ Customer checkout URL: {url_with_customer}")


# Example 7: Error handling
def error_handling_example(client):
    """Demonstrates error handling"""

    from metrifox_sdk import APIError, ConfigurationError

    try:
        # Try to get a non-existent customer
        customer = client.customers.get("nonexistent_customer")
    except APIError as e:
        print(f"\n✗ API Error: {e}")
        print(f"  Status Code: {e.status_code}")

    try:
        # Try to initialize without API key
        bad_client = MetrifoxClient()
    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {e}")


# Example 8: Using type-safe dataclasses
def type_safe_example(client):
    """Demonstrates using type-safe dataclasses"""

    from metrifox_sdk import (
        CustomerCreateRequest,
        UsageEventRequest,
        CheckoutConfig
    )
    import time

    # Create customer with dataclass
    customer_request = CustomerCreateRequest(
        customer_key="cust_typed_001",
        customer_type="BUSINESS",
        primary_email="business@example.com",
        legal_name="Example Business LLC",
        display_name="Example Business"
    )

    customer = client.customers.create(customer_request)
    print(f"\n✓ Created customer with dataclass: {customer['data']['customer_key']}")

    # Record usage with dataclass
    usage_request = UsageEventRequest(
        customer_key="cust_typed_001",
        event_name="api_call",
        event_id=f"evt_{int(time.time())}",
        amount=5,
        metadata={"endpoint": "/api/data"}
    )

    response = client.usages.record_usage(usage_request)
    print(f"✓ Recorded usage with dataclass: {response['message']}")

    # Generate checkout with dataclass
    checkout_config = CheckoutConfig(
        offering_key="premium_plan",
        billing_interval="monthly",
        customer_key="cust_typed_001"
    )

    url = client.checkout.url(checkout_config)
    print(f"✓ Generated checkout URL with dataclass")


# Example 9: Bulk CSV upload
def csv_upload_example(client):
    """Demonstrates CSV customer upload"""

    # Note: You need to have a CSV file available
    try:
        result = client.customers.upload_csv("customers.csv")
        print(f"\n✓ CSV Upload Results:")
        print(f"  Total: {result['data']['total_customers']}")
        print(f"  Successful: {result['data']['successful_upload_count']}")
        print(f"  Failed: {result['data']['failed_upload_count']}")

        if result['data']['failed_upload_count'] > 0:
            print("\n  Failed entries:")
            for failure in result['data']['customers_failed']:
                print(f"    Row {failure['row']}: {failure['error']}")
    except FileNotFoundError:
        print("\n✗ CSV file 'customers.csv' not found")


# Main execution
if __name__ == "__main__":
    print("Metrifox Python SDK Examples\n")
    print("=" * 50)

    # Initialize client (using environment variable)
    # Make sure to set METRIFOX_API_KEY in your environment
    try:
        client = MetrifoxClient()
        print("✓ Client initialized successfully\n")

        # Run examples
        print("\n=== Customer Management ===")
        # complete_customer_example(client)

        print("\n=== Usage Tracking ===")
        # usage_tracking_example(client)

        print("\n=== Checkout ===")
        # checkout_example(client)

        print("\n=== Type-Safe Examples ===")
        # type_safe_example(client)

        print("\n=== Error Handling ===")
        # error_handling_example(client)

        print("\n" + "=" * 50)
        print("\nUncomment the example functions above to run them!")

    except Exception as e:
        print(f"\n✗ Error initializing client: {e}")
        print("\nMake sure to set the METRIFOX_API_KEY environment variable:")
        print("  export METRIFOX_API_KEY=your_api_key_here")
