## Installation

install as **pip**

```shell
pip install nest-helper==1.1.0
```

## Usage

- 生成 uuid

  > :syntax: generate_uuid(fmt:str='-') -> int
  >
  > :param: fmt 替换的字符串
  >
  > :return: string

  ```python
  >>> from pyhelper.helper import generate_uuid
  >>> print(generate_uuid())
  >>> c294bfab-5249-4c01-8e38-02f7957afdfa
  >>> print(generate_uuid(fmt=''))
  >>> 2204d86f2815482c83d697acd0b36c16
  ```

  

- 生成11位的唯一识别码

  > :syntax: generate_unique_id() -> str
  >
  > :return: string

  ```python
  >>> from pyhelper.helper import generate_unique_id
  >>> print(generate_unique_id())
  >>> 78LM0XLpnpv
  ```

  

- 生成自定义位数的随机字符串

  > :syntax: generate_rnd_string(n:int=6) -> str
  >
  > :param: n 生成的字符串的位数
  >
  > :return: string

  ```python
  >>> from pyhelper.helper import generate_rnd_string
  >>> print(generate_rnd_string())
  w9y5Yk
  >>> print(generate_rnd_string(n=10))
  T65rZduWMC
  ```

  

- 生成雪花id

  > :syntax: snow_flake(datacenter_id: int = 1, worker_id: int = 1, sequence: int = 0) -> int
  >
  > :param datacenter_id:  数据中心（机器区域）ID
  >
  > :param worker_id:  机器ID
  >
  > :param sequence: 序列号
  >
  > :return: int

  ```shell
  >>> from pyhelper.helper import snow_flake
  >>> print(snow_flake())
  >>> 1448838354849370112
  >>> print(snow_flake(1,2,0))
  1448838475976679424
  ```

  

- url 编码

  > :syntax: urlencode(url:str) -> str
  >
  > :param url: 需要编码的url
  >
  > :return: string

  ```python
  >>> from pyhelper.helper import urlencode
  >>> url = "https://baidu.com?a=1&b=2"
  >>> print(urlencode(url))
  https%3A//baidu.com%3Fa%3D1%26b%3D2
  ```

  

- url 解码

  > :syntax: urldecode(url:str) -> str
  >
  > :param url: 需要解码的url
  >
  > :return: string
  
  ```python
  >>> from pyhelper.helper import urldecode
  >>> url = "https%3A//baidu.com%3Fa%3D1%26b%3D2"
  >>> print(urldecode(url))
  https://baidu.com?a=1&b=2
  ```
  
  