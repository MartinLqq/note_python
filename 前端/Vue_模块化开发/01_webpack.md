

# ==== webpack ====

# 从前后端不分离到 前端模块化

1. 前后端不分离,  javascript 只需要实现较少功能,  页面渲染主要由后端进行

2. ajax异步,  前后端分离,  javascript 需要执行非常多的操作,  代码混乱

3. javascript 多文件在同一个作用域内, 变量名/函数名 冲突/覆盖, 容易引起难以解决的bug

4. 采用匿名函数的方式解决作用域问题,  但内部代码无法复用

   ```javascript
   // html文件使用两个 script 标签分别引入 foo.js bar.js
   
   // ===== foo.js =====
   ;(function(){
     var a = 123;
     var foo = function(){};
   })()
   
   // ===== bar.js =====
   ;(function(){
     var a = 123;
   })()
   ```

5. 使用一个模块作为出口, 解决作用域问题, 同时增加复用性

   ```javascript
   // ===== foo.js =====  模块化的雏形
   var moduleFoo = function(){
     var a = 123;
     var sayHello = function(){};
       
     var obj = {};
     obj.sayHello = sayHello;
     return obj
   }();
   
   // ===== bar.js =====
   ;(function(){
     moduleFoo.sayHello();
   }()
   )
   ```

6. 模块化规范化, 规定模块化怎么写:  CommonJS 规范, AMD 规范, CMD 规范, ES6 的 Modules 规范

7. 模块化两个核心: 导出, 导入

   CommonJS 规范的导出, 导入

   ```javascript
   // ===== foo.js =====
   var a = 123;
   var sayHello = function(){};
   // module.exports 导出
   module.exports = {    //注: 这种导出导入语法依赖支持CommonJS的环境, 如 Node 环境
     a: a,
     sayHello: sayHello,
   }
   
   
   // ===== bar.js =====
   // require 导入
   //(A)
   let { a, sayHello } = require('./foo.js');
   //(B)
   // let _foo = require('./foo.js');
   // _foo.sayHello();
   ```

# ES6 模块化的导出, 导入

   ```javascript
   // ===== index.html =====
   // type="module"
   <script src="./foo.js" type="module"></script>
   <script src="./bar.js" type="module"></script>
   
   // ===== foo.js =====
   let a = 123;
   // export
   export let b = 456;
   let sayHello = function(){};
   // export
   export { a, sayHello }
   // export
   export function eat(food){};
   export class Person{
       constructor(name, age){}
   };
   // export default : 让导入方自己命名
   // 在一个模块内, export default 只能有一个
   // export default function(){}
   export default const address = '江西省'
   
   
   // ===== bar.js =====
   import {sayHello, a, b} from "./foo.js"
   sayHello();
   import addr from "./foo.js"  //不需要大括号 {}
   console.log(addr)
   // 统一全部导入
   import * as myfoo from "./foo.js"
   ```



# webpack

### 概念

webpack 本质上是一个现代 javascript 应用的静态模块打包工具

1. 模块化:  支持模块化开发,  底层支持多种模块化规范
2. 打包:  处理模块间的依赖关系

在 webpack 中, 一个模块不仅仅是 javascript 文件, 也包含 CSS, 图片, json文件等等 (需要安装对应的 loader)

> 思考:  webpack 和 grunt/gulp 的对比

webpack 与 node 与 npm

- webpack 本身依赖 node 环境
- npm 是 **n**ode **p**ackages **m**anager

webpack 支持多种模块化规范,  如 CommonJS 规范, AMD 规范, CMD 规范, ES6 的 Modules 规范, .....



### 文档

**webpack 配置 中文文档**有对各个配置项的列举和说明:   https://www.webpackjs.com/configuration/ 



### 安装

1. 安装 Node.js

2. Node.js 自带 npm

3. 安装 webpack

   ```bash
   # 全局安装
   npm search webpack
   npm install webpack@3.12.0 -g --registry=http://registry.npm.taobao.org
   
   # 局部安装
   npm install webpack@3.12.0 --save-dev --registry=http://registry.npm.taobao.org
   ```

### 简单使用

简单使用 webpack

1. CommonJS 语法

(1) index.html

```html
<script src="./dist/bundle.js"></script>
```

(2) src/bar.js

```javascript
let name = "Martin";
let sayHello = function(){
    console.log("Hello!");
}
// CommonJS 语法
module.exports = {
    name, 
    sayHello,
}
```

(3) src/main.js

```javascript
// ES6 语法
import {message, eat} from "./bar.js";
console.log(message);
eat();
```

(4) 终端命令,  打包生成最终 js 文件

```bash
webpack  ./src/main.js  ./dist/bundle.js
```



2. ES6 语法

(1) index.html

```html
<script src="./dist/bundle.js"></script>
```

(2) src/bar.js

```javascript
// ES6 语法
let message = "It's time to eat launch!";
export { message };
export let eat = (food, )=>{
    console.log("Eating ", food);
}
```

(3) src/main.js

```javascript
// ES6 语法
import {message, eat} from "./bar.js";
console.log(message);
eat();
```

(4) 重新打包, 生成最终 js 文件

```bash
$ webpack  ./src/main.js  ./dist/bundle.js
```



> npm run build



### webpack 配置

> webpack 配置文件常用命名:  
>
> - webpack.config.js
> - webpack.base.conf.js
> - webpack.dev.conf.js
> - webpack.prod.conf.js
> - ......

```javascript
const path = require('path');
/*
安装 path 模块, 后面将用来生成绝对路径.
(它是一个 Node.js 核心模块，用于操作文件路径)
    1. 初始化: npm init  输入相关信息, 最终生成一个 package.json (npm包管理文件)
    2. 查看 package.json 的内容
    3. ...

*/

const config = {
    entry: "./src/main.js",
    output: {
        // path: "./dist/",  // 报错! 要求绝对路径
        path: path.resolve(__dirname, 'dist'),
        filename: "bundle.js",
    }
}

module.exports = config;
```

配置好之后,  打包的命令可以简化为

```bash
$ webpack
```



### package.json

先看一个 package.json 的例子

```json
{
  "name": "blog",
  "version": "1.0.0",
  "description": "A Vue.js project",
  "author": "lqq <18770915328@163.com>",
  "private": true,
  "scripts": {
    "dev": "webpack-dev-server --inline --progress --config build/webpack.dev.conf.js",
    "start": "npm run dev",
    "unit": "jest --config test/unit/jest.conf.js --coverage",
    "e2e": "node test/e2e/runner.js",
    "test": "npm run unit && npm run e2e",
    "lint": "eslint --ext .js,.vue src test/unit test/e2e/specs",
    "build": "node build/build.js"
  },
  "dependencies": {
    "element-ui": "^2.13.0",
    "vue": "^2.5.2",
    "vue-router": "^3.0.1"
  },
  "devDependencies": {
    "autoprefixer": "^7.1.2",
    "babel-core": "^6.22.1",
    "babel-eslint": "^8.2.1",
    "babel-helper-vue-jsx-merge-props": "^2.0.3",
    "babel-jest": "^21.0.2",
    "babel-loader": "^7.1.1",
    "babel-plugin-dynamic-import-node": "^1.2.0",
    "babel-plugin-syntax-jsx": "^6.18.0",
    "babel-plugin-transform-es2015-modules-commonjs": "^6.26.0",
    "babel-plugin-transform-runtime": "^6.22.0",
    "babel-plugin-transform-vue-jsx": "^3.5.0",
    "babel-preset-env": "^1.3.2",
    "babel-preset-stage-2": "^6.22.0",
    "babel-register": "^6.22.0",
    "chalk": "^2.0.1",
    "chromedriver": "^2.27.2",
    "copy-webpack-plugin": "^4.0.1",
    "cross-spawn": "^5.0.1",
    "css-loader": "^0.28.0",
    "eslint": "^4.15.0",
    "eslint-config-standard": "^10.2.1",
    "eslint-friendly-formatter": "^3.0.0",
    "eslint-loader": "^1.7.1",
    "eslint-plugin-import": "^2.7.0",
    "eslint-plugin-node": "^5.2.0",
    "eslint-plugin-promise": "^3.4.0",
    "eslint-plugin-standard": "^3.0.1",
    "eslint-plugin-vue": "^4.0.0",
    "extract-text-webpack-plugin": "^3.0.0",
    "file-loader": "^1.1.4",
    "friendly-errors-webpack-plugin": "^1.6.1",
    "html-webpack-plugin": "^2.30.1",
    "jest": "^22.0.4",
    "jest-serializer-vue": "^0.3.0",
    "nightwatch": "^0.9.12",
    "node-notifier": "^5.1.2",
    "optimize-css-assets-webpack-plugin": "^3.2.0",
    "ora": "^1.2.0",
    "portfinder": "^1.0.13",
    "postcss-import": "^11.0.0",
    "postcss-loader": "^2.0.8",
    "postcss-url": "^7.2.1",
    "rimraf": "^2.6.0",
    "selenium-server": "^3.0.1",
    "semver": "^5.3.0",
    "shelljs": "^0.7.6",
    "uglifyjs-webpack-plugin": "^1.1.1",
    "url-loader": "^0.5.8",
    "vue-jest": "^1.0.2",
    "vue-loader": "^13.3.0",
    "vue-style-loader": "^3.0.1",
    "vue-template-compiler": "^2.5.2",
    "webpack": "^3.6.0",
    "webpack-bundle-analyzer": "^2.9.0",
    "webpack-dev-server": "^2.9.1",
    "webpack-merge": "^4.1.0"
  },
  "engines": {
    "node": ">= 6.0.0",
    "npm": ">= 3.0.0"
  },
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not ie <= 8"
  ]
}
```



- scripts:  定义一些 npm run xxx 命令的映射关系,  如执行 npm run build 时,  真正执行的是  "node build/build.js"。**与在终端直接运行命令不同的是**， npm run xxx **优先从本地找** xxx 所映射的命令

- dependencies: 项目运行时依赖.

- devDependencies:  项目开发时依赖.  在局部安装 webpack,  即 `npm install webpack@3.12.0 --save-dev` 时:
  
  > - 仅在项目开发阶段用到 webpack， 项目运行时(打包完成之后) 不需要用到
> - package.json 一般不会手动去修改, 安装依赖包后会自动更新

  ```
  1. package.json 会增加一个 devDependencies 项,  新增刚安装的 webpack:
    "devDependencies": {
      "webpack": "^3.12.0"
    }
  2. 本地生成一个 node_modules 目录, 保存当前项目的依赖包. 不同于全局的 node_modules
  ```

  在项目下安装依赖包, 使用: 

  ```bash
  $ npm install 包名@版本号 --save-dev   --registry=http://registry.npm.taobao.org
  ```

  

# loader

### 概念

- loader 是 webpack 中的一个非常核心的内容
- loader 用于对模块的源代码进行转换。

loader 可以使你在 `import` 或"加载"模块时预处理文件。因此，loader 类似于其他构建工具中“任务(task)”，并提供了处理前端构建步骤的强大方法。loader 可以将文件从不同的语言（如 TypeScript）转换为 JavaScript，或将内联图像转换为 data URL。loader 甚至允许你直接在 JavaScript 模块中 `import` CSS文件！ 

### 文档

webpack loaders 中文文档:   https://www.webpackjs.com/loaders/ 



### 使用 loader 的步骤

1. 安装 loader
2. 配置 module 项的 rules 项
3. 导入 loader



### css 文件 loader

1. 安装 css-loader 和 style-loader

```
# css-loader 只负责加载 css 文件, 不负责解析, style-loader 负责将样式添加到 DOM 中
npm install --save-dev css-loader  
npm install --save-dev style-loader

安装的 loader 都会自动更新到 package.json 的 devDependencies 中
```

2. 配置  webpack.config.js 的 rules

```json
{
  ...

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          // style-loader 依赖 css-loader
          // 注意: style-loader 放在 css-loader 前面, 读取loader时是从后到前的!
          { loader: "style-loader" },  
          { loader: "css-loader" }
        ]
        //或直接:  use: ["style-loader", "css-loader"]
      },
      { test: /\.ts$/, use: 'ts-loader' }
    ]
  }
}
```

3. 导入

```javascript
import Css from "./css/my.css"
// 或CommonJS语法:
// require("./css/my.css")
```

> 如果想用 less, scss,  stylus 写样式,  相应的 loader 查官网



### 图片文件 loader

使用  `url-loader` 加 `file-loader`  处理 css 中引用的图片地址:

```
# 1. 在 css 文件中引用一个图片地址
body{
    background: url('./images/test.jpg')
}

# 2. 在 webpack 配置的 output 中增加一项:  publicPath: "dist/".
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: "bundle.js",
        // 默认会将 url 地址对应到项目根目录下的资源, 即默认会404, 
        // 需要配置所有 url地址 解析后增加 "dist/", 
        publicPath: "dist/",
    }
    
 # 3. npm run buid
 # 4. 尝试访问图片， 可以访问
 
 # 5. 做更多配置: 修改图片名称、图片路径
 # webpack 打包到 dist 的图片文件的名称默认是一个 hash 值, 且图片路径直接是在 dist 目录下, 
 # 可以配置 url-loader 的 options 的 name，修改打包后的 图片名称、图片路径
     module: {
        rules: [
        ...,
        {
            test: /\.(png|jpg|gif|jpeg)$/,
            use: [
              {
                loader: 'url-loader',
                options: {
                  // 图片大小限制, 如果超过此限制, 需要配合 file-loader 使用.
                  limit: 10000,
                  // name取原图片名, 下划线取`_`, hash:8取8位hash值, ext取原图片扩展名.
                  name: "img/[name]_[hash:8].[ext]"  
                }
              }
            ]
          }
        ]
    }
```

**注:**

- **上面这些配置在使用 vue-cli 搭建脚手架时基本都会自动配置好,  仅需要知道实际作用.**

- 需要在  webpack.config.js 配置的 **output** 中增加一项:  **publicPath: "dist/"**.

  配置 **publicPath: "dist/"** 后,  所有与 url 链接都会加上 "dist/"

- 按文档配置好后,  如果指定图片的大小 大于配置的 **limit**,  就需要用到 **file-loader**,  file-loader 只需要安装一下,  不需要特别配置.
  1. 如果指定图片小于配置的 limit,  图片资源以 base64 字符串的形式返回; 

  2. 如果指定图片大于配置的 limit,  配合 file-loader, 返回一个图片地址





### ES6 打包为 ES5

如果想把 ES6 语法代码打包成 ES5 语法代码,  需要使用 **[babel-loader](https://www.webpackjs.com/loaders/babel-loader/)**

```
npm install --save-dev  babel-loader@7 babel-core babel-preset-es2015
```

webpack rules 增加一项配置:

```javascript
{
  test: /\.m?js$/,
  exclude: /(node_modules | bower_components)/,
  use: {
    loader: 'babel-loader',
    options: {
      presets: ['es2015']
    }
  }
}
```

重新 npm run build 打包,  查看 bundle.js 中没有了 ES6 语法的代码





# 在 webpack 中集成 Vue

1. npm 安装 Vue

   ```
   npm  install  --save  vue
   # vue 是开发时依赖, 也是运行时依赖, 所以安装时不使用 --save-dev 选项,
   # 而是使用 --save
   ```

2. 导入方式

   main.js

   ```
   import Vue from 'vue'
   
   new Vue({
     el: "#app",
     data: {
       message: "Hello webpack!",
     }
   })
   ```

3. 使用 Vue

   index.html

   ```html
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <meta http-equiv="X-UA-Compatible" content="ie=edge">
       <title>Document</title>
   </head>
   <body>
       <div id='app'>
           {{ message }}
       </div>
       <script src="./dist/bundle.js"></script>
   </body>
   </html>
   ```

4. 测试访问,  出现报错:

   ```
   [Vue warn]: You are using the runtime-only build of Vue where the template compiler is not available. Either pre-compile the templates into render functions, or use the compiler-included build.
   
   错误原因:  
     默认使用的是 runtime-only 版本的 Vue,  需要指定为 runtime-compiler 版本的 Vue
   ```

5. 解决报错

   ```javascript
   //在 webpack 配置对象的 顶级增加 resolve 配置:
   {
       entry: "./src/main.js",
       output: {
           path: path.resolve(__dirname, 'dist'),
           filename: "bundle.js",
           publicPath: "dist/",
       },
       module: {
           rules: [
           {
               test: /\.css$/,
               use: [
               { loader: "style-loader" },
               { loader: "css-loader" }
               ]
               // use: ["style-loader", "css-loader"]
           },
           { test: /\.ts$/, use: 'ts-loader' },
           {
               test: /\.(png|jpg|gif|jpeg)$/,
               use: [
                 {
                   loader: 'url-loader',
                   options: {
                     limit: 8192,
                     name: "img/[name]_[hash:8].[ext]"
                   }
                 }
               ]
             },
             {
               test: /\.m?js$/,
               exclude: /(node_modules | bower_components)/,
               use: {
                 loader: 'babel-loader',
                 options: {
                   presets: ['es2015']
                 }
               }
             }
           ]
       },
       // 增加此项
       resolve: {
           alias: {
               // 配置在导入资源时不需要加以下后缀
               extensions: [".js", ".json", ".jsx", ".css"],
   
               //下面版本vue包含compiler
               //使用vue-cli搭建脚手架时也会有下面这一项配置
               //在 import Vue from 'vue' 时会去找 node_modules/vue/dist/vue.esm.js
               'vue$': 'vue/dist/vue.esm.js',
           }
       },
   }
   ```



# el 与 template 组合

1. 只使用 el 时, Vue 接管的标签之下的代码需要写在 index.html 中

   ````
   # index.html
   <div id="app">
     <!-- 在这里写内容, 会造成之后可能要频繁修改 index.html,
          需求: 后续不想修改 index.html
     -->
     <div>
       {{ message }}
     </div>
   </div>
   
   
   # main.js
   import Vue from 'vue'
   new Vue({
       el: "#app",
       data: { message: "Hello webpack" }
   })
   ````

2. 使用 el + template, Vue 接管的标签下的代码可以写在 template 指定的字符串中

   ```
   # index.html
   <div id="app">
     <!-- 在这里不写内容 -->
   </div>
   
   
   # main.js
   import Vue from 'vue'
   new Vue({
       el: "#app",
       //这里写一个 template, Vue 接管的标签下的代码写在 template 字符串中
       template: `
         <div>
           {{ message }}
         </div>
       `,
       data: { message: "Hello webpack" },
   })
   ```

3. 进一步将 template 字符串抽出为一个单独文件,  即写成一个组件

   > **注意**: 下一步将安装一个解析 .vue 文件的 loader

   ```
   # index.html
   同上, 不变
   
   
   # App.vue 组件, 里面固定有3个标签: <template>, <script>, <style>
   <template>
     <div id="app">
     </div>
   </template>
   
   <script>
   export default {
     name: 'App',
     data() {
       return { message: "Hello webpack" }
     }
   }
   </script>
   
   <style>
   </style>
   
   
   
   # main.js
   import Vue from 'vue'
   import App from 'App'   //如果没有配置webpack的 resolve->extensions 列表, 需要 from "App.vue"
   
   new Vue({
       el: "#app",
       components: {       //注册 App.vue 组件, 名为 App
         App
       },
       template:"<App/>",  //在template项使用组件 App
   })
   ```

4. 安装处理 vue 组件文件的 loader

   ```
   npm install --save-dev vue-loader vue-template-compiler
   ```

5. 配置新安装的 loader,  使其生效

   ```
   // 增加 webpack 的 rules 配置
             {
               test: /\.vue$/,
               use: ['vue-loader']
             }
   ```

6. 重新 buid,  发现报错

   ```
   ERROR in ./src/App.vue
   vue-loader was used without the corresponding plugin. Make sure to include VueLoaderPlugin in your webpack config.
   ```

7. 解决报错

   ```
   1. 修改 package.json devDependencies 中 vue-loader 的版本号为 13.x.x, 如 "^13.3.0"
   2. npm install
   ```

8. 重新编译打包,  测试访问

   ```
   npm run build
   ```

   

# ~~ 阶段总结 ~~

**请看 `vue_webpack_test_proj` 目录**

###### 

# webpack plugin

### 概念

webpack 中的 [插件](https://www.webpackjs.com/plugins/) 就是对 webpack 现有功能的各种扩展,  如打包优化、文件压缩等

loader 和 plugin

1. loader 是转换器， 主要用于转换某些类型的模块，如加载 css 文件、加载图片、加载json文件等等
2. plugin 是插件，是对 webpack 本身的扩展

plugin 的使用步骤

1. 如果不是 webpack 自带 plugin, 需要先安装
2. 在 webpack js配置 中配置 plugin



### 用于添加版权声明的 plugin

[BannerPlugin](https://www.webpackjs.com/plugins/banner-plugin/):   webpack 自带插件,  为每个 chunk 文件头部添加 banner。 

1. 修改 webpack.config.js 配置

   ```javascript
   const path = require('path')
   const webpack = require('webpack')  //导入 webpack
   
   module.exports = {
     ...
     plugins: [
       new webpack.BannerPlugin('最终版权归 Martin 所有\n\n\n'),
     ]
   }
   ```

2. 重新打包程序,  查看 bundle.js 文件的头部

   ```
   npm run build
   ```

   

### 打包 html 的插件

当前阶段下,  index.html 文件是放在项目根目录下的,  而不是 dist/ 目录下,  在发布项目时只会发布 dist/,  

所以需要将 index.html 打包到 dist/ 下.   使用 **[HtmlWebpackPlugin](https://www.webpackjs.com/plugins/html-webpack-plugin/)**

HtmlWebpackPlugin 可以做:

1. 自动生成一个 index.html 文件 (可以指定模板来生成)
2. 将打包的 js 文件,  自动通过 script 标签插入到 body 中,  即 **不再需要在原来的 index.html 中插入 script 标签来指定打包后的 js 文件路径**.

使用 HtmlWebpackPlugin

1. 安装开发时依赖

   ```
   npm  install  --save-dev  html-webpack-plugin
   ```

2. 修改配置

   ```javascript
   ...
   const HtmlWebpackPlugin = require('html-webpack-plugin');
   
   module.exports = {
     ...
     plugins: [
       new webpack.BannerPlugin('最终版权归 Martin 所有\n\n\n'),
       
       //新增一个 HtmlWebpackPlugin
       new HtmlWebpackPlugin({
         template: 'index.html'  //不用默认的模板, 用自己的index.html, 因为默认模板中没有`<div id='app'><div>`
       }),
     ]
   }
   
   ! 删除一项配置:
     删除 output 中的 publicPath 属性, 
     否则 HtmlWebpackPlugin 插入的 script 标签的 src 可能有问题.
   ```

3. 重新打包程序,  查看 dist/ 目录下多了个 index.html

   ```
   npm run build
   ```

> PS:  测试时安装的是 `"html-webpack-plugin": "^4.2.0"`,  打包时报错 `TypeError: Cannot read property 'make' of undefined`,  把版本号降低为 `"^3.2.0"`,  再试一次就没有问题

4. 观察 dist/index.html 中的 script 标签,  发现 `src="dist/bundle.js"`,  多了 `dist/`,  需要把之前配置的 output > `publicPath: "dist/"`  删除





### JS 压缩的插件

在项目发布之前,  需要对打包的 JS 文件进行压缩 (丑化)

1. 安装插件

   ```
   npm install --save-dev uglifyjs-webpack-plugin@1.1.1
   ```

2. 配置

   ```javascript
   const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
   
   module.exports = {
     ...
     plugins: [
       new webpack.BannerPlugin('最终版权归 Martin 所有\n\n\n'),
       new HtmlWebpackPlugin({
         template: 'index.html'
       }),
       new UglifyJsPlugin(),
     ]
   }
   ```

3. 重新打包程序,  查看 bundle.js

   ```
   npm run build
   ```





# webpack-dev-server 搭建本地服务器

webpack-dev-server 模块可以用来搭建本地服务器,  这个服务器基于 node.js 搭建,  内部使用 express 框架,  可以让浏览器自动刷新显示我们修改代码后的结果

1. 安装
2. 配置 webpack
3. 配置 package.json 的 scripts 项
4. 启动本地开发服务器
5. 测试访问

详细步骤

1. 安装

   ```
   npm install --save-dev webpack-dev-server@2.9.1
   ```

2. 配置 webpack

   ```javascript
   module.exports = {
     ...
   
     devServer: {
       contentBase: './dist',
       inline: true,
     }
   }
   ```

3. 配置 package.json 的 scripts 项

   ```javascript
   {
     ...
     "scripts": {
       ...
       "dev": "webpack-dev-server --inline --progress  --open",  //--open 是打开浏览器
     },
   }
   ```

4. 启动本地开发服务器

   ```
   npm run dev
   ```

5. 测试访问

   ```
   默认访问: localhost:8080
   在每次修改代码后, 不再需要手动执行 npm run build 来重新编译、打包.
   不过这种自动更新是更新到 内存中, 而不是硬盘, 最终项目发布前还是需要手动 npm run build
   ```

6. 临时关闭 JS 压缩的插件 `uglifyjs-webpack-plugin`,  方便开发时进行调试

   ```javascript
       plugins: [
         ...
         // new UglifyJsPlugin(),
       ],
   ```

   

# webpack 配置文件分离

需求:  配置文件分离,  开发时用一个配置文件,  发布时用;另一个配置文件

1. 基础配置   `build/webpack.base.conf.js`
2. 开发时需要的配置    `build/webpack.dev.conf.js`
3. 打包发布时需要的配置     `build/webpack.prod.conf.js`



配置文件分离步骤

1. 安装 `webpack-merge`

   ```bash
   $ npm install webpack-merge@4.1.5 --registry=http://registry.npm.taobao.org
   ```

2. 创建目录 build,  在 build 目录下创建上面三个配置文件

3.  `webpack.base.conf.js`  的内容:   见 `vue_webpack_test_proj`  目录

4. `webpack.dev.conf.js`  的内容:  见 `vue_webpack_test_proj`  目录

5. `webpack.prod.conf.js`   的内容:  见 `vue_webpack_test_proj`  目录

6. 修改 package.json 的 scripts

   ```javascript
     "scripts": {
       ...
       "dev": "webpack-dev-server --inline --progress --config ./build/webpack.dev.conf.js --open",
       "build": "webpack --config ./build/webpack.dev.conf.js",
     }
   ```

7. 测试  npm run build

8. 修改 `webpack.base.conf.js` 的 output 项

   ```javascript
       output: {
           //path: path.resolve(__dirname, 'dist'),  //最终打包后的所有资源的根目录
           path: path.resolve(__dirname, '../dist'),
           ...
       },
   ```

9. 测试  npm run build

# ~~ 阶段总结 ~~

**请看 `vue_webpack_test_proj` 目录**

