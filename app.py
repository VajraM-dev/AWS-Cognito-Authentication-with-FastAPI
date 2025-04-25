from fastapi import Depends, FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import JSONResponse
from authentication.auth_api import auth_router
from defaults.errors import BaseAppError
from authentication.get_user import get_user

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

@app.exception_handler(BaseAppError)
async def app_error_handler(request: Request, exc: BaseAppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

app.include_router(auth_router, prefix="/auth", tags=['auth'])

@app.get("/dummy")
async def dummy_api(current_user = Depends(get_user)):
    return current_user

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7410)