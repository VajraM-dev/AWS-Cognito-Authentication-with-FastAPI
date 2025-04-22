from errors import (
    InvalidJWTError,
    InvalidKidError,
    SignatureError,
    TokenExpiredError,
    InvalidIssuerError,
    InvalidTokenUseError,
)

from functools import lru_cache
from pydantic import BaseModel
from jose import jwk, jwt
from jose.utils import base64url_decode
import time
import urllib.request
from typing import Dict, List
import json

class JWK(BaseModel):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str

class CognitoAuthenticator:
    def __init__(self, pool_region: str, pool_id: str, client_id: str) -> None:
        self.pool_region = pool_region
        self.pool_id = pool_id
        self.client_id = client_id
        self.issuer = f"https://cognito-idp.{self.pool_region}.amazonaws.com/{self.pool_id}"
        self._jwks = None

    @property
    @lru_cache(maxsize=1)
    def jwks(self) -> List[JWK]:
        """Cached JWKs retrieval to reduce network calls"""
        if self._jwks is None:
            self._jwks = self._get_jwks()
        return self._jwks

    def _get_jwks(self) -> List[JWK]:
        """Fetch and parse the JWKs from Cognito"""
        try:
            file = urllib.request.urlopen(f"{self.issuer}/.well-known/jwks.json")
            res = json.loads(file.read().decode("utf-8"))
            if not res.get("keys"):
                raise Exception("The JWKS endpoint does not contain any keys")
            return [JWK(**key) for key in res["keys"]]
        except Exception as e:
            raise Exception(f"Failed to retrieve JWKS: {str(e)}")

    def verify_token(self, token: str) -> Dict:
        """Verify the JWT token and return its claims"""
        self._is_jwt(token)
        self._get_verified_header(token)
        return self._get_verified_claims(token)

    def _is_jwt(self, token: str) -> bool:
        """Check if the token is a valid JWT format"""
        try:
            jwt.get_unverified_header(token)
            jwt.get_unverified_claims(token)
            return True
        except jwt.JWTError:
            raise InvalidJWTError("Invalid JWT format")

    def _get_verified_header(self, token: str) -> Dict:
        """Verify the JWT header and signature"""
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]
        
        # Find the matching JWK
        key = None
        for k in self.jwks:
            if k.kid == kid:
                key = jwk.construct(k.model_dump())
                break

        if not key:
            raise InvalidKidError(f"Unable to find a signing key that matches '{kid}'")

        # Verify signature
        message, encoded_signature = str(token).rsplit(".", 1)
        signature = base64url_decode(encoded_signature.encode("utf-8"))

        if not key.verify(message.encode("utf8"), signature):
            raise SignatureError("Signature verification failed")

        return headers

    def _get_verified_claims(self, token: str) -> Dict:
        """Verify the JWT claims"""
        claims = jwt.get_unverified_claims(token)
        
        # Verify expiration
        if claims["exp"] < time.time():
            raise TokenExpiredError("Token has expired")

        # Verify issuer
        if claims["iss"] != self.issuer:
            raise InvalidIssuerError(f"Invalid issuer: {claims['iss']}")

        # Verify token_use
        if claims["token_use"] != "access":
            raise InvalidTokenUseError(f"Invalid token_use: {claims['token_use']}")

        return claims