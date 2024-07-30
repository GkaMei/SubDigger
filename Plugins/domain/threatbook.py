import requests

def get_subdomains(domain):
    url = "https://api.threatbook.cn/v3/domain/sub_domains"
    
    query = {
        "apikey": "433a77647d4c47c6a870122a1f0b8efed752d1294d804b25bfbe7dc31668d772",
        "resource": domain
    }

    try:
        response = requests.get(url, params=query)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析 JSON 数据

        # 检查响应代码
        if data.get("response_code") != 0:
            print(f"threatbook API 返回错误: {data.get('verbose_msg')}")
            return []

        # 提取子域名
        subdomains = data['data']['sub_domains']['data']

        return list(set(subdomains))  # 去重并返回

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except ValueError as e:
        print(f"解析 JSON 失败: {e}")
        return []