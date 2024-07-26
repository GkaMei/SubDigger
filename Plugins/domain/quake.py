import re
import requests

def get_subdomains(domain):
    headers = {
        "X-QuakeToken": "65f4f16a-5ac6-4fb7-830a-3f071f620ff8"
    }

    data = {
        "query": f"domain:{domain}",
        "start": 0,
        "size": 100  # 增加返回的结果数量
    }

    response = requests.post(url="https://quake.360.net/api/v3/search/quake_service", headers=headers, json=data)
    # 使用正则表达式提取所有域名
    subdomain_pattern = r'\b([a-zA-Z0-9-]+)\.' + re.escape(domain) + r'\b'
    subdomains = re.findall(subdomain_pattern, response.text)
    # 组合成完整的域名
    full_domains = [f"{sub}.{domain}" for sub in subdomains]

    return list(set(full_domains))  # 去重并返回