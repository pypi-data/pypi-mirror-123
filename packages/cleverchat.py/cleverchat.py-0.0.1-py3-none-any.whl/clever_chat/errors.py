"""Error handlers"""

class BaseException(Exception):
    """Base exception"""

class MissingMessageArgument(BaseException):
    """Missing message argument"""

class APIError(BaseException):
    """API is down or having problems"""
