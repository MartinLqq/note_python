# 指定基础镜像
FROM daocloud.io/python:3-onbuild

# 复制代码
COPY . /code
WORKDIR /code

# 安装依赖
RUN pwd
RUN ls -la
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# 提示暴露的端口
EXPOSE 5000

# 指定容器启动时执行的命令
RUN whereis python
CMD ["/usr/local/bin/python", "manage.py"]   # 必须用双引号
