import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_subdomain(child: str, parent: str) -> bool:
    parent_domains = parent.split('.')
    child_domains = child.split('.')
    return child_domains[-len(parent_domains):] == parent_domains

def extract_links(soup: BeautifulSoup, base_url: str, subdomains: set) -> set:
    links = set()
    for tag in soup.find_all(['a', 'img', 'form', 'meta']):
        url_attr = 'href' if tag.name != 'img' else 'src'
        if tag.name == 'form':
            url_attr = 'action'
        if tag.name == 'meta' and tag.get('http-equiv') == 'refresh':
            content = tag.get('content')
            if content:
                url_part = content.split(';url=')[-1]
                link = urljoin(base_url, url_part)
        else:
            link = urljoin(base_url, tag.get(url_attr, ''))

        parsed_link = urlparse(link)
        if is_subdomain(parsed_link.netloc, urlparse(base_url).netloc):
            links.add(link)
            subdomains.add(parsed_link.netloc)
    return links

async def get_links(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore, base_url: str, visited: set, subdomains: set) -> set:
    async with semaphore:
        try:
            async with session.get(url, allow_redirects=True, timeout=10) as response:
                response.raise_for_status()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    return set()

                html = await response.text()
                if not html.strip():
                    logger.warning(f"Received empty HTML for {url}")
                    return set()

                soup = BeautifulSoup(html, 'html.parser')
                return extract_links(soup, base_url, subdomains)

        except aiohttp.ClientResponseError as e:
            logger.warning(f"Error fetching {url}: {e}")
            return set()
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            return set()

async def crawl(session: aiohttp.ClientSession, url: str, depth: int, semaphore: asyncio.Semaphore, base_url: str, visited: set, subdomains: set, max_depth: int):
    if depth > max_depth or url in visited:
        return

    logger.info(f"Crawling: {url}, Depth: {depth}")
    visited.add(url)

    links = await get_links(session, url, semaphore, base_url, visited, subdomains)
    tasks = [crawl(session, link, depth + 1, semaphore, base_url, visited, subdomains, max_depth) for link in links]
    await asyncio.gather(*tasks)

async def start_crawl(base_url: str, max_depth: int) -> set:
    semaphore = asyncio.Semaphore(100)
    visited = set()
    subdomains = set()

    async with aiohttp.ClientSession() as session:
        await crawl(session, base_url, 0, semaphore, base_url, visited, subdomains, max_depth)
    
    return subdomains

def get_subdomains(domain: str, max_depth: int = 3) -> list:
    """
    获取指定域名的子域名。

    参数:
    domain (str): 要爬取的域名，可能不包含协议（http:// 或 https://）。
    max_depth (int): 爬取的最大深度，默认为 3。
    """
    
    # 检查 domain 是否以 http:// 或 https:// 开头，如果没有则添加 http://
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain

    # 使用 asyncio.run 启动异步爬取，获取子域名
    subdomains = asyncio.run(start_crawl(domain, max_depth))

    return list(subdomains)