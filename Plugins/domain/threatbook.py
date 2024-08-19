import requests
import configparser

# 创建配置解析器
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中读取 ThreatBook API 密钥
threatbook_api_key = config['threatbook_api']['api_key']

def get_subdomains(domain):
    url = "https://api.threatbook.cn/v3/domain/sub_domains"
    
    query = {
        "apikey": threatbook_api_key,  # 使用从配置文件中读取的 API 密钥
        "resource": domain
    }

    try:
        response = requests.get(url, params=query)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析 JSON 数据

        # 检查响应代码
        if data.get("response_code") != 0:
            print(f"ThreatBook API 返回错误: {data.get('verbose_msg')}")
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