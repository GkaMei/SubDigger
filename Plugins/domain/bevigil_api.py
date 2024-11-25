import requests
import configparser

# 创建配置解析器
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中读取 ThreatBook API 密钥
bevigil_api_key = config['bevigil_api']['api_key']

def get_subdomains(domain):
    print(f"bevigil开始扫描: {domain}")  # 开始扫描的提示

    # 使用 f-string 格式化 URL
    url = f'http://osint.bevigil.com/api/{domain}/subdomains/'
    headers = {
        'X-Access-Token': bevigil_api_key  # 替换为你的实际 API 密钥
    }

    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 提取子域名列表
        subdomains = data.get('subdomains', [])
        
        print(f"bevigil扫描完成，找到 {len(subdomains)} 个子域名.")  # 统计数量的提示
        
        return subdomains  # 返回子域名列表
    else:
        print('请求失败，状态码为:', response.status_code)
        return []