# docker-machine

使用 docker-machine 安装和管理 Docker 运行环境：

- docker-machine 可以 通过 **多种后端驱动** 来管理不同的资源, 包括 **虚拟机、本地主机、云平台** 等。通过 -d 选项可以选择支持的驱动类型



通过 **后端驱动之一、虚拟机** 管理 docker 运行环境

1. 下载安装 docker-toolbox

   - 下载地址：http://mirrors.aliyun.com/docker-toolbox/windows/docker-toolbox/
   - **Docker的boot2docker.iso镜像使用**:  https://blog.csdn.net/jiangjingxuan/article/details/54908272

   

2. 查看命令帮助

   ```bash
   $ docker-machine -h
   ```

3. 通过 virtualbox 驱动启动一个虚拟机环境 (环境名为 test)

   ```bash
   $ docker-machine create --driver=virtualbox test
   ```

   create命令会先去找 boot2docker.iso, 没有则会下载,  但下载速度过慢,  因此需要按照上面的 **Docker 的 boot2docker.iso 镜像使用**  去操作:

   去 Docker Toolbox 安装目录下找 boot2docker.iso,  复制到 C:\Users\Administrator\\.docker\machine\cache\ 目录下

   

4. 查看访问 Docker 环境所需的配置信息
   docker-machine env test

   ```
   > docker-machine env test
   
   $Env:DOCKER_TLS_VERIFY = "1"
   $Env:DOCKER_HOST = "tcp://192.168.99.100:2376"
   $Env:DOCKER_CERT_PATH = "C:\Users\Administrator\.docker\machine\machines\test"
   $Env:DOCKER_MACHINE_NAME = "test"
   $Env:COMPOSE_CONVERT_WINDOWS_PATHS = "true"
   # Run this command to configure your shell:
   # & "C:\Program Files\Docker\Docker\Resources\bin\docker-machine.exe" env test | Invoke-Expression
   ```

   

5. 查看注册到本地管理列表中的 docker 主机

   ```bash
   $ docker-machine ls
   ```

6. 查看指定 docker 主机的具体信息

   ```bash
   $ docker-machine inspect
   ```

7. 通过 ssh 连接到指定主机上

   ```bash
   $ docker-machine ssh test
   ```

8. 更新镜像源:

   ```bash
   sudo vi /etc/docker/daemon.json
   # 添加下面的内容
   {
       "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
   }
   # 重启docker服务
   sudo service docker restart
   ```



使用 docker 环境完毕后，停止 docker 主机：

```bash
$ docker-machine stop test
```



客户端配置： 所有客户端配置数据保存在 ~/.docker/machine/machines/路径下





windows docker-machine 环境内重启 docker 服务

> 尝试使用 ` systemctl restart ` 和 `service docker restart` ,  都找不到命令

```bash
# 查找 dockerd 启动命令, 并复制下来
$ ps -ef | grep dockerd
# 关闭 docker 服务
$ sudo kill -9 [PID]
# 运行刚才复制的 dockerd 启动命令
$ sudo /usr/local/bin/dockerd -g /var/lib/docker -H unix:// -H tcp://0.0.0.0:2376 --label provider=virtualbox --tlsverify --tlscacert=/var/lib/boot2docker/ca.pem --tlscert=/var/lib/boot2docker/server.pem --tlskey=/var/lib/boot2docker/server-key.pem -s overlay2 &
```





# SSH 登录 docker-machine 环境

> 直接在 windows cmd 进入 docker-machine 开启的环境时,  vi 的使用出现问题,  无法保存文件,  导致无法在环境中更新 docekr 镜像源,  于是选择 SSH 登录方式

1. 如果没有环境,  创建一个 docker-machine 环境,  如:

   ```bash
   $ docker-machine create --driver=virtualbox test
   ```

2. 查看环境信息

   ```bash
   $ docker-machine inspect test
   ```

3. 复制环境信息中的 Driver 项下的 SSHKeyPath

   ```
       "Driver": {
           "IPAddress": "192.168.99.100",
           "MachineName": "test",
           "SSHUser": "docker",
           "SSHPort": 50826,
           "SSHKeyPath": "C:\\Users\\Administrator\\.docker\\machine\\machines\\test\\id_rsa",
   ```

4. 打开 SSH 远程连接终端工具,  如 Moba Xterm,  配置 SSH 连接时选择 `Use private key`,  按照 SSHKeyPath 选择文件 `id_rsa`

5. SSH 登录成功

