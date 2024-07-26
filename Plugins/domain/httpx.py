import os
import subprocess
import concurrent.futures

TOOLS_DIR = os.path.abspath("tools")

def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"命令执行错误: {e.stderr}"
    except FileNotFoundError:
        return "命令未找到。请确保命令已安装并在您的 PATH 中。"
    except Exception as e:
        return f"执行命令时发生错误: {e}"

def scan_domain(domain):
    httpx_command = f"{os.path.join(TOOLS_DIR, 'httpx', 'httpx')} -u {domain} -ip -title"
    return domain, execute_command(httpx_command).strip()

def process_domains(result):
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