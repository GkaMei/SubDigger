import requests
import re
import json

def get_subdomains(domain):
    print(f"chaziyu开始扫描域名: {domain}")  # 开始扫描的提示

    url = f'https://chaziyu.com/{domain}/'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Cookie': 'Hm_lvt_84b516ce8f9de1ceab6dfd1b5f9e8be0=1721359474; HMACCOUNT=E94E17342872267E; Hm_lpvt_84b516ce8f9de1ceab6dfd1b5f9e8be0=1721359565',
        'Referer': f'https://chaziyu.com/{domain}/',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        return json.dumps({"error": f"请求错误: {e}"}, ensure_ascii=False, indent=4)

    if response.status_code == 200:
        try:
            subdomains = re.findall(rf'\b(?:[a-zA-Z0-9-]+\.)*{re.escape(domain)}\b', response.text)
            unique_subdomains = list(set(subdomains))  # 去重
            print(f"chaziyu扫描完成，找到 {len(unique_subdomains)} 个子域名.")  # 统计数量的提示
            return unique_subdomains
        except Exception as e:
            return json.dumps({"error": f"解析错误: {e}"}, ensure_ascii=False, indent=4)
    else:
        return json.dumps({"error": f"请求失败，状态码: {response.status_code}"}, ensure_ascii=False, indent=4)