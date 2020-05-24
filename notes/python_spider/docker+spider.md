# Docker + Spider

### Dockerfile 安装配置 python

```
FROM python:alpine3.6
# 安装支持http/https协议客户端请求的库
RUN pip install requests && \
    pip install aiohttp && \
	pip install tornado && \
	pip install selenium && \
	pip install appium-python-client

# 安装 gcc 编译环境 (可在github中搜索如何安装)
RUN apk add --no-cache gcc musl-dev
# 下列模块的安装需要 gcc 编译环境
RUN pip install twisted && \
    pip install gevent

# 安装 scrapy 和ubuntu下的依赖
RUN apk add --no-cache libxml2-dev libxslt1-dev zlib-dev libffi-dev openssl-dev && \
    pip install scrapy

# 安装 pyspider 和ubuntu下的依赖
RUN apk add --no-cache curl-dev openssl-dev libxml2-dev libxslt-dev zlib-dev && \
    pip install pyspider
```



### selenium 与 chrome 爬虫开发环境搭建

```
docker search selenium
docker search appium
# 选择官方镜像/星数较多的镜像
# 查看对应Dockerfile 和镜像使用说明: 在github中搜索某个镜像名称

docker pull ...

docekr run ... (端口映射)
```



在docker外远程调用 webdriver

```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
    command_excutor="http://172.17.0.2:4444/ed/hub",
    desired_capabilities=DesiredCapabilities.CHROME
)

driver.get("http://www.baidu.com")
print(driver.title)
with open("/data/baidu_spider.html", "w") as file:
    file.write(driver.page_source)
driver.close()
```



docker-compose.yaml

```yaml
version: "3.6"
services:
  spider:
    image: spider-dev   # 构建好的python镜像
    volumes:
      - ./baidu_spider.py:/code/baidu_spider.py
      - ./data:/data
    command: python /code/baidu_spider.py
    depends_on:
      - chrome
  chrome:
    image: selenium/standalone-chrome:3.12.0-cobalt
    ports:
      - "4444:4444"
    shm_size: 2g   # 共享内存大小

# docker-compose up -d
# docker logs DOCKER 查看日志, 会发现报错Host is unreachable
# 这是因为代码中指定的 IP 不可达, 需要修改为:
# http://chrome:4444/ed/hub

# docker-compose down
# docker-compose up -d
```



优化

```python
# depends_on 的作用是: spider服务在chrome服务启动之后, 再启动.
# 问题: 
# 当chrome服务启动之后, 如果chrome服务中的selenium没有完全启动, 此时spider服务启动后, python客户端调用selenium会失败

# 解决:
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# add_start-----------------------------------------------
import requests


def test_chrome_server():
    while True:
        i = 0
        try:
            resp = requests.get("http://chrome:4444/ed/hub", timeout=0.5)
        except Exception:
            i += 1
            if i > 10:
                raise
        else:
            print(resp.content)
            break


test_chrome_server()
# add_end-------------------------------------------------

driver = webdriver.Remote(
    command_excutor="http://chrome:4444/ed/hub",
    desired_capabilities=DesiredCapabilities.CHROME
)

driver.get("http://www.baidu.com")
print(driver.title)
with open("/data/baidu_spider.html", "w") as file:
    file.write(driver.page_source)
driver.close()
```



### appium与android爬虫开发环境搭建



# 数据抓包

抓包工具 (代理服务器, 代理客户端)

Wireshark -- TCP/IP抓包

Fiddler -- http/https抓包

Charles(推荐) -- http/https 抓包

HttpWatch工具



### Charles配置PC端web抓包

https的抓包必须安装对应证书

安装证书和 SSL Proxy 配置

```
1. 安装
Charles软件界面--->Help--->ssl proxying--->install charles root certificate
添加信任:安装时选择存储到受信任的存储区

2. 配置
Charles软件界面--->Proxy--->SSL Proxying settings--->SSL Proxying--->Add--->Host填 * , Port填 443--->OK--->OK
```



### Charles配置移动端web抓包

与PC端不同(Charles直接安装在PC端),  移动端要进行代理的设置.

代理设置前提:  

移动端与PC端在同一个网段

代理设置:

手机连接wifi时设置代理服务器主机名为PC的IP,  端口对应Charles中设置的代理端口(Charles软件界面--->Proxy--->Proxy setting,   默认是8888),  保存

SSL 证书:

移动端在`手机浏览器`请求https网址时,  自动会向Charles请求下载SSL证书;

在访问微信小程序时(https),  不会自动下载SSL 证书,  此时需要手动配置:

```
Charles软件界面--->Help--->ssl proxying--->install charles root certificate on a mobile service or remote Browser--->按提示在手机中访问指定地址--->按提示为证书命名
```





# WebSocket协议与爬虫













