"""
Tests for the Subscriptions module
"""

import pytest
from unittest.mock import patch
from metrifox_sdk import MetrifoxClient
from metrifox_sdk.exceptions import APIError


@pytest.fixture
def client():
    return MetrifoxClient(api_key="test_api_key")


class TestBulkAssignPlan:
    """Test subscriptions.bulk_assign_plan method"""

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_assign_plan_success(self, mock_request, client):
        """Test bulk assigning a plan to multiple customers"""
        mock_response = {
            "statusCode": 200,
            "message": "Bulk Plan Assignment Completed",
            "meta": {},
            "data": {
                "succeeded": [
                    {"customer_key": "cust_001", "subscription_id": "sub_001"},
                    {"customer_key": "cust_002", "subscription_id": "sub_002"}
                ],
                "failed": []
            },
            "errors": {}
        }
        mock_request.return_value = mock_response

        result = client.subscriptions.bulk_assign_plan(
            customer_keys=["cust_001", "cust_002"],
            plan_key="pro-plan",
            billing_interval="monthly"
        )

        assert result == mock_response
        assert len(result["data"]["succeeded"]) == 2
        assert len(result["data"]["failed"]) == 0

        mock_request.assert_called_once_with(
            "POST",
            "subscriptions/bulk-assign-plan",
            json={
                "customer_keys": ["cust_001", "cust_002"],
                "plan_key": "pro-plan",
                "billing_interval": "monthly"
            },
            files=None
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_assign_plan_with_all_optional_params(self, mock_request, client):
        """Test bulk assign plan with all optional parameters"""
        mock_request.return_value = {"statusCode": 200, "data": {"succeeded": [], "failed": []}}

        client.subscriptions.bulk_assign_plan(
            customer_keys=["cust_001"],
            plan_key="pro-plan",
            billing_interval="yearly",
            currency_code="EUR",
            items=[{"feature_key": "api_calls", "quantity": 10000}],
            skip_invoice=True
        )

        mock_request.assert_called_once_with(
            "POST",
            "subscriptions/bulk-assign-plan",
            json={
                "customer_keys": ["cust_001"],
                "plan_key": "pro-plan",
                "billing_interval": "yearly",
                "currency_code": "EUR",
                "items": [{"feature_key": "api_calls", "quantity": 10000}],
                "skip_invoice": True
            },
            files=None
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_assign_plan_omits_none_optional_params(self, mock_request, client):
        """Test that None optional params are not sent in the request"""
        mock_request.return_value = {"statusCode": 200, "data": {"succeeded": [], "failed": []}}

        client.subscriptions.bulk_assign_plan(
            customer_keys=["cust_001"],
            plan_key="pro-plan"
        )

        mock_request.assert_called_once_with(
            "POST",
            "subscriptions/bulk-assign-plan",
            json={
                "customer_keys": ["cust_001"],
                "plan_key": "pro-plan"
            },
            files=None
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_assign_plan_partial_failure(self, mock_request, client):
        """Test bulk assign plan with partial failures"""
        mock_response = {
            "statusCode": 200,
            "message": "Bulk Plan Assignment Completed",
            "data": {
                "succeeded": [
                    {"customer_key": "cust_001", "subscription_id": "sub_001"}
                ],
                "failed": [
                    {"customer_key": "cust_002", "error": "Customer already has an active subscription"}
                ]
            }
        }
        mock_request.return_value = mock_response

        result = client.subscriptions.bulk_assign_plan(
            customer_keys=["cust_001", "cust_002"],
            plan_key="pro-plan"
        )

        assert len(result["data"]["succeeded"]) == 1
        assert len(result["data"]["failed"]) == 1
        assert result["data"]["failed"][0]["error"] == "Customer already has an active subscription"

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_bulk_assign_plan_api_error(self, mock_request, client):
        """Test bulk assign plan raises error on API failure"""
        mock_request.side_effect = APIError(
            message="API request failed: Unauthorized",
            status_code=401
        )

        with pytest.raises(APIError) as exc_info:
            client.subscriptions.bulk_assign_plan(
                customer_keys=["cust_001"],
                plan_key="pro-plan"
            )
        assert exc_info.value.status_code == 401
