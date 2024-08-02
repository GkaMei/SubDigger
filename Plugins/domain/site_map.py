import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_subdomain(child, parent):
    parent_domains = parent.split('.')
    child_domains = child.split('.')
    return child_domains[-len(parent_domains):] == parent_domains

async def get_links(session, url, semaphore, base_url, visited, subdomains, max_depth):
    async with semaphore:
        try:
            async with session.get(url, allow_redirects=True) as response:
                # 检查响应状态
                response.raise_for_status()

                # 检查内容类型
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    return set()  # 如果不是 HTML 内容，返回空集合

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                links = set()

                for tag in soup.find_all([True]):
                    url_attr = 'href' if tag.name != 'img' else 'src'
                    if tag.name == 'form':
                        url_attr = 'action'
                    if tag.name == 'meta' and tag.get('http-equiv') == 'refresh':
                        content = tag.get('content')
                        if content:
                            url_part = content.split(';url=')[-1]
                            link = urljoin(url, url_part)
                    else:
                        link = urljoin(url, tag.get(url_attr, ''))

                    parsed_link = urlparse(link)
                    if is_subdomain(parsed_link.netloc, urlparse(base_url).netloc):
                        links.add(link)
                        subdomains.add(parsed_link.netloc)

                return links

        except aiohttp.ClientResponseError as e:
            if e.status == 405:
                logger.warning(f"Method Not Allowed for {url}. Consider checking the request method.")
            else:
                return set()
        except Exception as e:
            return set()


async def crawl(session, url, depth, semaphore, base_url, visited, subdomains, max_depth):
    if depth > max_depth or url in visited:
        return

    logger.info(f"Crawling: {url}, Depth: {depth}")
    visited.add(url)

    links = await get_links(session, url, semaphore, base_url, visited, subdomains, max_depth)
    tasks = [crawl(session, link, depth + 1, semaphore, base_url, visited, subdomains, max_depth) for link in links]
    await asyncio.gather(*tasks)


async def start_crawl(base_url, max_depth):
    semaphore = asyncio.Semaphore(100)
    visited = set()
    subdomains = set()

    async with aiohttp.ClientSession() as session:
        await crawl(session, base_url, 0, semaphore, base_url, visited, subdomains, max_depth)
    
    return subdomains


def get_subdomains(domain, max_depth=3):
    subdomains = asyncio.run(start_crawl(domain, max_depth))
    return list(subdomains)