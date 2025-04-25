from authentication.auth_settings import Settings
from defaults.errors import AuthenticationError
from defaults.bearer_setting import TokenDep
settings = Settings()

client = settings.client

def get_user(access_token: TokenDep) -> dict:
    """
    Get user information from Cognito using the access token.
    """
    try:
        response = client.get_user(
            AccessToken=access_token
        )

        user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        return user_attributes
    except client.exceptions.NotAuthorizedException:
        raise AuthenticationError(message="Invalid access token")
    except Exception as e:
        print(f"Error signing out: {e}")
        return {"error": "An error occurred during sign-out"}
