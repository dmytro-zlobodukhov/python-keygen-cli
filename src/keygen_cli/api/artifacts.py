import requests
from ..config import API_BASE_URL, ACCOUNT_ID, HEADERS


# MARK: - Get artifacts
def get_artifacts():
    """
    Get all artifacts.
    Docs: https://keygen.sh/docs/api/artifacts/#artifacts-list

    Returns:
        list: A list of artifacts.
    """
    artifacts = []
    page = 1

    while True:
        response = requests.get(
            url=f"{API_BASE_URL}/accounts/{ACCOUNT_ID}/artifacts", 
            headers=HEADERS, 
            params={"page[number]": page, "page[size]": 100}  # Increase page size to 100
        )
        response.raise_for_status()
        data = response.json()
        artifacts.extend(data["data"])

        if 'next' not in data['links'] or not data['links']['next']:
            break

        page += 1

    return artifacts


# MARK: - Get artifacts by name
def get_artifacts_by_name(name):
    artifacts = get_artifacts()
    return [artifact for artifact in artifacts if name in artifact['attributes']['filename']]


# MARK: - Get artifacts by version
def get_artifacts_by_version(version):
    artifacts = get_artifacts()
    return [artifact for artifact in artifacts if version in artifact['attributes']['filename']]


# MARK: - Get artifacts by platform
def get_artifacts_by_platform(platform):
    artifacts = get_artifacts()
    return [artifact for artifact in artifacts if platform in artifact['attributes']['platform']]


# MARK: - Get artifacts by architecture
def get_artifacts_by_arch(arch):
    artifacts = get_artifacts()
    return [artifact for artifact in artifacts if arch in artifact['attributes']['arch']]