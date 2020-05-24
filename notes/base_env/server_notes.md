# 虚拟环境



## virtualenv

From yanqidong:  [Python中的虚拟环境（Virtualenv）及其工作原理](https://note.qidong.name/2019/03/python-virtualenv/)

- **简介**

也许Python由于2和3的分裂，Python发展出了虚拟环境（[virtualenv](https://virtualenv.pypa.io/)）的技术。 还有一个原因——可能这才是主要原因——Python的包只能同时安装一个版本。 这种行为是学自系统包管理器。 对系统来说，一个包安装一个版本就够了。 但是对一个开发多个复杂项目的环境来说，只有像Java系的Maven库那样，多个版本同时保留，依赖检查延迟到打包时，才能确保并行开发。 否则，A项目需要S软件的1.0版本，B项目需要它的2.0，这就没法一起玩了。

[virtualenv](https://virtualenv.pypa.io/)的关键词是隔离（Isolation）。 它能创造一个包含特定版本的Python环境，并且确保Python软件包非常干净。 它创造性地使用了一些Shell和Python原有的机制，实现了虚拟环境的功能。

因此，开发每个Python项目时，都推荐创建对应的[virtualenv](https://virtualenv.pypa.io/)来隔离开发。 这样可以不受系统Python软件包的影响，安装任意包的任意版本，并且最终能通过`pip freeze > requirements.txt`获取依赖列表。 （当然，这个列表通常需要裁剪。）



- **安装virtualenv**

使用`apt`、`yum`等包管理器安装的版本老旧，推荐使用`pip`安装。

```sh
pip3 install --user virtualenv
```



- **准备virtualenv**

每个项目，都需要独立创建一个（或多个）虚拟环境，隔离开发。

```sh
virtualenv -p python3 venv
```

`-p`是显式指定Python版本，避免使用默认的`python`。 虚拟环境的常用名，可选择`env`、`venv`、`.env`、`.venv`。 `venv`是PyCharm的默认虚拟环境名称。



- **激活 virtualenv**

默认使用的是用户+系统环境，激活后才是虚拟环境。

```sh
source venv/bin/activate
```

激活虚拟环境后，可以看到只有三个Python包。 这个环境可以随意使用，所有安装都会在`./venv/`下，不会影响系统环境。 干净的环境，也能帮助开发人员确认依赖。

```shell
$ pip list
Package    Version
---------- -------
pip        19.0.3
setuptools 40.8.0
wheel      0.33.1
```

在这个虚拟环境中，`python`就是`python3`，而系统环境的`python`通常是`python2`。 在安装软件时，直接使用`pip`，即可安装到虚拟环境中。 而不像一般状态下，要么加`sudo`提权（[brew]或Windows环境下不用），要么安装时需要加`--user`，安装到用户目录下。

以下是系统、用户、虚拟环境三种方式安装，以及可执行文件`pylint`被安装的位置。

```shell
$ sudo pip install pylint
$ ls /usr/local/bin/pylint
/usr/local/bin/pylint

$ pip install --user pylint
$ ls ~/.local/bin/pylint
/home/user/.local/bin/pylint

$ source venv/bin/activate
$ pip install pylint
$ ls venv/bin/pylint
venv/bin/pylint
```

- **退出 virtualenv**

```sh
deactivate
```



- **虚拟环境的原理**

[virtualenv](https://virtualenv.pypa.io/)是如何创建一个隔离的Python虚拟环境？这个环境有什么特点？

这个环境的特点有二：

- Python版本固定。即使系统的Python升级了，虚拟环境中的仍然不受影响，保留开发状态。
- 所有Python软件包，都只在这个环境生效。一旦退出，则回到用户+系统的默认环境中。

这两个特点，由两个小手段实现。

- 改变当前Shell的`PATH`。
- 改变Python运行时的`sys.path`。

以下为`python:alpine`镜像中，以`root`用户演示的例子。



- **改变`PATH`**

首先看一下它的目录结构：

```shell
# ls venv
bin      include  lib
# ls /usr/local
bin      include  lib      share
```

环境内所有的新内容，都在这个新生成目录下。 `bin`是可执行文件的位置，`include`是C/C++的头文件位置，`lib`是库文件位置。 它和`/usr/local`内的主要目录几乎相同，也和`~/.local`下类似。

魔法都在两个`PATH`中。

```shell
# echo $PATH
/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# . venv/bin/activate
(venv) # echo $PATH
/root/venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

显然，这个`activate`，为当前`PATH`增加了`venv/bin`这个位置在最前方，因此虚拟环境中的可执行文件拥有最高优先级。 而`lib`与`include`，仅仅是`bin`下面的可执行文件做相对路径运算来寻找的位置。 所以，改变了`PATH`，就改变了很多事。

```shell
# ls -hl venv/bin/
total 88
-rw-r--r--    1 root     root        2.0K Mar 31 08:06 activate
-rw-r--r--    1 root     root        1.1K Mar 31 08:06 activate.csh
-rw-r--r--    1 root     root        3.0K Mar 31 08:06 activate.fish
-rw-r--r--    1 root     root        1.5K Mar 31 08:06 activate.ps1
-rw-r--r--    1 root     root         986 Mar 31 08:06 activate.xsh
-rw-r--r--    1 root     root        1.5K Mar 31 08:06 activate_this.py
-rwxr-xr-x    1 root     root         238 Mar 31 08:06 easy_install
-rwxr-xr-x    1 root     root         238 Mar 31 08:06 easy_install-3.7
-rwxr-xr-x    1 root     root         220 Mar 31 08:06 pip
-rwxr-xr-x    1 root     root         220 Mar 31 08:06 pip3
-rwxr-xr-x    1 root     root         220 Mar 31 08:06 pip3.7
-rwxr-xr-x    1 root     root       35.8K Mar 31 08:06 python
-rwxr-xr-x    1 root     root        2.3K Mar 31 08:06 python-config
lrwxrwxrwx    1 root     root           6 Mar 31 08:06 python3 -> python
lrwxrwxrwx    1 root     root           6 Mar 31 08:06 python3.7 -> python
-rwxr-xr-x    1 root     root         216 Mar 31 08:06 wheel
```

由于优先级最高，所以环境里的`python`、`pip`等，包括后来用`pip`安装的可执行文件，都使用的是`venv`下的。



- **改变`sys.path`**

```shell
(venv) # python -m site
sys.path = [
    '/root',
    '/root/venv/lib/python37.zip',
    '/root/venv/lib/python3.7',
    '/root/venv/lib/python3.7/lib-dynload',
    '/usr/local/lib/python3.7',
    '/root/venv/lib/python3.7/site-packages',
]
USER_BASE: '/root/.local' (doesn't exist)
USER_SITE: '/root/.local/lib/python3.7/site-packages' (doesn't exist)
ENABLE_USER_SITE: False
(venv) # deactivate
# python -m site
sys.path = [
    '/root',
    '/usr/local/lib/python37.zip',
    '/usr/local/lib/python3.7',
    '/usr/local/lib/python3.7/lib-dynload',
    '/usr/local/lib/python3.7/site-packages',
]
USER_BASE: '/root/.local' (doesn't exist)
USER_SITE: '/root/.local/lib/python3.7/site-packages' (doesn't exist)
ENABLE_USER_SITE: True
```

可见，`sys.path`发生了翻天覆地的变化。 除了当前路径`/root`和标准库`/usr/local/lib/python3.7`被保留以外，其它位置都换成了`venv`下的。 这就是为什么`pip list`看不见什么软件包的原因，也是环境隔离的最大秘密。



- **标准库venv**

从Python 3.3开始，标准库中就自带了一个[venv](https://docs.python.org/3/library/venv.html)模块，拥有[virtualenv](https://virtualenv.pypa.io/)的部分功能。 因此，也可以通过以下命令来创建虚拟环境。

```sh
python3 -m venv venv
```

但还是推荐使用[virtualenv](https://virtualenv.pypa.io/)。 [venv](https://docs.python.org/3/library/venv.html)只能创建当前版本的虚拟环境，不能创建其它Python 3.x的版本，以及Python 2的环境。





## + virtualenvwrapper

### 如何搭建虚拟环境?

- 安装虚拟环境:

```
sudo pip install virtualenv
sudo pip install virtualenvwrapper
```

> 安装完虚拟环境后，如果提示找不到mkvirtualenv命令，须配置环境变量：

```
# 1、创建目录用来存放虚拟环境
mkdir $HOME/.virtualenvs

# 2、打开~/.bashrc文件，并添加如下：
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

# 3、运行
source ~/.bashrc
```

- 创建虚拟环境 :

  - 提示：如果不指定python版本，默认安装的是python2的虚拟环境

  - 在python2中，创建虚拟环境

    ```
    mkvirtualenv 虚拟环境名称
    例 ：
    mkvirtualenv py_flask
    ```

  - 在python3中，创建虚拟环境

    ```
    mkvirtualenv -p python3 虚拟环境名称
    例 ：
    mkvirtualenv -p python3 py3_flask
    ```

- 提示 :

  - 创建虚拟环境需要联网
  - 创建成功后, 会自动工作在这个虚拟环境上
  - 工作在虚拟环境上, 提示符最前面会出现 “虚拟环境名称”

### 如何使用虚拟环境?

- 查看虚拟环境的命令 :

```
workon 两次tab键
```

- 使用虚拟环境的命令 :

```
workon 虚拟环境名称

例 ：使用python2的虚拟环境
workon py_flask

例 ：使用python3的虚拟环境
workon py3_flask
```

- 退出虚拟环境的命令 :

```
deactivate
```

- 删除虚拟环境的命令 :

```
rmvirtualenv 虚拟环境名称

例 ：删除虚拟环境py3_flask

先退出：deactivate
再删除：rmvirtualenv py3_flask
```

### 如何在虚拟环境中安装工具包?

- 提示 : 工具包安装的位置 :
  - python2版本下：
    - `~/.virtualenvs/py_flask/lib/python2.7/site-packages/`
  - python3版本下：
    - `~/.virtualenvs/py3_flask/lib/python3.5/site-packages`
- python3版本下安装flask-0.10.1的包 :

```
pip install 包名称

例 : 安装flask-0.10.1的包
pip install flask==0.10.1
```

- 查看虚拟环境中安装的包 :

```
pip freeze
```





# Linux root配置

配置 Linux系统用户自动登陆不需要输入 root 密码

NO.1 删除密码

```
sudo passwd -d root
或
sudo passwd root -d
```



NO.2 修改sshd_config文件

```
cd /etc/ssh/
vim sshd_config   #如果没有，使用touch创建一个

# 在 sshd_config末尾添加：
PermitEmptyPasswords yes
PermitRootLogin yes
# 或使用 echo 命令:
echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
```

配置后重启系统

```
reboot
```



# Linux工具安装

安装 ping

```
apt-get install inetutils-ping
```

安装 ifconfig

```
apt-get install net-tools
```

安装 curl

```
apt-get install curl
```

安 ssh服务

```bash
# 安装 ssh 服务
apt-get install openssh-server
# 创建正常运行时必须的目录
mkdir -p /var/run/sshd
# 启动ssh服务
/usr/sbin/sshd -D &
# 查看 22 端口
netstat -tunlp
# 修改 ssh 安全登录配置, 取消 pam 登录限制
sed -ri 's/session required pam_loginuid.so/#session required pam_loginuid.so/g' /etc/pam.d/sshd
# 在root用户目录下创建目录 .ssh, 并复制需要登录的公钥信息到 authorized_keys 文件中
# (一般为主机用户目录下的 .ssh/id_rsa.pub 文件, 可由 ssh-keygen -t rsa 命令生成)
mkdir root/.ssh
vi /root/.ssh/authorized_keys

# 创建自动启动 ssh 服务的可执行文件 run.sh, 并添加可执行权限
vi /run.sh
chmod +x run.sh
# ----ssh 脚本内容----:
    #!/bin/bsh
    /usr/sbin/sshd -D
```



# IP与域名之间的对应配置

Windows环境是在  `C:\Windows\System32\drivers\etc\hosts`

```
增加地址转换：
10.200.100.190  www.test.com
```

Linux是在 `/ect/hosts` 中配置, 根据发行版本的差异也可能是在 `/etc/hostname` 目录配置



# 域名和DNS服务器详解

 https://truedei.blog.csdn.net/article/details/106037921 