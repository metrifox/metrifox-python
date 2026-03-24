"""
Tests for the Customers module
"""

import pytest
from unittest.mock import patch, MagicMock
from metrifox_sdk import MetrifoxClient
from metrifox_sdk.exceptions import APIError


@pytest.fixture
def client():
    return MetrifoxClient(api_key="test_api_key")


class TestBulkCreate:
    """Test customers.bulk_create method"""

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_create_all_successful(self, mock_request, client):
        """Test bulk creating customers where all succeed"""
        mock_response = {
            "statusCode": 200,
            "message": "Bulk Customer Creation Completed",
            "meta": {},
            "data": {
                "total": 2,
                "successful_count": 2,
                "failed_count": 0,
                "customers_created": [
                    {
                        "index": 0,
                        "customer_key": "acme_corp_001",
                        "data": {
                            "id": "764c80e3-ed59-44a5-ba07-7ee5ba547774",
                            "customer_type": "BUSINESS",
                            "primary_email": "contact@acmecorp.com",
                            "display_name": "Acme Corp"
                        }
                    },
                    {
                        "index": 1,
                        "customer_key": "jane_doe_001",
                        "data": {
                            "id": "864c80e3-ed59-44a5-ba07-7ee5ba547775",
                            "customer_type": "INDIVIDUAL",
                            "primary_email": "jane@example.com",
                            "display_name": "Jane Doe"
                        }
                    }
                ],
                "customers_failed": []
            },
            "errors": {}
        }
        mock_request.return_value = mock_response

        result = client.customers.bulk_create([
            {
                "customer_type": "BUSINESS",
                "customer_key": "acme_corp_001",
                "primary_email": "contact@acmecorp.com",
                "legal_name": "Acme Corporation",
                "display_name": "Acme Corp"
            },
            {
                "customer_type": "INDIVIDUAL",
                "customer_key": "jane_doe_001",
                "primary_email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Doe"
            }
        ])

        assert result == mock_response
        assert result["data"]["successful_count"] == 2
        assert result["data"]["failed_count"] == 0
        assert len(result["data"]["customers_created"]) == 2

        # Verify the request was made with correct params
        mock_request.assert_called_once_with(
            "POST",
            "customers/bulk-create",
            json={
                "customers": [
                    {
                        "customer_type": "BUSINESS",
                        "customer_key": "acme_corp_001",
                        "primary_email": "contact@acmecorp.com",
                        "legal_name": "Acme Corporation",
                        "display_name": "Acme Corp"
                    },
                    {
                        "customer_type": "INDIVIDUAL",
                        "customer_key": "jane_doe_001",
                        "primary_email": "jane@example.com",
                        "first_name": "Jane",
                        "last_name": "Doe"
                    }
                ]
            },
            files=None
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_create_partial_failure(self, mock_request, client):
        """Test bulk creating customers with partial failures"""
        mock_response = {
            "statusCode": 200,
            "message": "Bulk Customer Creation Completed",
            "meta": {},
            "data": {
                "total": 2,
                "successful_count": 1,
                "failed_count": 1,
                "customers_created": [
                    {
                        "index": 0,
                        "customer_key": "acme_corp_001",
                        "data": {
                            "id": "764c80e3-ed59-44a5-ba07-7ee5ba547774",
                            "customer_type": "BUSINESS",
                            "primary_email": "contact@acmecorp.com",
                            "display_name": "Acme Corp"
                        }
                    }
                ],
                "customers_failed": [
                    {
                        "index": 1,
                        "customer_key": "jane_doe_001",
                        "error": "Primary email has already been used"
                    }
                ]
            },
            "errors": {}
        }
        mock_request.return_value = mock_response

        result = client.customers.bulk_create([
            {
                "customer_type": "BUSINESS",
                "customer_key": "acme_corp_001",
                "primary_email": "contact@acmecorp.com"
            },
            {
                "customer_type": "INDIVIDUAL",
                "customer_key": "jane_doe_001",
                "primary_email": "jane@example.com"
            }
        ])

        assert result["data"]["successful_count"] == 1
        assert result["data"]["failed_count"] == 1
        assert result["data"]["customers_failed"][0]["error"] == "Primary email has already been used"

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_create_accepts_dict_with_customers_key(self, mock_request, client):
        """Test that bulk_create accepts a dict with 'customers' key"""
        mock_request.return_value = {"statusCode": 200, "data": {"total": 1, "successful_count": 1, "failed_count": 0}}

        client.customers.bulk_create({
            "customers": [
                {"customer_key": "cust_001", "customer_type": "BUSINESS", "primary_email": "a@b.com"}
            ]
        })

        mock_request.assert_called_once_with(
            "POST",
            "customers/bulk-create",
            json={
                "customers": [
                    {"customer_key": "cust_001", "customer_type": "BUSINESS", "primary_email": "a@b.com"}
                ]
            },
            files=None
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_create_api_error(self, mock_request, client):
        """Test bulk create raises error on API failure"""
        mock_request.side_effect = APIError(
            message="API request failed: At least one customer is required for bulk creation",
            status_code=400
        )

        with pytest.raises(APIError) as exc_info:
            client.customers.bulk_create([])
        assert exc_info.value.status_code == 400
