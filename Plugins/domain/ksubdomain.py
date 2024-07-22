import subprocess
import json
import re
import os

TOOLS_DIR = os.path.abspath("tools")

def execute_command(command):
    try:
        # 执行命令并捕获输出
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"命令执行错误: {e.stderr}"
    except FileNotFoundError:
        return f"命令未找到。请确保命令已安装并在您的 PATH 中。"
    except Exception as e:
        return f"执行命令时发生错误: {e}"

def extract_useful_info(output):
    # 提取域名解析路径
    domain_pattern = re.compile(r"(\S+ => \S+)")
    domain_matches = domain_pattern.findall(output)
    
    if domain_matches:
        return [match.split(" => ")[0] for match in domain_matches]  # 返回提取的子域名
    else:
        return []  # 返回空列表表示未找到

def get_subdomains(domain):
    # 使用 subfinder 进行被动子域名发现
    subfinder_command = f"{os.path.join(TOOLS_DIR, 'subfinder', 'subfinder')} -d {domain} -silent"
    subfinder_output = execute_command(subfinder_command)
    
    # 使用 assetfinder 进行被动子域名发现
    assetfinder_command = f"{os.path.join(TOOLS_DIR, 'assetfinder', 'assetfinder')} --subs-only {domain}"
    assetfinder_output = execute_command(assetfinder_command)
    
    # 使用 findomain 进行主动子域名发现
    findomain_command = f"{os.path.join(TOOLS_DIR, 'findomain', 'findomain')} -t {domain} -q"
    findomain_output = execute_command(findomain_command)

    # ksubdomain 进行主动子域名发现
    ksubdomain_command = f"{os.path.join(TOOLS_DIR, 'ksubdomain', 'ksubdomain')} -d {domain}"
    output = execute_command(ksubdomain_command)
    ksubdomain_output = extract_useful_info(output)

    # 合并结果并去重
    all_subdomains = set(
        (subfinder_output.splitlines() if subfinder_output else []) +
        (assetfinder_output.splitlines() if assetfinder_output else []) +
        (findomain_output.splitlines() if findomain_output else []) +
        ksubdomain_output
    )
    
    # JSON 输出
    output_data = {
        "domain": domain,
        "subdomains": list(all_subdomains)
    }
    
    return json.dumps(output_data, ensure_ascii=False, indent=4)