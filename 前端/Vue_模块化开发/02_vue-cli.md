

# ==== vue-cli ====

# vue-cli 脚手架

vue-cli 是 vue官方出品的快速构建单页应用的脚手架，里面集成了webpack，npm，nodejs，babel，vue，vue-router 等等



### 安装 vue-cli

1. 安装 node.js (默认自动安装 npm,  node 环境需要在 8.9 以上版本)

2. 可选:  更改镜像源为淘宝 NPM 镜像 (或其他加速方式: 如代理)

   ```bash
   $ npm install -g cnpm --registry=http://registry.npm.taobao.org
   # 后续就可以用 cnpm install [name] [--save-dev] [-g]  来安装模块了
   ```

3. 安装 vue-cli 脚手架

   ```bash
   # Vue CLI3 的安装
   $ npm install -g @vue/cli  --registry=http://registry.npm.taobao.org
   # 附: Vue CLI2 的安装: npm install -g vue-cli
   # 查看脚手架版本
   $ vue -V
   ```

### 命令行创建项目

```bash
# Vue CLI3 初始化项目
vue create my-proj
```

> Vue CLI >= 3 和旧版使用了相同的 `vue` 命令，所以 Vue CLI 2 (`vue-cli`) 被覆盖了。如果你仍然需要使用旧版本的 `vue init` 功能，你可以全局安装一个桥接工具：
>
> ```bash
> $ npm install -g @vue/cli-init
> # `vue init` 的运行效果将会跟 `vue-cli@2.x` 相同
> $ vue init webpack hello-vue-cli2
> ```



### Web 界面创建和管理项目

你也可以通过 `vue ui` 命令以图形化界面创建和管理项目：

```bash
vue ui
```



### Runtime-compiler  vs. Runtime-only

a. 选择 Runtime-compiler 最终生成的 main.js 是

```javascript
import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})

// template --> ast抽象语法树 --> render --> virtual DOM --> UI
```

b. 选择 Runtime-only 最终生成的 main.js 是

```javascript
import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  render: function (h) {
      return h(App)
  }
})

// render --> virtual DOM --> UI
// 此时 <template> 的解析是由 `vue-template-compiler` 来完成,
// 可以尝试在import App 之后打印一下 App, 发现没有 template 属性, 而有 render 函数
```



1. Runtime-only 性能更高
2. Runtime-only 最终编译后的代码量更少,  没有 compiler 部分的代码



# Vue CLI2 体验

### 初始化项目

基于 Vue CLI2 创建一个 hello-vue-cli2 项目

```bash
$ vue init webpack hello-vue-cli2
# 会有根据输入提示:
	Project name (默认以文件夹名 hello-vue-cli2 为项目名)
	Project description
	Author (默认从全局的 .gitconfig 配置中读取)
	Vue build (使用上下方向键选择: 1. Runtime + Compiler; 2. Runtime-only.  在此选 1 即可, 熟悉两者区别后推荐选 2 )
	Install vue-router? (Y/n)  # 当前先选择 n
	Use ESLint to lint your code? (Y/n)  (是否使用 ESLint 对 JS 代码进行规范化限制)
	    # 如果上一步输入 Y, 需要选择一种 ESLint 标准:
	    Pick a ESLint preset  (Standard / Airbnb / none-自己配置)
	Set up unit tests? (Y/n)  # 国内需要写 ut 的公司比较少
	Setup e2e tests with Nightwatch? (Y/n)  # 端到端测试, Nightwatch是一个自动化测试框架
	Should we run `npm install` for you after the project has been created?
		# 三个选项
		> Yes, use NPM
		Yes, use Yarn
		No, I will handle that myself
```

### package.json

```javascript
{
  "name": "hello-vue-cli2",
  "version": "1.0.0",
  "description": "test Vue CLI2",
  "author": "lqq <18770915328@163.com>",
  "private": true,
  "scripts": {
    "dev": "webpack-dev-server --inline --progress --config build/webpack.dev.conf.js",
    "start": "npm run dev",
    "lint": "eslint --ext .js,.vue src",
    "build": "node build/build.js"  // node xx.js  可以脱离浏览器环境 直接运行 js 文件
  },
  "dependencies": {
    "vue": "^2.5.2"
  },
  "devDependencies": {
    
      ...
    
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

### 目录结构说明

梁兴华  http://doc.liangxinghua.com/vue-family/2.3.html 





# Vue CLI3 体验

### 与 2 的区别

3 与 2 有很大区别

1. vue-cli 2 对应 webpack 3;  vue-cli 3 对应 webpack 4
2. vue-cli 3 的设计原则是 '0 配置',  移除了配置文件根目录下的 build 和config 等目录
3. vue-cli 3 提供 vue ui 界面,  可视化配置
4. vue-cli 3 移除了 static 目录, 新增 public ,  并把 index.html 移到 public 内

### 初始化项目

基于 Vue CLI3 或更新版本 创建一个 hello-vue-cli-gte-3 项目

```bash
$ vue create hello-vue-cli-gte-3

# 会有根据输入提示:
	Please pick a preset: (Use arrow keys)
        default (babel, eslint)     (默认只选中两个)
        > Manually select features  (回车, 进入手动选择特性的命令界面)
             (*) Babel
             ( ) TypeScript
             ( ) Progressive Web App (PWA) Support
             ( ) Router
             ( ) Vuex
             ( ) CSS Pre-processors
             (*) Linter / Formatter
             ( ) Unit Testing
             ( ) E2E Testing
    Where do you prefer placing config for Babel, ESLint, etc.? (Use arrow keys)
        > In dedicated config files  (放到独立的配置文件里. 先选择此项) 
          In package.json            (放到 package.json 里)
    Save this as a preset for future projects? (y/N)  (是否保存此次预设)
```

运行本地开发服务:

```bash
$ npm run serve
```

### 看一下 mian.js

```javascript
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)  //h ===> createElement
}).$mount('#app')  //等同于===> el: "#app"
```

### 配置怎么定义 ?

vue cli 3 里把很多配置放在 cli-service 里了:

```
node_modules/@vue/cli-service/webpack.config.js
node_modules/@vue/cli-service/lib/Service.js
```

a. 第一种方式:  在 vue ui 命令启动的web界面上修改配置

b.第二种方式:  在当前项目根目录下创建一个 `vue.config.js`,  写入:

```javascript
// 文件名不能改
// 内容是用户自定义配置, 会被vue读取并更新
module.exports = {
  // ...
}
```


