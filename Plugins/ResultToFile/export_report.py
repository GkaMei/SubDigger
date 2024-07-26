import json
import os
import datetime

def extract_domains_to_file(result):
    unique_domains = set()  # 使用集合来去重

    # 遍历字典中的每个键值对
    for key, domains in result.items():
        # 检查 domains 是否为 None 或者不是列表
        if domains is not None and isinstance(domains, list):
            # 将每个域名添加到集合中
            unique_domains.update(domains)

    result =  list(unique_domains)  # 转换为列表返回
    # 获取当前时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 创建相对路径目录
    directory = "result"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 创建文件名
    filename = f"{directory}/result_{timestamp}.json"
    
    # 将结果转换为 JSON 字符串并写入文件
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)