

# ==== Apache HTTP 服务器 ====

# 介绍

### Apache 2.4 文档

http://httpd.apache.org/docs/2.4/



### 安装

```bash
# Installing on Ubuntu/Debian

# 查看是否安装
apachectl

# 通过命令安装
sudo apt install apache2

# 查看命令帮助
apachectl -h
```

### 查看配置

```
/etc/apache2         ServerRoot, 服务器配置根目录
├── apache2.conf     主配置文件
├── conf-available
├── conf-enabled
├── envvars
├── magic
├── mods-available
├── mods-enabled
├── ports.conf
├── sites-available
└── sites-enabled


默认配置文件: /usr/local/apache2/conf

静态文件放置目录:  /var/www/html
```



# ==== To Be Continued ====

看 Apache 官方文档:  http://httpd.apache.org/docs/2.4/