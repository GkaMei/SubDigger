import requests
from bs4 import BeautifulSoup
import time
import re
import random



def get_subdomains(search_query):
    base_url = "https://www.bing.com/search"
    subdomains = set()
    offset = 0
    query = f'site:{search_query}'
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.bing.com/'
    }

    while True:
        params = {
            'q': query,
            'first': offset + 1,
            'count': 10
        }
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                break
        except requests.RequestException as e:
            print(f"请求异常: {e}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = soup.find_all('li', class_='b_algo')
        if not results:
            break
        
        for result in results:
            link = result.find('a')['href']
            # 从链接中提取子域名
            domain_match = re.search(r'https?://([a-zA-Z0-9.-]+)', link)
            if domain_match:
                subdomain = domain_match.group(1)
                if subdomain.endswith(search_query):
                    subdomains.add(subdomain)
        
        offset += 10
        print(f"当前偏移量: {offset}")
        time.sleep(random.uniform(1, 2))

    return list(subdomains)

# 示例调用
if __name__ == "__main__":
    search_query = "qq.com"
    subdomains = get_subdomains(search_query)
    print(subdomains)