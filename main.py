import argparse
import Plugins.domain.check_url as check_url
import Plugins.domain.crt_sh as crt_sh
import Plugins.domain.ksubdomain as ksubdomain
import Plugins.domain.chaziyu_com as chaziyu_com
import Plugins.domain.dig as dig
import Plugins.domain.quake as quake 
import Plugins.domain.threatbook as threatbook
import Plugins.domain.google_search as google_search
import Plugins.domain.baidu_search as baidu_search
import Plugins.domain.js_finder as js_finder
import Plugins.domain.bevigil_api as bevigil_api
import Plugins.domain.censys_api as censys_api
import Plugins.domain.bing_search as bing_search
import Plugins.domain.httpx as httpx
import Plugins.domain.dns_search as dns_search
import Plugins.domain.site_map as site_map
import Plugins.ResultToFile.result_to_file as result_to_file
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_domain(domain):
    """
    检查域名是否存在泛解析。
    :return: 如果不存在泛解析，返回True；否则返回False
    """
    result = check_url.random_to_A(domain)
    if result == 5:
        print("该域名存在泛解析")
        return False
    else:
        print("该域名不存在泛解析,开始爆破子域名")
        return True


def get_subdomains(domain, mode='passive'):
    """
    :param domain: 要检查的域名
    :param mode: 'passive' 或 'active'，根据模式获取子域名。
    :return: 包含各个服务结果的字典
    """
    with ThreadPoolExecutor() as executor:
        futures = {}
        
        if mode == 'passive':
            futures = {
                # executor.submit(crt_sh.get_subdomains, domain): 'crt_sh',
                # executor.submit(chaziyu_com.get_subdomains, domain): 'chaziyu_com',
                executor.submit(bing_search.get_subdomains, domain): 'bing_search',
                # executor.submit(google_search.get_subdomains, domain): 'google_search',
                # executor.submit(baidu_search.get_subdomains, domain): 'baidu_search',
                # executor.submit(dig.get_subdomains, domain): 'dig', #测试域传送
                # executor.submit(dns_search.get_subdomains, domain): 'dns_search',
                # executor.submit(censys_api.get_subdomains, domain): 'censys_api',
                # executor.submit(bevigil_api.get_subdomains, domain): 'bevigil_api',
                # executor.submit(quake.get_subdomains, domain): 'quake', #360_api目前api可以使用
                # executor.submit(threatbook.get_subdomains, domain): 'threatbook', #微步,目前无api
            }
        elif mode == 'active':
            futures = {
                executor.submit(site_map.get_subdomains, domain): 'site_map',
                executor.submit(js_finder.get_subdomains, domain): 'js_finder',
                executor.submit(ksubdomain.get_subdomains, domain): 'ksubdomain',
            }
        else:
            print("请选择一种扫描的方式 'passive' 或 'active'")
            return {}

        results = {}
        for future in as_completed(futures):
            service_name = futures[future]
            try:
                result = future.result()
                results[service_name] = result
            except Exception as e:
                print(f"{service_name} generated an exception: {e}")
        
        return results


def main():
    """
    主函数，获取用户输入的域名并执行子域名获取和保存操作。
    """
    parser = argparse.ArgumentParser(description='强大的子域收集工具')
    parser.add_argument('-active', dest='mode', action='store_const', const='active', help='选择主动扫描')
    parser.add_argument('-passive', dest='mode', action='store_const', const='passive', help='选择被动扫描')
    parser.add_argument('domain', help='要扫描的域名')
    
    args = parser.parse_args()
    
    domain = args.domain
    mode = args.mode
    
    if mode is None:
        parser.error("必须选择一种扫描模式: -active 或 -passive")
    
    if check_domain(domain):
        results = get_subdomains(domain, mode=mode)
        
        httpx_results = httpx.process_domains(results)
        result_to_file.save_result_to_file(httpx_results)


if __name__ == '__main__':
    main()