import json

import click
import requests

from ..config import ACCOUNT_ID, API_BASE_URL, HEADERS


# MARK: - Get licenses
def get_licenses():
    """Get all licenses.
    Docs: https://keygen.sh/docs/api/licenses/#licenses-list

    Returns:
        list: A list of licenses.

    """
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


# MARK: - Create license
def create_license(name, group, policy, metadata):
    """Create a new license.
    Docs: https://keygen.sh/docs/api/licenses/#licenses-create

    Args:
        name (str): The name of the license.
        group (str): The ID of the group to associate with the license.
        policy (str): The ID of the policy to associate with the license.
        metadata (dict): Metadata to be associated with the license.

    """
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


# MARK: - Delete license
def delete_license(license_id):
    """Delete a license by its ID.
    Docs: https://keygen.sh/docs/api/licenses/#licenses-delete

    Args:
        license_id (str): The ID of the license to delete.

    Returns:
        bool: True if the license was deleted successfully, False otherwise.

    """
    response = requests.delete(f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/licenses/{license_id}", headers=HEADERS)
    response.raise_for_status()
    return response.status_code == 204  # Returns True if deletion was successful


# MARK: - Checkout license
def checkout_license(license_id, ttl, encrypt=True):
    """Checkout a license with the specified TTL (time to live) and encryption option.
    Docs: https://keygen.sh/docs/api/licenses/#licenses-actions-check-out

    Args:
        license_id (str): The ID of the license to checkout.
        ttl (int): The time to live for the license in seconds.
        encrypt (bool): Whether to encrypt the license. Defaults to True.

    Returns:
        dict: The response from the API containing the checked out license details.

    """
    url_params = {
        "ttl": ttl,
        "encrypt": encrypt
        # TODO: Add includes
        # https://keygen.sh/docs/api/licenses/#licenses-check-out-query-include
        # Include relationship data in the license file. Can be any combination of:
        # entitlements, product, policy, owner, users, environment, or group.
    }
    response = requests.post(
        f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/licenses/{license_id}/actions/check-out",
        headers=HEADERS,
        params=url_params
    )
    response.raise_for_status()
    return response.json()['data']
