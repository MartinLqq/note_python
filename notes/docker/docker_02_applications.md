# 链接

获取镜像源:

- Daocloud:  https://dashboard.daocloud.io



# 准备带 SSH 服务的镜像

## a.基于 commit 命令创建

1、获取 ubuntu:18.04 镜像, 并创建一个容器

```bash
docker pull ubuntu:18.04
```

2、配置容器 apt 下载源

3、下载和配置 SSH 服务

```bash
# 选择主流的 `openssh-server` 作为服务端
apt-get install openssh-server

# 如果需要正常启动 SSH 服务, 则目录 /var/run/sshd/ 必须存在
mkdir -p /var/run/sshd

# 查看容器的 22 端口 (SSH 服务默认监听的端口)
netstat -tunlp

# 修改 SSH 服务的安全登录配置, 取消 pam 登录限制
sed -ri 's/session required   pam_loginuid.so/#session required   pam_loginuid.so/g'  /etc/pam.d/sshd

# 配置 SSH 登录时需要的公钥
# 1.本地（宿主）主机生成公钥文件: ssh-keygen -t rsa
# 2.本地主机从文件中复制公钥:  ~/.ssh/id_rsa.pub
mkdir root/.ssh
vi root/.ssh/authorized_keys  # 粘贴公钥

# 创建启动 SSH 服务的可执行文件 run.sh, 并添加可执行权限
"""
脚本内容:
#!/bin/bash
/usr/sbin/sshd -D
"""
vi run.sh
chmod +x run.sh

# 退出容器
exit
```

4、保存镜像

```bash
docker commit fc1 sshd:ubuntu
docker images
```

5、使用镜像

```bash
docker run -p 10022:22 -d sshd:ubuntu /run.sh
docker ps
```

6、测试 SSH 链接



## b.使用 Dockerfile 创建

1、创建工作目录

```bash
mkdir sshd_ubuntu && cd sshd_ubuntu/
```

2、编写 run.sh 脚本和 zuthorized_keys 文件

```bash
touch run.sh
mkdir root/.ssh
vi root/.ssh/authorized_keys  # 粘贴公钥
```

3、编写 Dockerfile

```dockerfile
# 以下为 Dockerfile 内容

# 设置继承镜像
FROM ubuntu:18.04
# 提供一些作者信息
MAINTAINER docker_user (user@docker.com)

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse" > /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

RUN apt-get update

# 设置容器用户和密码
RUN echo 'root:password' |chpasswd

# 安装 SSH 服务
RUN apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh
# 取消 pam 限制
RUN sed -ri 's/session    required     pam_loginuid.so/#session    required     pam_loginuid.so/g'  /etc/pam.d/sshd
# RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# 复制配置文件到相应位置
ADD authorized_keys /root/.ssh/authorized_keys
ADD run.sh /run.sh

# 开放端口
EXPOSE 22

# 设置自启动命令
CMD ["/run.ssh"]  # 或直接: CMD ["/usr/sbin/sshd", "-D"]
```

4、创建镜像

```bash
# 在 sshd_ubuntu 目录下
docker build -t sshd:dockerfile .
docker images
```

5、测试镜像， 运行容器

```bash
docker run -p 10022:22 -d sshd:ubuntu /run.sh
docker ps
```







# Web 服务与应用

使用 docker 来运行常见的 web 服务器: Apache、Nginx、Tomcat 等，以及一些常用应用：LAMP、CI/CD



## Apache

### **1.DockerHub 镜像**

- DockerHub 官方提供的 Apache 镜像， 并不带 PHP 环境。如果需要 PHP 环境支持，可以选择 PHP 镜像： https://registry.hub.docker.com/_/php/， 并使用含 -apache 标签的镜像，如 7.0.7-apache
- 如果仅需要使用 Apache 运行静态 HTML 文件，使用默认官方镜像即可



编写 Dockerfile

- 记录此笔记时无法访问阿里云等多个镜像源,  因此先手动从 **Daocloud**  https://dashboard.daocloud.io 上 pull 镜像:  
  - docker login daocloud.io
  - sudo docker pull daocloud.io/library/httpd:2.4.27

```dockerfile
#FROM httpd:2.4   # The Apache HTTP Server Project
FROM daocloud.io/library/httpd:2.4.27  # 对应从Daocloud下载到本地的镜像
COPY ./public-html/index.html  /usr/local/apache2/htdocs/
```

创建项目目录 public-html, 并在此目录下创建 index.html

```html
<!DOCTYPE html>
<html>
    <body>
        <p>Hello, Docker</p>
    </body>
</html>
```

构建自定义镜像,  通过本地 80 端口 即可访问静态页面

```bash
docker build -t apache2-image .
```

也可以不创建自定义镜像,  直接通过映射目录的方式运行 Apache 容器:

```bash
# docker run -it --rm --name my-apache-app -p 80:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4

docker run -it --rm --name my-apache-app -p 80:80 -v "$PWD":/usr/local/apache2/htdocs/ daocloud.io/library/httpd:2.4.27  # 对应从Daocloud下载到本地的镜像
```



###  **2.自定义镜像**

创建一个 apache_ubuntu 的工作目录,  在其中创建 Dockerfile、run.sh、sample目录

```BASH
mkdir apache_ubuntu && cd apache_ubuntu
touch Dockerfile run.sh
mkdir sample
```

> Dockerfile (继承自 [用户创建的 sshd 镜像](#b.使用 Dockerfile 创建 "标题")) 

```dockerfile
# 设置继承自创建的 sshd 镜像
FROM sshd:dockerfile
MAINTAINER docker_user (user@docker.com)

# 设置环境变量
ENV DEBIAN_FRONTEND noninteractive

# 安装
RUN apt-get -yp install apache2 && \
    rm -rf /var/lib/apt/lists*
    
# 注意: 要更改系统的时区设置, 因为在 web 应用中经常会用到时区这个系统变量, 默认 Ubuntu 的设置会让 web 应用程序发生不可思议的效果
RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata
    
# 添加用户的脚本, 并设置权限, 这会覆盖之前放在这个位置的脚本
ADD run.sh /run.sh
RUN chmod 755 /*.sh

# 添加一个示例的 web 站点,  删掉默认安装在 apache 文件夹下面的文件, 并将用户添加的示例用软链接, 链接到 /var/www/html 目录下
RUN mkdir -p /var/lock/apache2 && mkdir -p /app && rm -rf /var/www/html && ln -s /app /var/www/html
COPY sample/ /app

# 设置 apache 相关的一些变量. 在容器启动时可以使用 -e 参数取代
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_SERVERADMIN admin@localhost
ENV APACHE_SERVERNAME localhost
ENV APACHE_SERVERALIAS docker.localhost
ENV APACHE_DOCUMENTROOT /var/www

EXPOSE 80
WORKDIR /app
CMD ["/run.sh"]
```

> sample/index.html

```html
<!DOCTYPE html>
<html>
    <body>
        <p>Hello, Docker</p>
    </body>
</html>
```

> run.sh

```bash
#!/bin/bash

# 启动 SSH, 用于 ssh 远程登录 docker 容器
/usr/sbin/sshd &

# 启动 Apache
exec apache2 -D FOREGOUND
```



开始创建 apache:ubuntu 镜像

```bash
docker build -t apache:ubuntu .
docker images
```

运行容器

```bash
docker run -d -P apache:ubuntu
```

测试访问

```bash
curl 127.0.0.1:49172  # 先查看一下端口号
```







## Nginx

- 功能强大的开源 **反向代理服务器**，  也可以作为 **负载均衡器** 、**HTTP 缓存服务器**、**Web 服务器**。
- 支持 HTTP、HTTPS、SMTP、POP3、IMAP等协议
- Nginx 特性：
  - 热部署
  - 高并发
  - 高可靠
  - 低内存
  - 响应快



### **1.DockerHub 镜像**

```bash
docker run -d -p 80:80 --name webserver nginx
```

1.9.8 版本后的镜像支持 debug 模式,  镜像包含 nginx-debug,  可以支持更丰富的 log 信息

```bash
docker run --name my-nginx -v /host/path/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx nginx-debug -g 'daemon off;'
```

相应的 docker-compose.yaml 配置如下:

```yaml
web:
    image: nginx
    volums:
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
    command: [nginx-debug, '-g', 'daemon off;']
```

**自定义 Web 页面**

index.html

```html
<html>
    <title>text</title>
    <body>
        <div>
            hello world.
        </div>
    </body>

</html>
```

直接运行容器

```bash
docker run --name nginx-container -p 80:80 -v index.html:/usr/share/nginx/html:ro -d nginx

docker run \
    --name nginx-server \
    -p 80:80 \
    -v ~/workspace/nginx-test/html/:/usr/share/nginx/html:ro \
    -d \
    nginx
```

或使用 Dockerfile 来构建新镜像, 并运行容器

```dockerfile
FROM nginx
COPY ./index.html /usr/share/nginx/html

# 构建镜像: docker build -t my-nginx .
# 运行容器: docker run --name nginx-container -d my-nginx
```



###  2.自定义镜像

1、自定义 Dockerfile

Dockerfile 内容

```dockerfile
# 继承自创建的 sshd 镜像
FROM sshd:dockerfile
MAINTAINER docker_user (user@docker.com)

# 安装 nginx, 设置 nginx 以非 daemon 方式启动
RUN apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/* && \
    echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R www-data:www-data /var/lib/nginx
    
RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata
    
ADD run.sh /run.sh
RUN chmod 755 /*.sh

# 定义可以被挂载的目录, 分别是虚拟主机的 挂载目录、证书目录、配置目录、日志目录
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx"]

WORKDIR /etc/nginx
CMD ["/run.sh"]

EXPOSE 80
EXPOSE 443
```

> rm -rf /var/lib/apt/lists/*:  减少最终镜像的大小。通常是可以减少21M以上

run.sh 内容

```bash
#!/bin/bash
/usr/sbin/sshd &
/usr/sbin/nginx
```



2、创建镜像

```bash
docker build -t nginx:stable .
```

3、启动容器, 测试

```bash
docker run -d -P nginx:stable

curl 127.0.0.1:49193
```



### 3.参数优化

为了能充分发挥 Nginx 的性能， 用户可以对系统内核参数做一些调整。

网上有常见的适合运行 Nginx 服务器的内核优化参数。









## Tomcat



## Jetty



## LAMP、LNMP

目前流行的 Web 工具栈：

- LAMP： Linux-Apache-MySQL-PHP/Python/Peral
- LNMP/LEMP： Linux-Nginx-MySQL-PHP/Python/Peral

优点：

- Web 资源丰富、轻量、快速开发
- 通用、跨平台、高性能、低价格



1.使用官方镜像

- 使用 linode/lamp 镜像

```bash
# 运行容器, 并进入容器
docker run -p 80:80 -it linode/lamp /bin/bash

# 在容器内部启动 Apache 和 MySQL 服务
service apache2 start
service mysql start
```

- 使用 tutum/lamp 镜像

```bash
docker run -d -p 80:80 -p 3306:3306 tutum/lamp
```











## CI/CD

### Jenkins

一键部署 Jenkins 服务:

```bash
docker run -p 8080:8080 -p 5000:5000 jenkins
```

数据持久化

```bash
docker run -p 8080:8080 -p 5000:5000 -v /your/home:/var/jenkins_home jenkins
```



### GitLab

- 开源源码管理系统,  支持基于 Git 的源码管理、代码评审、issue 跟踪、活动管理、wiki 页面、持续集成和测试等功能。
- GitLab 官方提供了社区版本 （GitLab CE）的 Dockerfile 镜像， 可以直接 docker run指定运行

```bash
docker run --detach \
    --hostname gitlab.example.com \
    --publish 443:443 --publish 80:80 --publish 23:23 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest
```











# 数据库应用

## MySQL

```
docker run -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 mysql:5.7
```





## MongoDB

## Redis





# 分布式处理与大数据平台

## Hadoop

## Spark

## Storm

## Elasticsearch





# Docker+Minio

> [MinIO Quickstart Guide](https://docs.min.io/docs/minio-quickstart-guide.html)
>
> [MinIO Docker Quickstart Guide](https://docs.min.io/docs/minio-docker-quickstart-guide.html)

Minio 是一个基于 Apache License v2.0 开源协议的对象存储服务。它兼容亚马逊 S3云存储服务接口，非常适合于存储大容量非结构化的数据，例如图片、视频、日志文件、备份数据和容器/虚拟机镜像等，而一个对象文件可以是任意大小，从几 kb 到最大 5T 不等。

Minio 是一个非常轻量的服务,可以很简单的和其他应用的结合，类似 NodeJS, Redis 或者 MySQL。



**Docker Container -- Stable**

Simple Start

```bash
docker pull minio/minio
docker run -p 9000:9000 minio/minio server /data
```

Add Parameters

```bash
# To create a MinIO container with persistent(持久的) storage, you need to map local persistent directories from the host OS to virtual config ~/.minio and export /data directories. 

docker run -p 9000:9000 --name minio1 \
  -v /mnt/data:/data \
  -v /mnt/config:/root/.minio \
  minio/minio server /data
```

Override Access and Secret Keys

```bash
# To override MinIO's auto-generated keys, you may pass secret and access keys explicitly as environment variables.

docker run -p 9000:9000 --name minio1 \
  -e "MINIO_ACCESS_KEY=my_access_key" \
  -e "MINIO_SECRET_KEY=my_secret_key" \
  -v /mnt/data:/data \
  -v /mnt/config:/root/.minio \
  minio/minio server /data
```

MinIO Custom Access and Secret Keys using [Docker secrets](https://docs.docker.com/engine/swarm/secrets/)

```bash
echo "AKIAIOSFODNN7EXAMPLE" | docker secret create access_key -
echo "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" | docker secret create secret_key -

# Create a MinIO service using docker service to read from Docker secrets.
docker service create --name="minio-service" --secret="access_key" --secret="secret_key" minio/minio server /data
```



安装后使用浏览器访问 `http://127.0.0.1:9000`



**了解更多**

- [Minio纠删码入门](https://docs.minio.io/docs/minio-erasure-code-quickstart-guide)
- [`mc`快速入门](https://docs.minio.io/docs/minio-client-quickstart-guide)
- [使用 `aws-cli`](https://docs.minio.io/docs/aws-cli-with-minio)
- [使用 `s3cmd`](https://docs.minio.io/docs/s3cmd-with-minio)
- [使用 `minio-go` SDK](https://docs.minio.io/docs/golang-client-quickstart-guide)
- [Minio文档](https://docs.minio.io/)





### 使用 s3cmd

`s3cmd` 是Linux上的命令行工具,  用于操作基于 `s3协议` 的对象存储桶(bucket),  如 `minio`

1-安装 `s3cmd`

```bash
sudo pip install s3cmd
```

2-配置 `s3cmd`

```bash
vim ~/.s3cfg

# 复制如下内容, 并修改
# ===========start============
# Setup endpoint
host_base = play.min.io:9000
host_bucket = play.min.io:9000
bucket_location = us-east-1
use_https = True

# Setup access keys
access_key =  Q3AM3UQ867SPQQA43P2F
secret_key = zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG

# Enable S3 v4 signature APIs
signature_v2 = False
# ===========end=============
```

3-操作 `s3cmd`

```bash
s3cmd --help

部分 Commands:
  Make bucket						s3cmd mb s3://BUCKET
  Remove bucket						s3cmd rb s3://BUCKET
  List objects or buckets			s3cmd ls [s3://BUCKET[/PREFIX]]
  List all object in all buckets	s3cmd la 
  Put file into bucket				s3cmd put FILE [FILE...] s3://BUCKET[/PREFIX]
  Get file from bucket				s3cmd get s3://BUCKET/OBJECT LOCAL_FILE
  Delete file from bucket			s3cmd rm s3://BUCKET/OBJECT
  Disk usage by buckets				s3cmd du [s3://BUCKET[/PREFIX]]
  Modify object metadata			s3cmd modify s3://BUCKET1/OBJECT
  Move object						s3cmd mv s3://BUCKET1/OBJECT1 s3://BUCKET2[/OBJECT2]
  Get object info					s3cmd info s3://BUCKET[/OBJECT]
```



### 使用 boto3

> [适用于 Python 的 AWS 开发工具包 (Boto3)](https://aws.amazon.com/cn/sdk-for-python/)
>
> [更多用法见:   Boto 3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
>
> [Available Services -- S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

1- 安装 `boto3`

```bash
sudo pip install boto3
```

2- 使用 `boto3` 

**List buckets using [list_buckets](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets).**

```python
import boto3

# Create an S3 client
s3 = boto3.client('s3',
                  endpoint_url='http://192.168.31.176:9000',
                  aws_access_key_id='my_access_key',
                  aws_secret_access_key='my_secret_key')

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
print("Bucket List: %s" % buckets)
```

**Create a new bucket using [create_bucket](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket).**

```python
import boto3

s3 = boto3.client('s3')
s3.create_bucket(Bucket='my-bucket')
```

**Upload a file to a bucket using [upload_file](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file).**

```python
import boto3

# Create an S3 client
s3 = boto3.client('s3')

filename = 'file.txt'
bucket_name = 'my-bucket'

# 上传之前, 先确定 bucket 是否存在, 使用方法: head_bucket(**kwargs)

# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
s3.upload_file(filename, bucket_name, filename)
```

**download an S3 object to a file**. If the service returns a 404 error, it prints an error message indicating that the object doesn't exist.

```python
import boto3
import botocore

BUCKET_NAME = 'my-bucket' # replace with your bucket name
KEY = 'my_image_in_s3.jpg' # replace with your object key

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
```

















# Docker+Keycloak

> [Keycloak source code in Github](https://github.com/keycloak/keycloak/)



[**Demo of keycloak & mysql in docker**](https://my.oschina.net/landas/blog/2253041)

1. 下载 Keycloak 镜像

```bash
docker pull jboss/keycloak
```

2. 下载 Mysql 镜像

```bash
docker pull mysql:5.7
```

3. 创建网络环境

```bash
docker network create keycloak-network
```

4. 启动 Mysql 实例

```bash
# Avalibale Command
docker run --name mysql-keycloak -d -p 3306:3306 --net keycloak-network -e MYSQL_DATABASE=keycloak -e MYSQL_USER=keycloak -e MYSQL_PASSWORD=password -e MYSQL_ROOT_PASSWORD=root_password mysql:5.7
```

5. 启动Keycloak

```bash
# Avalibale Command
docker run -d -p 8080:8080 --name keycloak -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e DB_VENDOR=mysql -e DB_USER=keycloak -e DB_PASSWORD=password -e DB_ADDR=192.168.31.176 -e DB_PORT=3306 -e DB_DATABASE=keycloak -e JDBC_PARAMS='connectTimeout=30' jboss/keycloak
```

6. 配置Keycloak

   6.1 找到配置文件

```bash
docker exec -it keycloak bash
vi keycloak/standalone/configuration/standalone.xml
```

​	6.2 允许局域网 IP 访问在 interfaces 节点添加 any 子节点，并将 socket-binding-group 的默认 interface 改为 any：

```xml
<interfaces>
    <interface name="management">
        <inet-address value="${jboss.bind.address.management:127.0.0.1}"/>
    </interface>
    <interface name="public">
        <inet-address value="${jboss.bind.address:127.0.0.1}"/>
    </interface>
    <interface name="any">
        <any-ipv4-address/>
    </interface>
</interfaces>
<socket-binding-group name="standard-sockets" default-interface="any" port- 
   offset="${jboss.socket.binding.port-offset:0}">
    ……
</socket-binding-group>
```

​	6.3 增加admin账号

```bash
./keycloak/bin/add-user-keycloak -r master -u landas -p …

```

​	6.4 验证身份并关闭SSL

```bash
./kcadm.sh config credentials --server http://localhost:8080/auth --realm master --user landas
./kcadm.sh update realms/master -s sslRequired=NONE

```

​	6.5 设置User、Client、Resource

```bash
# 使用刚设置的 admin 账号登录控制台 http://${虚拟机IP}:8080
# 依次创建 Realm/Clients/Role/User。 注意在 client 中要正确填写后面项目实际运行的机器局域网 IP。

```



**备注**：项目启动前记得将虚拟机时区设置为中国区(CST)，并使用 `ntp update` 同步时间，否则可能会报 invalid token错误。具体错误请见 keycloak-user [邮件列表](http://lists.jboss.org/pipermail/keycloak-user/2016-March/005550.html)。



使用 `mysql`:

```
mysql -u keycloak -p

```







# Docker+pgweb





# Docker+RabbitMQ

RabbitMQ操作

```
安装	sudo apt-get install rabbitmq-server
启动	service rabbitmq-server start
查看运行状态	rabbitmqctl status

用户管理:
	查看所有:	rabbitmqctl list-users
	添加用户:	rabbitmqctl add-user [name] [password]
	删除用户:	rabbitmqctl delete-user [name]
	修改密码:	rabbitmqctl change-password [name] [new_password]
	
开启网页控制台:
	1. 进入rabbitmq安装目录: cd /usr/lib/rabbitmq
	2. 查看已安装插件: tabbitmq-plugins list
	3. 开启网页版控制台: rabbitmq-plugins enable rabbitmq-management
	4. 重启rabbitmq服务: service rabbitmq-server restart
	5. 进入网页控制台: http://localhost:15672/
	6. 使用默认账号登录: guest/guest (guest用户的权限不足,只能通过localhost登录)
为用户设置超级权限:
	1. rabbitmqctl set_user_tags [name] administrator
	2. rabbitmqctl set_permissions -p / name "." "." ".*"  (配置权限、写权限、读权限)
	3. 重启服务： service rabbitmq-server restart


```





# Docker+Jira

1.pull docker 镜像： jira, mysql:5.7

```bash
docker pull cptactionhank/atlassian-jira
docker pull mysql:5.7

```

2.启动mysql docker实例

```bash
docker run --name atlassian-mysql --restart always -p 3306:3306 -v /opt/mysql_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

```

3.进入mysql

```bash
docker run -it --link atlassian-mysql:mysql --rm mysql:5.7 sh -c 'exec mysql -h 192.168.31.176 -P 3306 -uroot -p  "$MYSQL_ROOT_PASSWORD"'

```

4.创建jira数据库, 并添加jira用户 【mysql操作台执行】

```bash
create database jira default character set utf8 collate utf8_bin;
CREATE USER `jira`@`%` IDENTIFIED BY 'jira';
GRANT ALL ON *.* TO `jira`@`%` WITH GRANT OPTION;
alter user 'jira'@'%' identified with mysql_native_password by 'jira';

```

5.修改mysql事物隔离级别 【mysql操作台执行】

```bash
set global transaction isolation level read committed;
set session transaction isolation level read committed;

```

6.启动jira实例

```bash
docker run --user root --name atlassian-jira --detach --restart always -v /data/atlassian/confluence:/home --publish 8080:8080 cptactionhank/atlassian-jira

# 存疑: 是否需要以及可以按一下方式指定数据库信息?
docker run --name atlassian-jira --detach --restart always -e DB_USER=jira -e DB_PASSWORD=123456 -e DB_ADDR=192.168.31.176 -e DB_PORT=3306 -e DB_DATABASE=jira -v /data/atlassian/confluence:/home --publish 8080:8080 cptactionhank/atlassian-jira

```

7.访问 192.168.31.176:8080, 进行 [jira配置](https://confluence.atlassian.com/adminjiraserver080/running-the-setup-wizard-967896939.html)。

```bash
http://192.168.31.176:8080/secure/WelcomeToJIRA.jspa

```



8.下载破解补丁后进行破解

```bash
docker exec --user root CONTAINER_ID mv /opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-3.2.jar /opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-3.2.jar_bak

docker cp /home/lqq/atlassian-extras-3.2.jar CONTAINER_ID:/opt/atlassian/jira/atlassian-jira/WEB-INF/lib/

docker restart CONTAINER_ID     # 97为jira容器短id
```





# Docker+Jenkins

Docker+Jenkins 持续集成环境

https://www.baidu.com/link?url=SdaOFSohmZRQGRFkX3ljvxdbggzDJuv5MosE_GVzQJ08K31bcYOg22a9l1rwVA4tzu6TRSYiQWod7U-N1GRb4CiQyCER5c38imf73Tb_bG3&wd=&eqid=e4dcd9ad0004be7c000000045cc46969





# ELK日志系统



# Choerodon

Choerodon猪齿鱼是开源多云应用平台，是基于Kubernetes的容器编排和管理能力，整合DevOps工具链、微服务和移动应用框架，来帮助企业实现敏捷化的应用交付和自动化的运营管理，并提供IoT、支付、数据、智能洞察、企业应用市场等业务组件，来帮助企业聚焦于业务，加速数字化转型。





