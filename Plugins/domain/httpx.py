import os
import asyncio

# 使用环境变量或默认路径设置工具目录
TOOLS_DIR = os.getenv('TOOLS_DIR', os.path.abspath("tools"))

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

async def process_domains(result):
    """处理域名列表，使用异步扫描每个域名，并收集结果。"""
    unique_domains = set()

    # 收集去重后的域名
    for key, domains in result.items():
        if domains is not None and isinstance(domains, list):
            unique_domains.update(domains)

    # 使用 asyncio.gather 并发处理所有域名
    tasks = [scan_domain(domain) for domain in unique_domains]
    httpx_results = await asyncio.gather(*tasks, return_exceptions=True)

    # 处理结果，过滤掉错误
    processed_results = []
    for result in httpx_results:
        if isinstance(result, Exception):
            print(f"处理域名时发生错误: {result}")
        else:
            processed_results.append(result)

    return processed_results

def run_process_domains(result):
    """同步函数，运行异步处理域名的函数。"""
    return asyncio.run(process_domains(result))