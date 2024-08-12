import aiohttp
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_subdomain(domain):
    search_query = f'site:{domain}'
    num_pages = 100
    subdomains = set()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(num_pages):
            start_index = page * 10
            url = f'https://www.bing.com/search?q={search_query}&first={start_index}'
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for html in responses:
            regex_pattern = rf'https?://([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.{re.escape(domain)})'
            subdomains.update(re.findall(regex_pattern, html))

    return list(subdomains)

def run_async(domain):
    loop = asyncio.new_event_loop()  # 创建新的事件循环
    asyncio.set_event_loop(loop)  # 设置为当前事件循环
    subdomains = loop.run_until_complete(get_subdomain(domain))
    loop.close()  # 关闭事件循环
    return subdomains

def get_subdomains(domain):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(run_async, domain)
        return future.result()