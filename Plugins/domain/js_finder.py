import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 提取 JavaScript 中的 URL
def extract_URL(JS):
    pattern_raw = r"""
      (?:"|')                               # 开始的引号
      (
        ((?:[a-zA-Z]{1,10}://|//)           # 匹配协议 [a-z]*1-10 或 //
        [^"'/]{1,}\.                        # 匹配域名（任意字符 + 点）
        [a-zA-Z]{2,}[^"']{0,})              # 域名后缀和/或路径
        |
        ((?:/|\.\./|\./)                    # 以 /, ../, ./ 开头
        [^"'><,;| *()(%%$^/\\\[\]]          # 下一个字符不能是...
        [^"'><,;|()]{1,})                   # 剩余字符不能是
        |
        ([a-zA-Z0-9_\-/]{1,}/               # 相对路径以 / 结尾
        [a-zA-Z0-9_\-/]{1,}                 # 资源名称
        \.(?:[a-zA-Z]{1,4}|action)          # 后面 + 扩展名（长度 1-4 或 action）
        (?:[\?|/][^"|']{0,}|))              # ? 符号后带参数
        |
        ([a-zA-Z0-9_\-]{1,}                 # 文件名
        \.(?:php|asp|aspx|jsp|json|         # . + 扩展名
             action|html|js|txt|xml)             
        (?:\?[^"|']{0,}|))                  # ? 符号后带参数
      )
      (?:"|')                               # 结束的引号
    """
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result is None:
        return None
    js_url = []
    return [match.group().strip('"').strip("'") for match in result if match.group() not in js_url]

# 提取 HTML 内容
def extract_html(URL):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    try:
        raw = requests.get(URL, headers=header, timeout=3, verify=False)
        raw = raw.content.decode("utf-8", "ignore")
        return raw
    except:
        return None

# 处理 URL，生成绝对 URL
def process_url(URL, re_URL):
    black_url = ["javascript:"]
    URL_raw = urlparse(URL)
    ab_URL = URL_raw.netloc
    host_URL = URL_raw.scheme
    if re_URL[0:2] == "//":
        result = host_URL + ":" + re_URL
    elif re_URL[0:4] == "http":
        result = re_URL
    elif re_URL[0:2] != "//" and re_URL not in black_url:
        if re_URL[0:1] == "/":
            result = host_URL + "://" + ab_URL + re_URL
        else:
            if re_URL[0:1] == ".":
                if re_URL[0:2] == "..":
                    result = host_URL + "://" + ab_URL + re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + re_URL[1:]
            else:
                result = host_URL + "://" + ab_URL + "/" + re_URL
    else:
        result = URL
    return result

# 查找子域名
def find_subdomain(urls, mainurl):
    url_raw = urlparse(mainurl)
    domain = url_raw.netloc
    miandomain = domain
    positions = [m.start() for m in re.finditer(r'\.', domain)]
    if len(positions) > 1:
        miandomain = domain[positions[-2] + 1:]
    subdomains = []
    for url in urls:
        suburl = urlparse(url)
        subdomain = suburl.netloc
        if subdomain.strip() == "":
            continue
        if miandomain in subdomain:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return subdomains

# 根据 URL 查找相关链接
def find_by_url(url):
    html_raw = extract_html(url)
    if html_raw is None:
        print("无法访问 " + url)
        return None
    html = BeautifulSoup(html_raw, "html.parser")
    html_scripts = html.findAll("script")
    script_array = {}
    script_temp = ""
    for html_script in html_scripts:
        script_src = html_script.get("src")
        if script_src is None:
            script_temp += html_script.get_text() + "\n"
        else:
            purl = process_url(url, script_src)
            script_array[purl] = extract_html(purl)
    script_array[url] = script_temp
    allurls = []
    for script in script_array:
        temp_urls = extract_URL(script_array[script])
        if len(temp_urls) == 0:
            continue
        for temp_url in temp_urls:
            allurls.append(process_url(script, temp_url))
    return sorted(set(allurls))

# 获取子域名列表
def get_subdomains(url):
    urls = find_by_url(url)
    if urls is None:
        return None
    subdomains = find_subdomain(urls, url)    
    return list(subdomains)