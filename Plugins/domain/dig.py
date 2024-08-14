import subprocess
import dns.resolver

def get_ns_records(domain):
    """
    获取目标域名的NS记录
    """
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        return [str(ns_record.target).rstrip('.') for ns_record in ns_records]
    except Exception:
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
    except Exception:
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
    获取目标域名的子域名并返回子域名列表
    """
    try:
        ns_servers = get_ns_records(domain)
        if not ns_servers:
            return []

        all_subdomains = set()
        for ns_server in ns_servers:
            zone_data = perform_zone_transfer(ns_server, domain)
            if zone_data:
                subdomains = extract_subdomains(zone_data)
                all_subdomains.update(subdomains)

        if not all_subdomains:
            print("该域名不存在域传送漏洞")

        return list(all_subdomains)
    except Exception as e:
        print(f"发生错误: {e}")
        return []