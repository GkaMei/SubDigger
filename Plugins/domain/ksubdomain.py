import subprocess
import os
import re
import json

def execute_command(domain):
    try:
        # 确保使用绝对路径
        ksubdomain_path = os.path.abspath("iniFile/ksubdomian/ksubdomain")
        
        # 执行命令并捕获输出
        result = subprocess.run([ksubdomain_path, "-d", domain], capture_output=True, text=True, check=True)
        
        # 处理并提取有用信息
        output = result.stdout
        return extract_useful_info(output)
    
    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"请root启动,错误输出: {e.stderr}"}, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        return json.dumps({"error": f"命令未找到。请确保 '{ksubdomain_path}' 已安装并在您的 PATH 中。"}, ensure_ascii=False, indent=4)
    except Exception as e:
        return json.dumps({"error": f"执行命令时发生错误: {e}"}, ensure_ascii=False, indent=4)

def extract_useful_info(output):
    # 提取域名解析路径
    domain_pattern = re.compile(r"(\S+ => \S+)")
    domain_matches = domain_pattern.findall(output)
    
    if domain_matches:
        domain_info = domain_matches
    else:
        domain_info = ["未找到域名解析路径"]
    
    # 返回 JSON 格式的结果
    return json.dumps({"domain_info": domain_info}, ensure_ascii=False, indent=4)