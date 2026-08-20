"""Tests for usage event recording."""

from unittest.mock import patch

import pytest

from metrifox_sdk import MetrifoxClient, UsageEventRequest


@pytest.fixture
def client():
    return MetrifoxClient(api_key="test_api_key")


class TestRecordUsage:
    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_records_dict_request_with_aggregation_properties(self, mock_request, client):
        mock_request.return_value = {"message": "Event received"}

        result = client.usages.record_usage(
            {
                "customer_key": "customer_123",
                "feature_key": "feature_active_users",
                "event_id": "evt_unique_123",
                "properties": {
                    "workspace_id": "workspace_42",
                    "user_id": "user_7",
                },
            }
        )

        assert result == {"message": "Event received"}
        mock_request.assert_called_once_with(
            "POST",
            "usage/events",
            json={
                "customer_key": "customer_123",
                "feature_key": "feature_active_users",
                "event_id": "evt_unique_123",
                "properties": {
                    "workspace_id": "workspace_42",
                    "user_id": "user_7",
                },
            },
            files=None,
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_records_typed_request_with_aggregation_properties(self, mock_request, client):
        mock_request.return_value = {"message": "Event received"}
        request = UsageEventRequest(
            customer_key="customer_123",
            feature_key="feature_active_users",
            event_id="evt_unique_456",
            properties={"user_id": "user_7"},
        )

        client.usages.record_usage(request)

        mock_request.assert_called_once_with(
            "POST",
            "usage/events",
            json={
                "customer_key": "customer_123",
                "feature_key": "feature_active_users",
                "event_id": "evt_unique_456",
                "quantity": 1,
                "properties": {"user_id": "user_7"},
            },
            files=None,
        )

    @patch("metrifox_sdk.base.BaseClient._make_request")
    def test_typed_request_omits_properties_when_not_supplied(self, mock_request, client):
        mock_request.return_value = {"message": "Event received"}
        request = UsageEventRequest(
            customer_key="customer_123",
            event_name="api_call",
            event_id="evt_existing_123",
        )

        client.usages.record_usage(request)

        payload = mock_request.call_args.kwargs["json"]
        assert "properties" not in payload
