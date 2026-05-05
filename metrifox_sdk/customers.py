"""
Customers module for Metrifox SDK
"""

from typing import Dict, Any, List, Union, Optional
from .base import BaseClient
from .types import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerListRequest,
)


class CustomersModule:
    """Module for managing customers"""

    def __init__(self, client: BaseClient):
        self._client = client

    def create(self, request: Union[CustomerCreateRequest, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new customer

        Args:
            request: Customer creation data (CustomerCreateRequest or dict)

        Returns:
            API response with data typed as CustomerResponse

        Example:
            >>> customer = client.customers.create({
            ...     "customer_key": "cust_123",
            ...     "customer_type": "INDIVIDUAL",
            ...     "primary_email": "user@example.com",
            ...     "first_name": "John",
            ...     "last_name": "Doe"
            ... })
            >>> print(customer['data']['customer_key'])
        """
        data = request.to_dict() if hasattr(request, 'to_dict') else request
        return self._client.post("customers/new", json=data)

    def update(self, customer_key: str, request: Union[CustomerUpdateRequest, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update an existing customer

        Args:
            customer_key: The customer's unique key
            request: Customer update data (CustomerUpdateRequest or dict)

        Returns:
            API response with data typed as CustomerResponse

        Example:
            >>> customer = client.customers.update("cust_123", {
            ...     "display_name": "John Doe Jr.",
            ...     "primary_email": "newemail@example.com"
            ... })
        """
        data = request.to_dict() if hasattr(request, 'to_dict') else request
        return self._client.patch(f"customers/{customer_key}", json=data)

    def get(self, customer_key: str) -> Dict[str, Any]:
        """
        Get a customer by key

        Args:
            customer_key: The customer's unique key

        Returns:
            API response with data typed as CustomerResponse

        Example:
            >>> customer = client.customers.get("cust_123")
            >>> print(customer['data']['full_name'])
        """
        return self._client.get(f"customers/{customer_key}")

    def get_details(self, customer_key: str) -> Dict[str, Any]:
        """
        Get detailed customer information including subscriptions and wallets

        Args:
            customer_key: The customer's unique key

        Returns:
            API response with data typed as CustomerDetailsResponse

        Example:
            >>> details = client.customers.get_details("cust_123")
            >>> for sub in details['data']['subscriptions']:
            ...     print(sub['product_name'], sub['status'])
        """
        return self._client.get(f"customers/{customer_key}/details")

    def list(self, params: Optional[Union[CustomerListRequest, Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        List customers with optional pagination and filters

        Args:
            params: Optional filtering and pagination parameters

        Returns:
            API response with list of customers and pagination metadata

        Example:
            >>> customers = client.customers.list({"page": 1, "per_page": 50})
            >>> for customer in customers['data']:
            ...     print(customer['customer_key'], customer['primary_email'])
        """
        query_params = params.to_dict() if hasattr(params, 'to_dict') else (params or {})
        return self._client.get("customers", params=query_params)

    def delete(self, customer_key: str) -> Dict[str, Any]:
        """
        Delete a customer

        Args:
            customer_key: The customer's unique key

        Returns:
            API response confirming deletion

        Example:
            >>> response = client.customers.delete("cust_123")
        """
        return self._client.delete(f"customers/{customer_key}")

    def archive(self, customer_key: str) -> Dict[str, Any]:
        """
        Archive a customer

        Args:
            customer_key: The customer's unique key

        Returns:
            API response with archived customer data

        Example:
            >>> result = client.customers.archive("cust_123")
            >>> print(result['data']['archived_at'])
        """
        return self._client.post(f"customers/{customer_key}/archive")

    def unarchive(self, customer_key: str) -> Dict[str, Any]:
        """
        Unarchive a customer

        Args:
            customer_key: The customer's unique key

        Returns:
            API response with unarchived customer data

        Example:
            >>> result = client.customers.unarchive("cust_123")
        """
        return self._client.post(f"customers/{customer_key}/unarchive")

    def has_active_subscription(self, customer_key: str) -> bool:
        """
        Check if a customer has an active subscription

        Args:
            customer_key: The customer's unique key

        Returns:
            True if customer has an active subscription, False otherwise

        Example:
            >>> is_active = client.customers.has_active_subscription("cust_123")
            >>> if is_active:
            ...     print("Customer has active subscription")
        """
        response = self._client.get(f"customers/{customer_key}/check-active-subscription")
        return response.get('data', {}).get('has_active_subscription', False)

    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload customers via CSV file

        Args:
            file_path: Path to the CSV file

        Returns:
            API response with upload results

        Example:
            >>> result = client.customers.upload_csv("/path/to/customers.csv")
            >>> print(f"Uploaded: {result['data']['successful_upload_count']}")
            >>> print(f"Failed: {result['data']['failed_upload_count']}")
        """
        with open(file_path, 'rb') as f:
            files = {'csv': (file_path.split('/')[-1], f, 'text/csv')}
            return self._client.post("customers/csv-upload", files=files)

    def bulk_create(self, customers: Union[List[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk create multiple customers in a single request

        Args:
            customers: List of customer data dicts, or a dict with 'customers' key

        Returns:
            API response with creation results including successful and failed entries

        Example:
            >>> result = client.customers.bulk_create([
            ...     {
            ...         "customer_key": "cust_001",
            ...         "customer_type": "BUSINESS",
            ...         "primary_email": "contact@acme.com",
            ...         "legal_name": "Acme Inc"
            ...     },
            ...     {
            ...         "customer_key": "cust_002",
            ...         "customer_type": "INDIVIDUAL",
            ...         "primary_email": "jane@example.com",
            ...         "first_name": "Jane",
            ...         "last_name": "Doe"
            ...     }
            ... ])
            >>> print(f"Created: {result['data']['successful_count']}")
            >>> print(f"Failed: {result['data']['failed_count']}")
        """
        if isinstance(customers, list):
            data = {"customers": customers}
        else:
            data = customers
        return self._client.post("customers/bulk-create", json=data)
