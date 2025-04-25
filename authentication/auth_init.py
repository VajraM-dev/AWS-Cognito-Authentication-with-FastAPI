from authentication.auth_settings import Settings
from authentication.secret_hash import create_hash
from defaults.errors import NotFoundError, AuthenticationError
settings = Settings()

client = settings.client

def sign_in(username: str, password: str):
    try:
        response = client.initiate_auth(
            ClientId=settings.client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': create_hash(username),
            }
        )
        return response
    except client.exceptions.NotAuthorizedException:
        raise AuthenticationError(message="Invalid username or password")
    except client.exceptions.UserNotFoundException:
        raise NotFoundError(resource_type="User", resource_id=username)
    except Exception as e:
        print(f"Error signing in: {e}")
        return {"error": "An error occurred during sign-in"}

