# HTML

## 1 常用HTML标签(元素)

`VS Code` 快速创建 html：

```
! + tab键  
或
html:5 + tab键
```



#### 标签按显示效果分类

```
块元素标签：	默认独占一行
内联元素标签：默认可以排列在一行
```



#### 常用块元素标签

1-6 级标题标签

```
<h1></h1> ---- <h6></h6>
标题独占一行 （块元素）
默认含有样式 ---- 间距、文字大小等
```

段落标签 p

```
<p></p>
段落独占一行，只有末尾一个换行（也属于块元素）
如果要增加换行，使用 <br />标签
```

```
字符实体
换行：<br />
不间断空格：&nbsp;	（non-breaking space）
小于号、大于号的字符实体：
	<	&lt;	(less than) 
	>	&gt;	(greater than)
标签的字符实体：&lt;p&gt;是一个段落标签 ---- 显示为 <p>是一个段落标签

§	小节	&sect;	&#167;
×	乘号	&times;	&#215;
÷	除号	&divide;
¥	元（yen）	&yen;
&	和号	&amp;	&#38;
"	引号	&quot;
```

```
与：and
按位与：&，相当于每一个二进制数之间用 and 运算
```

#### 文本格式化标签

![文本格式化标签](.\images\文本格式化标签.png)

```
<small>		定义小号字
<sub>		定义下标字
<sup>		定义上标字
```



通用块元素标签 `<div> </div>`

```
div 是一个容器，常做嵌套使用，没有默认样式
输入 div*3 + 按Tab键，一次创建多个标签
自带换行
```





#### 常用内联元素标签

1 超链接标签 a

```html
-- 通过href属性设置链接地址
 
文字增加链接
<a href="http://www.zhihu.com">转到知乎</a>

图片增加链接
<a href="http://www.zhihu.com">
    <img src="xxxx.png" alt="xxxx"> <img>
</a>

默认链接地址 # (不跳转)
<a href="#">默认链接地址</a>
```

2 图片标签 img

```
-- 通过src属性设置图片地址, 根据地址自动获取图片
-- 通过title设置图片文字说明
-- 通过alt属性设置在图片无法加载时的文字描述
<img src="img_path" title="img_name" alt="failed_to_load"> <img>
```

3  通用内联标签 span 

```
<span>普通文字</span>
```



## 2 html布局

####网页布局原理

```
1.由整体到局部
2.由行到列
```

#### 标签的语义化

为什么要语义化标签？

```
-- 在合适的地方，用合适的标签

1 首先是为了让搜索引擎能更好地理解网页的结构，提高网站在搜索中的排名(也叫做SEO搜索引擎优化)；
2 其次是方便代码的阅读和维护。
```

带语义的标签

```
h1~h6	表示标题
p		表示段落
img		表示图片
a		表示链接
```

不带语义的标签 

```
div		表示一块内容
span	表示行内的一块内容
```



## 3 html列表

#### 无序列表 ul

```html
<ul> unOrder list 无序列表
      <li>列表项1</li>
      <li>列表项2</li>
      <li>列表项3</li>
</ul>
```

#### 有序列表 ol

```html
<ol>  order list 有序
    <li>列表项1</li>
    <li>列表项2</li>
    <li>列表项3</li>
</ol>
```

#### 自定义列表 dl

```
<dl> 自定义列表 dl
	<dt>
        <dd>。。。</dd>
        <dd>。。。</dd>
        <dd>。。。</dd>
    </dt>
</dl>
```



## 4 html表格 + css样式

#### 表格的基本语法

```
<table>
  <aption>标题</aption>
  <tr>
  	<th>表头单元格1</th>
  	<th>表头单元格2</th>
  	<th>表头单元格3</th>
  </tr>
  <tr>
    <td>第二行单元格1</td>
    <td>第二行单元格2</td>
    <td>第二行单元格3</td>
  </tr>
</table>
```

#### 表格属性设置

1- 快捷键创建表格

```
<!-- 创建一个4行3列的表格 -->

table>(tr>td*3)*4  +  Tab键
```

2- 整个表格的宽度、高度设置

```
width: 800px;
height: 800px;
```

3- 表格边框

```
border: 1px solid skyblue;
border-collapse: collapse

cellspacing 设置单元格 与 单元格边框之间的空白间距
cellpadding 设置单元格内容 与 单元格边框之间的空白间距
```

4- 表格背景

```
background-color: grey;
```

5- 表格居中、文本居中

```
margin: 0 auto;
text-align: center;
```

6- 合并单元格

```
行间合并
<td rowspan="2">合并后显示的文本</td>
列间合并
<td colspan="2">合并后显示的文本</td>
```



## 5 表单

在HTML中，一个完整表单的组成:

1. 表单域
2. 提示信息
3. 表单控件（也称为表单元素）



#### form 表单域

form 标签被用于定义表单域，即创建一个表单，以实现用户信息的收集和传递，form中的所有内容都会被提交给服务器。创建表单的基本语法格式如下：

```html
<form action="url地址" method="提交方式" name="表单名称">
  各种表单控件
</form>
```

常用属性：

1. action
   在表单收集到信息后，需要将信息传递给服务器进行处理，action属性用于指定接收并处理表单数据的服务器程序的url地址。
2. method
   用于设置表单数据的提交方式，其取值为 get 或 post。
3. name
   用于指定表单的名称，以区分同一个页面中的多个表单。

**注意：  每个表单都应该有自己表单域。**



#### label 标注

label 标签为 input 元素定义标注（标签）。

作用：  用于绑定一个表单元素, 当点击 label 标签的时候, 被绑定的表单元素就会获得输入焦点, for 属性规定 label 与哪个表单元素绑定。

```html
<label for="male">Male</label>
<input type="radio" name="sex" id="male" value="male">
```



#### input 控件

`<input />` 标签为单标签, 有多种属性:

```
type: 最基本的属性, 用于指定不同的空间类型: <input type="text" /> 
name: 控件名称, 由用户自定义.
value: input控件中的默认文本值, 由用户自定义
size: input控件在页面中的显示宽度, 正整数
checked: 定义radio控件默认被选中的项, checked="checked", 如:
      <form action="">
        <input type="radio" checked="checked" name="a">A 
        <input type="radio" name="a">B 
        <input type="radio" name="a">C 
        
        <select name="b">
            <option value="A">A</option>
            <option value="B" selected="selected">B</option>
            <option value="C">C</option>
        </select>
      </form>

selected: 定义select下拉框默认被选中的项, selected="selected"
maxlength:  输入型控件允许输入的最多字符数, 正整数
```

type 属性值:

- text:  单行文本输入框
- password:  密码输入框
- radio:  单选按钮
- checkbox:  复选框
- button:  普通按钮
- submit:  提交按钮
- reset:  重置按钮
- image:  图像形式的提交按钮
- file:  文件域
- color:  颜色按钮,  可以打开系统的颜色选择框

```html
<input value="#ff0000" type="color">  初始value有值是设置了一个默认值, 选好颜色后会更新value
```



#### textarea 控件(文本域)

如果需要输入大量的信息，就需要用到 `<textarea> </textarea>` 标签。通过 textarea 控件可以轻松地创建多行文本输入框，其基本语法格式如下：

```html
<textarea cols="每行中的字符数" rows="显示的行数">
  文本内容
</textarea>
```



#### select 下拉菜单

```html
<select>
  <option>选项1</option>
  <option>选项2</option>
  <option>选项3</option>
  ...
</select>
```

1. <select&gt;</select&gt;中至少应包含一对&lt;option></option&gt;。
2. 在option 中定义selected ="selected "时，当前项即为默认选中项。



#### 更多

更多见标题: HTML5新标签与特性





## 6 HTML5 新标签与特性



#### 字符设定

```
<meta http-equiv="charset" content="utf-8">   HTML与XHTML中建议这样去写
<meta charset="utf-8">   HTML5的标签中建议这样去写
```

#### 常用新标签

- header：定义文档的页眉
- nav：定义导航链接的部分
- footer：定义文档或节的页脚
- article：标签规定独立的自包含内容
- section：定义文档中的节（section、区段）
- aside：定义其所处内容之外的内容

#### 常用新属性

| 属性         | 用法                                             | 含义                                        |
| ------------ | ------------------------------------------------ | ------------------------------------------- |
| placeholder  | `<input type="text" placeholder="请输入用户名">` | 占位符提供可描述输入字段预期值的提示信息    |
| autofocus    | `<input type="text" autofocus>`                  | 规定当页面加载时 input 元素应该自动获得焦点 |
| multiple     | `<input type="file" multiple>`                   | 多文件上传                                  |
| autocomplete | `<input type="text" autocomplete="off">`         | 规定表单是否应该启用自动完成功能            |
| required     | `<input type="text" required>`                   | 必填项                                      |
| accesskey    | `<input type="text" accesskey="s">`              | 规定激活（使元素获得焦点）元素的快捷键      |

#### 新增的type属性值

| 类型     | 示例                      | 含义                 |
| -------- | ------------------------- | -------------------- |
| email    | `<input type="email">`    | 输入邮箱格式         |
| tel      | `<input type="tel">`      | 输入手机号码格式     |
| url      | `<input type="url">`      | 输入url格式          |
| number   | `<input type="number">`   | 输入数字格式         |
| search   | `<input type="search">`   | 搜索框（体现语义化） |
| range    | `<input type="range">`    | 自由拖动滑块         |
| time     | `<input type="time">`     |                      |
| date     | `<input type="date">`     |                      |
| datetime | `<input type="datetime">` |                      |
| month    | `<input type="month">`    |                      |
| week     | `<input type="week">`     |                      |

#### 示例

```html
<form action="">
    <fieldset>
        <legend>学生档案</legend>
        
        <label for="userName">姓名:</label>
        <input type="text" name="userName" id="userName" placeholder="请输入用户名"> <br>
        
        <label for="userPhone">手机号码:</label>
        <input type="tel" name="userPhone" id="userPhone" pattern="^1\d{10}$"><br>
        
        <label for="email">邮箱地址:</label>
        <input type="email" required name="email" id="email"><br>
        
        <label for="collage">所属学院:</label>
        <input type="text" name="collage" id="collage" list="cList" placeholder="请选择"><br>
        <datalist id="cList">
        <option value="前端与移动开发学院"></option>
        <option value="java学院"></option>
        <option value="c++学院"></option>
        </datalist><br>
        
        <label for="score">入学成绩:</label>
        <input type="number" max="100" min="0" value="0" id="score"><br>
        
        <label for="level">基础水平:</label>
        <meter id="level" max="100" min="0" low="59" high="90"></meter><br>
        
        <label for="inTime">入学日期:</label>
        <input type="date" id="inTime" name="inTime"><br>
        
        <label for="leaveTime">毕业日期:</label>
        <input type="date" id="leaveTime" name="leaveTime"><br>
        
        <input type="submit">
        
    </fieldset>
</form>
```



#### 多媒体标签

- embed：标签定义嵌入的内容

  ```html
  embed可以用来插入各种多媒体，格式可以是 Midi、Wav、AIFF、AU、MP3等等。url为音频或视频文件及其路径，可以是相对路径或绝对路径。
  
  <embed src="http://player.youku.com/player.php/sid/XMTI4MzM2MDIwOA==/v.swf" allowFullScreen="true" quality="high" width="480" height="400" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash"></embed>
  ```

- audio：播放音频

  ```html
  <audio src="./1.mp3" autoplay controls loop> </audio>
  属性说明:
      autoplay 自动播放
      controls 是否显不默认播放控件
      loop 循环播放
  
  PS:
  由于版权等原因，不同的浏览器可支持播放的格式是不一样的,
  多浏览器支持的方案:
  <audio controls>
  	<source src="./1.mp3">
  	<source src="./1.wav">
  	<source src="./1.ogg">
  	您的浏览器不支持 html 音频播放功能
  <audio>
  ```

- video：播放视频

  ```html
  <video src="" controls="controls"></video>
  autoplay 自动播放
  controls 是否显示默认播放控件
  loop 循环播放
  width 设置播放窗口宽度
  height 设置播放窗口的高度
  
  PS:
  由于版权等原因，不同的浏览器可支持播放的格式是不一样的,
  多浏览器支持的方案:
  <video controls="controls">
      <source src="./1.ogg">
      <source src="./1.mp4">
     	您的浏览器不支持 html 视频播放功能
  </video>
  ```