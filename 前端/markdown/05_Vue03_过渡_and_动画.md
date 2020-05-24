# ==== Vue 过渡 & 动画 ====

 https://cn.vuejs.org/v2/guide/transitions.html 



# 进入/离开 & 列表过渡

Vue 在插入、更新或者移除 DOM 时，提供多种不同方式的应用过渡效果。
 包括以下工具： 

- 在 CSS 过渡和动画中自动应用 class
- 可以配合使用第三方 CSS 动画库，如 **Animate.css**
- 在过渡钩子函数中使用 JavaScript 直接操作 DOM
- 可以配合使用第三方 JavaScript 动画库，如 Velocity.js

在这里，我们只会讲到进入、离开和列表的过渡.



## 单元素/组件的过渡 

Vue 提供了 `transition` 的封装组件，在下列情形中，可以给任何元素和组件添加 entering/leaving 过渡 

- 条件渲染 （使用 `v-if`）	 
- 条件展示 （使用 `v-show`）	 
- 动态组件	 
- 组件根节点 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <style>
        .fade-enter-active, .fade-leave-active {
            transition: opacity .5s
        }
        .fade-enter, .fade-leave-active {
            opacity: 0
        }
    </style>
</head>
<body>
    <div id="app">
        <button v-on:click="show = !show">Toggle</button>
        <transition name="fade">
            <p v-if="show">hello</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
        })
    </script>
</body>
</html>
```

元素封装成过渡组件之后，在遇到插入或删除时，Vue 将 

1. 自动嗅探目标元素是否有 CSS 过渡或动画，并在合适时添加/删除 CSS 类名。		 
2. 如果过渡组件设置了过渡的 JavaScript 钩子函数，会在相应的阶段调用钩子函数。		 
3. 如果没有找到 JavaScript 钩子并且也没有检测到 CSS 过渡/动画，DOM 操作（插入/删除）在下一帧中立即执行。(注意：此指浏览器逐帧动画机制，与 Vue，和Vue的 `nextTick` 概念不同) 





### 过渡的-CSS-类名 

会有 4 个(CSS)类名在 enter/leave 的过渡中切换 

1. `v-enter`: 定义进入过渡的开始状态。在元素被插入时生效，在下一个帧移除。		 
2. `v-enter-active`: 定义进入过渡的结束状态。在元素被插入时生效，在 `transition/animation` 完成之后移除。		 
3. `v-leave`:  定义离开过渡的开始状态。在离开过渡被触发时生效，在下一个帧移除。		 
4. `v-leave-active`: 定义离开过渡的结束状态。在离开过渡被触发时生效，在 `transition/animation` 完成之后移除。

![Transition Diagram](https://cn.vuejs.org/images/transition.png)



### CSS 过渡 

常用的过渡都是使用 CSS 过渡。 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <style>
        /* 可以设置不同的进入和离开动画 */
        /* 设置持续时间和动画函数 */
        .slide-fade-enter-active {
            transition: all .3s ease;
        }
        .slide-fade-leave-active {
            transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
        }
        .slide-fade-enter, .slide-fade-leave-active {
            padding-left: 10px;
            opacity: 0;
        }
    </style>
</head>
<body>
    <div id="app">
        <button v-on:click="show = !show">Toggle</button>
        <transition name="slide-fade">
            <p v-if="show">hello</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
        })
    </script>
</body>
</html>
```





### CSS 动画 

CSS 动画用法同 CSS 过渡，区别是在动画中 `v-enter` 类名在节点插入 DOM 后不会立即删除，而是在 `animationend` 事件触发时删除。 

​	示例： (省略了兼容性前缀) 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <style>
        .bounce-enter-active {
            animation: bounce-in .5s;
        }
        .bounce-leave-active {
            animation: bounce-out .5s;
        }
        @keyframes bounce-in {
            0% {
                transform: scale(0);
            }
            50% {
                transform: scale(1.5);
            }
            100% {
                transform: scale(1);
            }
        }
        @keyframes bounce-out {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.5);
            }
            100% {
                transform: scale(0);
            }
        }
    </style>
</head>
<body>
    <div id="app">
        <button v-on:click="show = !show">Toggle</button>
        <transition name="bounce">
            <p v-if="show">hello</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
        })
    </script>
</body>
</html>
```



### 自定义过渡类名 

我们可以通过以下特性来自定义过渡类名： 

- `enter-class` 	
- `enter-active-class` 	
- `leave-class` 	
- `leave-active-class` 	

他们的优先级高于普通的类名，这对于 Vue 的过渡系统和其他第三方 CSS 动画库，如 [Animate.css](https://daneden.github.io/animate.css/) 结合使用十分有用。 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <link href="https://unpkg.com/animate.css@3.5.1/animate.min.css" rel="stylesheet" type="text/css">
    <style>
        .bounce-enter-active {
            animation: bounce-in .5s;
        }
        .bounce-leave-active {
            animation: bounce-out .5s;
        }
        @keyframes bounce-in {
            0% {
                transform: scale(0);
            }
            50% {
                transform: scale(1.5);
            }
            100% {
                transform: scale(1);
            }
        }
        @keyframes bounce-out {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.5);
            }
            100% {
                transform: scale(0);
            }
        }
    </style>
</head>
<body>
    <div id="app">
        <button @click="show = !show">Toggle render</button>
        <transition
        name="custom-classes-transition"
        enter-active-class="animated tada"
        leave-active-class="animated bounceOutRight">
            <p v-if="show">hello</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
        })
    </script>
</body>
</html>
```





### 同时使用 Transitions 和 Animations 

Vue 为了知道过渡的完成，必须设置相应的事件监听器。它可以是 `transitionend` 或 `animationend` ，这取决于给元素应用的 CSS 规则。如果你使用其中任何一种，Vue 能自动识别类型并设置监听。 

​	但是，在一些场景中，你需要给同一个元素同时设置两种过渡动效，比如 `animation` 很快的被触发并完成了，而 `transition` 效果还没结束。在这种情况中，你就需要使用 `type` 特性并设置 `animation` 或 `transition` 来明确声明你需要 Vue 监听的类型。 



### JavaScript 钩子 

可以在属性中声明 JavaScript 钩子 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <!-- <link href="https://unpkg.com/animate.css@3.5.1/animate.min.css" rel="stylesheet" type="text/css"> -->
</head>
<body>
    <div id="app">
        <button @click="show = !show">Toggle render</button>
        <transition
        v-on:before-enter="beforeEnter"
        v-on:enter="enter"
        v-on:after-enter="afterEnter"
        v-on:enter-cancelled="enterCancelled"
        v-on:before-leave="beforeLeave"
        v-on:leave="leave"
        v-on:after-leave="afterLeave"
        v-on:leave-cancelled="leaveCancelled">
            <p v-if="show">hello</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
            methods: {
                beforeEnter: function (el) {
                    // ...
                    console.log('beforeEnter');
                },
                // 此回调函数是可选项的设置, 与 CSS 结合时使用
                enter: function (el, done) {
                    // ...
                    done()
                },
                afterEnter: function (el) { },
                enterCancelled: function (el) { },

                beforeLeave: function (el) { },
                // 此回调函数是可选项的设置, 与 CSS 结合时使用
                leave: function (el, done) {
                    // ...
                    done();
                },
                afterLeave: function (el) { },
                // leaveCancelled 只用于 v-show 中
                leaveCancelled: function (el) { }
            }
        })
    </script>
</body>
</html>
```

这些钩子函数可以结合 CSS `transitions/animations` 使用，也可以单独使用。 

​	当只用 JavaScript 过渡的时候，  **在 `enter` 和 `leave` 中，回调函数 `done` 是必须的** 。 否则，它们会被同步调用，过渡会立即完成。 

​	推荐对于仅使用 JavaScript 过渡的元素添加 `v-bind:css="false"`，Vue 会跳过 CSS 的检测。这也可以避免过渡过程中 CSS 的影响。 

​	一个使用 Velocity.js 的简单例子： 

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <!--
    Velocity works very much like jQuery.animate and is
    a great option for JavaScript animations
    -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/velocity/1.2.3/velocity.min.js"></script>
</head>
<body>
    <div id="app">
        <button @click="show = !show">Toggle</button>
        <transition
        v-on:before-enter="beforeEnter"
        v-on:enter="enter"
        v-on:leave="leave"
        v-bind:css="false">
            <p v-if="show">Demo</p>
        </transition>
    </div>

    <script>
        var vm = new Vue({
            el: '#app',
            data: {
                show: true
            },
            methods: {
                beforeEnter: function (el) {
                    el.style.opacity = 0
                },
                enter: function (el, done) {
                    Velocity(el, { opacity: 1, fontSize: '1.4em' }, { duration: 300 })
                    Velocity(el, { fontSize: '1em' }, { complete: done })
                },
                leave: function (el, done) {
                    Velocity(el, { translateX: '15px', rotateZ: '50deg' }, { duration: 600 })
                    Velocity(el, { rotateZ: '100deg' }, { loop: 2 })
                    Velocity(el, {
                        rotateZ: '45deg',
                        translateY: '30px',
                        translateX: '30px',
                        opacity: 0
                    }, { complete: done })
                }
            }

        })
    </script>
</body>
</html>
```





# ==== TODO ====

## 初始渲染的过渡 

## 多个元素的过渡 

### 过渡模式 

## 多个组件的过渡 

## 列表过渡 

### 列表的进入和离开过渡 

### 列表的位移过渡 

### 列表的渐进过渡 

## 可复用的过渡 

## 动态过渡 

# 过渡状态

## 状态动画 与 watcher 

## 动态状态转换 

## 通过组件组织过渡 