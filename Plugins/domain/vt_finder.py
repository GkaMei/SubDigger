from __future__ import print_function
import sys
import requests
import time

__author__ = "Bharath"
__version__ = "0.1.0"
__description__ = "A script to extract sub-domains that VirusTotal has found for a given domain name"

# 在这里定义您的 API 密钥
API_KEY = "007b5aef53b4d4e57b2279af1c7065dc3012b2478db29fb481026d8cda1ba753"

def get_subdomains(domain_name):
    """Check VirusTotal for all subdomains of the given domain."""
    url = f"https://www.virustotal.com/api/v3/domains/{domain_name}/subdomains"
    print(f"VT开始扫描: {domain_name}")

    subdomains = []
    headers = {
        'x-apikey': API_KEY
    }
    params = {'limit': 2000}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'data' in data:
                subdomains.extend(item['id'] for item in data['data'])
                print(f"VT找到 {len(data['data'])} subdomains.")
            else:
                print("\033[33mNo more subdomains found.\033[0m")
                break

            # 检查是否有更多的子域名
            if 'meta' in data and 'next' in data['meta']:
                params['offset'] = data['meta']['next']  # 更新偏移量以获取下一页
            else:
                break  # 没有更多的子域名

            time.sleep(1)

        except requests.RequestException as e:
            print(f"\033[31mError: {e}\033[0m")
            sys.exit(1)

    return subdomains

def print_results(subdomains):
    """Print the subdomains from the search results."""
    if subdomains:
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("\033[33mNo subdomains found.\033[0m")