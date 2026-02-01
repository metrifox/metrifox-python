"""
Pytest configuration and fixtures
"""

import pytest
from unittest.mock import Mock, MagicMock
from metrifox_sdk import MetrifoxClient
from metrifox_sdk.base import BaseClient


@pytest.fixture
def mock_api_key():
    """Provide a mock API key"""
    return "test_api_key_12345"


@pytest.fixture
def mock_client(mock_api_key):
    """Provide a mock Metrifox client"""
    return MetrifoxClient(api_key=mock_api_key)


@pytest.fixture
def mock_base_client(mock_api_key, monkeypatch):
    """Provide a mock base client with mocked requests"""
    client = BaseClient(mock_api_key, "https://api.test.com")
    
    # Mock the session to avoid actual HTTP calls
    mock_session = MagicMock()
    monkeypatch.setattr(client, 'session', mock_session)
    
    return client, mock_session


@pytest.fixture
def sample_customer_data():
    """Provide sample customer data"""
    return {
        "customer_key": "cust_test_123",
        "customer_type": "INDIVIDUAL",
        "primary_email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def sample_usage_data():
    """Provide sample usage event data"""
    return {
        "customer_key": "cust_test_123",
        "event_name": "test_event",
        "event_id": "evt_test_001",
        "amount": 1
    }


@pytest.fixture
def sample_access_data():
    """Provide sample access check data"""
    return {
        "feature_key": "test_feature",
        "customer_key": "cust_test_123"
    }
