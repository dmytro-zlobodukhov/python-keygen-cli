import requests

from ..config import ACCOUNT_ID, API_BASE_URL, HEADERS


def get_packages():
    packages = []
    page = 1
    while True:
        response = requests.get(
            f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/packages",
            headers=HEADERS,
            params={"page[number]": page, "page[size]": 100}
        )
        response.raise_for_status()
        data = response.json()
        packages.extend(data['data'])

        if 'next' not in data['links'] or not data['links']['next']:
            break

        page += 1

    return packages
