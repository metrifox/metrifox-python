"""
Base HTTP client for Metrifox SDK
"""

import requests
from typing import Dict, Any, Optional
from .exceptions import APIError


class BaseClient:
    """Base client for making HTTP requests to Metrifox API"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Metrifox API

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json: JSON body
            files: Files for multipart upload

        Returns:
            Parsed JSON response

        Raises:
            APIError: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            # For file uploads, we need to remove Content-Type header
            # and let requests set it with the boundary
            headers = {}
            if files:
                headers = {'x-api-key': self.api_key}
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    files=files,
                    headers=headers,
                    timeout=30
                )
            else:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=30
                )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            try:
                error_body = e.response.json() if e.response else None
                error_message = error_body.get('message', str(e)) if error_body else str(e)
            except:
                error_message = str(e)

            raise APIError(
                message=f"API request failed: {error_message}",
                status_code=status_code,
                response_body=e.response.text if e.response else None
            )

        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

        except ValueError as e:
            raise APIError(f"Invalid JSON response: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return self._make_request("POST", endpoint, json=json, files=files)

    def patch(self, endpoint: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PATCH request"""
        return self._make_request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self._make_request("DELETE", endpoint)
