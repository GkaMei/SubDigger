import subprocess
import dns.resolver
import json
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)

def get_ns_records(domain):
    """
    获取目标域名的NS记录
    """
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        return [str(ns_record.target).rstrip('.') for ns_record in ns_records]
    except Exception as e:
        logging.error(f"获取NS记录失败: {e}")
        return []

def perform_zone_transfer(ns_server, domain, timeout=5):
    """
    使用dig命令执行域传送，并设置超时时间
    """
    try:
        result = subprocess.run(['dig', f'@{ns_server}', domain, 'AXFR'], capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            logging.info(f"域传送返回数据: {result.stdout}")  # 打印返回数据
            return result.stdout
        else:
            logging.warning(f"域传送失败，返回码: {result.returncode}")
            return ""
    except subprocess.TimeoutExpired:
        logging.error("域传送超时")
        return ""
    except Exception as e:
        logging.error(f"执行域传送时发生错误: {e}")
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
                subdomain = parts[0].rstrip('.')
                subdomains.add(subdomain)
    return subdomains

def get_subdomains(domain):
    """
    获取目标域名的子域名并返回JSON格式的字符串
    """
    ns_servers = get_ns_records(domain)
    if not ns_servers:
        return json.dumps({"domain": domain, "subdomains": []}, indent=4)

    all_subdomains = set()
    for ns_server in ns_servers:
        zone_data = perform_zone_transfer(ns_server, domain)
        if zone_data:
            subdomains = extract_subdomains(zone_data)
            logging.info(f"域传送成功，提取子域名: {subdomains}")
            all_subdomains.update(subdomains)
        else:
            logging.info(f"域传送失败或没有返回数据，尝试下一个NS服务器。")

    if all_subdomains:
        return json.dumps({"domain": domain, "subdomains": list(all_subdomains)}, indent=4)
    else:
        logging.info("未能成功进行域传送，未提取到子域名。")
        return json.dumps({"domain": domain, "subdomains": []}, indent=4)