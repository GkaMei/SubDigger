from censys.search import CensysCerts
from censys.common.exceptions import (
    CensysUnauthorizedException,
    CensysRateLimitExceededException,
    CensysException,
)
import configparser
import sys

# 创建配置解析器
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中读取 Censys API 凭据
censys_api_id = config['censys_api']['api_id']
censys_api_secret = config['censys_api']['api_secret']

def get_subdomains(domain):
    try:
        # 使用从配置文件中读取的 API 凭据
        censys_certificates = CensysCerts(api_id=censys_api_id, api_secret=censys_api_secret)
        query = f"names: {domain}"
        subdomains = set()
        page_number = 1
        
        while page_number <= 2:
            results = censys_certificates.search(query, per_page=100, page=page_number)
                        
            if not results:
                break

            for result in results:
                if isinstance(result, list):
                    for item in result:
                        subdomains.update(item.get("names", []))
                else:
                    subdomains.update(result.get("names", []))
                
            page_number += 1
            
        filter_subdomains = [
            subdomain for subdomain in subdomains
            if "*" not in subdomain and subdomain.endswith(domain) and subdomain != domain
        ]

        return filter_subdomains

    except CensysUnauthorizedException:
        sys.stderr.write("[-] Invalid Censys credentials or access limited.\n")
        sys.exit(1)
    except CensysRateLimitExceededException:
        sys.stderr.write("[-] Censys rate limit exceeded.\n")
        return list()
    except CensysException as e:
        sys.stderr.write(f"[-] An error occurred: {e}\n")
        return list()