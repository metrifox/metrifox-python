"""
Simple Flask app to test the Metrifox Python SDK
"""

from flask import Flask, jsonify, request
import sys
import os

# Add the parent directory to the path to import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metrifox_sdk import MetrifoxClient, APIError, ConfigurationError

app = Flask(__name__)

# Initialize Metrifox client
# Make sure to set METRIFOX_API_KEY environment variable
try:
    metrifox = MetrifoxClient()
    print("✓ Metrifox SDK initialized successfully")
except ConfigurationError as e:
    print(f"✗ Configuration Error: {e}")
    print("\nPlease set METRIFOX_API_KEY environment variable:")
    print("  export METRIFOX_API_KEY=your_api_key_here")
    metrifox = None


@app.route('/')
def home():
    """Home page with API documentation"""
    return jsonify({
        "message": "Metrifox Python SDK Test App",
        "endpoints": {
            "/health": "Check if SDK is initialized",
            "/customers": "List customers (GET) or Create customer (POST)",
            "/customers/<customer_key>": "Get, Update (PUT), or Delete customer",
            "/customers/<customer_key>/details": "Get detailed customer info",
            "/access/<customer_key>/<feature_key>": "Check feature access",
            "/usage": "Record usage event (POST)",
            "/checkout": "Generate checkout URL (POST)"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    if metrifox is None:
        return jsonify({
            "status": "error",
            "message": "SDK not initialized. Set METRIFOX_API_KEY environment variable."
        }), 500

    return jsonify({
        "status": "ok",
        "sdk_initialized": True,
        "base_url": metrifox.base_url,
        "meter_service_url": metrifox.meter_service_base_url
    })


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    """List or create customers"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        if request.method == 'POST':
            # Create customer
            data = request.json
            result = metrifox.customers.create(data)
            return jsonify(result), 201
        else:
            # List customers
            params = request.args.to_dict()
            result = metrifox.customers.list(params)
            return jsonify(result)

    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/customers/<customer_key>', methods=['GET', 'PUT', 'DELETE'])
def customer_detail(customer_key):
    """Get, update, or delete a customer"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        if request.method == 'GET':
            result = metrifox.customers.get(customer_key)
            return jsonify(result)

        elif request.method == 'PUT':
            data = request.json
            result = metrifox.customers.update(customer_key, data)
            return jsonify(result)

        elif request.method == 'DELETE':
            result = metrifox.customers.delete(customer_key)
            return jsonify(result)

    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/customers/<customer_key>/details')
def customer_details(customer_key):
    """Get detailed customer information"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        result = metrifox.customers.get_details(customer_key)
        return jsonify(result)
    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/customers/<customer_key>/subscription')
def check_subscription(customer_key):
    """Check if customer has active subscription"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        has_subscription = metrifox.customers.has_active_subscription(customer_key)
        return jsonify({
            "customer_key": customer_key,
            "has_active_subscription": has_subscription
        })
    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/access/<customer_key>/<feature_key>')
def check_access(customer_key, feature_key):
    """Check if customer has access to a feature"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        result = metrifox.usages.check_access({
            "customer_key": customer_key,
            "feature_key": feature_key
        })
        return jsonify(result)
    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/usage', methods=['POST'])
def record_usage():
    """Record a usage event"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        data = request.json
        result = metrifox.usages.record_usage(data)
        return jsonify(result), 201
    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


@app.route('/checkout', methods=['POST'])
def generate_checkout():
    """Generate a checkout URL"""
    if metrifox is None:
        return jsonify({"error": "SDK not initialized"}), 500

    try:
        data = request.json
        url = metrifox.checkout.url(data)
        return jsonify({
            "checkout_url": url
        })
    except APIError as e:
        return jsonify({
            "error": str(e),
            "status_code": e.status_code
        }), e.status_code or 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Metrifox Python SDK Test App")
    print("="*60)

    if metrifox:
        print("\n✓ SDK initialized successfully!")
        print(f"  Base URL: {metrifox.base_url}")
        print(f"  Meter Service: {metrifox.meter_service_base_url}")
    else:
        print("\n✗ SDK not initialized")
        print("  Set METRIFOX_API_KEY environment variable")

    print("\nStarting Flask app on http://localhost:5000")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
