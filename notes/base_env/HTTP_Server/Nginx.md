# ==== Nginx ====

# 资源

1. B 站视频教程:  尚硅谷Nginx教程(nginx快速上手)
2. [Nginx中文文档](https://www.nginx.cn/doc/)
3. [W3Scool Nginx 使用文档  (进阶)](https://www.w3cschool.cn/nginxsysc/)



# 介绍

Nginx ("engine x") 是一个高性能的 HTTP 和反向代理服务器,特点是占有内存少，并发能力强。

1. Nginx 作为 web 服务器

   Nginx 可以作为静态页面的 web 服务器，同时还支持 CGI 协议的动态语言，比如 perl、php 等。 但是不支持 java。Java 程序只能通过与 tomcat 配合完成。 Nginx 专为性能优化而开发，性能是其最重要的考量,实现上非常注重效率 ，能经受高负载的考验,有报告表明能支持高达 50,000 个并发连接数。  https://lnmp.org/nginx.html 

2. 正向代理

   Nginx 不仅可以做反向代理，实现负载均衡。还能用作正向代理来进行上网等功能。 
   正向代理：如果把局域网外的 Internet 想象成一个巨大的资源库，则局域网中的客户端要访问 Internet，则需要通过代理服务器来访问，这种代理服务就称为正向代理。 

3. 反向代理

   反向代理，其实客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只需要将请求发送到反向代理服务器， 由反向代理服务器去选择目标服务器获取数据后， 在返回给客户端， 此时反向代理服务器和目标服务器对外就是一个服务器， 暴露的是代理服务器地址，隐藏了真实服务器 IP 地址。 

4. 负载均衡

   随着访问量和数据量的剧增,  单个服务器不能满足需求，我们增加服务器的数量，然后将请求分发到各个服务器上。将负载分发到不同的服务器， 也就是我们所说的负载均衡。

5. 动静分离

   为了加快网站的解析速度， 可以把动态页面和静态页面由不同的服务器来解析， 加快解析速度。降低原来单个服务器的压力。

# web 服务器对比

几种常用 Web 服务器对比：

![img](https://pics3.baidu.com/feed/2fdda3cc7cd98d10dbbf91702e71510b7aec90d8.jpeg?token=95c4261794ef7422a5b01ca0881dcd03&s=35187C33515F45CE4ADD11CA0300D0B1)



# 安装

## on Windows

1. 下载:  http://nginx.org/en/download.html

2. 基本操作:  

   ````bash
   # 启动 nginx 
   $ start nginx
   
   # nginx 命令帮助
   $ nginx -h
   
   # 重启 nginx （注意不会重新读取配置文件）
   $ nginx -s reopen    # s ==> signal
   # 重载  (重载配置, 区别于 reopen 重启)
   $ nginx -s  reload
   
   # 测试配置文件是否正确
   $ nginx -t
   ````

## on Linux

1. 下载

2. 基本操作

   ```bash
   # nginx 命令在 /usr/local/nginx/sbin 目录下
   
   # 启动
   $ ./nginx
   
   # 关闭
   $ ./nginx -s  stop
   
   # 重启 nginx （注意不会重新读取配置文件）
   $ ./nginx -s reopen    # s ==> signal
   # 重载  (重载配置, 区别于 reopen 重启)
   $ ./nginx -s  reload
   ```



# 默认服务目录

Windows:  Nginx 解压目录下的 html 目录下,  如 `nginx-1.17.10\html`

Nginx:  

# 配置

配置文件路径

- Linux:   `/usr/local/nginx/conf/nginx.conf`
- Windows:   Nginx 解压目录下的 conf 目录下,  如 `nginx-1.17.10\conf\`

默认服务目录

- Linux:  `/usr/share/nginx/html`
- Windows:  Nginx 解压目录下的 html 目录下,  如 `nginx-1.17.10\html`



一个简单的 Nginx 配置示例

> Nginx 提供静态文件服务的例子

```nginx
worker_processes    1;

events {
    worker_connections    1024;
}

http {
    include            mime.types;
    default_type       application/octet-stream;
    sendfile           on;
    keepalive_timeout  65;
    
    server {
        listen         80;
        server_name    localhost;
        
        location / {
            # root指定静态文件的根目录, 如果是相对路径, 是相对于 nginx 安装目录
            # 按以下配置, 若访问 uri 为 /mydata, 就去 nginx路径/html/mydata 下面找静态资源.
            # 注意 root 与 alias 配置项的区别, alias 不包含 uri 的内容
            root       html;
            # index指定访问Nginx时的首页
            index      index.html index.htm;
        }
    }
}

```





## 1. 全局块

> 配置服务器整体运行的配置指令

从配置文件开始到 events 块之间的内容，主要会设置一些影响 nginx 服务器整体运行的配置指令，主要包括配置运行 Nginx 服务器的用户（组）、允许生成的 worker process 数，进程 PID 存放路径、日志存放路径和类型以及配置文件的引入等。 

```nginx
worker_processes  1;   处理的并发数

# 这是 Nginx 服务器并发处理服务的关键配置，worker_processes 值越大，可以支持的并发处理量也越多，但是会受到硬件、软件等设备的制约 
```



## 2. events 块

> 影响 Nginx 服务器与用户的网络连接

events 块涉及的指令主要影响 Nginx 服务器与用户的网络连接，常用的设置包括是否开启对多 work process 下的网络连接进行序列化，是否允许同时接收多个网络连接，选取哪种事件驱动模型来处理连接请求，每个 word process 可以同时支持的最大连接数等。 
这部分的配置对 Nginx 的性能影响较大，在实际中应该灵活配置。

```nginx
events {
    worker_connections  1024;   支持的最大连接数为 1024 
}
```



## 3. http 块

> 配置最频繁的部分

这算是 Nginx 服务器配置中最频繁的部分， 代理、 缓存和日志定义等绝大多数功能和第三方模块的配置都在这里。  
需要注意的是：http 块也可以包括 http 全局块、server 块。

```nginx
http {
    include             mime.types;
    default_type        application/octet-stream;
    sendfile            on;
    keepalive_timeout   65;
    
    server {
        listen          80;
        server_name     localhost;
        
        location / {
            root        html;
            index       index.html index.htm;
        }
        
        #error_page  404              /404.html;
        error_page      500 502 503 504  /50x.html;
        location = /50x.html {
            root        html;
        }
    }

}
```



http 块细分

```
1. http 全局块
2. server 块
	全局 server 块
	location 块
```

### http 全局块

http 全局块配置的指令包括文件引入、MIME-TYPE 定义、日志自定义、连接超时时间、单链接请求数上限等。

### server 块

server 块和虚拟主机有密切关系，虚拟主机从用户角度看，和一台独立的硬件主机是完全一样的，该技术的产生是为了
节省互联网服务器硬件成本。 
每个 http 块可以包括多个 server 块，而每个 server 块就相当于一个虚拟主机。 而每个 server 块也分为全局 server 块，以及可以同时包含多个 locaton 块。

#### > 全局 server 块 

  最常见的配置是本虚拟机主机的监听配置和本虚拟主机的名称或 IP 配置。

#### > location 块 

  一个 server 块可以配置多个 location 块。 

 location 块的主要作用是基于 Nginx  服务器接收到的请求字符串（例如 server_name/uri-string），对虚拟主机名称
（也可以是 IP 别名）之外的字符串（例如 前面的 /uri-string）进行匹配，对特定的请求进行处理。地址定向、数据缓
存和应答控制等功能，还有许多第三方模块的配置也在这里进行。 

>  **注意**:  
>
> location 后面的路径的末尾加`/`  与 不加`/`  是不同的,  例如匹配的 uri 为 `/edu`,  如果访问 `/edu/` 且没有对应路由处理 `/edu/`,  则返回 404





# 配置实例

## 部署静态文件服务器

```
worker_processes    1;

events {
    worker_connections    1024;
}

http {
    include            mime.types;
    default_type       application/octet-stream;
    sendfile           on;
    keepalive_timeout  65;

    server {
        listen         80;
        server_name    localhost;
        
        #location / {
        #    root    html;
        #    index   index.html;
        #}
    
        location / {
            root       html/data/;
            autoindex  on;
        }
    }
}
```





## 反向代理1

需求:  配置 nginx 反向代理，浏览器访问 `www.martin.com` 时直接跳转到 `127.0.0.1:8080`

1. 本地测试时先在 hosts 文件中增加一条 `127.0.0.1   www.martin.com`

   ```
   # windows hosts 文件路径
   "C:\Windows\System32\drivers\etc\hosts"
   
   # linux hosts 文件路径
   /etc/hosts
   ```

2. 开启一个 flask 本地开发服务器

3. 配置 nginx

   ```nginx
   worker_processes    1;
   
   events {
       worker_connections    1024;
   }
   
   http {
       include            mime.types;
       default_type       application/octet-stream;
       sendfile           on;
       keepalive_timeout  65;
       
       server {
           listen         80;
           server_name    www.martin.com;    # 也可以直接写 Nginx 所在主机的 IP
           
           location / {
               proxy_pass  http://127.0.0.1:5000;  # 代理地址
               index       index.html index.htm;
           }
       }
   }
   ```

4. 重载 nginx

   ```bash
   $ nginx -s reload
   ```

5. 测试访问 www.martin.com



## 反向代理2

需求：配置 nginx 反向代理，匹配访问的路径,  跳转到不同端口的服务中

```
nginx 监听端口为 9001，
    访问 http://127.0.0.1:9001/edu 直接跳转到 127.0.0.1:8081
    访问 http://127.0.0.1:9001/vod/ 直接跳转到 127.0.0.1:8082
```



1. 参考前面,  配置 hosts

2. 开启两个 flask 本地开发服务器, 两个文件代码分别为

   (1)  run_4_edu.py

   ```python
   import json
   from flask import Flask
   from flask_cors import CORS
   
   app = Flask(__name__)
   cors = CORS(app, resources={r"/*": {"origins": "*"}})
   
   @app.route('/edu')
   def edu_index():
       return "Hello edu"
   
   @app.route('/edu/foo')
   def edu_foo():
       return "Foo!"
   
   if __name__ == '__main__':
       app.run(debug=True, port=8001)
   ```

   (2)  run_4_vod.py

   ```python
   import json
   from flask import Flask
   from flask_cors import CORS
   
   app = Flask(__name__)
   cors = CORS(app, resources={r"/*": {"origins": "*"}})
   
   @app.route('/vod/')
   def vod_index():
       return "Hello vod"
   
   @app.route('/vod/bar')
   def vod_bar():
       return "Bar!"
   
   if __name__ == '__main__':
       app.run(debug=True, port=8002)
   ```

   

3. 配置 nginx

   ```nginx
   worker_processes    1;
   
   events {
       worker_connections    1024;
   }
   
   http {
       include            mime.types;
       default_type       application/octet-stream;
       sendfile           on;
       keepalive_timeout  65;
   
       server {
           listen         9001;
           server_name    www.martin.com;
           
           location ~ /edu {
               proxy_pass  http://127.0.0.1:8001;
               
               # 访问 www.martin.com:9001/edu      ==> 转发到 127.0.0.1:8001/edu
               # 访问 www.martin.com:9001/edu/     ==> 404
               # 访问 www.martin.com:9001/edu/foo  ==> 转发到 127.0.0.1:8001/edu/foo
           }
           location ~ /vod/ {
               proxy_pass  http://127.0.0.1:8002;
               
               # 访问 www.martin.com:9001/vod      ==> 404
               # 访问 www.martin.com:9001/vod/     ==> 转发到 127.0.0.1:8002/vod/
               # 访问 www.martin.com:9001/vod/bar  ==> 转发到 127.0.0.1:8002/vod/bar
           }
       }
   }
   
   ```

4. 测试访问

   ```
   www.martin.com:9001/edu
   www.martin.com:9001/edu/foo
   
   www.martin.com:9001/vod/
   www.martin.com:9001/vod/bar
   ```

   

### > location 指令说明

该指令用于匹配 URL。 
  语法如下： 

```nginx
location [=|~|~*|^~] /uri/ { ... }
```

1. `=` ：用于不含正则表达式的 uri 前，要求请求字符串与 uri 严格匹配，如果匹配成功，就停止继续向下搜索并立即处理该请求。 
2. `~`：用于表示 uri 包含正则表达式，并且区分大小写。 
3. `~*`：用于表示 uri 包含正则表达式，并且不区分大小写。
4. `^~`：用于不含正则表达式的 uri 前，要求 Nginx 服务器找到标识 uri 和请求字符串匹配度最高的 location 后，立即使用此 location 处理请求，而不再使用 location 块中的正则 uri 和请求字符串做匹配。 

注意：

1. 如果 uri 包含正则表达式，则必须要有 `~` 或者 `~*` 标识。 
2. 默认有个 location 对应根 uri,  找 Nginx 服务目录下的 index.html

例子

```nginx
location = / {
  # matches the query / only.
  [ configuration A ]
}

location / {
  # matches any query, since all queries begin with /, but regular
  # expressions and any longer conventional blocks will be matched first.
  [ configuration B ] 
}

location ^~ /images/ {
  # matches any query beginning with /images/ and halts searching,
  # so regular expressions will not be checked.
  [ configuration C ] 
}

location ~* \.(gif|jpg|jpeg)$ {
  # matches any request ending in gif, jpg, or jpeg. However, all
  # requests to the /images/ directory will be handled by Configuration C.   
  [ configuration D ] 
}
```

Example requests:

- / -> configuration A
- /documents/document.html -> configuration B
- /images/1.gif -> configuration C
- /documents/1.jpg -> configuration D

>  注:  以上四个配置例子不论顺序,  效果一致.

### > Nginx 如何匹配路径?

For example, lets say we have the following paths:

```
/
/a
/apple
/banana
```

Now, lets say the server gets the path "/az". nginx would begin search down this list. 

1. First, "/" would match, but "/ is less than "/az" so searching continues. 
2. "/a" also matches, but "/a" is still less than "/az" so we continue again. 
3. "/apple" does not match. 
4. The next string, "/banana", is greater than "/az" so searching stops and the last match, "/a", would be used. 



## 负载均衡

需求:  通过 Nginx 将请求分发到多个提供相同服务的应用服务器之一上

```
worker_processes    1;

events {
    worker_connections    1024;
}

http {
    include            mime.types;
    default_type       application/octet-stream;
    sendfile           on;
    keepalive_timeout  65;

    upstream myserver {
        ip_hash;
        server 127.0.0.1:5001 weight=1;
        server 127.0.0.1:5002 weight=1;
    }

    server {
        listen         80;
        server_name    www.martin.com;

        location ~ / {
            proxy_pass  http://myserver;
            proxy_connect_timeout  10;

            # 访问 www.martin.com/xx/yy/...
            # ==> 转发到 127.0.0.1:5001/xx/yy/... 或 127.0.0.1:5002/xx/yy/...
        }
    }
}
```



### > Nginx 分配策略

在 linux 下有 Nginx、LVS、Haproxy 等等服务可以提供负载均衡服务，Nginx 提供了几种分配方式(策略):

```
1. 轮询（默认）
2. weight
3. ip_hash
4. fair（第三方）
```

1. 轮询（默认） 

   每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器 down 掉，能自动剔除。

2. weight

   weight 代表权重,  默认为 1,  权重越高被分配的客户端越多

   指定轮询几率，weight 和访问比率成正比，用于后端服务器性能不均的情况。 例如： 

   ```
   upstream server_pool{    
       server 192.168.5.21 weight=10;     
       server 192.168.5.22 weight=10;     
   }
   ```

3. ip_hash 
   每个请求按访问 ip 的 hash 结果分配， 这样每个访客固定访问一个后端服务器， 可以解决 session 的问题。  例如：

   ```
   upstream server_pool{    
       ip_hash;     
       server 192.168.5.21:80;
       server 192.168.5.22:80;
   }
   ```

4. fair（第三方）
   按后端服务器的响应时间来分配请求，响应时间短的优先分配。

   ```
   upstream server_pool {    
       server 192.168.5.21:80;
       server 192.168.5.22:80;
       fair;
   }
   ```

   

## 动静分离

Nginx 动静分离简单来说就是把动态跟静态请求分开， 不能理解成只是单纯的把动态页面和静态页面物理分离。严格意义上说应该是动态请求跟静态请求分开，例如使用 Nginx 处理静态页面，Tomcat 处理动态页面。

动静分离从目前实现角度来讲大致分为两种:

1. 方法1:  动态跟静态文件混合在一起发布，通过 nginx 分开。 
2. 方法2:  纯粹把静态文件独立成单独的域名， 放在独立的服务器上， 也是目前主流推崇的方案；

通过 location 指定不同的后缀名实现不同的请求转发。

通过 expires 参数设置，可以使浏览器缓存过期时间，减少与服务器之前的请求和流量。

> 具体 Expires 定义： 
>
> 给一个资源设定一个过期时间， 也就是说无需去服务端验证， 直接通过浏览器自身确认是否过期即可，所以不会产生额外的流量。此种方法非常适合不经常变动的资源。（如果经常更新的文件，不建议使用 Expires 来缓存），设置 3d，表示在这 3 天之内访问这个 URL，发送一个请求，比对服务器该文件最后更新时间没有变化，则不会从服务器抓取，返回状态码 304，如果有修改，则直接从服务器重新下载，返回状态码 200。 





### > 部署 vue-cli 项目 (a)

> 下面的例子对应上面动静分离的 **方法1**,  这种方法用的更少
>
> 思考:  怎么部署多个前台服务?

前端:  vue-cli,  由 Nginx 提供静态文件服务

后端:  flask,  本地开发服务器



注意:

> 查看 vue-router 文档中关于 HTML5 History 模式的部分

1. Nginx 部署 vue-cli 项目时,  vue-router 有两个 URL 模式:   history模式 / hash 模式

2. history模式需要后台 (Nginx反向代理)  配置支持。因为我们的应用是个单页客户端应用，如果后台没有正确的配置，当用户在浏览器直接访问 `http://oursite.com/user/id` 就会返回 404，这就不好看了。

   所以要在服务端增加一个覆盖所有情况的候选资源：如果 URL 匹配不到任何静态资源，则应该返回同一个 `index.html` 页面，这个页面就是你 app 依赖的页面。

   ```nginx
   location / {
     try_files $uri $uri/ /index.html;
   }
   ```

3. 使用 history 模式 + Nginx 配置后，你的服务器就不再返回 404 错误页面，因为对于所有路径都会返回 `index.html` 文件。为了避免这种情况，你应该在 Vue 应用里面覆盖所有的路由情况，然后在给出一个 404 页面。

4. 如果用 `vue-router` 默认的 hash 模式,  就不需要 Nginx 做上面的配置



Nginx 配置例子

> 1. Nginx 作为静态文件服务器,  提供前端访问支持
>
> 2. 同时,  Nginx 将前端发出的 uri 以 /api 开头的异步请求,  转发给后台

```nginx
worker_processes    1;

events {
    worker_connections    1024;
}

http {
    include            mime.types;
    default_type       application/octet-stream;
    sendfile           on;
    keepalive_timeout  65;

    server {
        listen         80;
        server_name    localhost;
        
        location / {
            root    html;
            try_files $uri $uri/ /index.html;   # localhost:80 的请求交给 vue-cli 搭建的前台
        }
    
        location ~ /api {
            proxy_pass  http://localhost:5000;  # localhost:5000 的请求交给 flask 搭建的后台
        }
    }
}
```

前端 axios 封装示例

> 注意 baseURL 的配置,  uri 为 /api/ 的请求会被 Nginx 转发到 flask 服务器

```javascript
/*
    封装 axios 请求
*/

import axios from 'axios'

export function request (config) {
    const instance = axios.create({
        baseURL: 'http://localhost:5000/api/',
        timeout: 5000,
    })

    // 添加请求拦截器
    instance.interceptors.request.use(config => {
        /*
             a. 修改请求头
             b. 显示正在请求的提示界面(动画) (show)
             c. 根据url进行权限检查, 检查不通过时跳转页面
         */
        return config
    }, err => {
        alert(err)
    });
    // 添加响应拦截器
    instance.interceptors.response.use(res => {
        return res.data
    }, err => {
        alert(err)
    })

    return instance(config)
}
```





### > 部署 vue-cli 项目 (b)

对应动静分离方法2:  纯粹把静态文件独立成单独的域名， 放在独立的服务器上， 也是目前主流推崇的方案

以 Vue CLI3 + Flask + Nginx 为例:

1. host 分配

```
UI			localhost
Nginx		www.martin.com
Backend		api.martin.com
```

2. UI axios 实例部分配置

   ```javascript
       const instance = axios.create({
           baseURL: 'http://www.martin.com/api/',
           timeout: 5000,
       })
   ```

3. 开启 Vue CLI 本地开发服务, 服务地址:  localhost:8080

4. 开启 Flask 本地开发服务,  服务地址:  api.martin.com  (在 hosts 文件中先配上此域名)

5. Nginx 配置  (nginx.conf)

   ```nginx
   worker_processes    1;
   
   events {
       worker_connections    1024;
   }
   
   http {
       include            mime.types;
       default_type       application/octet-stream;
       sendfile           on;
       keepalive_timeout  65;
   
       server {
           listen         80;
           server_name    www.martin.com;
           location / {
               # www.martin.com/开头, 且非 www.martin.com/api/ 开头的请求, 转发给前台
               proxy_pass http://localhost:8080;
           }
           location ~ /api/ {
               # www.martin.com/api/ 开头的请求转发给后台
               proxy_pass http://api.martin.com:5000;
           }
       }
   }
   ```

   



# Nginx 健康检查

 **服务治理**的一个重要任务是感知服务节点变更，完成`服务自动注册`及`异常节点的自动摘除`。这就需要服务治理平台能够：`及时`、`准确`的感知service节点的健康状况。 

###  方案概述

Nginx 提供了三种HTTP服务健康检查方案供用户选择：

1. **TCP层默认检查方案**：

   定时与后端服务建立一条`tcp连接`，链接建立成功则认为服务节点是健康的。

2. **HTTP层默认检查方案**：

   TCP层检查有一定的局限性：

3. 1. 很多**HTTP服务是带状态**的，端口处于listen状态并不能代表服务已经完成预热；
   2. **不能真实反映**服务内部**处理逻辑**是否产生拥堵。
   3. 这时可以选择`http层`健康检查，会向服务发送一个http请求`GET / HTTP/1.0\r\n\r\n`，返回状态是2xx或3xx时认为后端服务正常。

4. 自定义方案：

   可根据下文描述自定义检查方案。

###  配置参数详解

 一个常用的健康检查配置如下： 

```nginx
check fall=3 interval=3000 rise=2 timeout=2000 type=http;
check_http_expect_alive http_2xx http_3xx ;
check_http_send "GET /checkAlive HTTP/1.0\r\n\r\n" ;
```

 下面针对每个配置参数，进行详细介绍。 

##### check

check 字段参数如下：

```
Syntax: check interval=milliseconds [fall=count] [rise=count] [timeout=milliseconds] [default_down=true|false] [type=tcp|http|ssl_hello|mysql|ajp] [port=check_port]

Default: 如果没有配置参数，默认值是：
	interval=30000 fall=5 rise=2 timeout=1000 default_down=true type=tcp
```

 `check` 字段各个参数含义如下： 

- `interval`：  向后端发送的健康检查包的间隔。

- `fall(fall_count)`: 如果连续失败次数达到 fall_count，服务器就被认为是 down。

- `rise(rise_count)`: 如果连续成功次数达到 rise_count，服务器就被认为是 up。

- `timeout`: 后端健康请求的超时时间。

- `default_down`: 设定初始时服务器的状态，如果是 true，就说明默认是 down 的，如果是 false，就是 up 的。默认值是 true，也就是一开始服务器认为是不可用，要等健康检查包达到一定成功次数以后才会被认为是健康的。

- `type`：健康检查包的类型，现在支持以下多种类型   

- - `tcp`：简单的 tcp 连接，如果连接成功，就说明后端正常。

  - `ssl_hello`：发送一个初始的 SSL hello 包并接受服务器的 SSL hello 包。

  - `http`：发送HTTP请求，通过后端的回复包的状态来判断后端是否存活。

  - `mysql`: 向 mysql 服务器连接，通过接收服务器的 greeting 包来判断后端是否存活。

  - `ajp`：向后端发送 AJP 协议的 Cping 包，通过接收 Cpong 包来判断后端是否存活。

  - `port`: 指定后端服务器的检查端口。

    可以指定不同于真实服务的后端服务器的端口，比如后端提供的是443端口的应用，你可以去检查80端口的状态来判断后端健康状况。

    默认是0，表示跟后端server提供真实服务的端口一样。

##### check_http_expect_alive

`check_http_expect_alive` 指定主动健康检查时HTTP回复的成功状态：

```
Syntax: check_http_expect_alive [ http_2xx | http_3xx | http_4xx | http_5xx ]

Default: http_2xx | http_3xx
```

##### check_http_send

`check_http_send` 配置http健康检查包发送的请求内容

为了减少传输数据量，推荐采用 ”HEAD” 方法。当采用长连接进行健康检查时，需在该指令中添加 keep-alive 请求头，如：”HEAD / HTTP/1.1\r\nConnection: keep-alive\r\n\r\n”。同时，在采用 ”GET” 方法的情况下，请求 uri 的 size 不宜过大，确保可以在 1 个 interval 内传输完成，否则会被健康检查模块视为后端服务器或网络异常。

```
Syntax: check_http_send http_packet
Default: "GET / HTTP/1.0\r\n\r\n"
```

###  完整示例

```nginx
http {
    upstream cluster1 {
        # simple round-robin
        server 192.168.0.1:80;
        server 192.168.0.2:80;
        check interval=3000 rise=2 fall=5 timeout=1000 type=http;
        check_http_send "HEAD / HTTP/1.0\r\n\r\n";
        check_http_expect_alive http_2xx http_3xx;
    }
    upstream cluster2 {
        # simple round-robin
        server 192.168.0.3:80;
        server 192.168.0.4:80;
        check interval=3000 rise=2 fall=5 timeout=1000 type=http;
        check_keepalive_requests 100;
        check_http_send "HEAD / HTTP/1.1\r\nConnection: keep-alive\r\n\r\n";
        check_http_expect_alive http_2xx http_3xx;
    }
    server {
        listen 80;
        location /1 {
            proxy_pass http://cluster1;
        }
        location /2 {
            proxy_pass http://cluster2;
        }
        location /status {
            check_status;
            access_log   off;
            allow SOME.IP.ADD.RESS;
            deny all;
        }
    }
}
```



# ==== To Be Continued ====



# 高可用集群

应对应用服务器可能的宕机:  配置 nginx 反向代理，可以匹配访问的路径,  跳转到不同端口的服务中

应对 Nginx 可能的宕机:  Nginx 主从 / 双主

配置高可用集群的前提

```
（1）需要两台 nginx 服务器 
（2）在两台服务器安装 keepalived
（3）需要虚拟 ip
```

1. 准备两台 Linux 虚拟机,  在虚拟机上都安装 Nginx  (推荐 Docker 容器 + Nginx 镜像)

2. 安装 keepalived

   ```bash
   $ yum install -y keepalived
   ```

3. 查看 keepalived 配置文件: /etc/keepalived/keepalived.conf



## Keepalived+Nginx（主从模式）

1. 修改 keepalived 配置文件: `/etc/keepalived/keepalived.conf`

   ```
   global_defs { 
      notification_email { 
        acassen@firewall.loc 
        failover@firewall.loc 
        sysadmin@firewall.loc 
      } 
      notification_email_from Alexandre.Cassen@firewall.loc 
      smtp_server 192.168.17.129 
      smtp_connect_timeout 30 
      router_id LVS_DEVEL 
   } 
     
   vrrp_script chk_http_port { 
      script "/usr/local/src/nginx_check.sh" 
      interval 2              # 检测脚本执行的间隔
      weight 2 
   } 
   
   vrrp_instance VI_1 { 
       state BACKUP           # 备份服务器上将 MASTER 改为 BACKUP   
       interface ens33        # 网卡 
       virtual_router_id 51   # 主、备机的 virtual_router_id 必须相同 
       priority 90            # 主、备机取不同的优先级，主机值较大，备份机值较小 
       advert_int 1 
       authentication { 
           auth_type PASS 
           auth_pass 1111 
       } 
       virtual_ipaddress { 
           192.168.17.50      # VRRP H 虚拟地址 
       } 
   } 
   ```

   

2. 在 `/usr/local/src` 中添加检测脚本

   ```shell
   #!/bin/bash 
   A=`ps -C nginx –no-header |wc -lìf [ $A -eq 0 ];then 
       /usr/local/nginx/sbin/nginx 
       sleep 2 
       if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then 
           killall keepalived 
       fi 
   fi
   ```



3. 启动两台服务器上 nginx 和 keepalived

   ```bash
   # 启动 nginx
   $ ./nginx 
   # 启动 keepalived
   $ systemctl start keepalived.service
   ```



4. 测试: 

   ```
   (1) 在浏览器地址栏输入 虚拟 ip 地址 192.168.17.50
   (2) 把主服务器（192.168.17.129）nginx 和 keepalived 停止，再输入 192.168.17.50
   ```





## Keepalived+Nginx（双主模式）





# Nginx 原理与优化参数配置

1、mater 和 worker

nginx 的两种工作进程,  查看:

```
ps -ef | grep nginx
```

2、worker 如何进行工作的

3、一个 master 和多个 woker 有好处 

（1）可以使用 nginx –s reload 热部署，利用 nginx 进行热部署操作 

（2）每个 woker 是独立的进程，如果有其中的一个 woker 出现问题，其他 woker 独立的，继续进行争抢，实现请求过程，不会造成服务中断 

4、设置多少个 woker 合适 

worker 数和服务器的 cpu 数相等是最为适宜的 

5、连接数 worker_connection 

第一个：发送请求，占用了 woker 的几个连接数？    答案：2 或者 4 个 

第二个：nginx 有一个 master，有四个 woker，每个 woker 支持最大的连接数 1024，支持的最大并发数是多少？ 

- 普通的静态访问最大并发数是： worker_connections * worker_processes /2， 
- 而如果是 HTTP 作 为反向代理来说，最大并发数量应该是 worker_connections * worker_processes/4。 

# Docker + Nginx

windows 上测试 docker + nginx

1. 按照    安装好 docker-machine

2. 拉取 nginx 镜像并启动容器,  启动时挂载主机的 `~/workspace/nginx-test/html/` 目录到容器内的 `/usr/share/nginx/html`  目录   (方便将静态文件放入容器内),   挂载 `~/workspace/nginx-test/nginx.conf` 文件到 `/etc/nginx/nginx.conf` 文件  (方便修改容器内 Nginx 配置)

   ```
   docker run \
       --name nginx-server \
       -p 80:80 \
       -v ~/workspace/nginx-test/html/:/usr/share/nginx/html:ro \
       -v ~/workspace/nginx-test/conf/:/etc/nginx/conf.d:ro \
       -d \
       nginx
   ```

> 如果需要进入容器:  `docker exec -it nginx-server bash`