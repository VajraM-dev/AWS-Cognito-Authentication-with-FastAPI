import json
from typing import Dict, Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from string import Template
from auth import (authenticator,
                  COGNITO_LOGIN_URL,
                  exchange_code_for_token,
                  get_current_user,
                  )
from fastapi.middleware.cors import CORSMiddleware
import os
# Load environment variables
load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
# Setup FastAPI
app = FastAPI(
    debug=ENVIRONMENT != "production",
    docs_url=None if ENVIRONMENT == "production" else "/docs",
    redoc_url=None if ENVIRONMENT == "production" else "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7410"],  # Add your production domains when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
HTML_DIR = Path("static/html")

# Routes
@app.get("/", response_class=RedirectResponse)
async def root():
    """Redirect to Cognito login page"""
    return RedirectResponse(COGNITO_LOGIN_URL, status_code=302)

@app.get("/login")
async def login():
    """Serve login page with Cognito login URL"""
    with open(HTML_DIR / "login.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
        content = template.safe_substitute(login_url=COGNITO_LOGIN_URL)
    return HTMLResponse(content)

@app.get("/home")
async def home(request: Request, code: Optional[str] = None):
    """Handle the OAuth callback with authorization code"""
    if not code:
        return RedirectResponse("/login")

    try:
        # Exchange code for token
        access_token = await exchange_code_for_token(code)
        
        # Verify token and get claims
        claims = authenticator.verify_token(access_token)
        
        # Use Template instead of format to avoid CSS curly braces conflicts
        with open(HTML_DIR / "home.html", "r", encoding="utf-8") as f:
            template = Template(f.read())
            content = template.safe_substitute(
                user_info=json.dumps(claims, indent=2),
                access_token=access_token
            )
        
        return HTMLResponse(content)
        
    except HTTPException as e:
        with open(HTML_DIR / "error.html", "r", encoding="utf-8") as f:
            template = Template(f.read())
            content = template.safe_substitute(error_message=e.detail)
        return HTMLResponse(content, status_code=e.status_code)
        
    except Exception as e:
        with open(HTML_DIR / "error.html", "r", encoding="utf-8") as f:
            template = Template(f.read())
            content = template.safe_substitute(error_message=f"Internal server error: {str(e)}")
        return HTMLResponse(content, status_code=500)

@app.get("/api/protected")
async def protected_route(user: Dict = Depends(get_current_user)):
    """Protected API endpoint requiring valid Cognito JWT"""
    return {
        "message": "This is a protected API route",
        "user": user
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7410)