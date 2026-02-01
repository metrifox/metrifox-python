"""
Custom exceptions for Metrifox SDK
"""


class MetrifoxError(Exception):
    """Base exception for all Metrifox SDK errors"""
    pass


class ConfigurationError(MetrifoxError):
    """Raised when there's an error in SDK configuration"""
    pass


class APIError(MetrifoxError):
    """Raised when an API request fails"""

    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self):
        if self.status_code:
            return f"{self.args[0]} (Status: {self.status_code})"
        return self.args[0]
