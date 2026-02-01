"""
Tests for the main Metrifox client
"""

import pytest
import os
from metrifox_sdk import MetrifoxClient, init
from metrifox_sdk.exceptions import ConfigurationError


class TestMetrifoxClient:
    """Test MetrifoxClient initialization and configuration"""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key"""
        client = MetrifoxClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == MetrifoxClient.DEFAULT_BASE_URL
        assert client.web_app_base_url == MetrifoxClient.DEFAULT_WEB_APP_BASE_URL

    def test_init_with_custom_urls(self):
        """Test initialization with custom URLs"""
        client = MetrifoxClient(
            api_key="test_key",
            base_url="https://custom.api.com/",
            web_app_base_url="https://custom.app.com"
        )
        assert client.base_url == "https://custom.api.com/"
        assert client.web_app_base_url == "https://custom.app.com"

    def test_init_with_env_var(self, monkeypatch):
        """Test initialization with environment variable"""
        monkeypatch.setenv("METRIFOX_API_KEY", "env_test_key")
        client = MetrifoxClient()
        assert client.api_key == "env_test_key"

    def test_init_without_api_key(self, monkeypatch):
        """Test that initialization fails without API key"""
        monkeypatch.delenv("METRIFOX_API_KEY", raising=False)
        with pytest.raises(ConfigurationError) as exc_info:
            MetrifoxClient()
        assert "API key is required" in str(exc_info.value)

    def test_modules_initialized(self, mock_client):
        """Test that all modules are properly initialized"""
        assert mock_client.customers is not None
        assert mock_client.usages is not None
        assert mock_client.checkout is not None

    def test_init_function(self):
        """Test the init convenience function"""
        client = init({"api_key": "test_key"})
        assert isinstance(client, MetrifoxClient)
        assert client.api_key == "test_key"

    def test_init_function_empty_config(self, monkeypatch):
        """Test init function with empty config uses environment"""
        monkeypatch.setenv("METRIFOX_API_KEY", "env_key")
        client = init()
        assert client.api_key == "env_key"
