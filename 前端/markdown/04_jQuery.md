# JQuery 必知

- **手册为主  手册为准**
- 手册网jQuery 教程:   http://www.shouce.ren/api/view/a/1520 

JQuery 库涉及: 

- HTML 元素选取
- HTML 元素操作
- CSS 操作
- HTML 事件函数
- JavaScript 特效和动画
- HTML DOM 遍历和修改
- AJAX
- Utilities
- 大量的插件



# (一)  JQuery入门

原生 Js 与 Js库的比较: 
​	使用原生 js 会出现浏览器兼容性问题,  js库如 JQuery, vue.js 封装功能,  基本兼容各浏览器;
​	JQuery性能更好

jQuery是目前使用最广泛的 javascript 函数库,  是一个 js 文件,  页面用 script 标签引入这个 js 文件就可以使用。
jquery库文件可在官网下载

## 1 设置 jquery文档加载完再执行

- 专门用一个<script>标签导入jquery库

  ```javascript
  <script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js"></script>
  ```

- 设置文档加载完再执行

  将获取元素的语句写到页面头部，会因为元素还没有加载而出错，jquery提供了ready方法解决这个问题，它的速度比原生的 window.onload 更快。

  ```javascript
  <script type="text/javascript">
  $(document).ready(function(){
       ......
  });
  </script>
  ```

  **可以简写为：**

  ```javascript
  <script type="text/javascript">
  $(function(){
       // 代码都在这里写
  });
  </script>
  ```
  

##2 jquery选择器

####选择规则 与 CSS 选择器规则相同

  ```javascript
  $('#myId') //选择id为myId的网页元素
  $('.myClass') // 选择class为myClass的元素
  $('li') //选择所有的li元素
  $('#ul1 li span') //选择id为为ul1元素下的所有li下的span元素
  $('input[name=first]') // 选择name属性等于first的input元素
  	--- CSS中也[可以]用input[name=first]选择标签并指定样式
  ```


####选择集过滤

  ```javascript
  $('div').has('p'); // 选择包含p元素的div元素
  $('div').not('.myClass'); //选择class不等于myClass的div元素
  $('div').eq(5); //选择第6个div元素
  ```

####选择集转移

  ```javascript
  $('#box').prev(); //选择id是box的元素前面紧挨的同辈元素
  $('#box').prevAll(); //选择id是box的元素之前所有的同辈元素

  $('#box').next(); //选择id是box的元素后面紧挨的同辈元素
  $('#box').nextAll(); //选择id是box的元素后面所有的同辈元素

  $('#box').parent(); //选择id是box的元素的父元素
  $('#box').children(); //选择id是box的元素的所有子元素
  $('#box').siblings(); //选择id是box的元素的同级元素 (除了自己)
  	---- siblings: 反选兄弟姐妹 (除了自己)

  $('#box').find('.myClass'); //选择id是box的元素内的class等于myClass的元素
  ```

#### 判断是否选择到了元素 .length

--- obj.length >= 1
jquery有容错机制，即使没有找到元素，也不会出错，可以用length属性来判断是否找到了元素, length等于0，就是没选择到元素，length大于0，就是选择到了元素。

```javascript
var $div1 = $('#div1');
var $div2 = $('#div2');
alert($div1.length); // 弹出1
alert($div2.length); // 弹出0
......
<div id="div1">这是一个div</div>
```



##3 jquery的样式操作

####操作行间样式.css({}) 

- 读

  ```javascript
  $('div').css('width');
  $('div').css('color');
  -- 一次只能获取一个值(第一个)
  ```

- 写  (修改 | 添加)

  - **有则覆盖, 无则添加**

  ```javascript
  $("div").css("width","30px");
  $("div").css("height","30px");
  $("div").css( {fontSize:"30px",color:"red"} );
  ```



####操作样式类名

- 先选择好元素

添加样式类 ---- .addClass()

```javascript
$("#div1").addClass("divClass2") //为id为div1的对象追加样式divClass2
```

删除样式类 ---- .removeClass()

```javascript
$("#div1").removeClass("divClass")  //移除id为div1的对象的class名为divClass的样式
```

删除多个样式类 ---- .removeClass()

```javascript
$("#div1").removeClass("divClass divClass2") //移除多个样式
```

重复切换样式

```javascript
$("#div1").toggleClass("anotherClass") //重复切换anotherClass样式
```



##4 jquery的click事件

####绑定click事件 .click(  function(){}  )

```javascript
$('#btn1').click(function(){
    // 内部的this指的是原生对象
    // 而使用jquery对象需要用   $(this)
})
```

####获取元素的索引值 .index()

​	有时候需要获得匹配元素 **相对于其同胞元素** 的索引位置，此时可以用index()方法获取
​	根据指定索引获取标签元素:	$('div').eq(5); //选择第6个div元素

```javascript
var $li = $('.list li').eq(1);
alert($li.index()); // 弹出1
......
<ul class="list">
    <li>1</li>
    <li>2</li>
    <li>4</li>
    <li>5</li>
    <li>6</li>
</ul>
```



##5 jquery动画

#### .animate()方法

​	通过animate方法可以设置元素某属性值上的动画，可以设置一个或多个属性值，动画执行完成后会执行一个函数。

```javascript
/*
    animate参数：
    参数一：要改变的样式属性值，写成字典的形式
    参数二：动画持续的时间，单位为毫秒，一般不写单位
    参数三：动画曲线，默认为‘swing’，缓冲运动，还可以设置为‘linear’，匀速运动
    参数四：动画回调函数，动画完成后执行的匿名函数
*/

$('#div1').animate(
    { width:300, height:300 },
    1000,
    'swing',
    () => alert('done!')
);
```




###### 

###### 

###### 

# (二)  JQuery进阶

## 1 jquery特殊效果

```javascript
$btn.click(function(){
	$('#div1').fadeIn(1000,'swing',function(){
		alert('done!');
	});
});

参数1		动画效果完成时间
参数2		"swing"表示缓冲效果, "linear"表示匀速效果
参数3		动画效果完成后自动执行的函数
```

fadeIn()			 淡入
fadeOut()	 	淡出
fadeToggle()	 	切换淡入淡出

hide()		 	隐藏元素
show()		 	显示元素
toggle()		 	切换可见状态

slideDown()		 向下展开
slideUp()		 向上卷起
slideToggle()	 依次展开或卷起某个元素



## 2 链式调用

**jquery对象的方法会在执行完后返回这个jquery对象**，jquery对象的方法可以连起来写



## 3 属性操作

1、html() 取出或设置html内容

```javascript
// 取出html内容		标签对象.html()
var htm = ('#div1').html();

// 设置html内容		标签对象.html('str')
$('#div1').html('<span>添加文字</span>');

// 注意: 原生js中的innerHTML, innerText 是属性, 不是方法, 与JQuery的html()不同.
```

2、prop() 取出或设置某个属性的值

```javascript
// 获取属性值		标签对象.prop('属性名')
var src = ('#img1').prop('src');

// 设置属性值		标签对象.prop({属性名:"属性值", 属性名:"属性值"})
$('#img1').prop({src: "test.jpg", alt: "Test Image" });
```

3、设置多个属性/值对

为被选元素设置一个以上的属性和值。

```
$(selector).attr({attribute:value, attribute:value ...})
```



## 4 jquery循环

#### jQuery 遍历 - each() 方法

输出每个 li 元素的文本：

```
$("button").click(function(){
  $("li").each(function(){
  
    alert($(this).text())
    
  });
});
```

#### 定义和用法

each() 方法规定为每个匹配元素规定运行的函数。

**提示**：返回 false 可用于提前停止循环。





## 5 jquery事件

事件冒泡

事件函数

```javascript
blur() 	元素失去焦点		blur---模糊,失去焦点
focus() 元素获得焦点

click() 鼠标单击
mouseover() 鼠标进入（进入子元素也触发）
mouseout() 	鼠标离开（离开子元素也触发）
-- mouseenter() 	鼠标进入（进入子元素不触发）
-- mouseleave() 	鼠标离开（离开子元素不触发）
-- hover() 			同时为mouseenter和mouseleave事件指定处理函数

ready() DOM加载完成
submit() 用户递交表单
```



## 6 表单验证

js中 一个正则是一个对象
正则只作用于 字符串类型数据

#### **正则表达式的写法**

```javascript
var re=new RegExp('规则', '可选参数');  // new一个正则对象
或
var re=/规则/参数;
```

#### **规则中的字符**

1）普通字符匹配：

如：/a/ 匹配字符 ‘a’，/a,b/ 匹配字符 ‘a,b’



2）转义字符匹配：

\d	 匹配一个数字，即0-9
\D 	匹配一个非数字，即除了0-9
\w	 匹配一个单词字符（字母、数字、下划线）
\W	 匹配任何一个非单词字符。等价于`[^A-Za-z0-9_]`
\s 	匹配一个空白符
\S 	匹配一个非空白符
\b 	匹配单词边界
\B 	匹配非单词边界
. 	匹配一个任意字符

```javascript
var sTr01 = '123456asdf';	# 待验证字符串
var re01 = /\d+/;			# 验证规则
//匹配纯数字字符串
var re02 = /^\d+$/;
alert(re01.test(sTr01)); //弹出true		# 获取验证结果
alert(re02.test(sTr01)); //弹出false
```

#### 匹配前一个字符指定个数

```javascript
? 出现零次或一次（最多出现一次）
+ 出现一次或多次（至少出现一次）
* 出现零次或多次（任意次）
{n} 出现n次
{n,m} 出现n到m次
{n,} 至少出现n次
```

#### **任意一个或者范围**

```javascript
[abc123] : 匹配‘abc123’中的任意一个字符
[a-z0-9] : 匹配a到z或者0到9中的任意一个字符
```

#### **限制开头结尾**

```javascript
^ 以紧挨的元素开头
$ 以紧挨的元素结尾
```

#### **修饰参数**

g： global，全文搜索，默认搜索到第一个结果接停止
i： ingore case，忽略大小写，默认大小写敏感



#### **常用函数 **

**正则.test('str')**

用法：正则.test(字符串) 匹配成功，就返回true，否则就返回false



**正则默认规则 **
匹配成功就结束，不会继续匹配，区分大小写

**常用正则规则**

```javascript
//用户名验证：(数字字母或下划线6到20位)
var reUser = /^\w{6,20}$/;

//邮箱验证：        
var reMail = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/i;

//密码验证：
var rePass = /^[\w!@#$%^&*]{6,20}$/;

//手机号码验证：
var rePhone = /^1[34578]\d{9}$/;
```







###### 

###### 



# (三)  JQuery高级

## 1 事件冒泡

#### **什么是事件冒泡 **

​	在一个对象上触发某类事件（比如单击onclick事件），如果此对象定义了此事件的处理程序，那么此事件就会调用这个处理程序，如果**没有定义此事件处理程序** 或者 **事件返回true**，那么这个事件会向这个对象的父级对象传播，从里到外，直至它被处理（父级对象所有同类事件都将被激活），或者它到达了对象层次的最顶层，即document对象（有些浏览器是window）。

#### **事件冒泡的作用 **

​	事件冒泡允许多个操作被集中处理（把事件处理器添加到一个父级元素上，避免把事件处理器添加到多个子级元素上），它还可以让你在对象层的不同级别捕获事件。

#### **阻止事件冒泡 **

event.stopPropagation() 

```javascript
$(function(){
    // 事件冒泡 是按html结构来传递, 不是简单地按页面显示的层级
    $('.son').click(function(event){  // 传入一个参数,如:event
      console.log(1);
      // 阻止事件冒泡
      event.stopPropagation();
    })
    $('.father').click(function(){
      console.log(2);
      // 阻止事件冒泡的 常用写法
      // return false 同时有 阻止默认行为 的作用
      return false;
      // 注: 阻止事件冒泡 不会影响click事件的传递, 只是不产生效果
    })
    $('.grandfather').click(function(){
      console.log(3);
    })
    $(document).click(function(){
      console.log(4);
})
    
......

<div class="father">
    <div class="son">
        <div class="grandson"></div>
    </div>
</div>
```

#### **阻止默认行为 **-- 阻止表单提交

```javascript
$('#form1').submit(function(event){
    event.preventDefault();
})
```

#### **合并阻止操作**

实际开发中，一般把阻止冒泡和阻止默认行为合并起来写

```javascript
// event.stopPropagation();
// event.preventDefault();

// 合并写法：
return false;
```

经典案例: 页面弹框（点击弹框外弹框关闭）



## 2 事件委托

​	事件委托就是利用冒泡的原理，把事件加到父级上，通过判断事件来源的子集，执行相应的操作.

​	事件委托首先可以极大减少事件绑定次数，提高性能；

​	其次可以让新加入的子元素也可以拥有相同的操作。

#### **普通绑定事件的写法**

```javascript
$(function(){
    $ali = $('#list li');
    $ali.click(function() {
        $(this).css({background:'red'});
    });
})
...
<ul id="list">
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>5</li>
</ul>
```

#### **事件委托的写法**

```javascript
$(function(){
    $list = $('#list');
    // 注:  jQuery 3.0中已弃用此方法，请用 on()代替。
    $list.delegate('li', 'click', function() {
        $(this).css({background:'red'});
    });
})
...
<ul id="list">
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>5</li>
</ul>
```



## 3 Dom操作

元素节点操作 --- 改变html的标签结构:

1、移动现有标签的位置
2、将新创建的标签插入到现有的标签中

#### **创建新标签**

```javascript
var $div = $('<div>'); //创建一个空的div
var $div2 = $('<div>这是一个div元素</div>');

var $MyStr = "<span> my str </span>"
var $span = $($MyStr)
```

#### **移动或者插入标签的方法 **

1、append()		appendTo()：在现存元素的内部，从后面放入元素

```javascript
var $span = $('<span>这是一个span元素</span>');
$('#div1').append($span);
......
<div id="div1"></div>
```

2、prepend()	prependTo()：在现存元素的内部，从前面放入元素

3、after()		insertAfter()：在现存元素的外部，从后面放入元素

4、before()		insertBefore()：在现存元素的外部，从前面放入元素

#### 删除标签

```javascript
$('#div1').remove();
```



## 4 ajax

#### ajax的作用

```javascript
// 异步请求数据
// 利用JavaScript在保证页面不被整体刷新、页面链接不改变的情况下与服务器交换数据实现 局部刷新
// 像"没有界面的浏览器",  ajax可以自己发送http请求，不用通过浏览器的地址栏
```

#### ajax相关概念

##### > 数据接口

```javascript
数据接口 是 一个url地址, 是后台程序提供的
访问这个地址，可以请求对数据进行增、删、改、查，
最终会返回 json/text/xml 格式的数据或者操作信息
```

##### > 同步和异步

```javascript
程序中的同步和异步是把现实生活中的概念对调:
    程序中的同步: 一件事做完之后, 才能做另一件事
    程序中的异步: 两件事一起做
ajax是异步的, 同时可以做几件事, 访问的时候不会阻止程序往下执行
```

##### > 局部刷新 == 无刷新

```
局部刷新 == 无刷新
ajax可以实现局部刷新，也叫做无刷新，无刷新指的是整个页面不刷新，只是局部刷新
```



#### jquery中封装的ajax

```
jquery 将 ajax技术 封装成了一个函数 $.ajax({})，可以直接用这个函数来执行ajax请求
ajax需要在服务器环境下运行
$.ajax()函数的常用参数
```



三种写法

##### > 1 以前的写法

```javascript
// 1 以前的写法
$.ajax({
    url: '/change_data',	  // 请求地址
    type: 'GET',			 // 请求方式
    dataType: 'json',		 // 请求参数类型
    data:{'code':300268},	 // 请求参数
    success:function(resp){	 // 请求成功时执行的函数
		alert(resp.name);
	},
	error:function(){		// 请求失败时执行的函数
    	alert('服务器超时，请重试！');
	}
});
```

##### > 2 新写法 (推荐)

```javascript
// 2 新写法 (推荐)
$.ajax({
    url: '/change_data',
    type: 'GET',
    dataType: 'json',
    data:{'code':300268}
})
.done(function(resp) {  // 请求成功时执行的函数
	alert(resp.name);
})
.fail(function() {  // 请求失败时执行的函数
	alert('服务器超时，请重试！');
});
```

##### > 3 简写方式

```javascript
// 3 简写方式
// 按请求方式简写成$.get()  |  $.post()
$.get("/change_data", {'code':300268}, function(dat){
    alert(dat.name);
});

$.post("/change_data", {'code':300268}, function(dat){
  	alert(dat.name);
});
```

#### ajax在mini-Web中的使用 过程

```
<1> 运行服务器 (在服务器程序所在路径框中, 输入cmd打开控制台, 按指定方式运行服务器)
<2> 在 html 内部, 使用 jquery 库中的 $.ajax() 函数 向服务器发送请求
<3> 服务器分析请求的url, 调用mini-Web框架处理
<4> 框架从数据库读取数据, 组成json格式数据, 返回给$.ajax()函数
<5> 在$.ajax()的请求成功 (success:) 的 function 中, 使用参数接收数据, 使用 for 循环将数据内容拼接成 标签字符串
<6> 用 jquery 的 .html() 方法 把字符串放入html中
```

#### 问题

```
浏览器向服务器请求一个html页面, 为什么服务器会接收到多个请求 ?
```
