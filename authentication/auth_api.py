from fastapi import APIRouter
from authentication.auth_init import sign_in
from authentication.sign_out import sign_out
from defaults.models import User
from defaults.standard_response import success_response

from defaults.bearer_setting import TokenDep
auth_router = APIRouter()


@auth_router.post("/login", 
                  response_model=success_response
                  )
def login(params: User):
    """
    Authenticate user with username and password.
    """
    # Implement authentication logic here

    sign_in_response = sign_in(params.username, params.password)
    return {
        "data": sign_in_response,
        "message": "User signed in successfully",
    }


@auth_router.get("/logout", 
                 response_model=success_response
                  )
def logout(token: TokenDep):
    """
    Sign out the user using the access token.
    """

    sign_out_response = sign_out(token)

    return {
        "data": sign_out_response,
        "message": "User signed out successfully",
    }