import asyncio
import aiodns
import random
import sys

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)


async def query(name, query_type):
    return await resolver.query(name, query_type)


def random_to_A(domain):
    total = 0
    for _ in range(5):  # 随机域名次数
        sub_domain = "".join(random.sample('abcdefghijklmnopqrstuvwxyz', random.randint(8, 12)))
        try:
            res = query(sub_domain + "." + domain, 'A')
            result = loop.run_until_complete(res)
            total += 1
        except aiodns.error.DNSError:
            pass  # 忽略不存在域名错误
    return total

def check_domain(domain):
    """
    检查域名是否存在泛解析。
    :return: 如果不存在泛解析，返回True；否则返回False
    """
    result = random_to_A(domain)
    if result == 5:
        print("该域名存在泛解析")
        return False
    else:
        print("该域名不存在泛解析,开始爆破子域名")
        return True