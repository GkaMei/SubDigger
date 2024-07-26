import os
import subprocess
import concurrent.futures

# 使用环境变量或默认路径设置工具目录
TOOLS_DIR = os.getenv('TOOLS_DIR', os.path.abspath("tools"))

def execute_command(command):
    """执行给定的命令并捕获输出，返回命令的输出或错误信息。"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"命令执行错误: {e.stderr}"
    except FileNotFoundError:
        return "命令未找到。请确保命令已安装并在您的 PATH 中。"
    except Exception as e:
        return f"执行命令时发生错误: {e}"

def scan_domain(domain):
    """使用 httpx 工具扫描指定域名，并返回结果。"""
    httpx_command = [os.path.join(TOOLS_DIR, 'httpx', 'httpx'), '-u', domain, '-ip', '-title', '-nc']
    return domain, execute_command(httpx_command).strip()

def process_domains(result):
    """处理域名列表，使用多线程扫描每个域名，并收集结果。"""
    unique_domains = set()

    for key, domains in result.items():
        if domains is not None and isinstance(domains, list):
            unique_domains.update(domains)

    httpx_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scan_domain, domain): domain for domain in unique_domains}
        for future in concurrent.futures.as_completed(futures):
            domain = futures[future]
            try:
                httpx_results.append(future.result())
            except Exception as e:
                print(f"处理域名 {domain} 时发生错误: {e}")

    return httpx_results