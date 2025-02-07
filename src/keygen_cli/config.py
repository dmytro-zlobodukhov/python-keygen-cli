import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_BASE_URL = os.environ.get("KEYGEN_API_BASE_URL", "https://api.keygen.sh/v1").strip()
KEYGEN_PRODUCT_TOKEN = os.environ.get("KEYGEN_PRODUCT_TOKEN", "").strip()
ACCOUNT_ID = os.environ.get("KEYGEN_ACCOUNT_ID", "").strip()

HEADERS = {
    "Authorization": f"Bearer {KEYGEN_PRODUCT_TOKEN}",
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
}
