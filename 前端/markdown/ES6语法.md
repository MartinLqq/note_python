# ==== ES6语法 ====

ES6是JavaScript语言的新版本，它也可以叫做ES2015，之前学习的JavaScript属于ES5，ES6在它的基础上增加了一些语法，ES6是未来JavaScript的趋势，而且vue组件开发中会使用很多的ES6的语法，所以掌握这些常用的ES6语法是必须的。

# 变量声明 let 和 const

let和const是新增的声明变量的开头的关键字，在这之前，变量声明是用var关键字，这两个关键字和var的区别是，它们声明的变量没有预解析，let和const的区别是，let声明的是一般变量，const申明的常量，不可修改。

```javascript
alert(iNum01) // 弹出undefined
// alert(iNum02); 报错，let关键字定义变量没有变量预解析
// alert(iNum03); 报错，const关键字定义变量没有变量预解析

var iNum01 = 6;
// 使用let关键字定义变量
let iNum02 = 12;
// 使用const关键字定义变量
const iNum03 = 24;

alert(iNum01); // 弹出6
alert(iNum02); // 弹出12
alert(iNum03); // 弹出24

iNum01 = 7;
iNum02 = 13;
//iNum03 = 25; // 报错,const定义的变量不可修改,const定义的变量是常量

alert(iNum01)
alert(iNum02); 
alert(iNum03);
```

# 箭头函数

可以把箭头函数理解成匿名函数的第二种写法，箭头函数的作用是可以在对象中绑定this，解决了JavaScript中this指定混乱的问题。

```javascript
// 定义函数的一般方式
/*
function fnRs(a,b){
    var rs = a + b;
    alert(rs);
}
fnRs(1,2);        
*/

// 通过匿名函数赋值来定义函数
/*
var fnRs = function(a,b){
    var rs = a + b;
    alert(rs);
}
fnRs(1,2);
*/

// 通过箭头函数的写法定义
var fnRs = (a,b)=>{
    var rs = a + b;
    alert(rs);
}        
// fnRs(1,2);

// 一个参数可以省略小括号
var fnRs2 = a =>{
    alert(a);
}
fnRs2('haha!');

// 函数体只有一行代码时, 可以省略 {} 和 return
var mul = (num1, num2) => num1 * num2


// 箭头函数的作用，可以绑定对象中的this
// 箭头函数中会向外层作用域一层层查找 this, 直到有 this 的定义
// 例 1
<script>
    let obj = {
        show1(){
            // setTimeout 传普通函数
            setTimeout(function () {
                console.log(this);  //window
            },1000)
        },
        show2(){
            // setTimeout 传箭头函数
            setTimeout(()=>{
                console.log(this);  // obj
            },1000)
        }
    }
    obj.show1();
    obj.show2();
</script>

// 例 2
<script>
    let obj = {
        show(){
            setTimeout(function(){
                setTimeout(function () {
                    console.log(this);  //window
                })
                setTimeout(() => {
                    console.log(this);  //window
                })
            }, 1000)

            setTimeout(() => {
                setTimeout(function () {
                    console.log(this);  //window
                })
                setTimeout(() => {
                    console.log(this);  //obj
                })
            }, 1000)
        }
    }
    obj.show();
</script>
```

# 模块 import 和 export

javascript之前是没有模块的功能的，之前做js模块化开发，是用的一些js库来模拟实现的，在ES6中加入了模块的功能，和python语言一样，python中一个文件就是一个模块，ES6中，一个js文件就是一个模块，不同的是，js文件中需要先导出(export)后，才能被其他js文件导入(import)

```javascript
// model.js文件中导出
var person = {name:'tom',age:18}
export default {person}

// index.js文件夹中导入
import person from 'js/model.js'

// index.js中使用模块
person.name
person.age

/*
上面导出时使用了default关键字，如果不使用这个关键字，导入时需要加大括号：
import {person} from 'js/model.js'
*/
```

目前 ES6 的模块功能需要在服务器环境下才可以运行。



# 对象的简写

javascript对象在ES6中可以做一些简写形式，了解这些简写形式，才能方便我们读懂一些在javascript代码中简写的对象。

```javascript
let name = '李思';
let age = 18;

/*
var person = {
    name:name,
    age:age,
    showname:function(){
        alert(this.name);
    },
    showage:function(){
        alert(this.age);
    }
}
*/

// 简写成下面的形式
var person = {
    name,
    age,
    showname(){
      alert(this.name);
    },
    showage(){
      alert(this.age);
    }
}

person.showname();
person.showage();
```



# Promise

## 介绍和基本使用

Promise 是异步编程的一种解决方案

> 同步  synchronization
>
> 异步  asynchronization 

Promise最大的好处是在异步执行的流程中，把执行代码和处理结果的代码清晰地分离了

```javascript
new Promise((resolve, reject) => {
    // 模拟网络请求
    setTimeout(() => {
        resolve('200 OK');  // reject('400 Error!');
    }, 1000);
}).then(data => {
    console.log(data)
}).catch(error => {
    console.log(error)
});

// 或者在 .then() 的第二个参数直接传reject的处理函数:
.then(data => {
    console.log(data)
}, error => {
    console.log(error)
})
```

Promise还可以做更多的事情，比如，有若干个异步任务，需要先做任务1，如果成功后再做任务2，任何任务失败则不再继续并执行错误处理函数。

要串行执行这样的异步任务，不用Promise需要写一层一层的嵌套代码。有了Promise，我们只需要简单地写：

```javascript
job1.then(job2).then(job3).catch(handleError); 
// 其中，job1、job2和job3都是Promise对象。
```

例

```html
<div id="test-promise-ajax-result" style="border: solid 1px #ccc; padding: 1em; margin: 15px 0;">
    Result:
</div>


<script>
'use strict';
 
let ajax = (method, url, data) => {
    let request = new XMLHttpRequest();
    return new Promise( (resolve, reject) => {
        request.onreadystatechange = () => {
            if (request.readyState === 4) {
                if (request.status === 200) {
                    resolve(request.responseText);
                } else {
                    reject(request.status);
                }
            }
        };
        request.open(method, url);
        request.send(data);
    });
}
let log = document.getElementById('test-promise-ajax-result');
let p = ajax('GET', '/static/json/globalData.min.json');
p.then((text) => {
    log.innerText = text;
}).catch(status => {
    log.innerText = 'ERROR: ' + status;
});
</script>
```



## 三种状态

异步操作之后有三种状态

1. pending  等待状态,  比如正在进行网络请求,  或定时器没有到时间
2. fulfill  满足状态,  当我们主动调用 resolve(data) 方法时就处于该状态,  会回调 .then(func)
3. reject  拒绝状态,  当我们主动调用 reject(error)  方法就处于该状态,  会回调  .catch(func)





## 链式调用

> 1. 推荐链式调用方式2
> 2. 如果中间有哪一步 reject 了,  后面的链式调用不会执行,  直接走到 .catch(error)

链式调用方式1

```javascript
      new Promise((resolve, reject) => {
        // 第一次网络请求
        setTimeout(() => {
          resolve('200 OK'); //模拟请求成功, 传入响应内容
        }, 1000);
      }).then(data => {
          console.log(data)
          // 第二次网络请求
          return new Promise((resolve, reject) => {
            setTimeout(() => {
              reject('400 Error!'); //模拟请求失败, 传入响应内容
            }, 1000);
          }).catch(data => {
            console.log(data)
          })
      }).catch(error => {
          console.log(error)
      });
```



**链式调用方式2**

```javascript
new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve('200 OK')
    }, 1000)
}).then((data) => {
    // 处理...
    let newData = data + ' *** '
    console.log(newData)
    return new Promise(resolve => {   // 第 1 种链式返回: 返回 new Promise(func)
        resolve(newData)
    })
}).then(newData => {
    // 处理...
    let newNewData = newData + ' *** '
    console.log(newNewData)
    //return Promise.resolve(newNewData)  // 第 2 种链式返回: 返回 Promise.resolve(data)
    return Promise.reject('Error!')
}).then(newNewData => {
    // 处理...
    let data = newNewData + ' *** '
    return data                        // 第 3 种链式返回: 直接返回 data
}).then(data => {
    console.log(data)
    
}).catch(error => {
    console.log(error)
})
```



## all 方法

场景:  需求本身依赖两个请求,  必须两个请求都成功,  才可以执行后面的分析

```javascript
Promise.all([
    new Promise((resolve, reject) => {
        // 发送请求1
        setTimeout(() => {
            resolve('200 OK')
        }, 2000)
    }),

    new Promise((resolve, reject) => {
        // 发送请求2
        setTimeout(() => {
            reject('400 Error!')
            // resolve('200 OK too')
        }, 1000)
    })
])
.then(results => {
    console.log(results[0])
    console.log(results[1])
})
.catch(error => {
    console.log(error)
    console.log('Error! 2 requests must be all done')
})
```