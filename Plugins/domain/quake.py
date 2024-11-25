import re
import requests
import configparser

def get_subdomains(domain):
    # 创建配置解析器
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 从配置文件中读取 Quake API 密钥
    quake_api_key = config['quake_api']['api_key']

    headers = {
        "X-QuakeToken": quake_api_key  # 使用从配置文件中读取的密钥
    }

    data = {
        "query": f"domain:{domain}",
        "start": 0,
        "size": 60  # 增加返回的结果数量
    }

    print(f"360开始扫描: {domain}")

    response = requests.post(url="https://quake.360.net/api/v3/search/quake_service", headers=headers, json=data)
    
    # 使用正则表达式提取所有域名
    subdomain_pattern = r'\b([a-zA-Z0-9-]+)\.' + re.escape(domain) + r'\b'
    subdomains = re.findall(subdomain_pattern, response.text)
    
    # 组合成完整的域名
    full_domains = [f"{sub}.{domain}" for sub in subdomains]

    unique_domains = list(set(full_domains))  # 去重并返回

    print(f"360扫描完成，找到 {len(unique_domains)} 个子域名.")  # 统计数量的提示

    return unique_domains