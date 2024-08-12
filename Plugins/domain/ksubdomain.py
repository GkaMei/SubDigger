import subprocess
import json
import re
import os
import logging
from typing import List, Optional

# 设置日志记录
logging.basicConfig(level=logging.INFO)

TOOLS_DIR = os.path.abspath("tools")

def execute_command(command: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with error: {e}")
        return None

def extract_useful_info(output: str) -> List[str]:
    # 提取域名解析路径
    domain_pattern = re.compile(r"(\S+ => \S+)")
    domain_matches = domain_pattern.findall(output)
    
    if domain_matches:
        return [match.split(" => ")[0] for match in domain_matches]  # 返回提取的子域名
    else:
        logging.warning("No useful information found in the output.")
        return []  # 返回空列表表示未找到

def get_subdomains_tools(domain: str) -> List[str]:
    logging.info(f"Starting subdomain discovery for domain: {domain}")

    commands = {
        'subfinder': [os.path.join(TOOLS_DIR, 'subfinder', 'subfinder'), '-d', domain, '-silent'],
        'assetfinder': [os.path.join(TOOLS_DIR, 'assetfinder', 'assetfinder'), '--subs-only', domain],
        'findomain': [os.path.join(TOOLS_DIR, 'findomain', 'findomain'), '-t', domain, '-q']
    }

    all_subdomains = set()

    for tool, command in commands.items():
        output = execute_command(command)
        if output:
            logging.info(f"{tool.capitalize()} output:\n{output}")
            all_subdomains.update(output.splitlines())

    logging.info(f"Total unique subdomains found: {len(all_subdomains)}")
    return list(all_subdomains)

def get_subdomains_dict(domain: str, dict_file: Optional[str] = None) -> List[str]:
    """
    使用 ksubdomain 进行主动子域名发现。
    
    :param domain: 要检查的域名
    :param dict_file: 字典文件路径，如果为 None 则使用默认字典
    :return: 子域名列表
    """
    
    if dict_file is None:
        logging.info(f"运行内置字典扫描: {domain}")
        dict_file = os.path.join(TOOLS_DIR, "passwd", "Subdomain.txt")
    
    ksubdomain_command = [
        os.path.join(TOOLS_DIR, 'ksubdomain', 'ksubdomain'),
        '-d', domain,
        '-f', dict_file,
        '-full'
    ]
    
    output = execute_command(ksubdomain_command)    
    ksubdomain_output = extract_useful_info(output)
    logging.info(f"Total unique subdomains found: {len(ksubdomain_output)}")
    
    return list(ksubdomain_output)