# 指定基础镜像
FROM daocloud.io/nginx

# 复制代码
COPY . /usr/local/nginx/html/


# 指定容器启动时执行的命令
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]

