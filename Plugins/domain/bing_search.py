from requests_html import HTMLSession
import re
import logging

logging.getLogger('pyppeteer').setLevel(logging.WARNING)

def get_subdomains(domain):
    search_query = f'site:{domain}'
    num_pages = 100

    # 创建一个HTML会话
    session = HTMLSession()
    subdomains = set()
    # 遍历每一页并提取子域名
    for page in range(num_pages):
        start_index = page * 10
        url = f'https://www.bing.com/search?q={search_query}&first={start_index}'
        try:
            response = session.get(url)
            response.html.render(sleep=2)  # 等待页面加载
            regex_pattern = rf'https?://([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.{re.escape(domain)})'
            # 提取子域名并更新集合
            subdomains.update(re.findall(regex_pattern, response.html.html))
        except Exception as e:
            print(f"请求失败: {e}")

    # 关闭会话
    session.close()

    return list(subdomains)