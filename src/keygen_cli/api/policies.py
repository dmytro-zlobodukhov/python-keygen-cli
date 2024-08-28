import requests
from ..config import API_BASE_URL, ACCOUNT_ID, HEADERS


def get_policies():
    response = requests.get(f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/policies", headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data['data']  # Return the full policy data