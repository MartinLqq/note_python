# 封装 TabBar 组件

看B站视频教程.

注意的内容包括:

1. 如何一步步封装一个独立的组件?
2. 项目/组件的目录层次怎么划分更好?
3. vue-cli3 怎么给路径起别名?
4. 怎么在 `<style>` 标签内部使用导入的方式,  导入 CSS 等样式文件?
5. 怎么给子组件传参?
6. 怎么使用 VueRouter ?
7. 怎么通过编程式的导航,  通过代码跳转路由
8. 为什么在 `<slot>` 标签里写 `v-if` 有效,  而 `:class="{active: isActive}"` 无效 ?
9. 如何注册一个全局的前置守卫 ?



效果图

<img src="G:/Important重要/Learning-Notes/前端/Vue_模块化开发/images/tabbar/tabbar效果图.jpg" alt="tabbar效果图" style="zoom: 80%;" />





# tab-bar

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

