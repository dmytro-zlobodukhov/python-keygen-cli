import requests
from ..config import API_BASE_URL, ACCOUNT_ID, HEADERS


def get_releases():
    releases = []
    page = 1
    while True:
        response = requests.get(
            f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/releases",
            headers=HEADERS,
            params={"page[number]": page, "page[size]": 100}  # Increase page size to 100
        )
        response.raise_for_status()
        data = response.json()
        releases.extend(data['data'])

        # Check if there's a next page
        if 'next' not in data['links'] or not data['links']['next']:
            break

        page += 1

    return releases


def get_releases_by_name(name):
    releases = get_releases()
    return [release for release in releases if release['attributes']['name'] == name]