import os
import asyncio
import logging

# 使用环境变量或默认路径设置工具目录
TOOLS_DIR = os.getenv('TOOLS_DIR', os.path.abspath("tools"))

def filter_domains(domains, base_domain):
    """过滤掉包含其他子域名的域名，只保留基准域名及其直接子域名。"""
    base_parts = base_domain.split('.')
    filtered_domains = []

    for domain in domains:
        # 检查域名是否以基准域名结尾
        if domain.endswith(base_domain):
            # 检查是否是直接子域名
            parts = domain.split('.')
            if len(parts) == len(base_parts) + 1:
                filtered_domains.append(domain)
            elif len(parts) == len(base_parts):
                filtered_domains.append(domain)

    return filtered_domains

async def execute_command(command):
    """异步执行给定的命令并捕获输出，返回命令的输出或错误信息。"""
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        return stdout.decode(errors='ignore').strip()  # 忽略解码错误
    else:
        return f"命令执行错误: {stderr.decode(errors='ignore').strip()}"  # 忽略解码错误

async def scan_domain(domain):
    """使用 httpx 工具扫描指定域名，并返回结果。"""
    httpx_command = [os.path.join(TOOLS_DIR, 'httpx', 'httpx'), '-u', domain, '-ip', '-title', '-nc']
    return domain, await execute_command(httpx_command)

async def process_domains(result, domain):
    """处理域名列表，使用异步扫描每个域名，并收集结果。"""
    unique_domains = set()

    # 收集去重后的域名
    for key, domains in result.items():
        if domains is not None and isinstance(domains, list):
            unique_domains.update(domains)

    # 过滤域名，只保留以domain结尾的域名
    filtered_domains = filter_domains(unique_domains, domain)

    # 使用 asyncio.gather 并发处理所有域名
    tasks = [scan_domain(domain) for domain in filtered_domains]
    httpx_results = await asyncio.gather(*tasks, return_exceptions=True)

    # 处理结果，过滤掉错误
    processed_results = []
    for result in httpx_results:
        if isinstance(result, Exception):
            print(f"处理域名时发生错误: {result}")
        else:
            processed_results.append(result)
    return processed_results

def run_process_domains(result, domain):
    """同步函数，运行异步处理域名的函数。"""
    return asyncio.run(process_domains(result, domain))