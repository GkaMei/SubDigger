import datetime
import os
import json

def save_result_to_file(result):
    # 获取当前时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 创建相对路径目录
    directory = "result"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 创建文件名
    filename = f"{directory}/result_{timestamp}.json"
    
    # 将结果转换为JSON字符串并写入文件
    with open(filename, 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)