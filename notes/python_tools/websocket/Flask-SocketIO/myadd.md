# flsk_socketio

- [结合manage.py，在flask项目中使用websocket模块--- flask-socketio](https://www.cnblogs.com/wt11/p/9288605.html)
- [vue-socket.io 和 flask_socketio使用](https://blog.csdn.net/weixin_34260991/article/details/87535753)
- [vuejs & flask with socketio](https://blog.csdn.net/weixin_33953249/article/details/87196976)
- [websocket 与 socket.io](https://www.cnblogs.com/mazg/p/5467960.html)



# Flask-SocketIO简单使用指南

https://blog.csdn.net/feng98ren/article/details/86544506 或 https://juejin.im/post/5bdad42bf265da392a7e2e0e



# Flask + Flask-socketio 实现简单的 WebServer

https://github.com/StartAt24/Python-Flask



# 用法相关

@copy_current_request_context

with app.app_context()

from flask import session

manage_session＝False



启动命令

>gunicorn -b :5000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 run:app



### docker容器化

https://github.com/chendongxtu/auction-ws-web

Dockerfile

```
FROM cr.cheanjiait.com/library/python:3.6

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /auction-ws-web

EXPOSE 5000

COPY requirements.txt /auction-ws-web

RUN set -x \
      && apk add --update --virtual .build-deps \
              musl-dev \
              g++ \
              tzdata \
              git \
              curl \
              openssh-client \
      && apk add libstdc++ \
      && ONVAULT pip install --no-cache-dir -r requirements.txt \
      && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
      && apk del .build-deps \
      && rm -rf /var/cache/apk/*

COPY . /auction-ws-web

ARG GIT_COMMIT

ENV GIT_COMMIT ${GIT_COMMIT}

CMD ["gunicorn", "-b", ":5000", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "wsgi:application"]
```

docker-compose.yaml

```
version: '2'
services:
  db:
    command: --character-set-server=utf8mb4
    image: mysql:5.6
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: dos_dev
      MYSQL_USER: planx
      MYSQL_PASSWORD: planx

  redis:
    image: redis:3.2.1-alpine
    ports:
    - 6379:6379

  web:
    build: .
    volumes:
      - .:/usr/src/app
    ports:
      - "5000:5000"
    depends_on:
      - db
      - redis
    links:
      - db
      - redis
    environment:
      FLASK_ENV: development
      REDIS_URL: redis://redis:6379/0
      SQLALCHEMY_DATABASE_URI: mysql+pymysql://planx:planx@db/dos_dev
```



??

> flask-socketio和gunicorn混用只能开启一个进程
>
> Flask-socketio多workers实现	https://www.jianshu.com/p/3c3e18456ccc