import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
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

def get_subdomains(domain, mode='passive', dict_file=None):
    """
    :param domain: 要检查的域名
    :param mode: 'passive' 或 'dict'，根据模式获取子域名。
    :param dict_file: 字典文件路径（仅在字典扫描模式下使用）
    :return: 包含各个服务结果的字典
    """
    with ThreadPoolExecutor() as executor:
        futures = {}
        
        if mode == 'passive':  # 被动扫描
            futures[executor.submit(dns_search.get_subdomains, domain)] = 'dns_search'
            futures[executor.submit(crt_sh.get_subdomains, domain)] = 'crt_sh'
            futures[executor.submit(chaziyu_com.get_subdomains, domain)] = 'chaziyu_com'
            futures[executor.submit(bing_search.get_subdomains, domain)] = 'bing_search'
            futures[executor.submit(google_search.get_subdomains, domain)] = 'google_search'
            futures[executor.submit(baidu_search.get_subdomains, domain)] = 'baidu_search'
            futures[executor.submit(quake.get_subdomains, domain)] = 'quake'
            futures[executor.submit(censys_api.get_subdomains, domain)] = 'censys_api'
            futures[executor.submit(bevigil_api.get_subdomains, domain)] = 'bevigil_api'
            futures[executor.submit(threatbook.get_subdomains, domain)] = 'threatbook'  # 需要企业api账号
        
        elif mode == 'dict':  # 工具字典扫描+主动扫描
            if dict_file is None:
                futures[executor.submit(dig.get_subdomains, domain)] = 'dig'
                futures[executor.submit(site_map.get_subdomains, domain)] = 'site_map'
                futures[executor.submit(js_finder.get_subdomains, domain)] = 'js_finder'
                futures[executor.submit(ksubdomain.get_subdomains_tools, domain)] = 'tools'
                futures[executor.submit(ksubdomain.get_subdomains_dict, domain)] = 'ksubdomain_dict'
            else:
                futures[executor.submit(ksubdomain.get_subdomains_dict, dict_file, domain)] = 'ksubdomain_dict'
        
        else:
            print("请选择一种扫描的方式 'passive' 或 'dict'")
            return {}

        results = {}
        for future in as_completed(futures):
            service_name = futures[future]
            try:
                result = future.result()
                results[service_name] = result
            except Exception as e:
                print(f"{service_name} 发生异常: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='子域收集工具')
    parser.add_argument('-passive', dest='mode', action='store_const', const='passive', help='选择被动扫描')
    parser.add_argument('-dict', dest='mode', action='store_const', const='dict', help='选择字典扫描')
    parser.add_argument('domain', help='要扫描的域名')
    parser.add_argument('dict_file', nargs='?', help='字典文件路径（仅在字典扫描模式下使用）')

    args = parser.parse_args()
    
    domain = args.domain
    mode = args.mode
    dict_file = args.dict_file if mode == 'dict' else None  # 仅在字典扫描模式下使用字典文件路径
        
    if check_url.check_domain(domain):
        results = get_subdomains(domain, mode=mode, dict_file=dict_file)
        
        httpx_results = httpx.run_process_domains(results, domain)
        result_to_file.save_result_to_file(httpx_results)

if __name__ == "__main__":
    main()