from authentication.auth_settings import Settings
from defaults.errors import AuthenticationError

settings = Settings()

client = settings.client

def sign_out(access_token: str):
    """
    Sign out the user from Cognito using the access token.
    """
    try:
        # Sign out the user
        response = client.global_sign_out(
            AccessToken=access_token
        )
        return response
    except client.exceptions.NotAuthorizedException:
        raise AuthenticationError(message="Invalid access token")
    except Exception as e:
        print(f"Error signing out: {e}")
        return {"error": "An error occurred during sign-out"}