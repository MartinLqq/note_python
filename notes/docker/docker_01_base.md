# ~Docker base

docker的实验特性, experimental

My Docker ID:   `martin1018` / `123456789`      `https://hub.docker.com`

查看 Docker 日志:

```bash
# Ubuntu / CentOS
journalctl -u docker.service

# RedHat
日志文件可能为: /var/log/messages
```

查看 Docker 信息:  `docker info`

后台运行容器,  不把执行命令的结果输出到当前宿主机下

```bash
docker run -d ubuntu:18.04 /bin/sh -C "while true; do echo hello; sleep 1; done"
# 如果要查看输出结果:
docker logs [container ID or NAMES]
```





# 资源汇总

## Docker 资源

- Docker 官方主页: [https://www.docker.com](https://www.docker.com/)
- Docker 官方博客: https://blog.docker.com/
- Docker 官方文档: https://docs.docker.com/
- Docker Store: [https://store.docker.com](https://store.docker.com/)
- Docker Cloud: [https://cloud.docker.com](https://cloud.docker.com/)
- Docker Hub: [https://hub.docker.com](https://hub.docker.com/)
- Docker 的源代码仓库: https://github.com/moby/moby
- Docker 发布版本历史: https://docs.docker.com/release-notes/
- Docker 常见问题: https://docs.docker.com/engine/faq/
- Docker 远端应用 API: https://docs.docker.com/develop/sdk/

## Docker 国内镜像

阿里云的加速器：https://help.aliyun.com/document_detail/60750.html

网易加速器：http://hub-mirror.c.163.com

官方中国加速器：https://registry.docker-cn.com

ustc 的镜像：https://docker.mirrors.ustc.edu.cn

daocloud：https://www.daocloud.io/mirror#accelerator-doc（注册后使用）



# 主机 ubuntu 初始化



**配置Ubuntu系统的默认下载源 (apt源)** 

加快 `apt-get`  `apt install` 速度

1-备份apt源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.back
```

2-修改apt源

```bash
sudo vi /etc/apt/sources.list
```

```bash
# 如修改为阿里云源:
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
```

3-更新apt源

```
sudo apt-get update
```



**安装 pip 命令**

```bash
sudo apt install python3-pip
# 注意: 安装后更新
sudo pip3 install --upgrade pip
```



**配置Pypi源**

加快 `pip install` 速度

创建或修改配置文件

```
linux的文件在~/.pip/pip.conf 
windows在%HOMEPATH%\pip\pip.ini）

修改内容为：
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```



**yum 下载命令安装**

```bash
sudo apt install yum
```



**tree 命令安装**

```bash
sudo apt install tree
```



**虚拟机时区设置**

使用 `tzselect` 命令 **获取设置方式**

```
输入 tzselect 命令, 按终端显示进行选择操作, 
一般流程: 第一步选 Asia, 第二步选 China, 第三步 yes
```

> **注:** 
>
> 执行完 `tzselect` 命令选择时区后，时区并没有更改，只是在命令最后提示如何修改 .profile 文件来设置时区

**正式修改 `.profile`** 

```bash
You can make this change permanent for yourself by appending the line
	TZ='Asia/Shanghai'; export TZ
to the file '.profile' in your home directory; then log out and log in again.
```







# Docker 初始化

##  手动安装Docker

更新ubuntu的apt源索引

```shell
sudo apt-get update
```

安装包允许apt通过HTTPS使用仓库

```shell
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

添加Docker官方GPG key

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# 返回:OK
```

添加Docker稳定版的 官方软件源

```shell
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

添加仓库后，更新apt源索引

```shell
sudo apt-get update
```

安装最新版 Docker CE（社区版）

```shell
sudo apt-get install docker-ce
```

检查 Docker CE 是否安装正确

```shell
sudo docker run hello-world
```





### > CentOS 7+ 安装 docker

 https://www.runoob.com/docker/centos-docker-install.html





## 自动安装Docker

不必手动添加软件源,  使用官方脚本自动化安装 Docker

```bash
sudo curl -sSL https://get.docker.com/ | sh
```

安装成功后, 自动启动Docker服务.

可以指定安装软件源中其他版本的Docker

```bash
# 获取不同版本docker的信息
sudo apt-cache madison docker-ce
# 安装指定版本docker
sudo apt-get install docker-ce=17.11.0~ce-0~ubuntu
```



## 配置Docker服务

1-配置用户组,  避免每次使用 docker 命令时都需要切换特权身份

查看用户组

```bash
cat /etc/group
# 安装 docker 的过程中自动创建了docker用户组
```

将当前用户加入docker用户组

```bash
sudo usermod -aG docker lqq
```

更新用户组信息

```bash
# 退出, 重新登录
```



2-配置docker服务启动参数的 几种方法

(a) Docker服务启动时,  实际是调用了 `dockerd` 命令,  支持多种启动参数.  可以使用 `dockerd` 来启动docker服务

```bash
# 如: 启动Docker服务时, 开启DEBUG模式, 监听本地2376端口
dockerd -D -H tcp://127.0.0.1:2376
```

(b) 参数也可以配置在 `/etc/docker/daemon.json` 文件中,  由 docker 服务启动时读取

```json
{
    "debug": true,
    "hosts": ["tcp://127.0.0.1:2376"]
}
```

(c) 操作系统也对 docker 服务进行了封装,  以使用 `Upstart` 来管理启动服务的 `Ubuntu` 系统为例,  Docker服务的默认配置文件是 `/etc/default/docker`,  可以通过修改其中的 `DOCKER_OPTS` 来修改服务启动参数

```
DOCKER_OPTS="$DOCKER_OPTS -H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock"
# 修改之后使用 service 命令重启docker服务
sudo service docker restart
```

对于 CentOS, RedHat 等系统,  服务通过 `systemd` 来管理,  配置文件路径为 `/etc/systemdsystem/docker.service.d/docker.conf` , 更新配置后需要通过 systemctl 命令来管理docker服务

```
sudo systemctl daemon-reload
sudo systemctl start docker.service
```



## 配置Docker镜像源

> 参考:   [简书 -- Docker快速安装以及换镜像源](https://www.jianshu.com/p/34d3b4568059)

配置Docker镜像源为 [中科大的docker源](https://link.jianshu.com/?t=https://lug.ustc.edu.cn/wiki/mirrors/help/docker)

````bash
sudo vim /etc/docker/daemon.json
# 添加下面的内容
{
    "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
# 重启docker服务
sudo service docker restart
````





# 常用的镜像



**BusyBox**

- BusyBox 是一个集成了 100 多个最常用的 Linux 命令的精简工具箱.
- 大小只有不到 2MB, 被誉为 "Linux 系统的瑞士军刀"

```bash
docker pull busybox:latest
docker run -it busybox
```



**Alpine**

- Alpine 操作系统是一个面向安全的轻型 Linux 发行版
- Alpine 采用了 musl、libc 和 BusyBox 以减小系统的体积和运行时资源消耗， 比 BusyBox 功能上更完善
- 目前 Docker 官方推荐使用 Alpine 作为默认的基础镜像环境。

```bash
docker run alpine echo "123"
```



**Debian / Ubuntu**

```bash
docker search --filter=stars=50 ubuntu
docker run -it ubuntu:18.04 bash
apt-get update
apt-get install curl
apt-get install -y apache2
service apache2 start
```



**CentOS / Fedora**

- CentOS 和 Fedora 都是基于 Redhat 的 Linux 发行版
- CentOS 是目前企业级服务器常用操作系统,  Fedora 则主要面向个人桌面用户

```bash
docker search --filter=stars=50 centos
docker run -it centos bash
```





# Docker+Harbor 仓库

**Docker+Harbor 仓库离线版搭建**

> 参考:
>
> https://blog.51cto.com/11093860/2117805
>
> https://blog.csdn.net/hongweigg/article/details/78908154

1-docker-compose安装

```
sudo pip install docker-compose
```

2-下载Harbor离线包

```
http://harbor.orientsoft.cn/
包名： harbor-offline-installer-v1.2.2.tgz
```

3-解压，进入安装包

```
tar -xvf harbor-online-installer-v1.1.1.tgz
cd harbor
```

4-修改 `docker-compose.yml` 和 `harbor.cfg` 文件

```
修改docker-compose.yml中的 ports, privileged
修改harbor.cfg中的 hostname,  如: hostname = http://192.168.31.174
```

5-更新配置文件

```
sudo ./prepare
```

这一步可能出现问题:   private_key生成失败

[对应github上的issue](https://github.com/goharbor/harbor/pull/5260/commits/ee60eaec163820c97b0b59cbb20259b69c902932)

解决方法:

```bash
sudo openssl  req -new -x509 -key ./common/config/ui/private_key.pem -out ./common/config/registry/root.crt -days 3650 -subj '/'
```

6-开始安装并启动

```
sudo ./install.sh
```

 

**使用：**
1、在客户机上登录

`docker login`  默认登录的是 Docker Hub,  如果要登陆自己搭建的Harbor仓库,  可以指定Harbor的 `URL`

```bash
docker login -u [username] -p [password] 容器名

docker login 127.0.0.1
然后输入密码
```

2、在项目中标记（tag）镜像

```
docker tag SOURCE_IMAGE[:TAG] 192.168.31.172/my-test/IMAGE[:TAG]

如:
docker tag hello-world:latest 127.0.0.1/my-test/hello-world-new:v1
```

注意，在客户机上添加对Harbor hostname的域名解析。在/etc/hosts中增加一行：

```
[Harbor 所在机器IP]    [Harbor hostname]
```

3、推送镜像到当前项目

```
docker push 192.168.31.172/my-test/IMAGE[:TAG]

如:
docker push 127.0.0.1/my-test/hello-world-new:v2
```



拉取镜像

```
docker pull 127.0.0.1/my-test/hello-world-new:v2
```





# Docker重要目录

```bash
/var/lib/docker/
	builder/
	buildkit/
	containers/
	image/
	network/
	overlay2/
	plugins/
	runtimes/
	swarm/
	tmp/
	trust/
	volumes/
```







# Docker命令

## 操作Docker镜像

### 获取镜像

#### pull

```
docker [image] pull [options] NAME[:TAG]
	-a, --all-tags=true|false	是否获取镜仓库中对应的所有镜像, 默认为 false
		--disable-content-trust		取消镜像的内容校验, 默认为 true
	
```

### 查看镜像信息

#### images

1-使用 `images` 命令列出镜像

```
docker images [OPTIONS] [REPOSITORY[:TAG]]
docker image ls [OPTIONS] [REPOSITORY[:TAG]]
	-a, --all=true|false
		--digests=true|false	列出镜像的数字摘要, 默认为 false
	-f, --filter=[]			过滤列出的镜像
		--format="TEMPLATE"		控制输出格式, .ID, .Respository
		--no-trunc=true|false	对输出太长的部分是否截断, 默认为 true
	-q, --quiet=true|false	仅输出ID, 默认为 false

查看更多子命令选项: 
    man docker-images
    docker images --help
    docker image --help
```

2-使用 `tag` 命令添加镜像标签

```
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```

#### inspect

3-使用 `inspect` 命令查看镜像详细信息,  包括 制作者, 适应架构, 各层的数字摘要

```
docker image inspect [OPTIONS] IMAGE [IMAGE...]
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

#### history

4-使用 `history` 查看镜像历史:  各层的创建信息

```
docker history [OPTIONS] IMAGE
```

### 搜寻镜像

#### search

搜索Docker Hub官方仓库中的镜像

```
docker search [OPTIONS] TERM
    -f, --filter filter   Filter output based on conditions provided
    	--format string   Pretty-print search using a Go template
    	--limit int       Max number of search results (default 25)
    	--no-trunc        Don't truncate output
```

### 删除和清理镜像

#### rmi / image rm

使用 标签/镜像ID 删除镜像

```
docker rmi [OPTIONS] IMAGE [IMAGE...]
docker image rm [OPTIONS] IMAGE [IMAGE...]
  	-f, --force      Force removal of the image
      	--no-prune   Do not delete untagged parents
```

#### image prune

清理镜像

```
docker image prune [OPTIONS]
  	-a, --all             Remove all unused images, not just dangling(临时) ones
      	--filter filter   Provide filter values (e.g. 'until=<timestamp>')
  	-f, --force           Do not prompt for confirmation
```

### 创建镜像

#### commit / import / build

1- `commit` - 基于 已有容器 创建镜像

```
docker [container] commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
    -a, --author string    Author (e.g., "John Hannibal Smith <hannibal@a-team.com>")
    -c, --change list      Apply Dockerfile instruction to the created image
    -m, --message string   Commit message
    -p, --pause            Pause container during commit (default true)
```

2- `import` - 基于 本地镜像模板 导入镜像

```
docker [image] import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
    -c, --change list      Apply Dockerfile instruction to the created image
    -m, --message string   Set commit message for imported image
```

3- `build` - 基于 Dockerfile 创建镜像

```
docker [image] build [OPTIONS] PATH | URL | -
      --add-host list           Add a custom host-to-IP mapping (host:ip)
      --build-arg list          Set build-time variables
      --cache-from strings      Images to consider as cache sources
      --cgroup-parent string    Optional parent cgroup for the container
      --compress                Compress the build context using gzip
      --cpu-period int          Limit the CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int           Limit the CPU CFS (Completely Fair Scheduler) quota
  -c, --cpu-shares int          CPU shares (relative weight)
      --cpuset-cpus string      CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string      MEMs in which to allow execution (0-3, 0,1)
      --disable-content-trust   Skip image verification (default true)
  -f, --file string             Name of the Dockerfile (Default is 'PATH/Dockerfile')
      --force-rm                Always remove intermediate containers
      --iidfile string          Write the image ID to the file
      --isolation string        Container isolation technology
      --label list              Set metadata for an image
  -m, --memory bytes            Memory limit
      --memory-swap bytes       Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --network string          Set the networking mode for the RUN instructions during build (default
                                "default")
      --no-cache                Do not use cache when building the image
      --pull                    Always attempt to pull a newer version of the image
  -q, --quiet                   Suppress the build output and print image ID on success
      --rm                      Remove intermediate containers after a successful build (default true)
      --security-opt strings    Security options
      --shm-size bytes          Size of /dev/shm
  -t, --tag list                Name and optionally a tag in the 'name:tag' format
      --target string           Set the target build stage to build.
      --ulimit ulimit           Ulimit options (default [])
```

### 存出和载入镜像

#### save ~ load

1-存出镜像

导出镜像到 本地文件

```
docker [iamge] save [OPTIONS] IMAGE [IMAGE...]
	-o, --output string   Write to a file, instead of STDOUT
```

2-载入镜像

导入镜像及其相关的元数据 (包括标签等)

```
docker [image] load [OPTIONS]
    -i, --input string   Read from tar archive file, instead of STDIN
    -q, --quiet          Suppress the load output
```

### 上传镜像

#### push

```
docker [image] push [OPTIONS] NAME[:TAG]
	| [REGISTRY_HOST[:REGISTRY_PORT]/]NAME[:TAG]
	--disable-content-trust   Skip image signing (default true)

# 第一次上传时, 先 docker login
```



## 操作Dcoker容器

- 容器是镜像的一个运行实例;

- 镜像是静态的只读文件,  容器是可读写的,  带有运行所需要的可写文件层;

- Docker容器是独立运行的一个/一组应用 以及 它们运行时必需的运行环境
- 容器是整个Docker技术栈的核心

### 创建容器

#### create

```bash
docker create -it ubuntu:latest

选项参数很多:
create与容器运行模式相关de主要选项
	-a, --attach=[]			是否绑定到标准输入/输出和错误
	-d, --detach=false		是否在后台运行(守护态-Daemonized), 默认false
	--entrypoint=""			镜像存在入口命令时, 覆盖为新命令
	--expose=[]				容器暴露的端口/端口范围
	--group-add=[]			运行容器的用户组
	-i, --interactive=false	保持标准输入打开, 默认false
	--net="bridge"			容器网络模式
	-P						通过NAT将容器暴露的端口自动映射到本地主机某个临时端口
	-p						指定端口映射
	--restart="no"			容器重启策略, 包括 no, on-failure[:max-retry], always,,,
	--rm=true				容器退出后是否自动删除, 不能与 -d 同时用
	-t, --tty=false			是否分配一个伪终端, 默认false
	--tmfs=[]				挂载临时文件系统到容器
	-v						挂载主机文件卷到容器
	--volume-driver=""		挂载文件卷的驱动类型
	--volumes-from=[]		从其他容器挂载卷
	-w, --workdir=""		容器内默认工作目录

create与容器环境和配置相关de主要选项
	--add-host=[]			在容器内添加一个主机名到 IP 的映射关系(通过 /etc/hosts 文件)
	--dns-search			DNS搜索域
	--dns-opt=[]			自定义dns选项
	--dns=[]				自定义dns服务器
	-e						指定容器内环境变量
	--env-file=[]			从文件中读取env到容器内
	-h, --hostname=""		指定容器内主机名
	--ip=""					容器IPv4
	--link=[<name or id>:alias]	链接到其他容器
	--mac-address=""		容器MAC
	--name=""				容器别名

create命令与容器资源限制和安保相关de选项

```

#### start

```
docker start CONTAINER_ID
```

#### run

```
新建容器并启动
docker run ...

docker run 在后台运行的标准操作:
    1. 检查本地是否存在指定镜像, 不存在就从公有库下载
    2. 利用镜像创建 并启动 一个容器
    3. 分配一个文件系统 并在只读的镜像层外面挂载一层可写层
    4. 从宿主机配置的网桥接口中 桥接一个虚拟接口到容器中
    5. 从地址池配置一个 ip 给容器
    6. 执行用户指定的应用程序
    7.执行完毕后容器被终止
```

#### wait

等待容器退出, 并打印返回退出结果,  如查看docker run 无法运行时的出错码:

- 125:  Docker daemon执行出错, 如指定了不支持的 Docker命令参数
- 126:  命令无法执行,  如权限出错
- 127:  命令未找到

```
docker container wait CONTAINER [CONTAINER ...]
```

#### logs

查看容器输出信息

```bash
docker logs CONTAINER_ID
	-details
	-f, -follow
	-since string		输出从某个时间开始的logs
	-tail string		输出最近若干logs
	-t, -timestamps		显示时间戳信息
	-until string		输出某个时间之前的logs
```







### 停止容器

#### pause ~ unpause

暂停

#### stop ~ start

停止



#### prune

自动清除所有已停止的容器

#### kill

直接发送 SIGNAL 信号强行终止容器



### 进入容器

#### attach

使用 attach 有时不方便:  当多个窗口同时 attach 到同一个容器时, 所有窗口都会同步显示;  当某个窗口命令阻塞时,  其他窗口也无法执行操作

#### exec

```bash
docker 1.3.0+

	-d, --detach				在容器后台执行命令
	--deyach-keys=""			指定将容器切回后台的 按键
	-e, --env=[]				指定环境变量列表
	-i, --interactive=false		打开标准输入接受用户输入命令, 默认false
	--privileged=flase			是否给执行命令以最高权限
	-t, --tty=false				是否分配伪终端, 默认false
	-u, --user=""				执行命令的用户名或 ID
```

在容器查看用户和进程信息:

```
w
ps -ef
```



### 删除容器

#### rm

删除处于 终止 / 退出状态 的容器

```
-f, --force=false		true时, Docker会先发送SIGKILL信号给容器, 终止其中应用, 后强行删除
-l, --link=false		删除容器的链接,但保留容器
-v, --volumes=false		删除容器挂载的数据卷
```

### 导入导出

容器迁移

#### export ~ import

```bash
docker export -o xxx.tar CONTAINER
docker export --output="xxx.tar" CONTAINER
docker export CONTAINER >xxx.tar

docker import xxx.tar - test/ubuntu:v1.0
```



**容器快照文件** 与 **镜像存储文件**

```bash
docker load		-->		导入镜像存储文件到 本地镜像库
	仅保存容器当时快照状态, 丢弃所有历史记录 和 元数据
	从容器快照文件导入时 可以重新指定 标签等元数据
docker import	-->		导入容器快照文件到 本地镜像库
	保存完整记录
```



### 查看容器

#### ls / ps

```
docker ps			查看正在运行的容器
docker ps -q		查看正在运行容器的 ID
docker ps -a		查看所有容器
docker ps -aq		查看所有容器的 ID
```

#### inspect

查看容器具体信息 JSON,  包括ID 时间 路径 状态 镜像 配置 ...

```bash
docker container inspect [OPTIONS] CONTAINER [CONTAINER ...]
```

#### top

查看容器内进程



#### stats

查看统计信息,  包括 CPU 内存 存储 网络 ... 等使用情况

```bash
-a, --all
-format string
-no-stream
-no-trunc
```





### 其他命令

#### cp

在容器和主机之间 复制文件

```
docker cp /home/data container:/tmp/
```

#### diff

查看容器内文件系统变更

#### port

查看端口映射

#### update

更新容器一些运行时配置





# Docker仓库

Docker Hub 公共镜像市场

```
- docker login  ---> ~/.docker/config.json
- 上传个人镜像
- docker search IMAGE
- docker pull IMAGE
- docker pull user_name/IMAGE (Docker用户创建和维护的镜像)
```

第三方镜像市场

```
- 腾讯云, 阿里云, 网易云, 华为云, 时速云
- docker pull ...ubuntu...
- docker tag ...ubuntu... ubuntu:latest (更新镜像标签, 与官方标签保持一致, 方便使用)
```

搭建本地私有仓库

```
使用 registry 镜像搭建私有仓库
- docker run  -d -p 5000:5000 -v  /opt/data/registry:/var/lib/registry  registry:2
管理私有仓库
- docker tag ubuntu:18.04 10.0.2.2:5000/test
- docker push 10.0.2.2:5000/test
- curl http://10.0.2.2:5000/v2/search  查看仓库中的镜像
```





# Docker数据卷



# Dockerfile

- 菜鸟教程:  https://www.runoob.com/docker/docker-dockerfile.html

- Dockerfile 是一个用来构建镜像的文本文件，文本内容包含了一条条构建镜像所需的指令和说明。

- 使用 Dockerfile 定制镜像



## 指令

- Dockerfile 的指令每执行一次都会在 docker 上新建一层。
- 过多无意义的层，会造成镜像膨胀过大
- 以 **&&** 符号连接命令，减少镜像层数。 



**FROM**：定制的镜像都是基于 FROM 的镜像 

**RUN**：用于执行后面跟着的命令行命令。有 2 种格式： 

```dockerfile
# shell 格式
RUN <命令行命令>   # <命令行命令> 等同于，在终端操作的 shell 命令。

# exec 格式
RUN ["可执行文件", "参数1", "参数2"]
# RUN ["./test.php", "dev", "offline"] 等价于 RUN ./test.php dev offline
```



## 开始构建镜像

- 在 Dockerfile 文件的存放目录下，执行构建动作。

- 以下示例，通过目录下的 Dockerfile 构建一个 nginx:test（镜像名称:镜像标签）。

- **注**：最后的 **.** 代表本次执行的 **上下文路径**

```bash
$ docker build -t nginx:test .
```

### 上下文路径

- 上下文路径，是指 docker 在构建镜像，有时候想要使用到本机的文件（比如复制），docker build 命令得知这个路径后，会将路径下的所有内容打包。

**解析**：由于 docker 的运行模式是 C/S。我们本机是 C，docker 引擎是 S。实际的构建过程是在 docker 引擎下完成的，所以这个时候无法用到我们本机的文件。这就需要把我们本机的指定目录下的文件一起打包提供给 docker 引擎使用。

如果未说明最后一个参数，那么默认上下文路径就是 Dockerfile 所在的位置。

**注意**：上下文路径下不要放无用的文件，因为会一起打包发送给 docker 引擎，如果文件过多会造成过程缓慢。



### 命令选项

docker [image] build -h



### .dockerignore

- 可以通过 .dockerignore 文件,  在每一行添加一条忽略模式,  在创建镜像时不将无关数据发送到服务端

```.dockerignore
# 在 .dockerignore 文件中定义忽略模式
*/temp*
*/*/temp*
tmp?
~*
Dockerfile
!README.md    # 不忽略
```



### 多步骤创建

- 自 17.05 版本开始,  Docker 支持多步骤镜像创建特性 (Multi-stage build), 可以精简最终生成的镜像大小.
- 对于需要编译的应用 (如 C、Go 或 Java 语言等)来说， 通常至少需要准备两个环境的 Docker 镜像:
  1. 编译环境镜像： 包括完整的编译引擎、依赖库等，往往比较庞大。作用是编译应用为二进制文件
  2. 运行环境镜像： 利用编译好的二进制文件，运行应用，由于不需要编译环境，体积比较小
- 使用单一 Dockerfile 进行多步骤创建，降低维护复杂度 

例子：

创建 main.go 文件， 内容为：

```go
package main
import (
    "fmt"
)
func main() {
    fmt.Println("Hello, Docker")
}
```

创建一个 Dockerfile

```dockerfile

# 1.用于创建编译环境镜像
FROM golang:1.9 as builder  # define stage name as builder
RUN mkdir -p /go/src/test
WORKDIR /go/src/test
COPY main.go .
RUN CGO_ENABLE=0 GOOS=linux go build -o app .

# 2.在同一个 Docekrfile 中. 用于创建运行环境镜像
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/test/app .  # copy file from the builder stage
CMD ["./app"]
```

构建一个镜像:

```bash
docker build -t yeasy/test-multistage:latest .
```

查看最终生成的镜像大小:

```bash
docker images | grep test-multistage
```



### 最佳实践

从需求出发,  来定制适合自己、高效方便的镜像

1. 精简镜像的用途
2. 选择合适的基础镜像
3. 提供注释和维护者信息
4. 正确明确的基础镜像版本号
5. 减少镜像层数
6. 恰当使用多步骤创建
   - 如仅维护一个 Dockerfile， 可以将编译和运行等过程分开， 保证最终生成的镜像只包括运行应用所需要的最小化环境
7. 使用 .dockerignore 文件
8. 及时删除临时文件和缓存文件
   - 特别是在 apt-get 之后， /var/cache/apt 下面会缓存一些安装包
9. 提高生成速度
   - 如合理使用 cache，减少内容目录下的文件，或使用 .dockerignore 文件指定等
10. 调整合理的指令顺序
    - 在开启 cache 时，内容不变的指令尽量放在前面，可以尽量复用
11. 减少外部源的干扰
    - 如果确实要从外部引入数据，需要指定持久的地址，并带版本号，让他人可以复用而不出错







## 指令详解

### FROM

### RUN

### COPY

复制指令，从上下文目录中复制文件或者目录到容器里指定路径。

格式：

```dockerfile
COPY [--chown=<user>:<group>] <源路径1>...  <目标路径>
COPY [--chown=<user>:<group>] ["<源路径1>",...  "<目标路径>"]
```

**[--chown=:]**：可选参数，用户改变复制到容器内文件的拥有者和属组。

**<源路径>**：源文件或者源目录，这里可以是通配符表达式，其通配符规则要满足 Go 的 filepath.Match 规则。例如：

```dockerfile
COPY hom* /mydir/
COPY hom?.txt /mydir/
```

**<目标路径>**：容器内的指定路径，该路径不用事先建好，路径不存在的话，会自动创建。

### ADD

ADD 指令和 COPY 的使用格式一致（同样需求下，官方推荐使用 COPY）。功能也类似，不同之处如下：

- ADD 的优点：在执行 <源文件> 为 tar 压缩文件的话，压缩格式为 gzip, bzip2 以及 xz 的情况下，会自动复制并解压到 <目标路径>。
- ADD 的缺点：在不解压的前提下，无法复制 tar 压缩文件。会令镜像构建缓存失效，从而可能会令镜像构建变得比较缓慢。具体是否使用，可以根据是否需要自动解压来决定。

### CMD

类似于 RUN 指令，用于运行程序，但二者运行的时间点不同:

- RUN 是在 docker build 时运行。
- CMD 在docker run 时运行。

**作用**：为启动的容器指定默认要运行的程序，程序运行结束，容器也就结束。CMD 指令指定的程序可被 docker run 命令行参数中指定要运行的程序所覆盖。

**注意**：如果 Dockerfile 中如果存在多个 CMD 指令，仅最后一个生效。

格式：

```dockerfile
CMD <shell 命令> 
CMD ["<可执行文件或命令>","<param1>","<param2>",...] 
CMD ["<param1>","<param2>",...]  # 该写法是为 ENTRYPOINT 指令指定的程序提供默认参数
```

推荐使用第二种格式，执行过程比较明确。第一种格式实际上在运行的过程中也会自动转换成第二种格式运行，并且默认可执行文件是 sh。

### ENTRYPOINT

类似于 CMD 指令，但其不会被 docker run 的命令行参数指定的指令所覆盖，而且这些命令行参数会被当作参数送给 ENTRYPOINT 指令指定的程序。

但是, 如果运行 docker run 时使用了 --entrypoint 选项，此选项的参数可当作要运行的程序覆盖 ENTRYPOINT 指令指定的程序。

**优点**：在执行 docker run 的时候可以指定 ENTRYPOINT 运行所需的参数。

**注意**：如果 Dockerfile 中如果存在多个 ENTRYPOINT 指令，仅最后一个生效。

格式：

```
ENTRYPOINT ["<executeable>","<param1>","<param2>",...]
```

可以搭配 CMD 命令使用：一般是变参才会使用 CMD ，这里的 CMD 等于是在给 ENTRYPOINT 传参，以下示例会提到。

示例：

假设已通过 Dockerfile 构建了 nginx:test 镜像：

```
FROM nginx

ENTRYPOINT ["nginx", "-c"] # 定参
CMD ["/etc/nginx/nginx.conf"] # 变参 
```

1、不传参运行

```
$ docker run  nginx:test
```

容器内会默认运行以下命令，启动主进程。

```
nginx -c /etc/nginx/nginx.conf
```

2、传参运行

```
$ docker run  nginx:test -c /etc/nginx/new.conf
```

容器内会默认运行以下命令，启动主进程(/etc/nginx/new.conf:假设容器内已有此文件)

```
nginx -c /etc/nginx/new.conf
```

### ENV

设置环境变量，定义了环境变量，那么在后续的指令中，就可以使用这个环境变量。

格式：

```
ENV <key> <value>
ENV <key1>=<value1> <key2>=<value2>...
```

以下示例设置 NODE_VERSION = 7.2.0 ， 在后续的指令中可以通过 $NODE_VERSION 引用：

```
ENV NODE_VERSION 7.2.0

RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc"
```

### ARG

构建参数，与 ENV 作用一至。不过作用域不一样。ARG 设置的环境变量仅对 Dockerfile 内有效，也就是说只有 docker build 的过程中有效，构建好的镜像内不存在此环境变量。

构建命令 docker build 中可以用 --build-arg <参数名>=<值> 来覆盖。

格式：

```
ARG <参数名>[=<默认值>]
```

### VOLUME

定义匿名数据卷。在启动容器时忘记挂载数据卷，会自动挂载到匿名卷。

作用：

- 避免重要的数据，因容器重启而丢失，这是非常致命的。
- 避免容器不断变大。

格式：

```
VOLUME ["<路径1>", "<路径2>"...]
VOLUME <路径>
```

在启动容器 docker run 的时候，我们可以通过 -v 参数修改挂载点。

### EXPOSE

仅仅只是声明端口。

作用：

- 帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射。
- 在运行时使用随机端口映射时，也就是 docker run -P 时，会自动随机映射 EXPOSE 的端口。

格式：

```
EXPOSE <端口1> [<端口2>...]
```

### WORKDIR

指定工作目录。用 WORKDIR 指定的工作目录，会在构建镜像的每一层中都存在。（WORKDIR 指定的工作目录，必须是提前创建好的）。

docker build 构建镜像过程中的，每一个 RUN 命令都是新建的一层。只有通过 WORKDIR 创建的目录才会一直存在。

格式：

```
WORKDIR <工作目录路径>
```

### USER

用于指定执行后续命令的用户和用户组，这边只是切换后续命令执行的用户（用户和用户组必须提前已经存在）。

格式：

```
USER <用户名>[:<用户组>]
```

### HEALTHCHECK

用于指定某个程序或者指令来监控 docker 容器服务的运行状态。

格式：

```
HEALTHCHECK [选项] CMD <命令>：设置检查容器健康状况的命令
HEALTHCHECK NONE：如果基础镜像有健康检查指令，使用这行可以屏蔽掉其健康检查指令

HEALTHCHECK [选项] CMD <命令> : 这边 CMD 后面跟随的命令使用，可以参考 CMD 的用法。
```

### ONBUILD

用于延迟构建命令的执行。简单的说，就是 Dockerfile 里用 ONBUILD 指定的命令，在本次构建镜像的过程中不会执行（假设镜像为 test-build）。当有新的 Dockerfile 使用了之前构建的镜像 FROM test-build ，这是执行新镜像的 Dockerfile 构建时候，会执行 test-build 的 Dockerfile 里的 ONBUILD 指定的命令。

格式：

```
ONBUILD <其它指令>
```











# [批量删除容器和镜像](https://www.cnblogs.com/111testing/p/9715887.html)

删除单个镜像或者容器

```bash
docker rmi 镜像ID/镜像名字:TAG
docker rm 容器ID/容器名字
```

删除untagged images，也就是那些TAG为的<none>的images

```bash
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
# 或
docker image prune -f
```

删除所有镜像

```bash
docker rmi $(docker images -q)
# 强制删除
docker rmi -f $(docker images -q)
```

删除所有的容器

```bash
# 先停止所有的container
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```



# 端口映射与容器互联

- 主机: 容器与宿主机之间网络无隔离, 即容器直接使用宿主机网络
  None network - 容器禁用所有网络
  Overlay network - 覆盖网络: 利用VxLAN实现的网桥
  MacVlan network: 容器具备MAC地址, 使其显示为网络上的物理设备



**(1) bridge网络模式**

- 宿主机上需要单独 bridge 网卡,  如docker默认创建的 `docker0`

- `docker network create NAME` 创建 bridge 网络后,  在宿主机中会自动创建一个 `br-xxxxxxxxxxxx` 网卡,  其 IP 地址是 `docker network inspect NETWORK` 可查看到的 `网关的 IP`

- `docker run --network NETWORK -dti centos` 每次启动一个容器后,  在宿主机中会自动创建一个 `vethxxxxxxx` 网卡,  同时在容器中创建一个网卡 `eth0`,  与宿主机的 `vethxxxxxxx` 是成对的 (虚拟网络设备对)

- ```
  宿主机eth0网卡 <---> 宿主机docker0网卡 <---> 宿主机veth1网卡  <---> docker容器eth0网卡
                                     <---> 宿主机veth2网卡  <---> docker容器eth0网卡
                                     <---> 宿主机veth3网卡  <---> docker容器eth0网卡
  ```

- 容器之间, 容器与主机之间的网络通信,  需要借助每一个容器创建时生成的一对 veth pair 虚拟网络设备对.  一个在容器上,  一个在主机上

- 外部无法直接访问容器,  需要建立 `端口映射`

- ```
  docker run/create -P [HOST_IP]:[HOST_PORT]:CONTAINER_PORT ...
  docker run/create -p [HOST_IP]:[HOST_PORT]:CONTAINER_PORT ...
  # -p ::80		将容器的80端口随机映射到宿主机某个端口, 可通过任意IP访问 (0.0.0.0:xxxx)
  # -p :80:80		将容器的80端口指定映射到宿主机 80 端口, 可通过任意IP访问 (0.0.0.0:80)
  # -p 192.168.10.10::80  将容器的80端口随机映射到宿主机某个端口, 只可通过指定IP访问 (192.168.10.10:xxxx)
  ```

- 每一个容器具有单独的 IP

**(2) host**

- 容器完全共享宿主机网络,  没有网络隔离.  容器中看到的网络配置 (网卡信息,  路由表, Iptables规则等) 均与主机保持一致

- 容器和主机上的应用不能使用重复的端口,  例如宿主机占用了 80 端口,  则任何一个 host 模式的容器都不能使用 80 端口

- 外部可以直接访问容器 (安全性),  不需要端口映射

- 容器IP == 宿主机IP

- 网络性能最大化

- ```bash
  docker run --network host -dti centos bash
  ```

**(2+) 特殊 host 网络模式 (Container 网络模式)**

- 容器共享其他容器的网络,  容器与容器之间没有网络隔离

- ```bash
  docker run --network NETWORK:CONTAINER -dti centos bash
  ```

**(3) none**

- 容器上没有网络,  也没有任何网络设备 (没有网卡, IP等)

- 如果需要使用网络,  需要手动安装和配置

- none模式适用于 需要高度定制网络的场景

- ```
  docker run --network none -dti centos bash
  ```

**(4) overlay**

- overlay网络的实现方式有多种,  docker自身集成了一种, 基于VXLAN隧道技术实现

- overlay网络主要用于实现 跨主机容器之间的通信,  场景:  需要管理成百上千个跨主机的容器集群的网络时

- ```bash
  
  ```

**(5) macvlan**

- 直接基于 MAC 地址进行数据转发
- 宿主机充当一个二层交换机,  docker会维护一个MAC地址表,  当宿主机网络收到一个数据包后, 直接根据 MAC地址找到对应的容器,  在吧数据交给对应的容器
- 容器之间可以直接通过 IP 互通,  通过宿主机上内建的虚拟网络设备 (创建macvlan网络时自动创建),  但与主机无法直接利用 IP 互通
- 场景:   当需要让容器看起来像是一个真实的物理机时,  使用 macvlan 模式







### docker网络管理命令

查看网络列表

```bash
docker network ls
# NETWORK ID, NAME, DRIVER(网络驱动模式), SCOPE(使用范围)
```

查看指定网络的详情

```bash
docker [network] inspect NETWORK
```

创建

```bash
docker network create NETWORK
```

 删除

```bash
docker network rm NETWORK
```



**使用网络**

`--network` 指定

```bash
docker run --network NETWORK -dti centos bash
```

**网络连接与断开**

```bash
docker network connect NETWORK CONTAINER_ID
docker network disconnect NETWORK CONTAINER_ID

# 查看网络连接
docker [container] inspect CONTAINER_ID
```





- `docker network create NAME` 创建 bridge 网络后,  在宿主机中会自动创建一个 `br-xxxxxxxxxxxx` 网卡,  其 IP 地址是 `docker network inspect NETWORK` 可查看到的 `网关的 IP`

- `docker run --network NETWORK -dti centos` 每次启动一个容器后,  在宿主机中会自动创建一个 `vethxxxxxxx` 网卡,  同时在容器中创建一个网卡 `eth0`,  与宿主机的 `vethxxxxxxx` 是成对的 (虚拟网络设备对)

- ```
  宿主机eth0网卡 <---> 宿主机docker0网卡 <---> 宿主机veth1网卡  <---> docker容器eth0网卡
                                     <---> 宿主机veth2网卡  <---> docker容器eth0网卡
                                     <---> 宿主机veth3网卡  <---> docker容器eth0网卡
  ```





# 内网独立IP访问

> https://www.jb51.net/article/145472.htm

试过无效



[VMware虚拟机上网络连接（network type）的三种模式--bridged、host-only、NAT](https://www.cnblogs.com/xiaochaohuashengmi/archive/2011/03/15/1985084.html)

