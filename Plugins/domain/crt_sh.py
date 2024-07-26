import requests
from bs4 import BeautifulSoup
import json

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return []

    subdomains = set()
    for entry in data:
        if 'name_value' in entry:
            name_value = entry['name_value']
            if '\n' in name_value:
                for subdomain in name_value.split('\n'):
                    if subdomain.endswith(domain):
                        subdomains.add(subdomain.strip())
            else:
                if name_value.endswith(domain):
                    subdomains.add(name_value.strip())

    return list(subdomains)