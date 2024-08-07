import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import random

def get_subdomains(domain):
    subdomains = set()
    start = 0
    while True:
        query = f'site:{domain}'
        url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&pn={start}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
            new_subdomains = parse_results(html, domain)
            if not new_subdomains:
                break
            subdomains.update(new_subdomains)
            start += 10
            time.sleep(random.uniform(1, 2))
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            break
    return list(subdomains)

def parse_results(html, domain):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='result'):  # 根据实际的 HTML 结构更新类名
        link = g.find('a', href=True)
        if link:
            link_url = link['href']
            final_url = follow_redirect(link_url)
            if domain in final_url:
                subdomain = re.findall(r'https?://([^/]+)', final_url)
                if subdomain:
                    results.append(subdomain[0])
    return results

def follow_redirect(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except requests.RequestException:
        return url