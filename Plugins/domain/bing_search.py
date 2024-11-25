import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse

def extract_domain(url):
    """从 URL 中提取域名"""
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_subdomains(domain):
    print(f"bing开始扫描域名: {domain}")
    num_pages = 50
    subdomains = set()

    # 请求头
    headers = {
        'cookie': 'MUID=23CCCA69F86C6F4E3769DF54F9646E16; MUIDB=23CCCA69F86C6F4E3769DF54F9646E16; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=986C2441723D4948B3EE4BF53B33F2DA&dmnchg=1; SRCHUSR=DOB=20241122&T=1732259355000&TPC=1732259356000; USRLOC=HS=1&ELOC=LAT=38.86565399169922|LON=121.5214614868164|N=%E7%94%98%E4%BA%95%E5%AD%90%E5%8C%BA%EF%BC%8C%E8%BE%BD%E5%AE%81%E7%9C%81|ELT=4|; _EDGE_S=SID=28EFD4F271D96D361DF4C1CD70D16C4E; _Rwho=u=d&ts=2024-11-22; _SS=SID=28EFD4F271D96D361DF4C1CD70D16C4E&R=18&RB=0&GB=0&RG=200&RP=18; _RwBf=r=0&ilt=22&ihpd=0&ispd=22&rc=18&rb=0&gb=0&rg=200&pc=18&mtu=0&rbb=0&g=0&cid=&clo=0&v=22&lka=0&lkt=0&aad=0&TH=; SRCHHPGUSR=SRCHLANG=zh-Hans&IG=4FDB3952530E4C6CBB2DBDF3E71F95BC&HV=1732261910&DM=1&BRW=XW&BRH=S&CW=1728&CH=281&SCW=1728&SCH=1709&DPR=2.0&UTC=480&EXLTT=24&PV=15.2.0&PRVCW=1728&PRVCH=900&WTS=63867856156&BZA=0'
    }

    for page in range(num_pages):
        start_index = page * 10
        url = f'https://www.bing.com/search?q=site%3a{domain}&first={start_index}&rdr=1&rdrig=E34A52340775442FBD6C5AC2F96EB9CB'
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取所有链接
            for link in soup.select('li.b_algo h2 a'):
                href = link.get('href')
                if href:
                    subdomains.add(extract_domain(href))  # 提取域名并添加到集合中

            # 随机延迟
            time.sleep(random.uniform(0, 1))

        except requests.RequestException as e:
            print(f"请求失败: {e}")

    unique_subdomains = list(subdomains)
    print(f"bing扫描完成，找到 {len(unique_subdomains)} 个子域名.")
    return unique_subdomains