# AWS Cognito Authentication with FastAPI

## Features
- JWT Token Verification
- Secure Authorization Handling
- AWS Cognito Integration
- Async HTTP Requests
- Error Handling for Authentication Processes

## Prerequisites
- Python 3.10+
- AWS Cognito User Pool
- Environment Variables Configured

## Dependencies
- fastapi
- uvicorn
- httpx
- python-jose
- python-dotenv

## Environment Configuration

#### Sample `.env` File
```ini
# Cognito Configuration
COGNITO_DOMAIN=https://ap-south-1_xyzxyzxyzx.auth.ap-south-1.amazoncognito.com
COGNITO_CLIENT_ID=your_client_id_here
COGNITO_CLIENT_SECRET=your_client_secret_here
COGNITO_REGION=ap-south-1
COGNITO_USER_POOL_ID=ap-south-1_xyzxyzxyzx
COGNITO_REDIRECT_URI=http://localhost:7410

# Application Environment
ENVIRONMENT=development  # or production
```

#### Environment Variables Explanation
- `COGNITO_DOMAIN`: AWS Cognito authentication domain
- `COGNITO_CLIENT_ID`: Your Cognito application client ID
- `COGNITO_CLIENT_SECRET`: Your Cognito application client secret
- `COGNITO_REGION`: AWS region where your Cognito user pool is hosted
- `COGNITO_USER_POOL_ID`: Unique identifier for your Cognito user pool
- `COGNITO_REDIRECT_URI`: Callback URL after authentication
- `ENVIRONMENT`: Application running mode (development/production)

## Setup Instructions

### 1. Create Environment File
1. Copy the sample configuration above
2. Replace placeholder values with your actual Cognito credentials
3. Save as `.env` in project root directory

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python main.py
```

## [Click here to check out the implementation with Boto3](https://github.com/VajraM-dev/AWS-Cognito-Authentication-with-FastAPI/tree/withBoto)