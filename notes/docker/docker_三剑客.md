# Docker Machine

文档：

- https://www.cnblogs.com/ityouknow/p/8674247.html



介绍：

Docker Machine 是一种可以让您在虚拟主机上安装 Docker 的工具，并可以使用 docker-machine 命令来管理主机。Docker Machine 也可以集中管理所有的 docker 主机，比如快速的给 100 台服务器安装上 docker。

- 负责实现对 Docker 运行环境进行安装和管理
- go 语言编写
- 定位: 在本地或云环境中创建 Docker 主机
- 基本功能:
  - 在指定节点或平台上安装 Docker 引擎, 配置为可使用的 Docker 环境
  - 集中管理所安装的 Docker 环境
- Machine 连接不同类型的操作平台是通过 **对应驱动** 来实现的,  目前已经集成了 AWS、IBM、OpenStack、VirtualBox、vSphere等多种云平台的支持。



Docker Engine 和 Docker Machine 有什么区别？

- 当人们说 Docker 时，通常是指 Docker Engine。Docker Engine 是一个客户端 - 服务器应用程序，由 Docker daemon、REST API 和 Docker CLI 组成。

![img](http://www.ityouknow.com/assets/images/2018/docker/engine.png)

- Docker Machine 是一个用于配置和管理你的宿主机（上面具有 Docker Engine 的主机）的工具。通常，你在你的本地系统上安装 Docker Machine。Docker Machine有自己的命令行客户端 docker-machine 和 Docker Engine 客户端 docker。你可以使用 Machine 在一个或多个虚拟系统上安装 Docker Engine。

![img](http://www.ityouknow.com/assets/images/2018/docker/machine.png)





## 安装

Linux 安装命令

```
$ base=https://github.com/docker/machine/releases/download/v0.16.0 &&
  curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
  sudo mv /tmp/docker-machine /usr/local/bin/docker-machine &&
  chmod +x /usr/local/bin/docker-machine
```

macOS 安装命令

```
$ base=https://github.com/docker/machine/releases/download/v0.16.0 &&
  curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/usr/local/bin/docker-machine &&
  chmod +x /usr/local/bin/docker-machine
```

Windows 安装命令

如果你是 Windows 平台，可以使用 [Git BASH](https://git-for-windows.github.io/)，并输入以下命令：

```
$ base=https://github.com/docker/machine/releases/download/v0.16.0 &&
  mkdir -p "$HOME/bin" &&
  curl -L $base/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe" &&
  chmod +x "$HOME/bin/docker-machine.exe"
```

查看是否安装成功：

```
$ docker-machine version
docker-machine version 0.16.0, build 9371605
```



## 使用

Docker Machine 可以通过多种后端驱动来管理不同的资源,  包括虚拟机、本地主机、云平台，通过 -d 选项选择支持的驱动类型

### 1.虚拟机作为后端驱动

- 可以通过 virtualbox 驱动支持本地启动一个虚拟环境， 并配置为 Docker 主机。需要先安装 virtualbox。
- Machine 还支持 Microsoft Hyper-V 虚拟化平台

```bash
# 创建一个虚拟环境, 命名为 test
docker-machine create --driver=virtualbox test

# 查看访问 Docker 环境所需的配置信息
docker-machine env test

# 查看注册到本地管理列表中的 Docker 主机列表
docker-machine ls
```

### 2.本地主机驱动

- 首先确保本地主机 SSH 服务可用,  可以通过 user 账号的 key 直接 ssh 访问到目标主机
- Machine 通过 SSH 链接到指定节点, 并在上面安装 Docker 引擎
- 使用 generic 类型的驱动, 注册一台 Docker 主机, 名为 test:

```bash
docker-machine create \
    -d generic \
    --generic-ip-address=10.0.100.102 \
    --generic-ssh-user=user test
```



### 3.云平台驱动

- 以 Amazon Web Services 云平台为例,  配置其上的虚拟机为 Docker 主机.
- 需要指定 Access Key ID,  Secret Key,  VPC ID等信息.

```bash
docker-machine create \
    --driver amazonec2 \
    --amazonec2-access-key AKI******* \
    --amazonec2-secret-key 8T93C********* \
    --amazonec2-vpc-id vpc-******** \
    aws_instance
```



### 客户端配置

- 默认情况下所有的客户端配置数据都会自动存在 ~/.docker/machine/machines/ 路径下,
- 删除其下的内容并不会影响到已经创建的 Docker 环境



## 命令

```bash
 docker-machine <COMMAND> -h
```

常用命令

```bash
# 列出可用的机器
$ docker-machine ls
# 创建一个名为 test 的机器, 驱动类型为 virtualbox
$ docker-machine create --driver virtualbox test
# 查看机器的 ip
$ docker-machine ip test
# 停止机器
$ docker-machine stop test
# 启动机器
$ docker-machine start test
# 进入机器
$ docker-machine ssh test
```













# Docker Compose

文档:

- 官方文档
  - https://docs.docker.com/compose/compose-file/
  - https://docs.docker.com/compose/
- 菜鸟教程:  https://www.runoob.com/docker/docker-compose.html

介绍:

- Compose 是用于定义和运行多容器 Docker 应用程序的工具。

- 通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。 
- docker-compose 允许用户通过一个单独的 docker-compose.yaml 模板文件来定义一组相关联的应用容器为一个服务栈
- 重要概念:
  - 任务 (task):  一个容器被称为一个任务
  - 服务 (service):  某个相同应用镜像的容器副本集合,  一个服务可以横向扩展为多个容器实例
  - 服务栈 (stack):  由多个服务组成,  相互配合完成特定业务



## 安装

Linux

1、pip 安装 docker-compose

```bash
sudo pip install -U docker-compose
docker-compose -h
```

> 可选: 添加 bash 补全命令:

```bash
curl -L https://raw.githubusercontent.com/docker/compose/1.19.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
```



2、二进制包安装

- 下载二进制包： https://github.com/docker/compose/releases
- ...



## 使用步骤

1. 确定是直接使用镜像 image，还是使用 Dockerfile 来 build 镜像。或有的服务使用 image, 有的使用 build.

2. 使用 docker-compose.yml 定义构成应用程序的服务，使各服务在隔离环境中一起运行。
3. docker-compose config  检测 Docker Compose File 中的错误
4. docker-compose up -d     后台开启所有服务





## Compose 模板文件

- 模板文件是 Compose 的核心,  大部分指令与 docker create|run 相关参数的含义是类似的
- 默认的模板文件名称为 docker-compose.yaml,  目前最新的版本为 v3
- **注意**:  
  - 每个服务都必须通过 **image 指令指定镜像**， **或 build 指令使用 Dockerfile 所在目录** 来自动构建镜像。
  - 如果使用 build 指令, 在 **Dockerfile** 中设置的选项如 CMD、EXPOSE、VOLUME、ENV等，将会被自动获取，无需在 docker-compose.yml 中再次配置.
- 版本 1 的 Compose 文件结构:
  - 每个顶级元素为服务名称
  - 每个次级元素为服务容器的配置信息

```dockerfile
# version: "1"
webapp:
    image: example/web
    ports:
        - 80:80
    volume:
        - "/data"
```

- 版本 2 和版本 3 扩展了Compose 语法,  最大的不同是: 
  - ① 添加了版本信息,  如 `version:"3"`
  - ② 将所有服务放到 `services:` 根下面

```dockerfile
version:"3"
services:
    webapp:
        image: example/web
        deploy:  # 启用资源限制
            replicas: 2
            resources: 
                limits:
                    cpus: "0.1"
                    memory: 100M
                restart_policy: on-failure
        ports:
            - "80:80"
        networks:
            - mynet
        volumes:
            - "/data"
networks:
    mynet:
# 结束
```



`docker-compose config` 检测 Docker Compose File 中的错误

docker-compose up -d     后台开启所有服务

docker-compose down    关闭所有后台服务





## 实例

- Samples： https://docs.docker.com/samples/
- Docker redis 集群搭建:  https://www.runoob.com/docker/docker-redis-cluster.html



**1、准备**

创建一个测试目录：

```
$ mkdir composetest
$ cd composetest
```

在测试目录中创建一个名为 app.py 的文件，并复制粘贴以下内容：

```python
# composetest/app.py

import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

在此示例中，redis 是应用程序网络上的 redis 容器的主机名，该主机使用的端口为 6379。

在 composetest 目录中创建另一个名为 requirements.txt 的文件，内容如下：

```
flask
redis
```



**2、创建 Dockerfile 文件**

在 composetest 目录中，创建一个名为的文件 Dockerfile，内容如下：

```dockerfile
# FROM python:3.7-alpine
FROM daocloud.io/python:3-onbuild
WORKDIR /code

# 设置 flask 命令使用的环境变量
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# 安装 gcc，以便诸如 MarkupSafe 和 SQLAlchemy 之类的 Python 包可以编译加速。
RUN apk add --no-cache gcc musl-dev linux-headers

# 复制 requirements.txt 并安装 Python 依赖项
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 将 . 项目中的当前目录复制到 . 镜像中的工作目录
COPY . .

# 容器提供默认的执行命令
CMD ["flask", "run"]
```



**3、创建 docker-compose.yml**

在测试目录中创建一个名为 docker-compose.yml 的文件，然后粘贴以下内容：

```yaml
# yaml 配置
version: '3'
services:
    web:
        build: .  # 使用从 Dockerfile 当前目录中构建的镜像
        ports:
            - "5000:5000"
    redis:
        #image: "redis:alpine"  # 使用 Docker Hub 的公共 Redis 镜像
        image: "daocloud.io/library/redis:3.2.9"
```



**4、使用 Compose 命令构建和运行您的应用**

```
docker-compose up -d
```





## 指令参考

### version

指定本 yaml 依从的 compose 哪个版本制定的。

### build

- 指定为构建镜像上下文路径 ( Dockerfile 所在文件夹 )

例如 webapp 服务，指定为从上下文路径 ./dir/Dockerfile 所构建的镜像：

```
version: "3.7"
services:
  webapp:
    build: ./dir
```

或者，作为具有在上下文指定的路径的对象，以及可选的 Dockerfile 和 args：

```dockerfile
version: "3.7"
services:
  webapp:
    build:
      context: ./dir
      dockerfile: Dockerfile-alternate
      args:
        buildno: 1
      labels:
        - "com.example.description=Accounting webapp"
        - "com.example.department=Finance"
        - "com.example.label-with-empty-value"
      target: prod
```

- context：上下文路径。
- dockerfile：指定构建镜像的 Dockerfile 文件命。
- args：添加构建参数，这是只能在构建过程中访问的环境变量。
- labels：设置构建镜像的标签。
- target：多层构建，可以指定构建哪一层。

### cap_add，cap_drop

添加或删除容器拥有的宿主机的内核功能。

```
cap_add:
  - ALL # 开启全部权限

cap_drop:
  - SYS_PTRACE # 关闭 ptrace权限
```

### cgroup_parent

为容器指定父 cgroup 组，意味着将继承该组的资源限制。

```
cgroup_parent: m-executor-abcd
```

### command

覆盖容器启动的默认命令。可以为字符串格式或 JSON 数组。

```
command: ["bash", "-c", "echo", "hello world！"]
```

### configs

在 Docekr Swarm 模式下， 可以通过 configs 来管理和访问非敏感的配置信息，支持从文件读取或外部读取，

如：

```dockerfile
version : "3.3"
services:
    app:
        image: myApp:1.0
        deploy:
            replicas: 1
        configs:
            - file_config
            - external_config
configs:
    file_config:
        file: ./config_file.cfg
    external_config:
        external_config:
            external: true
```



### container_name

指定自定义容器名称，而不是生成的默认名称。目前不支持在 Swarm 模式下使用.

```
container_name: my-web-container
```

### depends_on

设置多个服务之间的依赖关系。

- docker-compose up ：以依赖性顺序启动服务。在以下示例中，先启动 db 和 redis ，才会启动 web。
- docker-compose up SERVICE ：自动包含 SERVICE 的依赖项。在以下示例中，docker-compose up web 还将创建并启动 db 和 redis。
- docker-compose stop ：按依赖关系顺序停止服务。在以下示例中，web 在 db 和 redis 之前停止。

```
version: "3.7"
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres
```

注意：**web 服务不会等待 redis db 完全启动 之后才启动**。



### deploy

指定与服务的部署和运行有关的配置。**只在 swarm 模式下才会有用**。

```
version: "3.7"
services:
  redis:
    image: redis:alpine
    deploy:
      mode：replicated
      replicas: 6
      endpoint_mode: dnsrr
      labels: 
        description: "This redis service label"
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
        reservations:
          cpus: '0.25'
          memory: 20M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

可以选参数：

**endpoint_mode**：访问集群服务的方式。

```
endpoint_mode: vip 
# Docker 集群服务一个对外的虚拟 ip。所有的请求都会通过这个虚拟 ip 到达集群服务内部的机器。
endpoint_mode: dnsrr
# DNS 轮询（DNSRR）。所有的请求会自动轮询获取到集群 ip 列表中的一个 ip 地址。
```

**labels**：在服务上设置标签。可以用容器上的 labels（跟 deploy 同级的配置） 覆盖 deploy 下的 labels。

**mode**：指定服务提供的模式。

- **replicated**：复制服务，复制指定服务到集群的机器上。

- **global**：全局服务，服务将部署至集群的每个节点。

- 图解：下图中黄色的方块是 replicated 模式的运行情况，灰色方块是 global 模式的运行情况。

  ![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-composex.png)

**replicas：mode** 为 replicated 时，需要使用此参数配置具体运行的节点数量。

**resources**：配置服务器资源使用的限制，例如上例子，配置 redis 集群运行需要的 cpu 的百分比 和 内存的占用。避免占用资源过高出现异常。

**restart_policy**：配置如何在退出容器时重新启动容器。

- condition：可选 none，on-failure 或者 any（默认值：any）。
- delay：设置多久之后重启（默认值：0）。
- max_attempts：尝试重新启动容器的次数，超出次数，则不再尝试（默认值：一直重试）。
- window：设置容器重启超时时间（默认值：0）。

**rollback_config**：配置在更新失败的情况下应如何回滚服务。

- parallelism：一次要回滚的容器数。如果设置为0，则所有容器将同时回滚。
- delay：每个容器组回滚之间等待的时间（默认为0s）。
- failure_action：如果回滚失败，该怎么办。其中一个 continue 或者 pause（默认pause）。
- monitor：每个容器更新后，持续观察是否失败了的时间 (ns|us|ms|s|m|h)（默认为0s）。
- max_failure_ratio：在回滚期间可以容忍的故障率（默认为0）。
- order：回滚期间的操作顺序。其中一个 stop-first（串行回滚），或者 start-first（并行回滚）（默认 stop-first ）。

**update_config**：配置应如何更新服务，对于配置滚动更新很有用。

- parallelism：一次更新的容器数。
- delay：在更新一组容器之间等待的时间。
- failure_action：如果更新失败，该怎么办。其中一个 continue，rollback 或者pause （默认：pause）。
- monitor：每个容器更新后，持续观察是否失败了的时间 (ns|us|ms|s|m|h)（默认为0s）。
- max_failure_ratio：在更新过程中可以容忍的故障率。
- order：回滚期间的操作顺序。其中一个 stop-first（串行回滚），或者 start-first（并行回滚）（默认stop-first）。

**注**：仅支持 V3.4 及更高版本。

### devices

指定设备映射列表。不支持 Swarm 模式.

```
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
```

### dns

自定义 DNS 服务器，可以是单个值或列表的多个值。

```
dns: 8.8.8.8

dns:
  - 8.8.8.8
  - 9.9.9.9
```

### dns_search

自定义 DNS 搜索域。可以是单个值或列表。

```
dns_search: example.com

dns_search:
  - dc1.example.com
  - dc2.example.com
```

### dockerfile

如果需要, 指定额外的编译镜像的 Dockerfile 文件,  可以通过该指令来指定

```
dockerfile: Dockerfile-externate
```

### entrypoint

覆盖容器默认的 entrypoint。注: 也会取消掉镜像中指定的入口命令和默认启动命令.

```
entrypoint: /code/entrypoint.sh
```

也可以是以下格式：

```
entrypoint:
    - php
    - -d
    - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
    - -d
    - memory_limit=-1
    - vendor/bin/phpunit
```

### env_file

从文件添加环境变量。可以是单个值或列表的多个值。

- 如果通过 docker-compose -f FILE 方式来指定 Compose 模板文件,  则 env_file 中变量的路径会基于模板文件路径
- 如果变量名与 environment 指令冲突,  则按照惯例,  以后者为准

```
env_file: .env
```

也可以是列表格式：

```
env_file:
  - ./common.env
  - ./apps/web.env
  - /opt/secrets.env
```

环境变量文件中每一行必须符合格式,  支持 # 开头的注释行, 如

```
# common.env: Set development environment
PROG_ENV=dev
```



### environment

添加环境变量。

- 可以使用数组或字典、任何布尔值
- 布尔值需要用引号引起来，以确保 YML 解析器不会将其转换为 True 或 False。

```docekrfile
environment:
  RACK_ENV: development  # 或 RACK_ENV=development
  SHOW: 'true'
```

### expose

暴露端口，但**不映射到宿主机**，**只被连接的服务访问**。

仅可以指定内部端口为参数：

```
expose:
 - "3000"
 - "8000"
```



### extends

基于其他模板文件进行扩展。

1. 定义一个基础模板文件 common.yml

```dockerfile
# common.yml
services:
    webapp：
        build： ./webapp
        environment: 
            - DEBUG=false
            - SEND_EMAILS=false
```

2. 定义一个新的 development.yml

```docekrfile
# development.yml
services:
    web:
        extends:
            file: common.yml
            service: webapp
        ports:
            - "8000:8000"
        links:
            - db
        environment:
            - DEBUG=true
    db:
        image: postgers
```

### extra_hosts

添加主机名映射。类似 docker client --add-host。

```
extra_hosts:
 - "somehost:162.242.195.82"
 - "otherhost:50.31.209.229"
```

以上会在此服务的内部容器中 /etc/hosts 创建一个具有 ip 地址和主机名的映射关系：

```
162.242.195.82  somehost
50.31.209.229   otherhost
```

### extra_links

链接到 docker-compose.yml 外部容器, 甚至非 Compose 管理的外部容器,  参数格式与 links 类似.

```dockerfile
external_links:
    - redis_1
    - project_db_1:mysql
    - project_db_1:postgresql
```



### healthcheck

用于检测 docker 服务是否健康运行。

```
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080"] # 设置检测程序
  interval: 1m30s # 设置检测间隔
  timeout: 10s # 设置检测超时时间
  retries: 3 # 设置重试次数
  start_period: 40s # 启动后，多少秒开始启动检测程序
```

### image

指定容器运行的镜像。以下格式都可以：

```
image: redis
image: ubuntu:14.04
image: tutum/influxdb
image: example-registry.com:4000/postgresql
image: a4bc65fd # 镜像id
```

### isolation

配置容器隔离的机制,  包括 default、process、htperv。

### labels

为容器添加 Docker 元数据信息，  辅助说明

### links

> links 属于旧用法， 可能在后续版本中被移除

链接到其他服务中的容器,  格式使用 服务名称 (同时作为别名) 或 服务名称:服务别名

```docekrfile
links:
  - db
  - db:datebase
  - redis
```

使用的别名会自动在服务容器中的 /etc/hosts 里创建,  如

```
172.17.2.186  db
172.17.2.186  database
172.17.2.187  redis
```

被链接容器中相应的环境变量也将被创建



### logging

服务的日志记录配置。

driver：指定服务容器的日志记录驱动程序，默认值为json-file。有以下三个选项

```
driver: "json-file"
driver: "syslog"
driver: "none"
```

仅在 json-file 驱动程序下，可以使用以下参数，限制日志得数量和大小。

```
logging:
  driver: json-file
  options:
    max-size: "200k" # 单个文件大小为200k
    max-file: "10" # 最多10个文件
```

当达到文件限制上限，会自动删除旧得文件。

syslog 驱动程序下，可以使用 syslog-address 指定日志接收地址。

```
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

### network_mode

设置网络模式。

```
network_mode: "bridge"
network_mode: "host"
network_mode: "none"
network_mode: "service:[service name]"
network_mode: "container:[container name/id]"
```

### networks

配置容器连接的网络，引用顶级 networks 下的条目 。

```
services:
  some-service:
    networks:
      some-network:
        aliases:
         - alias1
      other-network:
        aliases:
         - alias2
networks:
  some-network:
    # Use a custom driver
    driver: custom-driver-1
  other-network:
    # Use a custom driver which takes special options
    driver: custom-driver-2
```

**aliases** ：同一网络上的其他容器可以使用服务名称或此别名来连接到对应容器的服务。



### pid

跟主机系统共享进程命名空间,  打开该选项的容器之间,  以及容器和宿主机系统之间可以通过进程来相互访问和操作

```
pid: "host"
```

### ports

暴露端口信息

```dockerfile
ports:
    - "3000"  # 宿主随机选择端口
    - "8000:8000"
    - "49100:22"
    - "127.0.0.1:8001:8001"
    
# 或
ports:
    - target: 80
      published: 8080
      protocol: tcp
      mode: ingress
```



### restart

- no：是默认的重启策略，在任何情况下都不会重启容器。
- always：容器总是重新启动。
- on-failure：在容器非正常退出时（退出状态非0），才会重启容器。
- unless-stopped：在容器退出时总是重启容器，但是不考虑在Docker守护进程启动时就已经停止了的容器

```
restart: "no"
restart: always
restart: on-failure
restart: unless-stopped
```

注：swarm 集群模式，请改用 restart_policy。

### secrets

存储敏感数据，例如密码：

```
version: "3.1"
services:

mysql:
  image: mysql
  environment:
    MYSQL_ROOT_PASSWORD_FILE: /run/secrets/my_secret
  secrets:
    - my_secret

secrets:
  my_secret:
    file: ./my_secret.txt
```

### security_opt

修改容器默认的 schema 标签。

```
security-opt：
  - label:user:USER   # 设置容器的用户标签
  - label:role:ROLE   # 设置容器的角色标签
  - label:type:TYPE   # 设置容器的安全策略标签
  - label:level:LEVEL  # 设置容器的安全等级标签
```

### stop_grace_period

指定在容器无法处理 SIGTERM (或者任何 stop_signal 的信号)，等待多久后发送 SIGKILL 信号关闭容器。

```
stop_grace_period: 1s # 等待 1 秒
stop_grace_period: 1m30s # 等待 1 分 30 秒 
```

默认的等待时间是 10 秒。

### stop_signal

设置停止容器的替代信号。默认情况下使用 SIGTERM 。

以下示例，使用 SIGUSR1 替代信号 SIGTERM 来停止容器。

```
stop_signal: SIGUSR1
```

### sysctls

设置容器中的内核参数，可以使用数组或字典格式。

```
sysctls:
  net.core.somaxconn: 1024
  net.ipv4.tcp_syncookies: 0

sysctls:
  - net.core.somaxconn=1024
  - net.ipv4.tcp_syncookies=0
```

### tmpfs

在容器内安装一个临时文件系统。可以是单个值或列表的多个值。

```
tmpfs: /run

tmpfs:
  - /run
  - /tmp
```

### ulimits

覆盖容器默认的 ulimit。

```
ulimits:
  nproc: 65535
  nofile:
    soft: 20000
    hard: 40000
```

### volumes

将主机的数据卷或着文件挂载到容器里。

```
version: "3.7"
services:
  db:
    image: postgres:latest
    volumes:
      - "/localhost/postgres.sock:/var/run/postgres/postgres.sock"
      - "/localhost/data:/var/lib/postgresql/data"
```



### working_dir

指定容器中的工作目录

```docekrfile
working_dir: /workspace
```



### 其他指令

略



## 命令参考

```bash
docker-compose -h
```



```bash
# 校验和查看 Compose 文件的配置信息
docker-compose config

# 尝试自动完成一系列操作, 包括 构建镜像、（重新）创建服务、启动服务，并关联服务相关的容器。
docekr-compose up

# 重新构建镜像， 再启动
# 方法1
docker-compose built
docker-compose up
# 方法2
docker-compose up --build

# 列出项目中目前的所有容器
docker-compose ps

# 设置指定服务运行的容器个数
# 一般的， 当指定数目多于该服务当前实际运行容器，将新创建并启动容器， 反之停止容器
docker-compose scale web=3 db=3
```





## 读取环境变量

- https://docs.docker.com/compose/environment-variables/

从 1.5.0 版本开始,  Compose 模板文件支持动态读取主机操作系统的 系统环境变量

```dockerfile
db:
    # 读取系统环境变量 MONGO_VERSION 的值, 如果没有, 则默认为 3.2
    image: "mongo:${MONGO_VERSION-3.2}"
```

可以在执行 docker-compose up -e MONGO_VERSION=2.8 时覆盖系统环境变量的值



## Compose 环境变量







# Docker Swarm

## 简介

Docker Swarm 是 Docker 的集群管理工具。它将 Docker 主机池转变为单个虚拟 Docker 主机。 Docker Swarm 提供了标准的 Docker API，所有任何已经与 Docker 守护程序通信的工具都可以使用 Swarm 轻松地扩展到多个主机。 

## 原理

如下图所示，swarm 集群由管理节点（manager）和工作节点（work node）构成。

- **swarm mananger**：负责整个集群的管理工作包括集群配置、服务管理等所有跟集群有关的工作。
- **work node**：即图中的 available node，主要负责运行相应的服务来执行任务（task）。

[![img](https://www.runoob.com/wp-content/uploads/2019/11/services-diagram.png)](https://www.runoob.com/wp-content/uploads/2019/11/services-diagram.png)

------

## 使用

以下示例，均以 Docker Machine 和 virtualbox 进行介绍，确保你的主机已安装 virtualbox。

### 1.创建集群管理节点

创建 docker 机器：

```
$ docker-machine create -d virtualbox swarm-manager
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm1.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm1.png)

初始化 swarm 集群，进行初始化的这台机器，就是集群的管理节点。

```
$ docker-machine ssh swarm-manager
$ docker swarm init --advertise-addr 192.168.99.107 # 这里的 IP 为创建机器时分配的 ip。
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm2.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm2.png)

以上输出，证明已经初始化成功。需要把以下这行复制出来，在增加工作节点时会用到：

```
docker swarm join --token SWMTKN-1-4oogo9qziq768dma0uh3j0z0m5twlm10iynvz7ixza96k6jh9p-ajkb6w7qd06y1e33yrgko64sk 192.168.99.107:2377
```

### 2.创建集群工作节点

这里直接创建好俩台机器，swarm-worker1 和 swarm-worker2 。

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm3.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm3.png)

分别进入俩个机器里，指定添加至上一步中创建的集群，这里会用到上一步复制的内容。

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm4.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm4.png)

以上数据输出说明已经添加成功。

上图中，由于上一步复制的内容比较长，会被自动截断，实际运行的命令如下：

```
docker@swarm-worker1:~$ docker swarm join --token SWMTKN-1-4oogo9qziq768dma0uh3j0z0m5twlm10iynvz7ixza96k6jh9p-ajkb6w7qd06y1e33yrgko64sk 192.168.99.107:2377
```

### 3.查看集群信息

进入管理节点，执行 docker info 可以查看当前集群的信息。

```
$ docker info
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm5.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm5.png)

通过画红圈的地方，可以知道当前运行的集群中，有三个节点，其中有一个是管理节点。

### 4.部署服务到集群中

**注意**：跟集群管理有关的任何操作，都是在管理节点上操作的。

以下例子，在一个工作节点上创建一个名为 helloworld 的服务，这里是随机指派给一个工作节点：

```
docker@swarm-manager:~$ docker service create --replicas 1 --name helloworld alpine ping docker.com
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm6.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm6.png)

### 5.查看服务部署情况

查看 helloworld 服务运行在哪个节点上，可以看到目前是在 swarm-worker1 节点：

```
docker@swarm-manager:~$ docker service ps helloworld
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm7.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm7.png)

查看 helloworld 部署的具体信息：

```
docker@swarm-manager:~$ docker service inspect --pretty helloworld
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm8.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm8.png)

### 6.扩展集群服务

我们将上述的 helloworld 服务扩展到俩个节点。

```
docker@swarm-manager:~$ docker service scale helloworld=2
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm9.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm9.png)

可以看到已经从一个节点，扩展到两个节点。

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm10.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm10.png)

### 7.删除服务

```
docker@swarm-manager:~$ docker service rm helloworld
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm11.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm11.png)

查看是否已删除：

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm12.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm12.png)

### 8.滚动升级服务

以下实例，我们将介绍 redis 版本如果滚动升级至更高版本。

创建一个 3.0.6 版本的 redis。

```
docker@swarm-manager:~$ docker service create --replicas 1 --name redis --update-delay 10s redis:3.0.6
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm13.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm13.png)

滚动升级 redis 。

```
docker@swarm-manager:~$ docker service update --image redis:3.0.7 redis
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm14.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm14.png)

看图可以知道 redis 的版本已经从 3.0.6 升级到了 3.0.7，说明服务已经升级成功。

### 9.停止某个节点接收新的任务

查看所有的节点：

```
docker@swarm-manager:~$ docker node ls
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm16.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm16.png)

可以看到目前所有的节点都是 Active, 可以接收新的任务分配。

停止节点 swarm-worker1：

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm17.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm17.png)

**注意**：swarm-worker1 状态变为 Drain。不会影响到集群的服务，只是 swarm-worker1 节点不再接收新的任务，集群的负载能力有所下降。

可以通过以下命令重新激活节点：

```
docker@swarm-manager:~$  docker node update --availability active swarm-worker1
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/swarm19.png)](https://www.runoob.com/wp-content/uploads/2019/11/swarm19.png)

















## 配合 Compose

- docker-compose.yaml 中增加 deploy 项

- 不再使用 docker-compose up 启动,  而是使用 docker stack deploy,  用 -c 选项指定 docker-compose.yml

- ```bash
  docker swarm init
  docker stack deploy -c docker-compose.yaml STACK_NAME
  docker service ls
  docker service logs -f SERVICE_NAME
  
  docker stack rm STACK_NAME  # STACK_NAME表现为集群服务名称的共同前缀
  docker ps -a
  ```

- networks 必须是 "overlay" 模式

- docker service ls 查看所有服务

- docker service logs SERVICE -f  查看服务日志









## 不支持 DOCKER STACK DEPLOY 的指令

The following sub-options (supported for `docker-compose up` and `docker-compose run`) are *not supported* for `docker stack deploy` or the `deploy` key.

- [build](https://docs.docker.com/compose/compose-file/#build)
- [cgroup_parent](https://docs.docker.com/compose/compose-file/#cgroup_parent)
- [container_name](https://docs.docker.com/compose/compose-file/#container_name)
- [devices](https://docs.docker.com/compose/compose-file/#devices)
- [tmpfs](https://docs.docker.com/compose/compose-file/#tmpfs)
- [external_links](https://docs.docker.com/compose/compose-file/#external_links)
- [links](https://docs.docker.com/compose/compose-file/#links)
- [network_mode](https://docs.docker.com/compose/compose-file/#network_mode)
- [restart](https://docs.docker.com/compose/compose-file/#restart)
- [security_opt](https://docs.docker.com/compose/compose-file/#security_opt)
- [userns_mode](https://docs.docker.com/compose/compose-file/#userns_mode)