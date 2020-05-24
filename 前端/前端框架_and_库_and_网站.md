# ==== 前端框架/库 ====

```
介绍
官网
文档
说明
```

# Node.js

介绍: 

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境。Node.js 使用了一个事件驱动、非阻塞式 I/O 的模型，使其轻量又高效。 

Node.js 是一个后端语言，它的语法和 JavaScript 类似，所以可以说它是属于前端的后端语言，后端语言和前端语言的区别：

- 运行环境：后端语言一般运行在服务器端，前端语言运行在客户端的浏览器上
- 功能：后端语言可以操作文件，可以读写数据库，前端语言不能操作文件，不能读写数据库。

使用文档

[Node.js v12.16.1 文档](http://nodejs.cn/api/)

下载和安装

- nodejs 中文:    http://nodejs.cn/download/ 
- 例如:  下载:  node-v12.16.1-x64.msi
- 安装时选择同时安装 npm

使用 cnpm 加速

```bash
# 同理 nvm , npm 默认是从国外的源获取和下载包信息, 慢. 可以通过简单的 ---registry 参数, 使用国内的镜像 http://registry.npm.taobao.org :
npm install koa --registry=http://registry.npm.taobao.org

# 但是毕竟镜像跟官方的 npm 源还是会有一个同步时间差异, 目前 cnpm 的默认同步时间间隔是 10 分钟. 如果你是模块发布者, 或者你想马上同步一个模块, 那么推荐你安装 cnpm cli:
npm install cnpm -g --registry=http://registry.npm.taobao.org
```





# NPM

介绍: 

> **n**ode **p**ackages **m**anager

npm 是 node.js 的包管理器，安装了 node.js 同时会自动安装 npm，可以 npm 命令来安装 node.js 的包。这个工具相当于python 的 pip 管理器。

```
npm 由三个独立的部分组成：
    网站:  开发者查找包（package）、设置参数以及管理 npm 使用体验的主要途径。
    注册表（registry）:  一个巨大的数据库，保存了每个包（package）的信息。
    命令行工具 (CLI):  通过命令行或终端运行。开发者通过 CLI 与 npm 打交道。
```

官网:   https://www.npmjs.cn/ 

文档:    https://www.npmjs.cn/ 



# Bootstrap

介绍： 

Bootstrap 是全球最受欢迎的前端组件库，用于开发响应式布局、移动设备优先的 WEB 项目。Bootstrap 是一个用于 HTML、CSS 和 JS 开发的开源工具包。利用 Bootstrap 提供的 Sass 变量和混合（mixins）、响应式栅格系统、可扩展的预制组件以及强大的 jQuery 插件，能够让你快速地开发出产品原型或构建整个 app。 

官网:  Bootstrap 中文网, https://www.bootcss.com/ 

文档：

1. Bootstrap3中文文档：  https://v3.bootcss.com/
2. Bootstrap4中文文档： https://v4.bootcss.com/

说明：

-   **Bootstrap 中文网主页 有 Bootstrap 相关优质项目/框架推荐 (涉及本 md 文件记录的许多内容)**
-   Bootstrap 依赖 JQuery



# Vue 生态

### Vue

介绍

Vue 是一套用于构建用户界面的**渐进式框架**。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。Vue 的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。另一方面，当与[现代化的工具链](https://cn.vuejs.org/v2/guide/single-file-components.html)以及各种[支持类库](https://github.com/vuejs/awesome-vue#libraries--plugins)结合使用时，Vue 也完全能够为复杂的单页应用提供驱动。 

官网:   https://vuejs.org/ 

文档:   

- 教程:  https://cn.vuejs.org/v2/guide/ 
- API:   https://cn.vuejs.org/v2/api/ 
- Cookbook:   https://cn.vuejs.org/v2/cookbook/ 

说明

> 工具:
>
> - [Devtools](https://github.com/vuejs/vue-devtools)
> - [Vue CLI](https://cli.vuejs.org/zh/)
> - [Vue Loader](https://vue-loader.vuejs.org/zh/)
>
> 核心插件:
>
> - [Vue Router](https://router.vuejs.org/zh/)
> - [Vuex](https://vuex.vuejs.org/zh/)
> - [Vue 服务端渲染](https://ssr.vuejs.org/zh/)



### webpack

介绍:

 本质上，*webpack* 是一个现代 JavaScript 应用程序的*静态模块打包器(module bundler)*。当 webpack 处理应用程序时，它会递归地构建一个*依赖关系图(dependency graph)*，其中包含应用程序需要的每个模块，然后将所有这些模块打包成一个或多个 *bundle*。 
官网:   https://www.webpackjs.com/
文档:  https://www.webpackjs.com/concepts/ 

### vue-cli

- 官方:  https://cli.vuejs.org/zh/guide/ 
- [梁兴华 vue-cli](http://doc.liangxinghua.com/vue-family/2.html )

Vue CLI 是一个基于 Vue.js 进行快速开发的完整系统，提供：

- 通过 `@vue/cli` 搭建交互式的项目脚手架。
- 通过 `@vue/cli` + `@vue/cli-service-global` 快速开始零配置原型开发。
- 一个运行时依赖 (`@vue/cli-service`)，该依赖：
  - 可升级；
  - 基于 webpack 构建，并带有合理的默认配置；
  - 可以通过项目内的配置文件进行配置；
  - 可以通过插件进行扩展。
- 一个丰富的官方插件集合，集成了前端生态中最好的工具。
- 一套完全图形化的创建和管理 Vue.js 项目的用户界面。



### vue-router

-  [官方文档](https://router.vuejs.org/zh/) 
- [梁兴华 vue-router](http://doc.liangxinghua.com/vue-family/3.html )

Vue Router 是 Vue.js 官方的路由管理器。它和 Vue.js 的核心深度集成，让构建单页面应用变得易如反掌。
包含的功能有：

- 嵌套的路由/视图表
- 模块化的、基于组件的路由配置
- 路由参数、查询、通配符
- 基于 Vue.js 过渡系统的视图过渡效果
- 细粒度的导航控制
- 带有自动激活的 CSS class 的链接
- HTML5 历史模式或 hash 模式，在 IE9 中自动降级
- 自定义的滚动条行为

### vuex

-  [vuex官方文档](https://vuex.vuejs.org/zh/) 
- [梁兴华 vuex]( http://doc.liangxinghua.com/vue-family/4.html )

vuex是一个专为 Vue.js 应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。chrome安装调试工具 devtools extension 

### axios

- [官方文档](https://www.kancloud.cn/yunye/axios/234845) 
- [梁兴华 axios](http://doc.liangxinghua.com/vue-family/5.html)



###  Vue相关开源项目库汇总

Github 仓库:   awesome-github-vue:   https://github.com/opendigg/awesome-github-vue 



### ESLint

介绍: ESLint 是 一个插件化的javascript代码检测工具,  它的目标是保证代码的一致性和避免错误。 ESLint 主要在命令行中使用。

官网:  https://cn.eslint.org/ 

文档:   https://cn.eslint.org/docs/user-guide/getting-started 





### vue-simple-uploader

A Vue.js upload component powered by [simple-uploader.js](https://github.com/simple-uploader/Uploader) 

- 支持文件、多文件、文件夹上传
- 支持拖拽文件、文件夹上传
- 统一对待文件和文件夹，方便操作管理
- 可暂停、继续上传
- 错误处理
- 支持“快传”，通过文件判断服务端是否已存在从而实现“快传”
- 上传队列管理，支持最大并发上传
- 分块上传
- 支持进度、预估剩余时间、出错自动重试、重传等操作

#  [awesome-vue](https://github.com/vuejs/awesome-vue)

A curated list of awesome things related to Vue.js 



# UI 组件库

### Element UI

- 看文档:  https://element.eleme.cn/ 
- **看源码**:   https://github.com/ElemeFE/element 

Element UI 是一套采用 Vue 2.0 作为基础框架实现的组件库，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的组件库，提供了配套设计资源，帮助网站快速成型 

类似的有:

- [iView](https://cloud.tencent.com/developer/doc/1271):  一套基于 Vue.js 的开源 UI 组件库，主要服务于 PC 界面的中后台产品 
- [Mint UI](https://cloud.tencent.com/developer/doc/1273):  基于 Vue.js 的移动端组件库

### Vant

 https://youzan.github.io/vant/#/zh-CN/ 

 轻量、可靠的移动端 Vue 组件库 

Vant 生态

| 项目                                                         | 描述                       |
| :----------------------------------------------------------- | :------------------------- |
| [vant-demo](https://github.com/youzan/vant-demo)             | Vant 官方示例合集          |
| [vant-weapp](https://github.com/youzan/vant-weapp)           | 微信小程序组件库           |
| [vant-cli](https://github.com/youzan/vant/tree/dev/packages/vant-cli) | 开箱即用的组件库搭建工具   |
| [vant-icons](https://github.com/youzan/vant/tree/dev/packages/vant-icons) | Vant 图标库                |
| [vant-touch-emulator](https://github.com/youzan/vant/tree/dev/packages/vant-touch-emulator) | 在桌面端使用 Vant 的辅助库 |



### Cube UI

基于 Vue.js 实现的精致移动端组件库 

https://didi.github.io/cube-ui/#/zh-CN



### Better-Scroll

BetterScroll 是一款重点解决移动端（已支持 PC）各种滚动场景需求的插件。它的核心是借鉴的 [iscroll](https://github.com/cubiq/iscroll) 的实现，它的 API 设计基本兼容 iscroll，在 iscroll 的基础上又扩展了一些 feature 以及做了一些性能优化。

Github 地址:    https://github.com/ustbhuangyi/better-scroll/blob/dev/README_zh-CN.md 

# animate.css

- github:   https://github.com/daneden/animate.css

第三方 CSS 动画库





# [Sphinx ](https://www.sphinx.org.cn/)

Sphinx 是一个用于构建文档的工具，最初是为 Python 文档而开发的。

类似:

- Gitbook

# [Chart.js](https://chartjs.bootcss.com/)

开源的 HTML5 图表工具

Chart.js 是为设计和开发人员准备的简单、灵活的 JavaScript 图表工具。



# Lavas

 Lavas 是一套基于 Vue 的 **PWA** 解决方案，能够帮助开发者快速搭建 PWA 应用，解决接入 PWA 的各种问题，对提升用户体验，用户留存率等有明显提升，且开发者无须过多的关注 PWA 开发本身。 







#  VuePress

 https://www.vuepress.cn/guide/ 



# dragula

dragula是一个开源（MIT协议）JavaScript 拖放功能插件，支持每一个健全的浏览器，文档丰富、配置简单。支持触摸事件，无需任何配置即可无缝的处理点击。







# ==== 前端开发辅助网站 ====

# 颜色/icon

www.materialpalette.com/colors

# jQuery 之家

http://www.htmleaf.com/



包含多种前端开发内容,  帮助我们迅速实现 华丽布局/华丽特效

1. JQUERY 库
2. HTML5 库
3. CSS3 库
4. ...