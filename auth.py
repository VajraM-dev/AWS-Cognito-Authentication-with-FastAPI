from cognito_functions import CognitoAuthenticator

from errors import (
    CognitoError,
)
import httpx
import base64
from urllib.parse import quote_plus
from fastapi import HTTPException, Header
from typing import Dict, Optional
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Cognito configuration 
POOL_REGION = os.environ.get("COGNITO_REGION")
POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET")

if not all([POOL_REGION, POOL_ID, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Cognito environment variables not fully set.")

# Derived Cognito values
POOL_PREFIX = "".join(POOL_ID.split("_"))
REDIRECT_URI = os.environ.get("COGNITO_REDIRECT_URI")
COGNITO_LOGIN_URL = f"https://{POOL_PREFIX}.auth.{POOL_REGION}.amazoncognito.com/login/continue?client_id={CLIENT_ID}&redirect_uri={quote_plus(REDIRECT_URI)}&response_type=code&scope=email+openid+phone"
TOKEN_ENDPOINT = f"https://{POOL_PREFIX}.auth.{POOL_REGION}.amazoncognito.com/oauth2/token"

# Initialize Cognito authenticator as a global singleton
authenticator = CognitoAuthenticator(
    pool_region=POOL_REGION, 
    pool_id=POOL_ID, 
    client_id=CLIENT_ID
)

async def exchange_code_for_token(code: str) -> str:
    """Exchange authorization code for an access token"""
    # Create the authorization header
    client_id_secret = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_auth = base64.b64encode(client_id_secret.encode('utf-8')).decode('utf-8')

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}",
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    }

    # Use httpx for async HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_ENDPOINT, 
            headers=headers, 
            data=data,
            timeout=10.0  # Add explicit timeout
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Token exchange failed: {response.text}"
        )

    token_data = response.json()
    return token_data["access_token"]


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """Extract and verify token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        # Extract token from Bearer header
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        token = parts[1]
        claims = authenticator.verify_token(token)
        return claims
    except CognitoError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")