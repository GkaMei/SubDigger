import os
import argparse
import logging
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
import Plugins.domain.vt_finder as vt_finder
import Plugins.domain.bing_search as bing_search
import Plugins.domain.httpx as httpx
import Plugins.domain.dns_search as dns_search
import Plugins.domain.site_map as site_map
import Plugins.ResultToFile.result_to_file as result_to_file

# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_subdomains(domain, mode='passive', dict_file=None):
    """
    :param domain: 要检查的域名
    :param mode: 'passive' 或 'dict'，根据模式获取子域名。
    :param dict_file: 字典文件路径（仅在字典扫描模式下使用）
    :return: 包含各个服务结果的字典
    """
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        
        try:
            if mode == 'passive':  # 被动扫描
                futures[executor.submit(crt_sh.get_subdomains, domain)] = 'crt_sh'
                futures[executor.submit(chaziyu_com.get_subdomains, domain)] = 'chaziyu_com'
                futures[executor.submit(bing_search.get_subdomains, domain)] = 'bing_search'
                futures[executor.submit(google_search.get_subdomains, domain)] = 'google_search'
                futures[executor.submit(baidu_search.get_subdomains, domain)] = 'baidu_search'
                futures[executor.submit(vt_finder.get_subdomains, domain)] = 'vt_finder'
                futures[executor.submit(bevigil_api.get_subdomains, domain)] = 'bevigil_api'
                futures[executor.submit(quake.get_subdomains, domain)] = 'quake'
                # futures[executor.submit(censys_api.get_subdomains, domain)] = 'censys_api'  #需要升级账户
                # futures[executor.submit(threatbook.get_subdomains, domain)] = 'threatbook'  # 需要升级账户
            elif mode == 'active':  # 主动扫描
                futures[executor.submit(dig.get_subdomains, domain)] = 'dig'
                futures[executor.submit(site_map.get_subdomains, domain)] = 'site_map'
                futures[executor.submit(js_finder.get_subdomains, domain)] = 'js_finder'
                futures[executor.submit(dns_search.get_subdomains, domain)] = 'dns_search'
                futures[executor.submit(ksubdomain.get_subdomains_tools, domain)] = 'tools'
            elif mode == 'dict':  # 字典扫描
                if not dict_file:
                    logging.error("字典扫描模式需要提供字典文件路径！")
                    return {}
                futures[executor.submit(ksubdomain.get_subdomains_dict, domain, dict_file)] = 'ksubdomain_dict'
            else:
                logging.error("无效的扫描模式！请选择 'passive', 'active' 或 'dict'")
                return {}

            # 处理结果
            for future in as_completed(futures):
                service_name = futures[future]
                try:
                    results[service_name] = future.result()
                    logging.info(f"{service_name} 扫描完成。")
                except Exception as e:
                    logging.error(f"{service_name} 扫描发生异常: {e}")
        except Exception as e:
            logging.exception(f"线程池执行时发生异常: {e}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='子域名收集工具')
    parser.add_argument('-passive', dest='mode', action='store_const', const='passive', help='选择被动扫描 (-passive domain)')
    parser.add_argument('-active', dest='mode', action='store_const', const='active', help='选择主动扫描 (-active domain)')
    parser.add_argument('-dict', dest='mode', action='store_const', const='dict', help='字典扫描模式，需要字典文件 (-dict domain dict_file)')
    parser.add_argument('domain', help='要扫描的域名')
    parser.add_argument('dict_file', nargs='?', help='字典文件路径（仅在字典模式下需要）')

    args = parser.parse_args()
    
    domain = args.domain
    mode = args.mode
    dict_file = args.dict_file if mode == 'dict' else None

    print(domain,mode,dict_file)

    if check_url.check_domain(domain):
        results = get_subdomains(domain, mode=mode, dict_file=dict_file)
        logging.info(f"扫描结果: {results}")
        httpx_results = httpx.run_process_domains(results, domain)
        result_to_file.save_result_to_file(httpx_results)
    else:
        logging.error(f"无效的域名: {domain}")

if __name__ == "__main__":
    main()
