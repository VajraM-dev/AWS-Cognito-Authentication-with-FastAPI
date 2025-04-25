from dotenv import load_dotenv
import os
import boto3
load_dotenv()

COGNITO_DOMAIN=os.environ.get("COGNITO_DOMAIN")
COGNITO_CLIENT_ID=os.environ.get("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET=os.environ.get("COGNITO_CLIENT_SECRET")
COGNITO_REGION=os.environ.get("COGNITO_REGION")
COGNITO_USER_POOL_ID=os.environ.get("COGNITO_USER_POOL_ID")
COGNITO_REDIRECT_URI=os.environ.get("COGNITO_REDIRECT_URI")
ENVIRONMENT=os.environ.get("ENVIRONMENT")

CLIENT = boto3.client('cognito-idp', region_name=COGNITO_REGION)

class Settings:
    def __init__(self):
        self.client = CLIENT
        self.pool_region = COGNITO_REGION
        self.pool_id = COGNITO_USER_POOL_ID
        self.client_id = COGNITO_CLIENT_ID
        self.client_secret = COGNITO_CLIENT_SECRET
        self.issuer = f"https://cognito-idp.{self.pool_region}.amazonaws.com/{self.pool_id}"
        self.environment = ENVIRONMENT