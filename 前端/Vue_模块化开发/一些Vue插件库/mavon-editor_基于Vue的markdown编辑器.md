# mavon-editor

Github:   https://github.com/hinesboy/mavonEditor 



## -- markdown 编辑/显示

1. 安装

```bash
$npm install mavon-editor --save  --registry=http://registry.npm.taobao.org
```

2. Use (如何引入)

main.js

```
    // 全局注册
    // import with ES6
    import Vue from 'vue'
    import mavonEditor from 'mavon-editor'
    import 'mavon-editor/dist/css/index.css'
    // use
    Vue.use(mavonEditor)
    new Vue({
        'el': '#main',
        data() {
            return { value: '' }
        }
    })
```

.html / .vue

```
<div id="main">
    <mavon-editor v-model="value"/>
</div>
```





详细用法及配置见 Github

<div id="main">
    <mavon-editor v-model="value"/>
</div>