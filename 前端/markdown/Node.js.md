# Node.js

# 资源

- 菜鸟教程:   https://www.runoob.com/nodejs/nodejs-tutorial.html 
- 官网文档:   http://nodejs.cn/api/
- Express 4.x API 中文文档:   https://www.runoob.com/w3cnote/express-4-x-api.html 

# 介绍

- Node.js 是运行在服务端的 JavaScript 

- Node.js是一个事件驱动I/O服务端JavaScript环境，基于Google的V8引擎，V8引擎执行Javascript的速度非常快，性能非常好。



运行一个 javascript 文件

```bash
$ node test.js

# test.js 的内容:
# console.log('Hello node.js')
```

也可以进入一个 node 环境,  实时运行 javascript 代码

> 交互模式

```bash
$ node

> console.log(123)
```

### 安装

- Windows 上安装 Node.js

  - Windows 安装包(.msi)
  - Windows 二进制文件 (.exe)安装

- Linux 上安装 Node.js

  - Ubuntu apt-get 命令安装

    ```bash
    sudo apt-get install nodejs
    sudo apt-get install npm
    ```
  
  - CentOS
  
    ```bash
    yum install nodejs
    ```
  
  - 其他安装方式



### 创建一个 server

 Node.js 应用是由哪几部分组成的： 

1. **引入 required 模块：**我们可以使用 **require** 指令来载入 Node.js 模块。
2. **创建服务器：**服务器可以监听客户端的请求，类似于 Apache 、Nginx 等 HTTP 服务器。
3. **接收请求与响应请求** 服务器很容易创建，客户端可以使用浏览器或终端发送 HTTP 请求，服务器接收请求后返回响应数据。

```javascript
// 引入 required 模块
var http = require("http");

// 创建服务器
http.createServer(function (request, response) {
    // 发送 HTTP 头部 
    // HTTP 状态值: 200 : OK
    response.writeHead(200, {'Content-Type': 'text/plain'});

    // 发送响应数据 "Hello World"
    response.end('Hello World\n');
}).listen(8888);

// 终端打印如下信息
console.log('Server running at http://127.0.0.1:8888/');
```

运行服务

```bash
$ node server.js
# Server running at http://127.0.0.1:8888/
```



# NPM

### npm 使用介绍

NPM是随同NodeJS一起安装的包管理工具，能解决NodeJS代码部署上的很多问题，常见的使用场景有以下几种：

- 允许用户从NPM服务器下载别人编写的第三方包到本地使用。
- 允许用户从NPM服务器下载并安装别人编写的命令行程序到本地使用。
- 允许用户将自己编写的包或命令行程序上传到NPM服务器供别人使用。

npm 一些命令

```bash
npm -v
sudo npm install npm -g  # 升级
npm install -g cnpm --registry=https://registry.npm.taobao.org  # 使用淘宝镜像

npm uninstall [name]
npm update [name]
npm search [name]

# 使用 npm help <command> 可查看某条命令的详细帮助
npm help install
```

### npm 安装模块

```bash
# 安装常用的 Node.js web框架模块 express:
$ npm install express
# 或:  cnpm install express
```

全局安装与本地安装

```bash
npm install express          # 本地安装
npm install express -g       # 全局安装
```

1. 本地安装
   - 安装位置:   ./node_modules
   - 导入方式:   require()

2. 全局安装
   - 安装位置:   /usr/local 下或者 node 的安装目录下
   - 导入方式:    可以直接在命令行里使用,  无须导入

 查看所有全局安装的模块

```bash
npm list -g
# 查看某个全局模块的版本号
npm list express -g

npm ls -g
```





### package.json

 package.json 位于模块的目录下，用于定义包的属性 

Package.json 属性说明

- name - 包名。
- version - 包的版本号。
- description - 包的描述。
- homepage - 包的官网 url 。
- author - 包的作者姓名。
- contributors - 包的其他贡献者姓名。
- dependencies - 依赖包列表。如果依赖包没有安装，npm 会自动将依赖包安装在 node_module 目录下。
- repository - 包代码存放的地方的类型，可以是 git 或 svn，git 可在 Github 上。
- main - main 字段指定了程序的主入口文件，require('moduleName') 就会加载这个文件。这个字段的默认值是模块根目录下面的 index.js。
- keywords - 关键字

### 创建模块

创建模块，package.json 文件是必不可少的。我们可以使用 NPM 生成 package.json 文件，生成的文件包含了基本的结果。 

```bash
npm init
```

 在 npm 资源库中注册用户 

```bash
npm adduser
```

 发布模块 

```bash
npm publish
```





# REPL  交互式解释器

Read Eval Print Loop 

Node 自带了交互式解释器,   类似 Window 系统的终端或 Unix/Linux shell，我们可以在终端中输入命令，并接收系统的响应.   可执行以下任务:

- 读取 - 读取用户输入，解析输入了Javascript 数据结构并存储在内存中。
- 执行 - 执行输入的数据结构
- 打印 - 输出结果
- 循环 - 循环操作以上步骤直到用户两次按下 ctrl-c 按钮退出。

一些基础用法

1. 简单的表达式运算
2. 变量定义和使用
3. 多行表达式
4.  使用下划线 (_) 获取上一个表达式的返回值

REPL 命令

- ctrl + c - 退出当前终端。
- ctrl + c 按下两次 - 退出 Node REPL。
- ctrl + d - 退出 Node REPL.
- 向上/向下 键 - 查看输入的历史命令
- tab 键 - 列出当前命令
- .help - 列出使用命令
- .break - 退出多行表达式
- .clear - 退出多行表达式
- .save \*filename\* - 保存当前的 Node REPL 会话到指定文件
- .load \*filename\* - 载入当前 Node REPL 会话的文件内容。





# 回调函数

 Node.js 异步编程的直接体现就是回调。  大大提高了 Node.js 的性能，可以处理大量的并发请求 

回调函数一般作为函数的最后一个参数出现：

```javascript
function foo1(name, age, callback) { }
function foo2(value, callback1, callback2) { }
```

一个阻塞代码实例

```javascript
var fs = require("fs");  // fs --> 文件操作模块

var data = fs.readFileSync('input.txt');

console.log(data.toString());
console.log("程序执行结束!");
```

一个非阻塞代码实例

```javascript
var fs = require("fs");

fs.readFile('input.txt', function (err, data) {
    if (err) return console.error(err);
    console.log(data.toString());
});

console.log("程序执行结束!");
```





# 事件循环

Node.js 是单进程单线程应用程序，但是因为 V8 引擎提供的异步执行回调接口，通过这些接口可以处理大量的并发，所以性能非常高。

Node.js 几乎每一个 API 都是支持回调函数的。Node.js 基本上所有的事件机制都是用设计模式中观察者模式实现。

Node.js 单线程类似进入一个while(true)的事件循环，直到没有事件观察者退出，每个异步事件都生成一个事件观察者，如果有事件发生就调用该回调函数.

### 事件驱动程序

Node.js 使用事件驱动模型，当web server接收到请求，就把它关闭然后进行处理，然后去服务下一个web请求。

当这个请求完成，它被放回处理队列，当到达队列开头，这个结果被返回给用户。

在事件驱动模型中，会生成一个主循环来监听事件，当检测到事件时触发回调函数。 

<img src="https://www.runoob.com/wp-content/uploads/2015/09/event_loop.jpg" alt="img" style="zoom:80%;" />

### 内置事件

Node.js 有多个内置的事件，我们可以通过引入 events 模块，并通过实例化 EventEmitter 类来绑定和监听事件 

```javascript
// 引入 events 模块
const events = require('events');

// 创建 eventEmitter 对象
const eventEmitter = new events.EventEmitter();

// 绑定事件及事件的处理程序
eventEmitter.on('myEvent', (name, age) => {
	console.log('Hello ', name, age)
})

console.log('事件触发之前.')

// 触发事件, 以及事件传参
eventEmitter.emit('myEvent', 'Martin', 26)

```





# EventEmitter 类

Node.js 所有的异步 I/O 操作在完成时都会发送一个事件到事件队列。

Node.js 里面的许多对象都会分发事件：一个 net.Server 对象会在每次有新连接时触发一个事件， 一个 fs.readStream 对象会在文件被打开的时候触发一个事件。 所有这些产生事件的对象都是 events.EventEmitter 的实例。

events 模块只提供了一个对象： events.EventEmitter。EventEmitter 的核心就是事件触发与事件监听器功能的封装。 



event.js

```javascript
// event.js 文件
const EventEmitter = require('events').EventEmitter; 
const event = new EventEmitter(); 
event.on('some_event', function() { 
    console.log('some_event 事件触发'); 
}); 
setTimeout(function() { 
    event.emit('some_event'); 
}, 1000); 
```

运行

```bash
node event.js
```



### 实例方法

-  addListener(event, listener)     为指定事件添加一个监听器到监听器数组的尾部。 
-  on(event, listener)      为指定事件注册一个监听器，接受一个字符串 event 和一个回调函数。 
-  once(event, listener)      为指定事件注册一个单次监听器，即 监听器最多只会触发一次，触发后立刻解除该监听器。 
-  removeListener(event, listener)      移除指定事件的某个监听器，监听器必须是该事件已经注册过的监听器。 
-  removeAllListeners([event])      移除所有事件的所有监听器， 如果指定事件，则移除指定事件的所有监听器。 
-  setMaxListeners(n)    默认情况下， EventEmitters 如果你添加的监听器超过 10 个就会输出警告信息。 setMaxListeners 函数用于提高监听器的默认限制的数量。
-  listeners(event)      返回指定事件的监听器数组。 
-  emit(event, [arg1], [arg2], [...])      按监听器的顺序执行执行每个监听器，如果事件有注册监听返回 true，否则返回 false。 

### 类方法

-  listenerCount(emitter, event)      返回指定事件的监听器数量。 



### 事件

-  newListener      该事件在添加新监听器时被触发。 

-  removeListener      从指定监听器数组中删除一个监听器。 

- error 事件     一个特殊的事件，它包含了错误的语义 

  ```javascript
  var events = require('events'); 
  var emitter = new events.EventEmitter(); 
  emitter.emit('error'); 
  ```



### 继承 EventEmitter

大多数时候我们不会直接使用 EventEmitter，而是在对象中继承它。包括 fs、net、 http 在内的，只要是支持事件响应的核心模块都是 EventEmitter 的子类。

为什么要这样做呢？原因有两点：

1. 首先，具有某个实体功能的对象实现事件符合语义， 事件的监听和发生应该是一个对象的方法。

2. 其次 JavaScript 的对象机制是基于原型的，支持 部分多重继承，继承 EventEmitter 不会打乱对象原有的继承关系。



# Buffer  缓冲区

JavaScript 语言自身只有字符串数据类型，没有二进制数据类型。

但在处理像TCP流或文件流时，必须使用到二进制数据。因此在 Node.js中，定义了一个 Buffer 类，该类用来创建一个专门存放二进制数据的缓存区。



### Buffer 与字符编码

Buffer 实例一般用于表示编码字符的序列，比如 UTF-8 、 UCS2 、 Base64 、或十六进制编码的数据。 通过使用显式的字符编码，就可以在 Buffer 实例与普通的 JavaScript 字符串之间进行相互转换。

```javascript
const buf = Buffer.from('runoob', 'ascii');

// 输出 72756e6f6f62
console.log(buf.toString('hex'));

// 输出 cnVub29i
console.log(buf.toString('base64'));
```

Node.js 目前支持的字符编码包括：

- ascii - 仅支持 7 位 ASCII 数据。如果设置去掉高位的话，这种编码是非常快的。
- utf8 - 多字节编码的 Unicode 字符。许多网页和其他文档格式都使用 UTF-8 。
- utf16le - 2 或 4 个字节，小字节序编码的 Unicode 字符。支持代理对（U+10000 至 U+10FFFF）。
- ucs2 - utf16le 的别名。
- base64 - Base64 编码。
- latin1 - 一种把 Buffer 编码成一字节编码的字符串的方式。
- binary - latin1 的别名。
- hex - 将每个字节编码为两个十六进制字符。

### 创建 Buffer 类的方式

Buffer 提供了以下 API 来创建 Buffer 类：

- Buffer.alloc(size[, fill[, encoding]])： 返回一个指定大小的 Buffer 实例，如果没有设置 fill，则默认填满 0
- Buffer.allocUnsafe(size)： 返回一个指定大小的 Buffer 实例，但是它不会被初始化，所以它可能包含敏感的数据
- Buffer.allocUnsafeSlow(size)
- Buffer.from(array)： 返回一个被 array 的值初始化的新的 Buffer 实例（传入的 array 的元素只能是数字，不然就会自动被 0 覆盖）
- Buffer.from(arrayBuffer[, byteOffset[, length]])： 返回一个新建的与给定的 ArrayBuffer 共享同一内存的 Buffer。
- Buffer.from(buffer)： 复制传入的 Buffer 实例的数据，并返回一个新的 Buffer 实例
- Buffer.from(string[, encoding])： 返回一个被 string 的值初始化的新的 Buffer 实例

### 缓冲区操作

```javascript
// 写
buf.write(string[, offset[, length]][, encoding])
// 读
buf.toString([encoding[, start[, end]]])
// 将 Buffer 转换为 JSON 对象
buf.toJSON()
// 当字符串化一个 Buffer 实例时，JSON.stringify() 会隐式地调用该 toJSON()。

// 合并缓冲区
Buffer.concat(list[, totalLength])

// 缓冲区比较
buf.compare(otherBuffer);
buf.equals(otherBuffer)

// 拷贝
buf.copy(targetBuffer[, targetStart[, sourceStart[, sourceEnd]]])
// 裁剪
buf.slice([start[, end]])

// 缓冲区长度
buf.length

// 填充
buf.fill(value[, offset][, end])
```

Buffer 其他常用的方法 :  略





# Stream  流

Stream 是一个抽象接口，Node 中有很多对象实现了这个接口。例如，对 http 服务器发起请求的 request 对象就是一个 Stream，还有 stdout（标准输出）。

4 种流类型：

1. Readable - 可读操作。
2. Writable - 可写操作。
3. Duplex - 可读可写操作.
4. Transform - 操作被写入数据，然后读出结果。

所有的 Stream 对象都是 EventEmitter 的实例。常用的事件有：

- data - 当有数据可读时触发。
- end - 没有更多的数据可读时触发。
- error - 在接收和写入过程中发生错误时触发。
- finish - 所有数据已被写入到底层系统时触发。

 常用的流操作

1. 读取流
2. 写入流
3. 管道流
4. 链式流

### 读取流

```javascript
var fs = require("fs");
var data = '';

// 创建可读流
var readerStream = fs.createReadStream('input.txt');

readerStream.setEncoding('UTF8');

// 处理流事件 --> data, end, and error
readerStream.on('data', function(chunk) {
   data += chunk;
   console.log("chunk----->", chunk, '<------')
});

readerStream.on('end',function(){
   console.log(data);
});

readerStream.on('error', function(err){
   console.log("出错了: ", err.stack);
});

console.log("程序执行完毕");
```



### 写入流

```javascript
var fs = require("fs");
var data = '菜鸟教程官网地址：www.runoob.com\n';

// 创建一个可以写入的流，写入到文件 output.txt 中
var writerStream = fs.createWriteStream('output.txt');

// 使用 utf8 编码写入数据 (覆盖式写入)
writerStream.write(data, 'UTF8');

// 标记文件末尾
writerStream.end();

// 处理流事件 --> data, end, and error
writerStream.on('finish', function() {
    console.log("写入完成。");
});

writerStream.on('error', function(err){
   console.log(err.stack);
});

console.log("程序执行完毕");
```



### 管道流

 管道提供了一个输出流到输入流的机制。通常我们用于从一个流中获取数据并将数据传递到另外一个流中。 

```javascript
var fs = require("fs");

// 创建一个可读流
var readerStream = fs.createReadStream('input.txt');

// 创建一个可写流
var writerStream = fs.createWriteStream('output.txt');

// 管道读写操作
// 读取 input.txt 文件内容，并将内容写入到 output.txt 文件中
readerStream.pipe(writerStream);

console.log("程序执行完毕");
```



### 链式流

链式是通过连接输出流到另外一个流并创建多个流操作链的机制。链式流一般用于管道操作。

下面用管道和链式来 压缩和解压文件

```javascript
var fs = require("fs");
var zlib = require('zlib');

// 压缩 input.txt 文件为 input.txt.gz
fs.createReadStream('input.txt')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('input.txt.gz'));
  
console.log("文件压缩完成。");
```





# 模块系统

 一个 Node.js 文件就是一个模块，这个文件可能是JavaScript 代码、JSON 或者编译过的C/C++ 扩展。 

### 模块导出方式1

创建模块  hello.js

```javascript
exports.world = function() {
  console.log('Hello World');
}
```

导入模块 hello.js

```javascript
// main.js
var hello = require('./hello');
hello.world();
```



### 模块导出方式2

 **把一个对象封装到模块中**

```javascript
module.exports = function() {
  // ...
}

//hello.js 
function Hello() { 
    var name; 
    this.setName = function(thyName) { 
        name = thyName; 
    }; 
    this.sayHello = function() { 
        console.log('Hello ' + name); 
    }; 
}; 
module.exports = Hello;


//main.js 
var Hello = require('./hello'); 
hello = new Hello(); 
hello.setName('BYVoid'); 
hello.sayHello(); 
```

模块接口的唯一变化是使用 module.exports = Hello 代替了exports.world = function(){}。 在外部引用该模块时，其接口对象就是要输出的 Hello 对象本身，而不是原先的 exports。 

**exports 和 module.exports 的使用**

如果要对外暴露属性或方法，就用 **exports** 就行，要暴露对象(类似class，包含了很多属性和方法)，就用 **module.exports**。





###  require 查找策略

Node.js 中存在 4 类模块（原生模块和3种文件模块），尽管 require 方法极其简单，但是内部的加载却是十分复杂的，其加载优先级也各自不同。

1. 从文件模块缓存中加载
2. 从原生模块加载
3. 从文件加载

![img](https://www.runoob.com/wp-content/uploads/2014/03/nodejs-require.jpg)



流程举例

在路径 Y 下执行 require(X) 语句执行顺序：

```
1. 如果 X 是内置模块
   a. 返回内置模块
   b. 停止执行
2. 如果 X 以 '/' 开头
   a. 设置 Y 为文件根路径
3. 如果 X 以 './' 或 '/' or '../' 开头
   a. LOAD_AS_FILE(Y + X)
   b. LOAD_AS_DIRECTORY(Y + X)
4. LOAD_NODE_MODULES(X, dirname(Y))
5. 抛出异常 "not found"

LOAD_AS_FILE(X)
1. 如果 X 是一个文件, 将 X 作为 JavaScript 文本载入并停止执行。
2. 如果 X.js 是一个文件, 将 X.js 作为 JavaScript 文本载入并停止执行。
3. 如果 X.json 是一个文件, 解析 X.json 为 JavaScript 对象并停止执行。
4. 如果 X.node 是一个文件, 将 X.node 作为二进制插件载入并停止执行。

LOAD_INDEX(X)
1. 如果 X/index.js 是一个文件,  将 X/index.js 作为 JavaScript 文本载入并停止执行。
2. 如果 X/index.json 是一个文件, 解析 X/index.json 为 JavaScript 对象并停止执行。
3. 如果 X/index.node 是一个文件,  将 X/index.node 作为二进制插件载入并停止执行。

LOAD_AS_DIRECTORY(X)
1. 如果 X/package.json 是一个文件,
   a. 解析 X/package.json, 并查找 "main" 字段。
   b. let M = X + (json main 字段)
   c. LOAD_AS_FILE(M)
   d. LOAD_INDEX(M)
2. LOAD_INDEX(X)

LOAD_NODE_MODULES(X, START)
1. let DIRS=NODE_MODULES_PATHS(START)
2. for each DIR in DIRS:
   a. LOAD_AS_FILE(DIR/X)
   b. LOAD_AS_DIRECTORY(DIR/X)

NODE_MODULES_PATHS(START)
1. let PARTS = path split(START)
2. let I = count of PARTS - 1
3. let DIRS = []
4. while I >= 0,
   a. if PARTS[I] = "node_modules" CONTINUE
   b. DIR = path join(PARTS[0 .. I] + "node_modules")
   c. DIRS = DIRS + DIR
   d. let I = I - 1
5. return DIRS
```



# 路由

使用 http 模块时,  我们需要的所有数据都会包含在 request 对象中，该对象作为 onRequest() 回调函数的第一个参数传递。但是为了解析这些数据，我们需要 url 和 querystring 模块。 

>  也可以用 querystring 模块来解析 POST 请求体中的参数 

```javascript
// 例如一个 url 为:  http://localhost:8888/start?foo=bar&hello=world
url.parse(string).pathname  // /start
url.parse(string).query  // foo=bar&hello=world
querystring.parse(queryString)["foo"]  // bar
```



一个例子

1. router.js

```javascript
function route(pathname) {
  console.log("About to route a request for " + pathname);
}
exports.route = route;
```

2. server.js

```javascript
var http = require("http");
var url = require("url");

function start(route) {
  function onRequest(request, response) {
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received.");
 
    route(pathname);
 
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("Hello World");
    response.end();
  }
 
  http.createServer(onRequest).listen(8888);
  console.log("Server has started at localhost:8888.");
}

exports.start = start;
```

3. index.js

```javascript
var server = require("./server");
var router = require("./router");
server.start(router.route);
```





# 全局对象

### 一些全局对象

```
__filename     当前正在执行的脚本的文件名 ( 绝对路径 )
__dirname
setTimeout(cb, ms)
clearTimeout(t)
setInterval(cb, ms)
console
	console.log([data][, ...])    向标准输出流打印字符并以换行符结束。
    console.info([data][, ...])    [error, warn]
    console.dir(obj[, options])    用来对一个对象进行检查（inspect）
	console.time(label)    输出时间，表示计时开始。
	console.timeEnd(label)  结束时间，表示计时结束。
	console.trace(message[, ...])  当前执行的代码在堆栈中的调用路径
	console.assert(value[, message][, ...])
	用于判断某个表达式或变量是否为真，接收两个参数，第一个参数是表达式，第二个参数是字符串。只有当第一个参数为false，才会输出第二个参数，否则不会有任何结果。
```

# 全局变量 process

process 是一个全局变量，即 global 对象的属性。

它用于描述当前Node.js 进程状态的对象，提供了一个与操作系统的简单接口。通常在写本地命令行程序的时候，少不了process 

 process 对象的成员方法

```
exit  当进程准备退出时触发。
beforeExit  当 node 清空事件循环，并且没有其他安排时触发这个事件。
其他方法...
```

exit 例子

```javascript
process.on('exit', function(code) {
  // 以下代码永远不会执行
  setTimeout(function() {
    console.log("该代码不会执行");
  }, 0);
  
  console.log('退出码为:', code);
});
console.log("程序执行结束");
```



### process 属性

常用属性

```
stdout  标准输出流。  process.stdout.write("Hello World!" + "\n");
stderr  标准错误流。
stdin   标准输入流。
argv    返回一个数组，由命令行执行脚本时的各个参数组成。它的第一个成员总是node，第二个成员是脚本文件名，其余成员是脚本文件的参数。
execPath  返回执行当前脚本的 Node 二进制文件的绝对路径。
execArgv  返回一个数组，成员是命令行下执行脚本时，在Node可执行文件与脚本文件之间的命令行参数。
env       返回一个对象，成员为当前 shell 的环境变量

其他属性可打印 process 查看.
```

### process 方法

 Process 提供了很多有用的方法，便于我们更好的控制系统的交互 

常用方法

```
chdir(directory)
cwd()
exit([code])
nextTick(callback)    一旦当前事件循环结束，调用回调函数。
```



# 文件系统

```
const fs = require("fs")
```

### 异步和同步

 异步方法性能更高，速度更快，而且没有阻塞 

```javascript
const fs = require("fs")

// 异步读取
fs.readFile('input.txt', function (err, data) {
   if (err) {
       return console.error(err);
   }
   console.log("异步读取: " + data.toString());
});

// 同步读取
var data = fs.readFileSync('input.txt');
console.log("同步读取: " + data.toString());

console.log("程序执行完毕。");
```



### 获取文件信息

```javascript
fs.stat(path, callback)  //异步

callback - 回调函数，带有两个参数如：(err, stats), stats 是 fs.Stats 对象。

stats 主要属性:
	size
    atime
    mtime
    ctime
    birthtime
stats 主要方法:
	isFile()
	isDirectory()
	isSymbolicLink()
```



### 打开文件

```
fs.open(path, flags[, mode], callback)

参数:
    path - 文件的路径。
    flags - 文件打开的行为。
    mode - 设置文件模式(权限)，文件创建默认权限为 0666(可读，可写)。
    callback - 回调函数，带有两个参数如：callback(err, fd)。

flags:
    r	以读取模式打开文件。如果文件不存在抛出异常。
    r+	以读写模式打开文件。如果文件不存在抛出异常。
    rs	以同步的方式读取文件。
    rs+	以同步的方式读取和写入文件。
    w	以写入模式打开文件，如果文件不存在则创建。
    wx	类似 'w'，但是如果文件路径存在，则文件写入失败。
    w+	以读写模式打开文件，如果文件不存在则创建。
    wx+	类似 'w+'， 但是如果文件路径存在，则文件读写失败。
    a	以追加模式打开文件，如果文件不存在则创建。
    ax	类似 'a'， 但是如果文件路径存在，则文件追加失败。
    a+	以读取追加模式打开文件，如果文件不存在则创建。
    ax+	类似 'a+'， 但是如果文件路径存在，则文件读取追加失败。
```

### 读取文件

```
fs.read(fd, buffer, offset, length, position, callback)
```

结合 fs.open() 使用

```javascript
var fs = require("fs");
var buf = new Buffer.alloc(1024);

fs.open('../input.txt', 'r+', function(err, fd) {
   if (err) {
       return console.error(err);
   }
   console.log("文件打开成功！ 准备读取文件：");
   fs.read(fd, buf, 0, buf.length, 0, function(err, bytes){
      if (err){
         console.log(err);
      }
      console.log(bytes + "  字节被读取");
      
      if(bytes > 0){
         console.log(buf.slice(0, bytes).toString());
      }
       
       // 关闭文件
      fs.close(fd, function(err){
         if (err) console.log(err);
         console.log("文件关闭成功");
      });
   });
});
```

### 写入文件

```
fs.writeFile(file, data[, options], callback)

参数:
    file - 文件名或文件描述符。
    data - 要写入文件的数据，可以是 String(字符串) 或 Buffer(缓冲) 对象。
    options - 对象，包含 {encoding, mode, flag}。默认编码为 utf8, 模式为 0666 ， flag 为 'w'
    callback - 回调函数，回调函数只包含错误信息参数(err)，在写入失败时返回。
```

写入文件的例子

```javascript
var fs = require("fs");

fs.writeFile('input.txt', '我是通 过fs.writeFile 写入文件的内容',  function(err) {
   if (err) return console.error(err);
   console.log("数据写入成功！");
   console.log("--------我是分割线-------------")
   console.log("读取写入的数据！");
   fs.readFile('input.txt', function (err, data) {
      if (err) {
         return console.error(err);
      }
      console.log("异步读取文件数据: " + data.toString());
   });
});
```



### 其他操作

```javascript
// 关闭文件
fs.close(fd, callback)
// 截取文件
fs.ftruncate(fd, len, callback)
// 删除文件
fs.unlink(path, callback)

// 创建目录
fs.mkdir(path[, options], callback)
// 读取目录
fs.readdir(path, callback)
// 删除目录
fs.rmdir(path, callback)

// 查看更多方法
console.log(fs)
```



# http 模块

### 处理 GET/POST请求

处理 GET 请求

```javascript
var http = require('http');
var url = require('url');
var util = require('util');
 
http.createServer(function(req, res){
    res.writeHead(200, {'Content-Type': 'text/plain'});
 
    // 解析 url 参数
    var params = url.parse(req.url, true).query;
    res.write("网站名：" + params.name);
    res.write("\n");
    res.write("网站 URL：" + params.url);
    res.end();
 
}).listen(3000);
```

处理 POST 请求

> POST 请求的内容全部的都在请求体中，http.ServerRequest 并没有一个属性内容为请求体，原因是等待请求体传输可能是一件耗时的工作。
>
> 比如上传文件，而很多时候我们可能并不需要理会请求体的内容，恶意的POST请求会大大消耗服务器的资源，所以 node.js 默认是不会解析请求体的，当你需要的时候，需要手动来做。

```javascript
var http = require('http');
var querystring = require('querystring');
var util = require('util');
 
http.createServer(function(req, res){
    // 定义了一个post变量，用于暂存请求体的信息
    var post = '';     
 
    // 通过req的data事件监听函数，每当接受到请求体的数据，就累加到post变量中
    req.on('data', function(chunk){    
        post += chunk;
    });
 
    // 在end事件触发后，通过 querystring.parse 将 post 解析为真正的 POST 请求格式，然后向客户端返回。
    req.on('end', function(){    
        post = querystring.parse(post);
        res.end(util.inspect(post));
    });
}).listen(3000);
```



### 静态文件服务

```javascript
var http = require('http');
var fs = require('fs');
var url = require('url');
 
 
// 创建服务器
http.createServer( function (request, response) {  
   // 解析请求，包括文件名
   var pathname = url.parse(request.url).pathname;
   
   // 输出请求的文件名
   console.log("Request for " + pathname + " received.");
   
   // 从文件系统中读取请求的文件内容
   fs.readFile(pathname.substr(1), function (err, data) {
      if (err) {
         console.log(err);
         // HTTP 状态码: 404 : NOT FOUND
         // Content Type: text/html
         response.writeHead(404, {'Content-Type': 'text/html'});
      }else{             
         // HTTP 状态码: 200 : OK
         // Content Type: text/html
         response.writeHead(200, {'Content-Type': 'text/html'});    
         
         // 响应文件内容
         response.write(data.toString());        
      }
      //  发送响应数据
      response.end();
   });   
}).listen(8888);
 
// 控制台会输出以下信息
console.log('Server running at http://127.0.0.1:8888/');

```



### Web 客户端

client.js

```javascript
var http = require('http');
 
// 用于请求的选项
var options = {
   host: 'localhost',
   port: '8080',
   path: '/index.html'  
};
 
// 处理响应的回调函数
var callback = function(response){
   // 不断更新数据
   var body = '';
   response.on('data', function(data) {
      body += data;
   });
   
   response.on('end', function() {
      // 数据接收完成
      console.log(body);
   });
}
// 向服务端发送请求
var req = http.request(options, callback);
req.end();
```





# express 框架

 使用 Express 可以快速地搭建一个完整功能的网站。 

Express 框架核心特性：

- 可以设置中间件来响应 HTTP 请求。
- 定义了路由表用于执行不同的 HTTP 请求动作。
- 可以通过向模板传递参数来动态渲染 HTML 页面。



安装

```
npm install express --save
```

> 以下几个重要的模块是需要与 express 框架一起安装的：
>
> - **body-parser** - node.js 中间件，用于处理 JSON, Raw, Text 和 URL 编码的数据。
> - **cookie-parser** - 这就是一个解析Cookie的工具。通过req.cookies可以取到传过来的cookie，并把它们转成对象。
> - **multer** - node.js 中间件，用于处理 enctype="multipart/form-data"（设置表单的MIME编码）的表单数据。

demo

```javascript
//express_demo.js 文件
const express = require('express');
const app = express();
 
app.get('/', (req, res) => {
   res.send('Hello World');
})
 
const server = app.listen(8081, () => {
 
  const host = server.address().address
  const port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})
```

### request 对象

```
req.app    当callback为外部文件时，用 req.app 访问 express 的实例
req.baseUrl    获取路由当前安装的URL路径
req.body / req.cookies    获得「请求主体」/ Cookies
req.fresh / req.stale    判断请求是否还「新鲜」
req.hostname / req.ip    获取主机名和IP地址
req.originalUrl    获取原始请求URL
req.params    获取路由的parameters
req.path      获取请求路径
req.protocol  获取协议类型
req.query    获取URL的查询参数串
req.route    获取当前匹配的路由
req.subdomains  获取子域名
req.accepts()   检查可接受的请求的文档类型
req.acceptsCharsets / req.acceptsEncodings / req.acceptsLanguages  返回指定字符集的第一个可接受字符编码
req.get()  获取指定的HTTP请求头
req.is()   判断请求头 Content-Type 的 MIME 类型
req.files   获取上传的文件对象
```

### response 对象

```
res.app    同req.app一样
res.append()    追加指定HTTP头
res.set()      在 res.append() 后将重置之前设置的头
res.cookie(name，value [，option])    设置Cookie
	opition: domain / expires / httpOnly / maxAge / path / secure / signed
res.clearCookie()    清除Cookie
res.download()      传送指定路径的文件
res.get()   返回指定的HTTP头
res.json()  传送JSON响应
res.jsonp() 传送JSONP响应
res.location()    只设置响应的Location HTTP头，不设置状态码或者close response
res.redirect()    设置响应的Location HTTP头，并且设置状态码302
res.render(view,[locals],callback)  渲染一个view，同时向callback传递渲染后的字符串，如果在渲染过程中有错误发生next(err)将会被自动调用。callback将会被传入一个可能发生的错误以及渲染后的页面，这样就不会自动输出了。
res.send()    传送HTTP响应
res.sendFile(path [，options] [，fn])   传送指定路径的文件 -会自动根据文件extension设定Content-Type
res.set()     设置HTTP头，传入object可以一次设置多个头
res.status()  设置HTTP状态码
res.type()    设置Content-Type的MIME类型
```



### 路由与请求方式

```javascript
var express = require('express');
var app = express();
 
//  主页输出 "Hello World"
app.get('/', function (req, res) {
   console.log("主页 GET 请求");
   res.send('Hello GET');
})
 
 
//  POST 请求
app.post('/', function (req, res) {
   console.log("主页 POST 请求");
   res.send('Hello POST');
})
 
//  /del_user 页面响应
app.delete('/del_user', function (req, res) {
   console.log("/del_user 响应 DELETE 请求");
   res.send('删除页面');
})
 
// 对页面 abcd, abxcd, ab123cd, 等响应 GET 请求
app.get('/ab*cd', function(req, res) {   
   console.log("/ab*cd GET 请求");
   res.send('正则匹配');
})
 
 
var server = app.listen(8081, function () {
 
  var host = server.address().address
  var port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})
```



更多路由匹配规则见资源链接



### 静态文件

Express 提供了内置的中间件 **express.static** 来设置静态文件如：图片， CSS, JavaScript 等。

你可以使用 **express.static** 中间件来设置静态文件路径。例如，如果你将图片， CSS, JavaScript 文件放在 public 目录下，你可以这么写：

```
app.use('/public', express.static('public'));
```

访问方式:  ` http://127.0.0.1:8081/public/images/logo.png `





### 一个简单的 RESTful API 例子

 https://www.runoob.com/nodejs/nodejs-restful-api.html 





### 更多

更多主题见前面的资源链接,  如:

1. 返回 JSON 响应
2. 文件上传
3. Cookie 管理





# 多进程

 https://www.runoob.com/nodejs/nodejs-process.html 



# 连接 MySQL

 https://www.runoob.com/nodejs/nodejs-mysql.html 

```
npm install mysql
```

# 连接 MongoDB

 https://www.runoob.com/nodejs/nodejs-mongodb.html 

```
npm install mongodb
```



# ==== 一些模块记录 ====

```
fs		文件系统操作API
http	web模块
zlib	压缩文件处理
events	事件
Buffer	缓冲区
Stream	流
path	本地路径处理
	path.normalize(p)
	path.join()
    path.resolve([from ...], to)  将 to 参数解析为绝对路径
    path.isAbsolute(path)
    path.relative(from, to)    将绝对路径转为相对路径
    path.dirname(p)
    path.basename(p[, ext])
    path.extname(p)
    path.parse(pathString), path.format(pathObject)
    
    path.sep
    path.delimiter

url		url 处理
querystring  查询字符串处理
util	Node.js 一个核心模块，提供常用函数的集合
	util.callbackify()
	util.inherits()
	util.inspect()
	util.isArray()
	util.isRegExp()
	util.isDate()
	util.is......

os		系统操作
	os.tmpdir()
	os.platform()
    os.networkInterfaces()
    os.EOL    操作系统的行尾符的常量
net		用于底层的网络通信。提供了服务端和客户端的的操作
dns		解析域名
domain	简化异步代码的异常处理，可以捕捉处理try catch无法捕捉的

mysql   连接 mysql
mongodb 连接 mongodb
```