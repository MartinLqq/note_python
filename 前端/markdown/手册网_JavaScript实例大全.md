# 手册网_JavaScript实例大全 - 摘记

- 源版:   JavaScript实例大全:   http://www.shouce.ren/api/view/a/12180 
- this版:  过滤版

# 一.基础



## 在点击事件中获取对象的属性

```html
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
        <div id="div1" onclick="foo(this)">点我</div>
</body>
</html>

<script>
    var foo = function(obj){
        document.write(obj.id);
    }
</script>
```

## function 创建对象

```javascript
<script>
    function Foo(name, age){
        this.name = name;
        this.age = age;
        this.bar = function(){
            window.alert(this.name + ': ' + this.age);
        }
    }
    foo = new Foo("Martin", 26);
    foo.bar();

</script>
```

## 使用 with 省略对象名称

```javascript
<script>
    with(document){
        write('<h1>The usage of with statement</h1>');
    }
</script>
```

## 表单内容获取

```html
<html lang="en">
<head>
</head>
<body>
    <form name="form1" action="#">
        <input type="text" name="txt">
        <input type="button" value="显示" onclick="showText()">
    </form>
</body>
</html>
<script>
    function showText(){
        obj = document.form1.txt;  //获取 name='form1' 表单中 name="txt" 的一项
        alert('您输入的内容是: ' + obj.value);
    }
</script>
```

## 四舍五入、向下取整、向上取整

```javascript
<script>
    document.write( Math.round(1.5)); // 2
    document.write('<br />');
    document.write( Math.floor(1.8)); // 1
    document.write('<br />');
    document.write( Math.ceil(1.2) );  // 2
</script>
```



# 二.链接

## 超链接确认对话框

```html
<html lang="en">
<head>
</head>
<body>
    <a href="javascript:linkConfirm('http://www.shouce.ren')">手册网</a>
</body>
</html>

<script>
// <!--
    function linkConfirm(url){
        var question = confirm("您确认链接到 " + url + "?");
        if(question){
            location.href = url;
        }
    }
// -->
</script>
```

## 定时滚动超链接

```html
<html lang="en">
<head>
</head>
<body>
    <marquee direction="right" style="background: #6699CC"
    onmouseover="this.stop()"
    onmouseout="this.start()">
        <a href="#">超链接1</a>
        <a href="#">超链接2</a>
        <a href="#">超链接3</a>
    </marquee>
</body>
</html>
```



## 取得页面所有的超链接地址

```html
<html lang="en">
<head>
</head>
<script>
        function getLinks(){
            links = document.getElementsByTagName('a')
            console.log(links);
            for(i=0; i<links.length; i++){
                console.log(i + ": " + links[i].href);
            }
        }
</script>
<body onload="getLinks()">
    <a href="#">a</a>
    <a href="#">b</a>
    <a href="#">c</a>
</body>
</html>
```

## 从数组中随机选取一个值

```html
<html lang="en">
<head>
</head>
<body>
    <div>从数组中随机选取的值: <span></span></div>
</body>
</html>

<script>
    var randomChoice = function(arr){
        var random_float = Math.random() * arr.length;
        var random_int = Math.floor(random_float);
        return arr[random_int];
    }
    arr = new Array(1, 2, 3, 'a', 'b', 'c');
    result = randomChoice(arr);
    var span = document.getElementsByTagName('span')[0];
    span.innerText = result;
</script>
```



# 三.事件

## 单击、双击鼠标事件

```html
<html lang="en">
<head>
</head>
<body>
    <div onclick="alert('你单击了')">单击这一串文字...</div>
    <div ondblclick="alert('你双击了')">双击这一串文字...</div>
</body>
</html>
```

## 给网页设定快捷键

```html
<html lang="en">
<head>
</head>
<body>
    请在键盘上按 G/g 键, 或其他键试试看
    <div id='my-div'></div>
</body>
</html>

<script>
    function getKey(){
        var div = document.getElementById('my-div');
        var ascii = event.keyCode;
        key = String.fromCharCode(ascii);
        if (key == 'G'){
            div.innerText = '你按下了 G/g 键, 将会处理...';
        }else{
            div.innerText = '你按下了 [' + key + '] 键, 不会处理.';
        }
    }

    document.onkeydown = getKey;

</script>
```



## 跟着鼠标移动图片

```html
<html lang="en">
<head>
</head>
<body>
    <img src="https://www.baidu.com/favicon.ico" alt="百度icon图标" 
         id='pic' style="position:absolute;">
</body>
</html>

<script>
    function move(){
        var x = event.x;
        var y = event.y;
        img.style.left = x + 'px';
        img.style.top = y + 'px';
    }
    var img = document.getElementById('pic');
    console.log(img.style);

    document.onmousemove = move;

</script>
```



## 跟随鼠标逐个移动文字

```html
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>Document</title>
</head>
<body>
<script language="javascript">
	text = "跟随鼠标移动的文字";
	j = text.length - 1;
	mouseX = 0;
	mouseY = 0;
	function follow(){
		mouseX = event.x;
		mouseY = event.y;
	}
	function move(){
        var left = eval("t" + (j-1)).style.left;
        var top = eval("t" + (j-1)).style.top;
		eval("t" + j).style.left = parseInt(left) + 30;
		eval("t" + j).style.top  = parseInt(top);
		j--;
		if (j<1){
			j = text.length-1;
			t0.style.left = mouseX + 20;
			t0.style.top  = mouseY + 20;
		}
		setTimeout("move()", 5);
	}
    //文字拆分
	for(i=0;i<text.length;i++){
		str = "<div id=t" + i + " style='position:absolute;left=0;top=0;'>";
		str = str + text.charAt(i) + "</div>"
		document.write (str);
	}
    //监听鼠标移动事件, 实时修改坐标
    document.onmousemove = follow;
    move();

</script>
</body>
</html>
```



##  检查是否按下Ctrl、Alt、Shift键 

```html
<script>
	function showkey(){
		if(event.ctrlKey)alert("你按下了Ctrl键！");
		if(event.altKey)alert("你按下了Alt键！");
		if(event.shiftKey)alert("你按下了Shift键！");
	}
	document.onkeydown=showkey;
</script>
```

## 交换式图片按钮

```html
<html>
	<head>
		<title>交换式图片按钮
		</title>
	</head>
	<body>
		<img src="/upload/files/201612/1.jpg"
			 onMouseOver="this.src='/upload/files/201612/1.jpg'" 
			 onMouseOut="this.src='/upload/files/201612/2.jpg'">
	</body>
</html>
```

## 进入/离开网页时显示信息

```html
<html>
    <head>
        <title>进入、离开网页显示信息</title>
    </head>
    <body   
        onLoad="alert('您好，欢迎您的光临')" 
        onUnload="alert('您好，希望您下次再来')">
    </body>
</html>
```

## 禁用鼠标右键

```javascript
<script>
    function getButton(){
        if(event.button == 2){
            alert('鼠标右键已被禁用!');
        }
    }
    document.onmousedown = getButton;
</script>
```

绝对禁止单击鼠标右键

```html
<html>
    <head>
    	<title>绝对禁止单击鼠标右键</title>
    </head>
    	<body onContextMenu="alert('^_^不要偷看哦！');return false">
    绝对禁止用鼠标右键
    </body>
</html>
```



## 单击鼠标拖动文字

> 待解决的问题:  鼠标位置与第一个文字的坐标总是相同

```html
<html lang="en">
<head>
</head>
<body>
    <div id="myDiv" onclick="updateFlag()" style="position:absolute;cursor:pointer;">
        这是一串可以用鼠标拖动的文字.
    </div>
</body>
</html>


<script>
    var moving = false;
    function updateFlag(){
        if(moving){
            //停止移动
            console.log("stop moving.");
            moving = false;
            myDiv.style.cursor = 'pointer';
        }else{
            //开始移动
            console.log('start to move');
            moving = true;
            myDiv.style.cursor = 'move';
        }
    };
    function move(){
        if(moving){
            myDiv.style.left = event.x + 'px';  //一定要加上 px
            myDiv.style.top = event.y + 'px';   //一定要加上 px
        }
    }
    
    document.onmousemove = move;

</script>
```

## 取得按键的 ASCII 编码

```html
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    请在键盘上按任意键
</body>
</html>
<script language="javascript">
    function getkeyCode(){
        ascii = event.keyCode;
        console.log(ascii);
    }
    document.onkeydown = getkeyCode;
</script>
```

## 取得按下的按键名

```html
<html>
    <head>
    	<title>取得按下的按键</title>
        <script language="javascript">
            function getkey(){
                ascii = event.keyCode;
                key = String.fromCharCode(ascii);
                alert(key);
            }
            document.onkeypress=getkey;
        </script>
    </head>
    <body>
    	请在键盘上按任意键
    </body>
</html>
```

## 取得键盘的方向键

```html
<html lang="en">
<head>
</head>
<body>
    请在键盘上按方向键 [ ↑ ↓ ← →]
</body>
</html>
<script language="javascript">
	function showkey(){
		key = event.keyCode;
         switch(key){
            case 37:
                console.log("你按了←键！");
                break
            case 38:
                console.log("你按了↑键！");
                break
            case 39:
                console.log("你按了→键！");
                break
            case 40:
                console.log("你按了↓键！");
                break
            default:
                console.log("event.keyCode: " + key);
                break
        }
	}
	document.onkeydown=showkey;
</script>
```

## 取得鼠标按键

```html
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    在页面上任意单击鼠标键
</body>
</html>

<script>
    function getMouseButton(){
        var button = event.button;
        switch(button){
            case 0:
                console.log('单击了鼠标<左>键');
                break
            case 1:
                console.log('单击了鼠标<中>键');
                break
            case 2:
                console.log('单击了鼠标<右>键');
                break
            default:
                console.log("event.button: " + button);
                break
        }
    }
    
    document.onmousedown = getMouseButton;
    
</script>
```



## 按住鼠标拖动图片

```html
<html lang="en">
<head>
</head>
<body>
    <img src="https://www.baidu.com/favicon.ico" alt="百度icon图标" 
    id='pic' style="position:absolute;left:0px;top:0px"
    onMouseDown="dragImage(this)">
</body>
</html>

<script language="javascript">
    down = false;
    var x,y,imgID;
    function dragImage(obj){
        imgID = obj;
        x = event.x - parseInt(imgID.style.left);
        y = event.y - parseInt(imgID.style.top);
        down=true;
    }
    function cancelDrag(){	down=false;	}
    function moveImage(){
        if(down){
            imgID.style.left  = event.x - x;
            imgID.style.top   = event.y - y;
            event.returnValue = false;
        }
    }
    document.onmousemove = moveImage;
    document.onmouseup = cancelDrag;
</script>
```



## 鼠标经过时改变一列表格的颜色

```html
<html lang="en">
<head>
</head>
<body>
    <table width="240" border="1">
        <tr onMouseOver="this.style.background='#0066FF'" 
            onMouseOut="this.style.background=''">
            <td>A</td>
            <td>B</td></tr>
        <tr onMouseOver="this.style.background='#0066FF'" 
            onMouseOut="this.style.background=''">
            <td>C</td>
            <td>D</td></tr>
        <tr onMouseOver="this.style.background='#0066FF'" 
                onMouseOut="this.style.background=''">
            <td>E</td>
            <td>F</td></tr>
    </table>
</body>
</html>
```

## 鼠标控制文字的滚动

```html
<html>
    <head>
        <title>鼠标控制文字的滚动</title>
        <style type="text/css">
            marquee{
                position:absolute;
                left:30px;
                width:200px;
                height:200px;
                background:#6699FF;
            }
            pre{
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <marquee direction="up" onMouseOver="this.stop()" onMouseOut="this.start()">
<pre>
    JavaScript特效制作
    最新JavaScript特效
    常用HTML标签讲解
    ASP入门教程
    Dreamweaver 8 教程
</pre>
        </marquee>
    </body>
</html>
```

## 定义鼠标右键弹出菜单

```html
<html>
    <head>
        <title>网页弹出菜单</title>
        <style type="text/css">
            #menu{
                position: absolute;  /* 定位模式: 绝对定位 */
                background-color:#cccccc;
                width: 80px;
                visibility:hidden;   /* 起始状态, 隐藏 */
            }
        </style>
    </head>
    <body oncontextmenu="return false">   <!-- body标签, 屏蔽默认的弹出菜单 -->
        <div id="menu" >
            <a href="#">给我留言</a><br>
            <a href="#">在线聊天</a><br>
            <a href="#">网上图片</a><br>
            <a href="#">关于我们</a><br>
        </div>
    </body>
</html>

<script language="javascript">
    function popmenu(){
        console.log(event.button);
        if(event.button == 2){  // 单击鼠标右键时显示菜单
            menu.style.left = event.x;
            menu.style.top  = event.y;
            menu.style.visibility = "visible";
        }else if(event.button == 0 || event.button == 1){  // 单击鼠标左键/中键时隐藏菜单
            menu.style.visibility = "hidden";
        }
    }
    // 注册鼠标单击事件
    document.onmousedown = popmenu;
</script>
```



## 网页树形目录展开与收缩

```html
<html lang="en">
<head>
</head>
<body>
    <a href="javascript:showTree('tree1')" style="text-decoration:none;"><strong id='tree1-icon'>+</strong></a>
    <span onclick="showTree('tree1')">树型目录-标题1</span>
    <div id='tree1' style="display:none;">
        <a href="#">A</a><br/>
        <a href="#">B</a><br/>
        <a href="#">C</a><br/>
    </div>
    <br />
    <a href="javascript:showTree('tree2')" style="text-decoration:none;"><strong id='tree2-icon'>+</strong></a>
    <span onclick="showTree('tree2')">树型目录-标题2</span>
    <div id='tree2' style="display:none;">
        <a href="#">D</a><br/>
        <a href="#">E</a><br/>
        <a href="#">F</a><br/>
    </div>
</body>
</html>

<script>
    function showTree(treeId){
        var treeObj = document.getElementById(treeId);
        var iconId = treeId + '-icon';
        var icon = document.getElementById(iconId);
        if (treeObj.style.display == 'none'){
            treeObj.style.display = 'block';
            icon.innerText = '- '
        }else{
            treeObj.style.display = 'none';
            icon.innerText = '+';
        }
    }
</script>
```



## 网页下拉菜单

```html
<html lang="en">
<head>
</head>
<style>
    #menu{
        display: none;
        background-color: #ccc;
        width: 200px;
    }
    a:link{ text-decoration: none; }
</style>
<body>
    <a href='javascript:switchShow()'>单击显示</div>
    <div id='menu'>
        <dl>
            <dd><a href="#">清蒸鲈鱼</a><br/></dd>
            <dd><a href="#">啤酒烧鸭</a><br/></dd>
            <dd><a href="#">青椒炒蛋</a><br/></dd>
        </dl>
    </div>
</body>
</html>

<script>
    var showing = false;
    var menu = document.getElementById('menu');
    function switchShow(){
        if(!showing){
            menu.style.display = 'block';
            showing = true;
        }else{
            // menu.style.display = 'none';
            // showing = false;
            hidden();
        }
    };
    function hidden(){
        if(showing){
            menu.style.display = 'none';
            showing = false;
        }
    };

    document.onclick = hidden;

</script>
```



## 显示不同的鼠标指针样式

```html
<html>
    <head>
    	<title>显示不同的鼠标指针样式</title>
    </head>
    <body>
        <div onmouseover="this.style.cursor='hand'">手形指针</div>
        <div onmouseover="this.style.cursor='move'">移动形指针</div>
    </body>
</html>
```

## 显示/隐藏图片

```html
<html>
    <head>
        <title>显示或隐藏图片</title>
    </head>
    <body>
        <img src="https://www.baidu.com/favicon.ico" id="pic"><br>
        <input type="button" value="显示图片" onClick="pic.style.visibility='visible'">
        <input type="button" value="隐藏图片" onClick="pic.style.visibility='hidden'">
    </body>
</html>
```

## 用方向键控制图片移动

```html
<html lang="en">
<head>
</head>
<body>
    <!-- 一定要初始化: position, left, top -->
    <img src="https://www.baidu.com/favicon.ico" alt="百度icon图标" 
    id='pic' style="position:absolute;left:0;top:0;">
</body>
</html>

<script>
    function moveImg(){
        var ascii = event.keyCode;
        var x = parseInt(pic.style.left);
        var y = parseInt(pic.style.top);
        var step = 10;
        console.log(x);
        console.log(ascii);
        switch(ascii){
            case 37:
                pic.style.left = x - step + 'px';
                break;
            case 38:
                pic.style.top = y - step + 'px';
                break;
            case 39:
                pic.style.left = x + step + 'px';
                break;
            case 40:
                pic.style.top = y + step + 'px';
                break;
        }
    }
    document.onkeydown = moveImg;

</script>
```



## 在超链接上显示自定义提示

```html
<html lang="en">
<head>
</head>
<style>
    #tip{
        color: lightblue;
        background-color: #555;
    }
    a:link{ text-decoration: none; }
</style>
<body>
    <div id='tip' style="visibility: hidden;position: absolute;left:0;top:0;">这是提示信息</div>
    <a href="#" onmouseover="showTip()" onmouseout="hiddenTip()">这是一个超链接</a>
</body>
</html>

<script>
    function showTip(){
        tip.style.left = event.x + 'px';
        tip.style.top = event.y + 'px';
        tip.style.visibility = 'visible';
    }
    function hiddenTip(){
        tip.style.visibility = 'hidden';
    }
</script>
```

## 在鼠标单击处显示图片

```html
<html lang="en">
<head>
</head>
<body>
    <img src="https://www.baidu.com/favicon.ico" alt="百度icon" id='img'
    style="position:absolute;left:0;top:0;visibility:hidden;">    
</body>
</html>
<script>
    function showImg(){
        img.style.left = event.x + 'px';
        img.style.top = event.y + 'px';
        img.style.visibility = 'visible';
    }
    document.onclick = showImg;
</script>

```





# 四.表单处理

## 查看表单文字字段的内容

```html
<html lang="en">
<head>
</head>
<body>
    <form action="" name='myForm'>
        <input type="text" name="myText" id="myInp">
        <input type="button" value="获取输入的文字" onClick="showText()">
    </form>
</body>
</html>

<script>
    function showText(){
        console.log(myForm.myText.value);
        // myForm --> 表单标签的 name='myForm'
        // myText --> input标签的 name='myText'
        // 除了 .value, 还可以 .class, .name, .id, .style, ......
    }
</script>
```



## 复选框 checkbox

```html
<html>
    <head>
        <title>带标签的复选框</title>
    </head>
    <body>
        <form name="myForm">
            <input type="checkbox" id="ch1"> <label for="ch1">第一项</label><br>
            <input type="checkbox" id="ch2"> <label for="ch2">第二项</label><br>
            <input type="checkbox" id="ch3"> <label for="ch3">第三项</label><br>
            <!-- <input type="submit" value="提交"> -->
            <input type="button" onclick="submitForm()" value="点我一下, 查看取到什么">
        </form>
    </body>
</html>

<script>
    function submitForm(){
        var checkedIds = [];
        for (i=1; i<=3; i++){
            var ch = document.getElementById('ch'+i);
            console.log(typeof ch);
            if(ch.checked){  // checkbox被选中时, checked=true
                checkedIds.push(ch.id);
            }
        }
        console.log(checkedIds);
    }


</script>
```

## 单击选项按钮改变网页背景颜色

```html
<html lang="en">
<head>
</head>
<body>
    <form name="form1">
        <input name="color" type="radio" value="#FFFFFF" onClick="chColor()" >白色  
        <input name="color" type="radio" value="lightblue" onClick="chColor()" >浅蓝色
        <input name="color" type="radio" value="lightgreen" onClick="chColor()" >浅绿色
        <input name="color" type="radio" value="lightyellow" onClick="chColor()" >浅黄色
    </form>
</body>
</html>

<script>
    function chColor(){
        for(i=0; i<4; i++){
            if(form1.color[i].checked){
                document.body.style.backgroundColor = form1.color[i].value;
            }
        }
    }
</script>
```

> 另一种

```html
<html lang="en">
<head>
</head>
<body>
    <form name="form1">
        <input name="color" type="radio" value="#FFFFFF" onClick="chColor(this)" >白色  
        <input name="color" type="radio" value="lightblue" onClick="chColor(this)" >浅蓝色
        <input name="color" type="radio" value="lightgreen" onClick="chColor(this)" >浅绿色
        <input name="color" type="radio" value="lightyellow" onClick="chColor(this)" >浅黄色
    </form>
</body>
</html>
<script>
    function chColor(obj){
        document.body.style.backgroundColor = obj.value;
    }
</script>
```

## 获取表单中所有控件的 name

```html
<html>
<head>
<title>读取表单中所有元素名称</title>
<script language="javascript">
// <!--
	function readForm(){
		len = form1.elements.length;
		str = "";
		for(i=0;i<len;i++){
			str = str + form1.elements[i].name + "\n";
		}
		alert("表单中所有元素的名称为：\n" + str);
	}
// -->
</script>
</head>
<body>
<form name="form1">
  <input type="text" name="name1"><br>
  <input type="text" name="name2">
  <input type="button" name="name3" value="发送" >
</form>
<a href="javascript:readForm()">显示</a>
</body>
</html>
```

## 防止表单多次发送

> 在表单处理成功后,  标记表单已被提交过一次, 不可再提交

```html
<html lang="en">
<head>
</head>
<body>
    <form action="#" name='myForm' onSubmit="return checkSubmit()">  <!-- form标签, onSubmit 事件 -->
        用户名: <input type="text" name="username">
        <input type="submit" value="提交表单" >
    </form>
</body>
</html>

<script>
    var submitted = false;
    function checkSubmit(){
        console.log(submitted);
        if(submitted){
            alert("该表单已提交过一次, 请勿重复提交!");
            return false;  // 返回 false
        }
        //处理表单提交... 处理成功后设置为已提交 (处理失败时不设置)
        submitted = true;  // 跟新标记
        return true;       // 返回 true
    }

</script>
```

## 改变文字的水平对齐方式

```html
<html>
    <head>
    	<title>改变文字字段中文字的对齐方式</title>
    <script language="javascript">
    //<!--
        function align(type){
            form1.name.style.textAlign = type;
        }
    //-->
    </script>
    </head>
    <body>
    <form name="form1">
        <input type="text" name="name" value="对齐方式"><br>
        <a href="javascript:align('left')">靠左对齐</a>
        <a href="javascript:align('center')">居中对齐</a>
        <a href="javascript:align('right')">靠右对齐</a>
    </form>
    </body>
</html>
```

## 检验一组复选框是否选中

```html
<html lang="en">
<head>
</head>
<body>
    <form action="#" name='myForm'>
        <input type="checkbox" name="ch" value='1'>第一项    <!-- checkbox 的 name 必须相同-->
        <input type="checkbox" name="ch" value='2'>第二项
        <input type="checkbox" name="ch" value='3'>第三项
        <input type="button" value="校验" onclick="check()">
    </form>
</body>
</html>
<script>
    function check(){
        // if(myForm.ch[0].checked && myForm.ch[1].checked){
        //     alert('两个复选框都被选中了');
        // }
        var msg = '';
        for(i=0; i<myForm.ch.length; i++){
            if(myForm.ch[i].checked){
                var msg = msg + '第' + i + '个复选框被选中了\n';
            }
        }
        if(msg != ''){
            alert(msg);
        }else{
            alert('没有复选框被选中');
        }
    }
</script>
```

## 检验一组单选按钮的选择情况

```html
<html lang="en">
<head>
</head>
<body>
    <form action="#" name='myForm'>
        <input type="radio" name="gender" value='0'>男    <!-- radio 的 name 必须相同-->
        <input type="radio" name="gender" value='1'>女
        <input type="radio" name="gender" value='2'>其他
        <input type="button" value="校验" onclick="check()">
    </form>
</body>
</html>
<script>
    function check(){
        var msg = '';
        for(i=0; i<myForm.gender.length; i++){
            if(myForm.gender[i].checked){
                var msg = getTotalTip() + '第' + i + '个单选按钮被选中了\n';
                break; //跳出循环, 没有必要再判断
            }
        }
        if(msg != ''){
            alert(msg);
        }else{
            alert('没有单选按钮被选中');
        }
    }
    function getTotalTip(){
        // like: `[0/1/2]`
        var total = '';
        for(i=0; i<myForm.gender.length; i++){
            total = total + '/' + i;
        }
        total = '[' + total.substring(1) + ']';
        return total;
    }
</script>
```

## 解除所有复选框的选取

```html
<html>
<head>
<title>解除所有复选框的选取</title>
<script language="javascript">
//<!--
	function removeAll(){
		for (i=0; i<form1.ch.length; i++){
			form1.ch[i].checked = false;
		}
	}
//-->
</script>
</head>
<body>
<form name="form1">
  <input name="ch" type="checkbox" checked="checked">第一项
  <input name="ch" type="checkbox" checked="checked">第二项
  <input name="ch" type="checkbox">第三项
  <input name="ch" type="checkbox">第四项
  <input type="button" value="解除选中" onClick="removeAll()">
</form>
</body>
</html>
```

## 全选或取消复选框

```html 
<html lang="en">
<head>
</head>
<body>
    <form action="#" name="form1">
        <input type="checkbox" name="ch" checked>第1项
        <input type="checkbox" name="ch" checked>第2项
        <input type="checkbox" name="ch">第3项
        <input type="checkbox" name="ch">第4项<br />
        <input type="checkbox" name="chs" onclick="selectOrCancelAll()">全选  <!-- onclick 或 onchange--><br>
        <input type="reset" value="重置所有">  <!-- reset -->
    </form>
</body>
</html>

<script>
    function selectOrCancelAll(){
        for(i=0; i<form1.ch.length; i++){
            form1.ch[i].checked = form1.chs.checked;
        }
    }
</script>
```



## 连动式选项按钮

```html
<html>
    <head>
    	<title>连动式选项按钮</title>
    <script language="javascript">
    //<!--
        function change(){
            for(i=0;i<2;i++){
                if (form1.sex1[i].checked){
                    form1.sex2[i].checked = true;
                }
            }
        }
    //-->
    </script>
    </head>
    <body>
        <form name="form1">
            <input name="sex1" type="radio" onClick="change()" >男  
            <input name="sex1" type="radio" onClick="change()" >女<br>
            <input name="sex2" type="radio" onClick="change()" >男  
            <input name="sex2" type="radio" onClick="change()" >女
        </form>
    </body>
</html>
```



## 取得多值下拉菜单中选取的多个值

```html
<html>
<head>
<title>取得列表中选取的多个值</title>
<script language="javascript">
// <!--
	function getValue(){
		str = "";

        //注意: 有两种方式可以获取 select 表单的每一项
        console.log(form1.select1.options[0]);
        console.log(form1.select1[0]);

		for(i=0; i<form1.select1.length; i++){
			if(form1.select1.options[i].selected){
				str = str + form1.select1[i].value + "\n";
			}
		}
		if(str != "")
			alert(str);	
		else
			alert("你未选取任何选项");
	}
//-->
</script>
</head>
<body>
    <form name="form1">
      <select name="select1" multiple>  <!-- 注意 name, multiple -->
        <option value="1">第一项</option>
        <option value="2">第二项</option>
        <option value="3">第三项</option>
        <option value="4">第四项</option>
        <option value="5">第五项</option>
      </select>
      <input type="button" value="显示" onClick="getValue()">
    </form>
</body>
</html>
```

## 取得文件中选取的文件名称

```html
<html>
<head>
    <title>取得文件中选取的文件名称(不包含路径)</title>
    <script language="javascript">
    //<!--
        function getFilename(){
            var str = new Array();
            var filename = form1.file.value;     // form1.file.value
            var arr = filename.split("\\");
            console.log(arr);  //例如: ["C:", "fakepath", "Hero.png"], 注意无法获得源路径
            if (filename !== ""){
                alert('文件名: ' + arr[arr.length-1]);
                //获取后缀
                extname = filename.split('.').slice(1).join('.');  // 如后缀: `tar.gz`
		       alert("后缀: " + extname);
            }else{
                alert("你还没有选取文件");
            }
        }
    //-->
    </script>
</head>
<body>
    <form enctype="multipart/form-data" name="form1">
    <input type="file" name="file">
    <input type="button" value="显示文件名称" onClick="getFilename()">
    </form>
</body>
</html>
```

## 实时反馈下拉菜单的选择

> 关键:  给 select 下拉菜单标签指定 onChange 事件

```html
<html lang="en">
<head>
</head>
<body>
    <form action="#" name='form1'>
        <select name="select1" onchange="showMsg()">  <!--注意: select, onchange-->
            <option value="0">----</option>
            <option value="1">选项A</option>
            <option value="2">选项B</option>
            <option value="3">选项C</option>
            <option value="4">选项D</option>
        </select>
    </form>
</body>
</html>

<script>
    function showMsg(){
        var value = form1.select1.value;
        alert("选择了: " + value);
        
        // 打印被选中的项的索引值
         var index = form1.select1.selectedIndex;
		alert("你选取项目的索引值是" + index);

        //打印被选中的 option 标签的内部文字
        for (i=0; i<form1.select1.options.length; i++){
            if(form1.select1.options[i].selected){
                console.log(form1.select1.options[i].innerText);
            }
        }
    }
</script>
```



## 页面加载时自动聚焦文字输入框

```html
<html>
    <head>
    	<title>使用文字字段取得focus</title>
    </head>
    <body onLoad="form1.username.focus()">
        <form name="form1">
            姓名:<input type="text" name="username"><br>
            电话:<input type="text" name="tel"><br>
        </form>
    </body>
</html>
```

##  鼠标经过时改变文字字段边框的颜色

```html
<html>
    <body onLoad="form1.username.focus()">
        <form name="form1">
            姓名: <input type="text" name="username"
            onmouseover="this.style.borderColor = 'blue'"
            onmouseout="this.style.borderColor = ''">
        </form>
    </body>
</html>
```

同理:

1. 鼠标经过时改变文字字段的背景颜色

```html
<input type="text" value="请将鼠标移过来！"
onMouseOver="this.style.background = 'red'"
onMouseOut="this.style.background = 'white'">
```

2. 鼠标经过时改变文字字段的文字颜色

```html
<input type="text" value="请将鼠标移过来！"
onMouseOver="this.style.color = 'red'"
onMouseOut="this.style.color = 'black'">
```

## 鼠标经过时选取文字字段中的文字

```html
<html>
    <body onLoad="form1.username.focus()">
        <form name="form1">
            <input type="text" name="username" value="输入框默认值"
            onmouseover="selectText();">
        </form>
    </body>
</html>
<script>
    function selectText(){
        form1.username.focus();  // 在文本域上设置焦点。
        // form1.username.blur();  // 从文本域上移开焦点。
        form1.username.select(); //选中文本域所有文字
    }
</script>
```

## 复制文本域的所有文字

```html
<html>
    <body onLoad="form1.username.focus()">
        <form name="form1">
            <input type="text" name="username" value="输入框默认值">
            <input type="button" value='复制' onclick="selectAndCopy();">
        </form>
    </body>
</html>
<script>
    function selectAndCopy(){
        form1.username.focus();  // 在文本域上设置焦点。
        form1.username.select(); // 选中文本域所有文字
        document.execCommand('Copy');  // 复制
        console.log('已复制到粘贴板!');
    }
</script>
```

## 双重输入文字

```html
<html>
<body>
    <form name="form1">
        <input type="text" name="text1"> <br />
        <input type="text" name="text2">
    </form>
</body>
</html>
<script>
    //需求: 在向第一个文本输入框输入文字时, 在第二个输入框也要自动输入相同文字
    //思路: 不好判断触发条件, 可以定义定时任务, 定时更新第二个输入框的内容
    function doubleInput(){
        form1.text2.value = form1.text1.value;
        setTimeout("doubleInput()", 500);
        //或: setTimeout(doubleInput, 500);
    }
    doubleInput();

    /*
    问题: 
        1.多久更新一次? 
        2.用 setInterval 还是 setTimeout?
        3.如何实现 在第二个输入框手动输入时也要向第一个输入框更新?
    */
</script>
```

## 跳页菜单的实现

```html
<html lang="en">
<body>
    <form action="#" name='form1'>
        <select name="select1" onchange="jumpMenu();">  <!-- onchange -->
            <option value="">选择要前往的页面</option>   <!-- value="" -->
            <option value="https://www.shouce.ren">手册网</option>
            <option value="https://www.baidu.com">百度</option>
        </select>
    </form>
</body>
</html>
<script>
    function jumpMenu(){
        //在选中select表单任意一项时, 都会触发 onchange 事件, 此时的value就是选中的option的value
        var url = form1.select1.value;
        if(url != ""){
            window.location = url;  // 在当前窗口打开页面
            // open(url);  // 在新窗口打开页面
        }
    }
</script>
```

## 图片发送按钮

```html
<html>
<head>
    <title>图片发送按钮</title>
</head>
<body>
    <form name="form1" method="post" action="http://www.baidu.com">
        姓名:<input type="text" name="name">
        <a href="javascript:form1.submit();" style="vertical-align:middle;">
            <svg t="1585715387398" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4386" width="28" height="28"><path d="M614.876794 8.441764C252.077632-55.207212-53.437452 250.307872 10.211523 613.107035c38.189386 197.311825 197.311825 362.799163 400.988548 400.988548 356.434265 70.013873 668.314247-241.866108 598.300373-598.300373C977.675957 212.118487 812.18862 46.631149 614.876794 8.441764zM341.186198 740.404986 169.333963 536.728264C150.23927 511.268673 156.604168 473.079288 182.063758 453.984595l0 0c25.45959-19.094693 63.648976-19.094693 82.743669 6.364898L353.915993 574.917649c19.094693 25.45959 57.284078 31.824488 82.743669 6.364898L767.634337 307.59195c25.45959-19.094693 63.648976-19.094693 82.743669 6.364898l0 0c19.094693 25.45959 19.094693 63.648976-6.364898 82.743669l-413.718343 350.069367C398.470276 772.229474 360.280891 765.864577 341.186198 740.404986z" p-id="4387" fill="#1296db"></path></svg>
        </a>
    </form>
</body>
</html>

```

## 文字字段自动调整大小

> 方法1:  在退格时,  输入框长度不会跟着减小

```html
<html>
<body>
    <form name="form1" method="post" action="#">
        姓名:<input type="text" name="username" 
        onkeypress="autoWidth();" size=6>      <!-- onkeypress事件, size属性 -->
        <a href="javascript:form1.submit();">提交</a>
    </form>
</body>
</html>
<script>
    function autoWidth(){
        var text = form1.username.value;
        if(text.length == 0){
            form1.username.size = 6;
        }else{
            form1.username.size = text.length;
        }
    }
</script>
```

> 方法2:  在退格时,  输入框长度会减小

```html
<html>
<body>
    <form name="form1" method="post" action="#">
        姓名:<input type="text" name="username">
        <a href="javascript:form1.submit();">提交</a>
    </form>
</body>
</html>
<script>
    function autoWidth(){
        var text = form1.username.value;
        if(text.length <= 6){
            form1.username.size = 6;
        }else{
            form1.username.size = text.length;
        }
        setTimeout('autoWidth()', 500);
    }
    autoWidth();
</script>
```

## 限制文字区域输入的字数

```html
<html>
    <body>
        <form name="form1" method="post" action="#" onsubmit="return check();">
            <textarea name="txt"></textarea>
            <input type="submit" value='提交'>
        </form>
    </body>
</html>
<script>
    var lenLimit = 10;
    function check(){ 
        if(form1.txt.value.length > lenLimit){
            alert('文本过长!');
            return false;
        }
        return true;
    }
</script>
```

## 限制文字区域输入的行数

```html
<html>
    <head>
    	<title>限制在文字区域中输入的文字行数</title>
    <script language="javascript">
    // <!--
        function rows(){
            i = form1.txt.value.match(/\n/g);
            if(i){	
                txtlen = i.length + 1;
            }else{	
                txtlen = 1;	
            }
            return txtlen;
        }
        function check(){
            if (rows() > 2){
                alert("你输入的文字不能超过2行！");
                return false;
            }
        }
    //-->
    </script>
    </head>
    <body>
        <form name="form1" action="#" onSubmit = "return check()">
          <textarea name="txt" rows="5"></textarea>
          <input type="submit" value="发送">
        </form>
    </body>
</html>
```

## 验证文字输入的是否是时间格式

```html
<html>
<head>
<title>验证文字字段中输入的是否是时间格式</title>
<script language="javascript">
//<!--
	function check(){
		str = form1.time.value;
		a = new Array();
		if (str != ""){
			a = str.split(":");
			if(a.length == 3){
				if (a[0]>24 || a[1]>59 || a[2]>59){
					alert("时间格式错误!");
					return false;
				}else{
					alert("时间格式正确！");
				}
			}else{
				alert("时间格式错误!");
				return false;
			} 
		}
	}
//-->
</script>
</head>
<body>
<form method="post" name="form1" onSubmit="return check()">
请输入一个时间:(00:00:00)
<input name="time" type="text">
<input type="submit" value="发送">
</form>
</body>
</html>
```

## 验证文字输入的是否是数字/字母

```html
<html>
    <head>
        <script language="javascript">
        // <!--
            function check(formObj){
                var num = "0123456789";
                var letter = "abcdefghijklmnopqrstuvwxyz";
		       var letter = letter + letter.toUpperCase();
                var str = formObj.input1.value;
                for (i=0; i < str.length; i++){   
                    if (num.indexOf(str.charAt(i)) == -1 && letter.indexOf(str.charAt(i)) == -1)
                    {
                        alert("只能输入数字或字母！");
                        return false;
                    }
                }
            }
        // -->
        </script>
    </head>
    <body>
        <form method="post" name="form1" onSubmit="return check(this)">
            请输入：
            <input name="input1" type="text">
            <input type="submit" value="发送">
        </form>
    </body>
</html>
```

## 一个简单的计算器

```html
<html>
    <head>
        <title>一个简单的计算器</title>
    <script language="javascript">
    //<!--
        function equal(op){
            a = form1.a.value;
            b = form1.b.value;
            switch(op){
                case "+": result = (a*1) + (b*1); break;
                case "-": result = a - b; break;
                case "*": result = a * b; break;
                case "/": result = a / b; break;
            }
            form1.result.value = result;
        }
    //-->
    </script>
    </head>
    <body>
        <form name="form1">
            数1: <input type="text" name="a" size=5><br>
            数1: <input type="text" name="b" size=5><br>
            <input type="button" value="加法运算" onClick="equal('+')">
            <input type="button" value="减法运算" onClick="equal('-')">
            <input type="button" value="乘法运算" onClick="equal('*')">
            <input type="button" value="除法运算" onClick="equal('/')"><br>
            结果：<input type="text" name="result" size=5>
        </form>
    </body>
</html>
```

## 以图片显示输入的数字

```html
<html>
<body>
    <form name="form1">
        输入一串数字: <input type="text" name="numbers" size=20>
        <input type="button" value="查看结果" onclick="showNumersImages();">
    </form>
    <div id='myDiv'></div>
</body>
</html>
<script>
    var urlPrefix = "http://pics.sc.chinaz.com/Files/pic/icons128/1111/Number_0";
    var urlSuffix = ".png";
    function showNumersImages(){
        var chars = form1.numbers.value;
        var imgTags = [];
        for(i=0; i<chars.length; i++){
            if(isNumChar(chars[i])){
                if(chars[i] == '0'){
                    var src = urlPrefix + '10' + urlSuffix;
                }else{
                    var src = urlPrefix + '0' + chars[i] + urlSuffix;
                }
                var tag = "<img src='" + src + "' width='30' height='30'>";
                imgTags.push(tag);
                console.log(imgTags);
            }
        }
        // 结果1: 一次性全部显示
        // myDiv.innerHTML = imgTags.join(' ');
        // 结果2: 逐渐显示
        for(i=0; i<imgTags.length; i++){
            setTimeout(function(index){
                myDiv.innerHTML = imgTags.slice(0, index).join(' ');
                console.log(index);
            }, 500*i, [i+1]);  // 传参方式: [i+1], 接收变量为index
        }
    }
    function isNumChar(char){
        var numAll = "0123456789";
        if (numAll.indexOf(char) == -1){
                return false;
        }else{
            return true;
        }
    }
</script>
```

## 允许/禁止对表单某字段的访问

```html
<html>
<body>
    <form name="form1">
        姓名：<input type="text" name="username">
        <input type="button" value="发送" >
    </form>
    <a href="javascript:set(false)">允许访问username</a>
    <a href="javascript:set(true)">禁止访问username</a>
</body>
</html>
<script language="javascript">
// <!--
    function set(f){
        document.form1.username.disabled = f;
    }
// -->
</script>
```





# 五.声音处理

# 六.图片处理

# 七.检查与验证

# 八.时间与日期

# 九.浏览器

# 十. cookie

## 操作cookie

1. 设置 cookie 值的函数
2. 获取 cookie 值的函数
3. 检测 cookie 值的函数

```javascript
function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires;
}
function getCookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
}
function checkCookie(){
    var user=getCookie("username");
    if (user!=""){
        alert("欢迎 " + user + " 再次访问");
    }
    else {
        user = prompt("请输入你的名字:","");
          if (user!="" && user!=null){
            setCookie("username",user,30);
        }
    }
}
```

## 检测浏览器是否关闭了Cookie功能

```html
<html>
<head>
<title>检测浏览器是否关闭了Cookie功能</title>
</head>
<body>
<script language="javascript">
<!--
	if (navigator.cookieEnabled){
		document.write("你的浏览器允许使用Cookie");
	}else{
		document.write("你的浏览器不允许使用Cookie");
	}
//-->
</script>
</body>
</html>
```



# 十一.window

## 打印当前网页

```html
<html>
    <head>
        <title>打印网页</title>
    </head>
    <body>
        <input type="button" value="打印网页" onClick="window.print()">
    </body>
</html>
```

## 更换内置页框(iframe)的内容

```html
<html>
    <head>
        <title>打印网页</title>
    </head>
    <body>
        <a href="javascript:gotoUrl('http://www.shouce.ren')">手册网</a><br>
        <a href="javascript:gotoUrl('http://www.shouce.ren/api/book')">手册网-在线文档</a><br>
        <iframe name="frame1" width="100%" height="70%"></iframe>
    </body>
</html>
<script language="javascript">
// <!--
    function gotoUrl(url){
        frame1.location=url;
    }
//-->
</script>
```

## 满天星背景

```html
<html>
<head>
<title>满天星背景</title>
<script language="javascript">
// <!--
	n = 0;
	function start(){
		width = Math.random() * document.body.clientWidth-10;
		height = Math.random() * document.body.clientHeight-10;
		document.all["s" + n].style.top = height;
		document.all["s" + n].style.left = width;
		n++;
		if (n>=30) n = 0;
		setTimeout("start()",30);
	}
//-->
</script>
</head>
<body bgcolor="#000000">
<script language="javascript">
// <!--
	for (i=0;i<30;i++){
		str = "<div id='s"+i;
		str += "' style='position:absolute;";
		str += "left:51px;top:38px;";
		str += "width:4;height:4;";
		str += "background-color: #FFFFFF;";
		str += "font-size:0;'></div>"
		document.write(str);
	}
	start();
//-->
</script>
</body>
</html>
```

## 载入网页进度条

```html
<html>
<head>
<title>载入网页进度条</title>
<style type="text/css">
	.style1{
		font-family:Arial;	font-weight:bolder; 
		color:#0066ff; 		background-color:#fef4d9; 
		padding:0px; 		border-style:none;
	}
	.style2{
		color:#0066ff;	text-align:center; 
		border-width:medium; 	border-style:none;
	}
</style>
<script language="javascript">
// <!--
	var bar=0;
	var line="||";
	var amount="||";
	function count(){
		bar=bar+2;
		amount =amount + line;
		document.loading.chart.value=amount;
		document.loading.percent.value=bar+"%";
		if (bar<99)	{
			setTimeout("count()",100);
		}else{
			window.location = "http://www.baidu.com";
		} 
	}
//-->
</script>
</head>
<body onLoad="count()">
    <form name="loading">
        <center>
            <font color="#0066ff" size="2">正在载入网页...</font>
            <input type="text" name="chart" size="46" class="style1"> 
            <input type="text" name="percent" size="47" class="style2"> 
        </center>
    </form>
</body>
</html>
```

## 弹出一个全屏幕窗口

```html
<html>
    <head>
        <title>弹出一个全屏幕窗口</title>
    </head>
    <body>
        <script language="javascript">
        // <!--
            function popfull(){
                window.open("http://www.shouce.ren","","fullscreen=yes");
            }
        //-->
        </script>
        <input type="button" value="弹出全屏幕窗口" onClick="popfull()">
    </body>
</html>
```

## 弹出一个自动关闭窗口

```html
<html>
    <head>
        <title>弹出一个自动关闭窗口</title>
        <script language="javascript">
        <!--
            window.open("tmp.html","","screenY=100,screenX=100,width=300,height=200");
        //-->
        </script>
    </head>
    <body>
        打开页面里的js代码是
        setTimeout("self.close()",5000);
    </body>
</html>
```

tmp.html

```html
<html>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type" />
    <head>
        <title>弹出一个自动关闭窗口</title>
        <script language="javascript">
        <!--
            setTimeout("self.close()",5000);
        //-->
        </script>
    </head>
    <body>
    	5秒钟后，本弹出式窗口将自动关闭
    </body>
</html>
```



# 十二.文本

## 不断变色的文字

```html
<html>
    <head>
        <title>不断变色的文字</title>
        <script language="javascript">
        // <!--
            i = 0;
            color = new Array("red","blue","green","black","yellow","pink");
            function chColor()
            { 
                txt.style.color = color[i];
                i++;
                if(i >= color.length) i=0;
                setTimeout("chColor()",500);
            }
        //-->
        </script>
    </head>
    <body onLoad="chColor()">
        <div id="txt">这是不断变色的文字</div>
    </body>
</html>
```

## 动感Loading文字 / 逐字变化文字颜色

```html
<html>
    <head>
    <title>动感Loading文字</title>
    <script language="javascript">
    // <!--
        var text = "Loading...";
        var i = 0;
        function flash(){
            char = text.charAt(i);
            char = "<b style='color:red;'>" + char + "</b>";
            leftStr  = text.substr(0,i);
            rightStr = text.substr(i+1,text.length-i);
            txt.innerHTML = leftStr + char + rightStr;
            i++;
            if (i>=text.length)i=0;
            setTimeout("flash()",500);
        }
    //-->
    </script>
    </head>
    <body onLoad="flash()">
        <div id="txt" style="font-size:28px;font-family:Arial"></div>
    </body>
</html>
```

## 逐字显示文字

```html
<html>
<head>
<title>逐字显示文字</title>
<script language="javascript">
//<!--
	text = "逐字显示文字!";
	i = 0;
	function type(){ 
		str  = text.substr(0,i);
		txt.innerHTML = str + "_";
		i++;
		if (i>text.length)i=0;
		setTimeout("type()",300);
	}
//-->
</script>
</head>
<body onLoad="type()">
<div id="txt"></div>
</body>
</html>
```





## 动态缩放文字

```html
<html>
    <body onLoad="changeSize()">
        <div id="txt">动态缩放的文字</div>
    </body>
</html>

<script language="javascript">
// <!--
    var minSize = 10;
    var maxSize = 50;
    var size = minSize;
    var op = '++';

    function changeSize(){
        txt.style.fontSize = size;
        eval('size' + op);
        if(size==maxSize) op = '--';
        if(size==minSize)  op = '++';
        setTimeout("changeSize();", 40);
    }
//-->
</script>
```

## 反弹文字

```html
<html>
<head>
<title>反弹文字</title>
<script language="javascript">
// <!--
	x = 0;
	y = 0;
	controlx = true;
	controly = true;
	function moveText(){ 
		docWidth  = parseInt(document.body.clientWidth);
		docHeight = parseInt(document.body.clientHeight)-20;
		textWidth    = parseInt(txt.style.width);
		txt.style.left = x;
		txt.style.top  = y;
		if(controlx && docWidth-textWidth > x){
			x+=2;
		}else{
			controlx = false;
		}
		if(!controlx && x > 0){
			x-=2;
		}else{
			controlx = true;
		}
		
		if(controly && docHeight > y){
			y+=2;
		}else{
			controly = false;
		}
		if(!controly && y > 0){
			y-=2;
		}else{
			controly = true;
		}
		setTimeout("moveText()",10);
	}
//-->
</script>
</head>
<body onLoad="moveText()">
<div id="txt" style="position:absolute;width:65">反弹文字</div>
</body>
</html>
```

## 让浏览者自己选择网页的文字颜色

```html
<html>
<head>
<title>让浏览者自己选择网页的文字颜色</title>
<script language="javascript">
//<!--
	function chColor(c){
		document.body.style.color = c;
	}
//-->
</script>
</head>
<body>
<input name="c" type="radio" value="#000000" onClick="chColor(this.value)" checked>黑色
<input name="c" type="radio" value="#0000FF" onClick="chColor(this.value)">蓝色
<input name="c" type="radio" value="#FF0000" onClick="chColor(this.value)">红色<br>
这是要改变颜色的文字! 
</body>
</html>
```

## 让浏览着自己选择网页文字的大小

```html
<html>
<head>
<title>让浏览着自己选择网页文字的大小</title>
<script language="javascript">
//<!--
	function chSize(n){
		document.body.style.fontSize = n;
	}
//-->
</script>
</head>
<body>
<input name="s" type="radio" value="12" onClick="chSize(this.value)">小
<input name="s" type="radio" value="16" checked onClick="chSize(this.value)">中
<input name="s" type="radio" value="20" onClick="chSize(this.value)">大<br>
这是要改变大小的文字! !
</body>
</html>
```



# 十三.综合

## 检查是否是闰年

```html
<html>
<head>
<title>检查是否为闰年</title>
<script language="javascript">
//<!--
	function isLeapYear(year){
		if (year % 4 == 0){
			if (year % 100 == 0){
				if(year % 400 == 0){
					str = year + "是闰年";
				}else{
					str = year + "不是闰年";
				}
			}else{
				str = year + "是闰年";
			}
		}else{
			str = year + "不是闰年";
		}
		alert(str);
	}
//-->
</script>
</head>
<body>
<form name="form1">
	<input type="text" name="year" value="2000">
	<input type="button" value="是否是闰年" onClick="isLeapYear(form1.year.value)">	
</form>
</body>
</html>
```



## 使用input标签 type='color'变换颜色

```html
<html>
<body onload="chColor();">
    <form name="form1" action="#" onchange="chColor();" onsubmit="return false;">
        请选择一个颜色作为页面背景: <input type="color" value="#ffffff" name="color">
    </form>
</body>
</html>

<script>
    function chColor(){
        var colorStr = form1.color.value;
        console.log(colorStr);
        document.bgColor = colorStr;
    }
</script>
```





## 手动变换颜色

```html
<html>
<body>

<form action="#" name='form1' onchange="display();">
    红(0~255): <input type="number" name="red" value="0" min="0" step="5" max="255"> <br />
    绿(0~255): <input type="number" name="green" value="0" min="0" step="5" max="255"> <br />
    蓝(0~255): <input type="number" name="blue" value="0" min="0" step="5" max="255"> <br />
    不透明度(0~1): <input type="number" name="opacity" value="1" min="0" step="0.1" max="1"> <br />
    <input type="button" value='确定' onclick="display();"> <br />
</form>
<div id='myDiv' style='width:200px;height:200px;'></div>

</body>
</html>
<script>
    function display(){
        var red = check(form1.red.value);
        var green = check(form1.green.value);
        var blue = check(form1.blue.value);
        var opacity = check(form1.opacity.value, true);
        var rgbColor = 'rgb(' + red + green + blue + opacity + ')';
        console.log(rgbColor);
        // document.bgColor = rgbColor;
        myDiv.style.backgroundColor = rgbColor;
    }
    function check(numStr, opacity=false){
        if(opacity){
            if(parseInt(numStr)<0) return '0';
            if(parseInt(numStr)>1) return '1';
            return numStr;
        }
        if(parseInt(numStr)<0) return '0,';
        if(parseInt(numStr)>255) return '255,';
        return numStr+',';
    }
</script>
```

颜色选择器

```html
<HTML>
<HEAD>
<TITLE>页面背景篇--颜色选择器</TITLE>
</HEAD>
 
<BODY bgcolor="#fef4d2" >
<center>
<!-- 案例代码开始 -->
 
<form>
<!-- [Step1]: 这里可以设置选择框的行数 -->
  <select size=6 name=clr onchange="document.bgColor=this.options[this.selectedIndex].value">
<!-- [Step2]: 在此能够按序增加选择的颜色 -->
    <option value="blue"  selected>蓝色
    <option value="gold">金色
    <option value="red">红色
    <option value="yellow">黄色
    <option value="aquamarine">碧绿色 
    <option value="darkred">暗红色
    <option value="cadetblue ">灰蓝色 
    <option value="darkkhaki">黄褐色
    <option value="slateblue">蓝灰色
    <option value="deeppink">粉红色
    <option value="tan">棕褐色
    <option value="wheat">淡黄色
    <option value="turquoise">青绿色
  </select>
</form>
 
<!-- 案例代码结束 -->
</BODY>
</HTML>
```





## 选择背景图片

```html
<HTML>
    <BODY bgcolor="#fef4d2" >
    <center>
    <!-- 案例代码开始 -->
    <SELECT onChange="document.body.style.background=this.options[this.selectedIndex].value"> 
    <option value="url('/upload/files/201612/5821d9472ae.jpg')" SELECTED>背景图形1 
    <!-- [Step1]: 这里可以按序增加图形名称 -->
    <option value="url('/upload/files/201612/9b9f681af66.gif')">背景图形2 
    <!-- 案例代码结束 -->
    </BODY>
</HTML>
```

## 背景图片居中

```html
<HTML>
<HEAD>
<TITLE>页面背景篇--背景图形居中</TITLE>
</HEAD>
<BODY bgcolor="#fef4d2" >
<center>
<!-- 案例代码开始 -->
<!-- [Step1]: 这里可以设置居中的背景图形名称 -->
<style type="text/css">
body {background-image: url('/upload/files/201612/9b9f681af66.gif');
background-position:  center 50%;
background-repeat: no-repeat;
background-attachment: fixed}
</style>
<!-- 案例代码结束 -->
</BODY>
</HTML>
```

## 十二生肖

```html
<HTML>
<HEAD>
<TITLE>综合篇--十二生肖</TITLE>
</HEAD>
<BODY bgcolor="#fef4d2" >
<center>
<!-- 案例代码1开始 -->
<script language=JavaScript>
 
function GetBirthYear () {
  var birthpet=" 丑牛"
  x = (1997 - document.frm.inyear.value) % 12
  if ((x == 1) || (x == -11)) { birthpet=" 子鼠" }
  else {
   if (x == 0) { birthpet=" 丑牛" }
   else {
    if ((x == 11) || (x == -1)) {birthpet=" 寅虎" }
    else {
     if ((x == 10) || (x == -2)) {birthpet=" 卯兔" }
     else {
      if ((x == 9) || (x == -3)) {birthpet=" 辰龙" }
      else {
       if ((x == 8) || (x == -4)) { birthpet=" 巳蛇" }
       else {
        if ((x == 7) || (x == -5)) { birthpet=" 午马" }
        else {
		 if ((x == 6) || (x == -6)) { birthpet=" 未羊" }
         else {
          if ((x == 5) || (x == -7)) {birthpet=" 申猴" }
		  else {
           if ((x == 4) || (x == -8)) {birthpet=" 酉鸡" }
           else {
            if ((x == 3) || (x == -9)) {birthpet=" 戌狗" }
            else {
              if ((x == 2) || (x == -10)) {birthpet=" 亥猪" } }}}}}}}}}}}
   document.frm.birth.value = birthpet;
}
</script>
 
<!-- 案例代码1结束 -->
<!-- 案例代码2开始 -->
 
<form NAME="frm">
  请输入您的出生年份：<br><br>
<!-- [Step1]: 在此能够设置文本框的列长度和初始值 -->
  <input TYPE="text" size=5 NAME="inyear" value=" 1975"> 
  <input TYPE="button" VALUE="属相" onClick="GetBirthYear()">
  <input TYPE="text" SIZE=5 NAME="birth" value=" 卯兔"> 
</form> 
 
<!-- 案例代码2结束 -->
</BODY>
</HTML>
```

## 计算器

<img src="G:\Important重要\Learning-Notes\前端\markdown\images\js计算器.png" alt="js计算器" style="opacity:0.5;" />

```html
<HTML>
<HEAD>
<TITLE>综合篇--计算器</TITLE>
</HEAD>
<BODY bgcolor="#fef4d2" onload=StartCal()>
<center>
<!-- 案例代码1开始 -->
<script language=JavaScript>
    
var opStack = new Array(4)
    opStack[0]  = 0
    opStack[1]  = ''
    opStack[2]  = ''
    opStack[3]  = ''
    
function StartCal(){
    document.PAD.SUM.value= "0"
}
    
function KeyinNum()  {
    if (opStack[0] >= 2) { opStack[0] = 3 }
    else { opStack[0] = 1 }
    opStack[opStack[0]] = '' + document.PAD.SUM.value
}
    
function resetNum ()  {
    opStack[0] = 0
    opStack[1] = 0
    document.PAD.CAL.value = ''
    document.PAD.SUM.value = '0'
}
    
function calc1 (x)  {
    var opFlag = opStack[0]
    if (opFlag == -1 || opFlag == 1)   { count(x)  }
    else if (opFlag == 3)  {
    opStack[1] = '' + eval(opStack[1] + opStack[2] + opStack[3])
    count(x)   }
}
    
function count (x)  {
    if (x == 'Si') { opStack[1] = '' + Math.sin (opStack[1])  }
    else if (x == 'aS') { opStack[1] = '' + Math.asin(opStack[1])  }
    else if (x == 'Co') { opStack[1] = '' + Math.cos (opStack[1])  }
        else if (x == 'aC') { opStack[1] = '' + Math.acos(opStack[1])  }
        else if (x == 'Ta') { opStack[1] = '' + Math.tan (opStack[1]) }
        else if (x == 'aT') { opStack[1] = '' + Math.atan(opStack[1]) }
        else if (x == '≡') { opStack[1] = '' + Math.pow (opStack[1],.5) }
            else if (x == '^2') { opStack[1] = '' + Math.pow (opStack[1], 2) }
            else if (x == '^3') { opStack[1] = '' + Math.pow (opStack[1], 3) }
            else if (x == '^4') { opStack[1] = '' + Math.pow (opStack[1], 4) }
            else if (x == 'AB') { opStack[1] = '' + Math.abs (opStack[1])    }
                else if (x == '∽') { }
    document.PAD.CAL.value = ''
    opStack[0] = -1
    display()
    document.PAD.SUM.focus()
    document.PAD.SUM.select()
}
    
function display ()  {
    var sum  = parseFloat(opStack[1])
    document.PAD.SUM.value = '' + Math.round (sum * Math.pow(10,14)) / Math.pow(10,14)
}
    
function fra(){
    var i
    var j = 1
    var k = document.PAD.SUM.value
    if (k >= 70) {opStack[1] = 0; document.PAD.SUM.value = "---Error---"; return}
    for (i = 1; i <= k; i++){j = j * i}
    opStack[1] = document.PAD.SUM.value = j
    document.PAD.SUM.focus()
    document.PAD.SUM.select()
}
    
function entry (x) {
    if (opStack[0] == -1) { opStack[0] = 1; opStack[1] = ''}
    if (opStack[0] == 0)  { opStack[0] = 1; opStack[1] = ''}
    if (opStack[0] == 2)  { opStack[0] = 3; opStack[3] = ''}
    var result = result = opStack[opStack[0]]
    if (result == '0')    { result = ''  }
    if (x>='1' && x<='9') { result = '' + result + x }
    else if  (x == 'P') { result = '' + Math.PI  }
        else if  (x == '0') { if (result != '') result = '' + result  + '0' }
            else if  (x == 'B') { if (result != '') result = result.substring(0, result.length - 1) }
                else if  (x == '.') {
                    if (result != '')  { if (result.indexOf(".") == -1) result += "." }
                    else    { result = '0.'    }   }
    if (result =='') result = '0'
    opStack[opStack[0]] = result
    document.PAD.SUM.value = result
}
    
function calc2 (x)  {
    var opFlag = opStack[0]
    if (opFlag != 2)  {
    if (opFlag == 3)  {
        opStack[1]=''+eval(opStack[1]+opStack[2]+opStack[3])
        display()    }
    opStack[0] = 2
    opStack[2] = x
    document.PAD.CAL.value = x
    document.PAD.SUM.focus()
    document.PAD.SUM.select()  }
}
    
function neg()  {
    if (opStack[0] != 2  && opStack[0] != 0)  {
        opStack[0] = Math.abs(opStack[0])
        var result = opStack[opStack[0]]
        if (result != '0' && result != '') {
        if (result.charAt(0) == '-')  { result = result.substring(1, result.length) }
        else  { result = '-' + result   }
        opStack[opStack[0]] = result
        document.PAD.SUM.value = result  }  }
}
    
function TurnOff(){
    var ask = confirm("您确定要关闭计算器么？")
    if (ask == true) {window.close()}
    else {return}
}
    
</script>
<!-- 案例代码1结束 -->
    
<!-- 案例代码2开始 -->
<FORM NAME="PAD">
    <TABLE BORDER>
    <TR><TD COLSPAN=8>
        <INPUT NAME="CAL" TYPE="TEXT" SIZE=1 VALUE="">结果：
        <INPUT NAME="SUM" TYPE="TEXT" SIZE=16 VALUE="" onChange="KeyinNum()">
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE="重置" onClick="resetNum()">
        <TD><INPUT TYPE="BUTTON" VALUE="开方" onClick="calc1('≡')">
        <TD><INPUT TYPE="BUTTON" VALUE="平方" onClick="calc1('^2')">
        <TD><INPUT TYPE="BUTTON" VALUE="X !" onClick="fra()"  >
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE=" 7 " onClick="entry('7')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 8 " onClick="entry('8')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 9 " onClick="entry('9')">
        <TD><INPUT TYPE="BUTTON" VALUE=" * " onClick="calc2('*')">
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE=" 4 " onClick="entry('4')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 5 " onClick="entry('5')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 6 " onClick="entry('6')">
        <TD><INPUT TYPE="BUTTON" VALUE=" / " onClick="calc2('/')">
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE=" 1 " onClick="entry('1')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 2 " onClick="entry('2')">
        <TD><INPUT TYPE="BUTTON" VALUE=" 3 " onClick="entry('3')">
        <TD><INPUT TYPE="BUTTON" VALUE=" - " onClick="calc2('-')">
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE=" 0 " onClick="entry('0')">
        <TD><INPUT TYPE="BUTTON" VALUE=" . " onClick="entry('.')">
        <TD><INPUT TYPE="BUTTON" VALUE="+/-" onClick="neg()"    >
        <TD><INPUT TYPE="BUTTON" VALUE=" + " onClick="calc2('+')">
        <TR>
        <TD><INPUT TYPE="BUTTON" VALUE="关闭" onClick="TurnOff()">
        <TD><INPUT TYPE="BUTTON" VALUE="后退" onClick="entry('B')">
        <TD><INPUT TYPE="BUTTON" VALUE=" Pi "onClick="entry('P')">
        <TD><INPUT TYPE="BUTTON" VALUE=" = " onClick="calc1('=')" >
    </TABLE>
</FORM>
    
<!-- 案例代码2结束 -->
</BODY>
</HTML>
```

## 页面加载进度

```html
<HTML>
<HEAD>
<TITLE>综合篇--页面加载进度</TITLE>
</HEAD>
 
<BODY bgcolor="#fef4d2" >
<center>
<!-- 案例代码开始 -->
<form name="loading">
  <div align="center">
   <font>
<!-- [Step1]: 这里可以修改显示进度条区域的列长度 -->
<!-- [Step2]: 在此能够设置进度条的背景和本身的颜色 -->
     <input name="chart" size=42 style="background-color: #fef4d2; color: #FF0000; font-family: Arial; font-weight: bolder; border-style: none; padding: 0px"><br>
	 <input name="percent" size=5 style="background-color: #fef4d2;color: #0000FF; text-align: center; border-style: none; border-width: medium"> 
   </font> 
  </div>
</form>  
<script language=JavaScript>  
var bar = 0  
<!-- [Step3]: 这里可以更改进度条的符号 -->
var line = ">"  
var amount =">"  
LoadBar()  
 
function LoadBar(){  
  bar= bar+3  
  amount =amount  +  line  
  document.loading.chart.value=amount  
  document.loading.percent.value=bar+"%"  
<!-- [Step4]: 在此能够设置进度条加载的速度，数值大速度慢 -->
  if (bar<99)  {setTimeout("LoadBar()",1000);} 
<!-- [Step5]: 这里可以更改加载页面的网址 -->
  else  {window.location = "http://www.263.net.cn";}  
}  
</script> 
 
<!-- 案例代码结束 -->
</BODY>
 
</HTML>
```

## 当前时间

> 实时更新显示当前时间

```html
<HTML>
<HEAD>
<TITLE>时间日期篇--当前时间</TITLE>
</HEAD>
<BODY onLoad=showTheCurrentTime()>

<center>

<!-- 案例代码1开始 -->
<script LANGUAGE="JavaScript"> 
    function showMilitaryTime() {
        if (document.form.showMilitary[0].checked) return true;
        return false;
    }
    function showTheHours(theHour) {
        if (showMilitaryTime() || (theHour > 0 && theHour < 13)) return theHour;
        if (theHour == 0) return 12;
        return theHour-12;
    }
    function showZeroFilled(inValue) {
        if (inValue > 9) return "" + inValue;
        return "0" + inValue;
    }
    function showAmPm() {
        if (showMilitaryTime()) return "";
        if (now.getHours() < 12) return " am";
        return " pm";
    }
    function showTheCurrentTime() {
        now = new Date;
        document.form.showTime.value = (
            showTheHours(now.getHours()) + ":" 
            + showZeroFilled(now.getMinutes()) + ":" 
            + showZeroFilled(now.getSeconds()) 
            + showAmPm()
        )
        setTimeout("showTheCurrentTime()", 1000)
    }
</script>
<!-- 案例代码1结束 -->
    
    
<!-- 案例代码2开始 -->
<form name="form">
    <input type="text" name="showTime" size="11"><br/>
    <input type="radio" name="showMilitary" checked>24 Hour Time<br>
    <input type="radio" name="showMilitary">12 Hour Time
</form>
<!--案例代码2结束 -->
    
</center>

</BODY>    
</HTML>
```

## 倒计时

```html
<HTML>
<HEAD>
	<TITLE>时间日期篇--倒计时1</TITLE>
</HEAD>

<BODY onLoad=DownCount()>
    <script language=JavaScript>
        var theDay = new Date("January 1, 2021")  
        var DayALL    

        function DownCount(){
            var today = new Date() 
            var seconds = Math.floor((theDay.getTime() - today.getTime())/1000)
            var minutes = Math.floor(seconds/60)  
            var hours = Math.floor(minutes/60)  
            var days = Math.floor(hours/24)   
            CDay= days    
            CHour= hours % 24   
            CMinute= minutes % 60   
            CSecond= seconds % 60    
            DayALL =  CDay + " 天 " + CHour + " 小时 " + CMinute + " 分钟 " + CSecond + " 秒 "
            document.clock.DownCount.value = DayALL
            var counter = setTimeout("DownCount()", 1000)
        }
    </script>

    <form name = "clock">
        距离 2021 年 1 月 1 日，您将还有 <br>
        <input type="TEXT" name= "DownCount" size= "35">
    </form>

</BODY>
</HTML>
```

## 文本自动输出

1. 手册网版本

```html
<HTML>
<HEAD>
    <TITLE>文本特效篇--文本自动输出</TITLE>
</HEAD>
    
<BODY onload=TextOutput()>
    <form name=TyperText>
    <textarea name=tickfield rows=10 cols=38 wrap=virtual></textarea>
    </form>
</BODY>
</HTML>
<script language="JavaScript">
    function TList() {
        max = TList.arguments.length;
        for (i=0; i<max; i++){
            this[i]=TList.arguments[i];
        }
    }
    tl = new TList("传统的HTML语言不能开发交互式的动态网页，" + 
        "而JavaScript却能很好的做到这一点。JavaScript是一门相当简单易学的网络化编程语言，" + 
        "通过把她和HTML语言相互结合起来，能够实现实时的动态网页特效，" + 
        "这给网页浏览者在浏览网页的同时也提供了某些乐趣。"
    );
    var x = 0; 
    var pos = 0;
    var l = tl[0].length;
    function TextOutput() {
        document.TyperText.tickfield.value = tl[x].substring(0, pos) + "I";
        if(pos++ == l) {
            pos = 0; 
            setTimeout("TextOutput()", 1000); 
            if(++x == max) x = 0; 
            l = tl[x].length;
        } else {
            setTimeout("TextOutput()", 50);
        }
    }
</script>
```

2. 自写版本

> 两个定时任务:  一个用于更新文本索引,  另一个用于根据实时更新的索引去切分文本 并显示.

```html
<html>
<body>
    <div style="width:300px; height:300px;">
        <div id="myDiv"></div>
    </div>
</body>
</html>
<script>
    var text = "传统的HTML语言不能开发交互式的动态网页，而JavaScript却能很好的做到这一点。" + 
            "JavaScript是一门相当简单易学的网络化编程语言，通过把她和HTML语言相互结合起来，" + 
            "能够实现实时的动态网页特效，这给网页浏览者在浏览网页的同时也提供了某些乐趣。";
    
    //1.定时将索引+1;
    var index = 0;
    function addIndex(){
        if(index >= text.length){
            // clearInterval(timer1);
            // 如果要重新开始逐个显示, 就不要clearInterval, 而是重置index
            index = 0;
        }
        index++;
    }

    //2.定时更新subText, 并显示
    function showText(){
        var subText = text.substr(0, index+1);
        if(subText == text){
            // clearInterval(timer2);
            // 如果要重新开始逐个显示, 就不要clearInterval, 不作任何操作
        }
        console.log(subText);
        myDiv.innerText = subText;
    }
    var timer1 = setInterval('addIndex()', 100);
    var timer2 = setInterval('showText()', 100);

</script>
```

## 左右晃动

 http://www.shouce.ren/api/view/a/12497 

## 显示滚动字段

```html
<HTML>
<HEAD>
<TITLE>按钮特效篇--显示滚动字段</TITLE>
</HEAD>

<BODY>
    <script language=Javascript>
    var s = 0
    var ScrollMessage = " 按钮上显示滚动的字段 "
    document.write("<form name='Button1'><input type='button' " + "name='ScMessage' value='" + ScrollMessage + "'></form>")
        
    function ScrollButton() {
        document.Button1.ScMessage.value = ScrollMessage.substring(s,ScrollMessage.length) + ScrollMessage.substring(0,s)
        s++
        if (s >= ScrollMessage.length) {s = 0}
        setTimeout("ScrollButton()", 100)
    }
    ScrollButton();
    </script>
</BODY>
</HTML>
```





## 变换的 html 文本

```html
<HTML>
<HEAD>
    <TITLE>文本特效篇--变换的文本内容</TITLE>
</HEAD>
    
<BODY >
<center>
<!-- 案例代码1开始 -->
    
<script language="JavaScript">
    
var NowMessage = '文本特效篇--变换的文本内容';
var index = 1;
var indexNum = 8;
var indexs = new ChangeArray(indexNum);

indexs[1] = "文本特效篇--变换的文本内容";
indexs[2] = "传统的HTML语言不能开发交互式的动态网页，";
indexs[3] = "而JavaScript却能很好的做到这一点。";       
indexs[4] = "JavaScript是一门相当简单易学的网络化编程语言，";
indexs[5] = "通过把她和HTML语言相互结合起来，";
indexs[6] = "能够实现实时的动态网页特效，";
indexs[7] = "这给网页浏览者在浏览网页的同时也提供了某些乐趣。"; 
    
function ChangeMessage() {
    Change(indexs[index++]);                           
    if(index>indexNum) {
        index=1;
    }  
}
    
function Change(Message) {
    var pad_str="";
    n = Message.length;
    if(n<72) {
        pad = (38-n)/2;
        for(var i=0; i<pad; i++){
            pad_str+=" ";
        }
    }
    NowMessage = pad_str + Message;
    document.messages.field.value = NowMessage;
    clearTimeout(timer);
    timer = setTimeout("ChangeMessage()",2000);
}
    
function ChangeArray(n) {
    this.length=n;
    for(var i = 1; i<= n; i++){
        this[i] = "";
    }
    return(this);
}
    
function nochange() {
    document.messages.field.value = NowMessage;        
}
    
var timer = setTimeout('ChangeMessage()',1000);
    
</script>

<center><font face="Helvetica">
    <FORM name="messages" onSubmit="return false">
        <input type="text" name="field" size=50 value=" " onChange="nochange()">
    </FORM></font>
</center>

</BODY>
</HTML>
```



# JS 中的 prototype

**1 原型法设计模式**

原型法的主要思想是，现在有1个类A,我想要创建一个类B,这个类是以A为原型的,并且能进行扩展。我们称B的原型为A。

javascript 中的每个对象都有 prototype 属性，prototype 属性的解释是：返回对象类型原型的引用。

**2 javascript的方法可以分为三类**
1. 类方法
2. 对象方法
3. 原型方法

例子：

```js
function People(name)
{
  this.name = name;
  //对象方法
  this.Introduce = function(){
    alert("My name is " + this.name);
  }
}
//类方法
People.Run = function(){
  alert("I can run");
}
//原型方法
People.prototype.IntroduceChinese = function(){
  alert("我的名字是" + this.name);
}

//测试
var p1 = new People("Windking");
p1.Introduce();
People.Run();
p1.IntroduceChinese();
```



To be continue          http://www.shouce.ren/api/view/a/12762 



# 问题

1. 如何实现各种对齐方式?

```
↖ ↑ ↗
← o →
↙ ↓ ↘

未成功的代码

<html lang="en">
<head>
</head>
<style>
    div{
        font-size: 16px;
    }
    a{
        text-decoration: none;
        font-weight: bolder;
    }
</style>
<body>
    <div id='myDiv' style='height:100px;width:400px;background-color: #ccc;'>
        <span id='text' style="height: 10px;">这是一串文字</span>
    </div>
        <a href="javascript:align('left', 'verticalTop')">↖</a>
        <a href="javascript:align('center', 'verticalTop')">↑</a>
        <a href="javascript:align('right', 'verticalTop')">↗</a> <br/>
        <a href="javascript:align('left', 'verticalMiddle')">←</a>
        <a href="javascript:align('center', 'verticalMiddle')">o</a>
        <a href="javascript:align('right', 'verticalMiddle')">→</a> <br/>
        <a href="javascript:align('left', 'verticalBottom')">↙</a>
        <a href="javascript:align('center', 'verticalBottom')">↓</a>
        <a href="javascript:align('right', 'verticalBottom')">↘</a>
    </div>
</body>
</html>

<script>
    var originLineHieght = myDiv.style.lineHeight;
    function align(row, col){
        myDiv.style.textAlign = row;
        switch(col){
            case 'verticalTop':
                init();
                break;
            case 'verticalMiddle':
                init();
                console.log(text);
                myDiv.style.lineHeight = myDiv.style.height;
                break;
            case 'verticalBottom':
                init();
                console.log(text.style.height);
                myDiv.style.position = 'relative';
                text.style.position = 'absolute';
                text.style.top = '50%';
        }
    }
    function init(){
        myDiv.style.lineHeight = originLineHieght;
        myDiv.style.position = undefined;
        text.style.position = undefined;
    }
</script>

```



