import requests

def get_subdomains(domain):
    # 使用 f-string 格式化 URL
    url = f'http://osint.bevigil.com/api/{domain}/subdomains/'
    headers = {
        'X-Access-Token': 'dnFutvGxy3RA7ZvM'  # 替换为你的实际 API 密钥
    }

    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 提取子域名列表
        subdomains = data.get('subdomains', [])
        return subdomains  # 返回子域名列表
    else:
        print('请求失败，状态码为:', response.status_code)
        return []