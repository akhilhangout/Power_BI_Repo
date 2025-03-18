import requests
import msal
from import_requests import (
    TENANT_ID, CLIENT_ID, CLIENT_SECRET, SCOPE, AUTHORITY_URL, GROUP_ID
)
# Configuration imported from module

def get_access_token_requests():
    """Acquire an access token using the requests library."""
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": " ".join(SCOPE)
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to retrieve token:", response.json())
        return None

def get_access_token_msal():
    """Acquire an access token using the MSAL library."""
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY_URL,
        client_credential=CLIENT_SECRET,
    )

    response = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in response:
        return response["access_token"]
    else:
        print("Failed to retrieve token:", response.get("error_description"))
        return None

def get_dataflows(access_token):
    """Retrieve dataflows from Power BI REST API."""
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{GROUP_ID}/dataflows"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"Failed to retrieve dataflows: {response.status_code}")
        print(response.json())
        return None

def get_datasets(access_token):
    """Retrieve datasets from Power BI REST API."""
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{GROUP_ID}/datasets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"Failed to retrieve datasets: {response.status_code}")
        print(response.json())
        return None

def main(use_msal=True):
    """Main function to acquire token and retrieve dataflows and datasets."""
    if use_msal:
        access_token = get_access_token_msal()
    else:
        access_token = get_access_token_requests()

    if access_token:
        dataflows = get_dataflows(access_token)
        if dataflows:
            print("Dataflows:")
            for dataflow in dataflows:
                print(f"- Name: {dataflow['name']}, ID: {dataflow['objectId']}")

        datasets = get_datasets(access_token)
        if datasets:
            print("Datasets:")
            for dataset in datasets:
                print(f"- Name: {dataset['name']}, ID: {dataset['id']}")

if __name__ == "__main__":
    main(use_msal=False)  # Set to False to use requests library