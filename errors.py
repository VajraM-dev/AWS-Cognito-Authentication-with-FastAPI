# Error Classes
class CognitoError(Exception):
    """Base exception for all Cognito-related errors"""
    pass


class InvalidJWTError(CognitoError):
    pass


class InvalidKidError(CognitoError):
    pass


class SignatureError(CognitoError):
    pass


class TokenExpiredError(CognitoError):
    pass


class InvalidIssuerError(CognitoError):
    pass


class InvalidAudienceError(CognitoError):
    pass


class InvalidTokenUseError(CognitoError):
    pass