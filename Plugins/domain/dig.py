import subprocess
import dns.resolver
import json

def get_ns_records(domain):
    """
    获取目标域名的NS记录
    """
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        return [str(ns_record.target) for ns_record in ns_records]
    except Exception as e:
        return []

def perform_zone_transfer(ns_server, domain, timeout=5):
    """
    使用dig命令执行域传送，并设置超时时间
    """
    try:
        result = subprocess.run(['dig', f'@{ns_server}', domain, 'AXFR'], capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
    except subprocess.TimeoutExpired:
        return ""
    except Exception as e:
        return ""

def extract_subdomains(zone_data):
    """
    从域传送数据中提取子域名
    """
    subdomains = set()
    for line in zone_data.splitlines():
        if line and not line.startswith(';'):
            parts = line.split()
            if len(parts) > 0:
                subdomain = parts[0]
                if subdomain.endswith('.'):
                    subdomain = subdomain[:-1]
                subdomains.add(subdomain)
    return subdomains

def get_subdomains(domain):
    """
    获取目标域名的子域名并返回JSON格式的字符串
    """
    # 获取目标域名的NS记录
    ns_servers = get_ns_records(domain)
    if not ns_servers:
        return json.dumps({"domain": domain, "subdomains": []}, indent=4)

    # 尝试对每个NS服务器执行域传送
    for ns_server in ns_servers:
        zone_data = perform_zone_transfer(ns_server, domain)
        if zone_data:
            subdomains = extract_subdomains(zone_data)
            print(f"域传送成功，提取子域名...")
            return json.dumps({"domain": domain, "subdomains": list(subdomains)}, indent=4)
    
    return json.dumps({"domain": domain, "subdomains": []}, indent=4)

# # 示例调用
# subdomains_json = get_subdomains("qq.com")
# print(subdomains_json)