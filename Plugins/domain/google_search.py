import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import random

def get_subdomains(domain):
    subdomains = set()  # 使用集合来存储不重复的子域名
    start = 0  # 从第一页开始
    while True:
        query = f'site:{domain}'
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            html = response.text
            new_subdomains = parse_results(html, domain)
            if not new_subdomains:  # 如果没有新子域名，停止抓取
                break
            subdomains.update(new_subdomains)
            start += 10  # 移动到下一页
            time.sleep(random.uniform(1, 2))
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            break
    return list(subdomains)

def parse_results(html, domain):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a', href=True)

        if title and link:
            link_url = link['href']
            if domain in link_url:
                subdomain = re.findall(r'https?://([^/]+)', link_url)
                if subdomain:
                    results.append(subdomain[0])  # 只保留子域名部分

    return results