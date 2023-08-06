'''
 辅助函数
'''
import uuid
import random
import string
import urllib.parse
from struct import unpack
from os import urandom


def generate_uuid(fmt: str = "-") -> str:
    '''
    生成uuid
    :param fmt: string, 默认为'-'
    :return: string
    '''
    return str(uuid.uuid4()).replace("-", fmt)


def generate_rnd_string(n: int = 6) -> str:
    '''
    生成随机字符串
    :param n: int, 生成的字符串的位数
    :return: string, 返回一个随机字符串
    '''
    # 原生字符串
    raw = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789"
    # 获取字符串长度 len(raw) = 56
    length = 56
    # 生成的字符串
    generate_srting = ""
    # 遍历数据
    for i in range(n):
        # 获取随机的索引值
        index = random.randint(0, length - 1)
        # 获取当前的字符串,并拼接到返回的字符串
        generate_srting += raw[index]
    # 返回的字符串
    return generate_srting


def generate_unique_id() -> str:
    '''
    生成一个11位唯一ID
    :return: string, 生成一个11位的随机唯一id
    '''
    num = unpack("<Q", urandom(8))[0]
    if num <= 0:
        result = "0"
    else:
        alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase
        key = []
        while num > 0:
            num, rem = divmod(num, 62)
            key.append(alphabet[rem])
        result = "".join(reversed(key))
    return result


def urlencode(url):
    '''
    url编码
    :param url: 原生的url地址
    :return: 编码后的url地址
    '''
    return urllib.parse.quote(url)


def urldecode(url):
    '''
    url解码
    :param url: url经过编码的地址
    :return: 返回解码后的url编码
    '''
    return urllib.parse.unquote(url)

