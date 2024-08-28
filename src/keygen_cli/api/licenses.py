import requests
import json
import click
from ..config import API_BASE_URL, ACCOUNT_ID, HEADERS


def get_licenses():
    licenses = []
    page = 1
    while True:
        response = requests.get(
            f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/licenses",
            headers=HEADERS,
            params={"page[number]": page, "page[size]": 100}  # Increase page size to 100
        )
        response.raise_for_status()
        data = response.json()
        licenses.extend(data['data'])
        
        # Check if there's a next page
        if 'next' not in data['links'] or not data['links']['next']:
            break
        
        page += 1

    return licenses


def create_license(name, group, policy, metadata):
    payload = {
        "data": {
            "type": "licenses",
            "attributes": {
                "name": name,
                "metadata": {
                    "email": metadata.get("email"),
                    "userName": metadata.get("userName"),
                    "companyName": metadata.get("companyName")
                }
            },
            "relationships": {
                "policy": {
                    "data": {"type": "policies", "id": policy}
                }
            }
        }
    }
    if group:
        payload["data"]["relationships"]["group"] = {
            "data": {"type": "groups", "id": group}
        }
    
    try:
        response = requests.post(f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/licenses", json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.HTTPError as e:
        click.echo(f"HTTP Error: {e}")
        click.echo(f"Response content: {response.text}")
        click.echo(f"Request payload: {json.dumps(payload, indent=2)}")
        raise
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")
        raise
        raise


def delete_license(license_id):
    response = requests.delete(f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/licenses/{license_id}", headers=HEADERS)
    response.raise_for_status()
    return response.status_code == 204  # Returns True if deletion was successful