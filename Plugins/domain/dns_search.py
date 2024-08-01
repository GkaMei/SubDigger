import dns.resolver
import re

def resolve_dns_records(domain, record_type):
    """解析指定类型的 DNS 记录，并返回结果列表。"""
    try:
        return dns.resolver.resolve(domain, record_type)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return []

def extract_subdomains_from_records(records, attr):
    """从 DNS 记录中提取子域名。"""
    subdomains = set()
    for record in records:
        subdomain = getattr(record, attr).to_text().rstrip('.')
        subdomains.add(subdomain)
    return subdomains

def get_subdomains(domain):
    subdomains = set()

    # 查询不同类型的 DNS 记录
    record_types = {
        'SRV': 'target',
        'MX': 'exchange',
        'NS': 'target'
    }
    for record_type, attr in record_types.items():
        records = resolve_dns_records(domain, record_type)
        subdomains.update(extract_subdomains_from_records(records, attr))

    # 查询 TXT 记录
    txt_records = resolve_dns_records(domain, 'TXT')
    for txt_record in txt_records:
        for subdomain in txt_record.strings:
            subdomain = subdomain.decode()
            if re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', subdomain):
                subdomains.add(subdomain)

    # 过滤有效的子域名
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    subdomains = {subdomain for subdomain in subdomains if re.match(pattern, subdomain)}

    return list(subdomains)