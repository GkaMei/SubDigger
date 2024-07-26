import re
import requests

def get_subdomains(domain):
    url = "https://api.threatbook.cn/v3/domain/sub_domains"

    query = {
    "apikey":"433a77647d4c47c6a870122a1f0b8efed752d1294d804b25bfbe7dc31668d772",
    "resource":domain
    }

    response = requests.request("GET", url, params=query)

    # 使用正则表达式提取所有域名
    subdomain_pattern = r'\b([a-zA-Z0-9-]+)\.' + re.escape(domain) + r'\b'
    subdomains = re.findall(subdomain_pattern, response.text)
    # 组合成完整的域名
    full_domains = [f"{sub}.{domain}" for sub in subdomains]

    return list(set(full_domains))  # 去重并返回
