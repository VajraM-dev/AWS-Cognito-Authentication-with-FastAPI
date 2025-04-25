import hmac
import hashlib
import base64 

from authentication.auth_settings import Settings

settings = Settings()

def create_hash(username):
    
    message = bytes(username+settings.client_id,'utf-8') 
    key = bytes(settings.client_secret,'utf-8') 
    secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode() 
    return secret_hash