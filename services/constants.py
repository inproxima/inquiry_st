import os
from dotenv import load_dotenv

load_dotenv(override=True)

REGION_NAME = os.getenv(
    "REGION", "ca-central-1"
)  # Default to "ca-central-1" if not set
ENV_NAME = os.getenv("ENV_NAME")

# AWS DynamoDB
UNIT_PLAN_TABLE_NAME = f"unit_plan"
USER_ID_INDEX_NAME = "user-id-index"
ORGANIZATION_TABLE_NAME = f"organization"

# AWS Cognito
USER_POOL_ID = os.getenv("USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

RegExPattern = "^Bearer\\s+(.*)"

# AWS PostgresDB
POSTGRES_ENDPOINT_URL = os.getenv("POSTGRES_ENDPOINT_URL")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APP_OPENAI_MODEL = "gpt-4o"
APP_OPENAI_MODEL_2 = "o1"
APP_OPENAI_MODEL_3 = "o3-mini"
APP_OPENAI_MODEL_4 = "gpt-4o-2024-08-06"

# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
# CLAUDE_MODEL = "claude-3-5-sonnet-20240620"
# Cognito User Roles
TEACHERS_INCLUDED_ROLES = ["Teacher"]
TEACHERS_EXCLUDED_ROLES = ["Admin"]

NEW_USERS_DEFAULT_ROLES = ["Teacher"]
AUTH_DOMAIN_NAME = os.getenv("AUTH_DOMAIN_NAME")
TOKEN_URL = (
    f"https://{AUTH_DOMAIN_NAME}.auth.{REGION_NAME}.amazoncognito.com/oauth2/token"
)