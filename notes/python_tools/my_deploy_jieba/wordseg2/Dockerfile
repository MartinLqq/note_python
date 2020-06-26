FROM dockerhub.datagrand.com/idps/python27_with_ssh_git:1.1
COPY . /code
RUN pip install -i http://mirrors.aliyun.com/pypi/simple \
    --trusted-host mirrors.aliyun.com tornado~=5.1.1 jieba~=0.42.1

WORKDIR /code/src
CMD ["/usr/bin/python2.7", "server.py"]

