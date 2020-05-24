# (〇) CSS 参考手册

- http://css.doyoe.com
- https://github.com/doyoe/css-handbook 

# (一)  CSS基础

CSS:  Cascading Style Sheets

CSS样式表 或 层叠样式表（级联样式表）,  主要用于设置HTML页面中的文本内容（字体、大小、对齐方式等）、图片的外形（宽高、边框样式、边距等）以及版面的布局等外观显示样式。



## css引入方式

1、**内联式**：通过标签的style属性，在标签上直接写样式

```
<div style="width:100px; height:100px; background:red ">
	......
</div>
```

2、**嵌入式**：通过style标签，在网页上创建嵌入的样式表

```
<style type="text/css">
    div{ 
    	width:100px; 
    	height:100px; 
    	background:red 
       }
</style>
```

3、**外链式**：通过link标签，链接外部样式文件到页面中

```
<link rel="stylesheet" type="text/css" href="css/main.css">

link标签需要放在 head 头部标签中，并且必须指定 link 标签的三个属性:
    href：定义外部样式表文件的URL，相对路径 或 绝对路径
    type：定义文档类型，需要指定为“text/CSS”
    rel：定义当前文档与被链接文档之间的关系，在这里需要指定为“stylesheet”，表示被链接的文档是一个样式表文件。
```

三种样式表总结

| 样式表     | 优点                     | 缺点                     | 使用情况       | 控制范围           |
| ---------- | ------------------------ | ------------------------ | -------------- | ------------------ |
| 行内样式表 | 书写方便，权重高         | 没有实现样式和结构相分离 | 较少           | 控制一个标签（少） |
| 内嵌样式表 | 部分结构和样式相分离     | 没有彻底分离             | 较多           | 控制一个页面（中） |
| 外部样式表 | 完全实现结构和样式相分离 | 需要引入                 | 最多，强烈推荐 | 控制整个站点（多） |



## 选择器

```html
1 标签选择器
2 类选择器
3 多类名选择器
4 层级选择器
5 id选择器
6 组选择器
	多个选择器，有同样的样式设置。
    .box1,.box2,.box3{ width:100px;height:100px }
    .box1{background:red}
    .box2{background:pink}
    .box2{background:gold}
	......
    <div class="box1">....</div>
7 伪类选择器
	常用的伪类选择器有hover，表示鼠标悬浮在元素上时的状态。
	.box1 {width:100px;height:100px;background:gold;}
	.box1:hover{width:300px;}
。。。
```



## 样式属性

#### 布局常用样式属性

```
width: 300px;
height: 300px;

float: left;
background: green;
border: 1px solid black; (增加边框)
table{ border-collapse:collapse; }   (表格边框合并在一起)

padding: 15px; (增加内边距)
padding-top: 15px; (增加顶部内边距，bottom，left， right)
margin: 15px; (增加外边距)
margin-top: 15px;(增加顶部外边距，bottom，left， right)
```



#### 文本常用样式属性

```
color: red; (字体颜色)
color: rgba(r,g,b,a)  a 是alpha  透明的意思  取值范围 0~1之间
	如: color: rgba(0,0,0,0.3)  

font-size:14px; (字体大小)
font-family: 'Microsoft YaHei'; (字体类型)
font-weight: 500; (字体比重--粗细--400~900)
font-style: xxx (字体风格)
	normal：默认值，浏览器会显示标准的字体样式。
    italic：浏览器会显示斜体的字体样式。
    oblique：浏览器会显示倾斜的字体样式。

font:  (综合设置字体样式)
	使用font属性时，必须按下面语法格式中的顺序书写，各个属性以空格隔开。
	选择器 {font: font-style  font-weight  font-size/line-height  font-family;}

line-height: 40px; (行高--一般设置行高等于字体高度)
text-indent: 2em;  (文本缩进，间距为 2*当前文本大小)
text-indent: 20px; (文本缩进，指定像素)

text-decoration: none; (设置是否显示下划线)
text-shadow: 水平位置 垂直位置 模糊距离 阴影颜色;  (文字阴影, 前两项必写, 后两项可选)

letter-spacing:  字间距, 其属性值可为不同单位的数值，允许使用负值，默认为normal。
word-spacing:    单词间距，其属性值可为不同单位的数值，允许使用负值，默认为normal。
```



#### 居中

```
带有宽度的块级元素居中对齐:   margin: 0 auto;
文字居中对齐:               text-align: center;
垂直对齐:                   vertical-align : middle;
```

**vertical-align** : baseline |top |middle |bottom

> vertical-align 不影响块级元素中的内容对齐，它只针对于 行内元素或者行内块元素，特别是行内块元素， 通常用来控制图片和表单等。
>
> 以一行内包含文字和图片为例:

1. vertical-align: baseline;   基线对齐(默认),  文字和图片基线对齐
2. vertical-align: middle;   垂直居中对齐,  文字和图片中部对齐
3. vertical-align: top;   顶部对齐, 文字和图片的顶部对齐

**去除图片底侧空白缝隙**

有个很重要特性要记住： 如果一个元素没有基线，比如图片或者表单等行内块元素，则他的底线会和父级盒子的基线对齐。这样会造成一个问题，就是图片底侧会有一个空白缝隙。

解决的方法就是：  

a.给img vertical-align:middle | top等等。  让图片不要和基线对齐。

b.给img 添加 display：block; 转换为块级元素就不会存在问题了。





## 样式的 继承性

```
color、text开头的、font开头的， 都可以继承
```



###### 

###### 

###### 



# (二)  CSS进阶

## 1 复合选择器

| 选择器     | 作用           | 特征         | 使用情况 | 隔开符号及用法                     |
| ------- | ------------ | ---------- | ---- | --------------------------- |
| 后代选择器   | 用来选择元素后代     | 是选择所有的子孙后代 | 较多   | 符号是**空格** .nav a            |
| 子代选择器   | 选择 最近一级元素    | 只选亲儿子      | 较少   | 符号是**>**   .nav>p           |
| 交集选择器   | 选择两个标签交集的部分  | 既是 又是      | 较少   | **没有符号**  p.one             |
| 并集选择器   | 选择某些相同样式的选择器 | 可以用于集体声明   | 较多   | 符号是**逗号** .nav, .header     |
| 链接伪类选择器 | 给链接更改状态      |            | 较多   | 重点记住 a{} 和 a:hover  实际开发的写法 |



## 2 标签显示模式 - display

1. none  (区别于 visibility: hidden;)
2. block
3. inline
4. inline-block
5. flex 弹性盒

#### 区别

| 元素模式                          | 元素排列                                     | 设置样式                               | 默认宽度                     | 包含                     |
| --------------------------------- | -------------------------------------------- | -------------------------------------- | ---------------------------- | ------------------------ |
| 块级元素                          | 一行只能放一个块级元素                       | 可以设置宽度高度                       | 容器的100%                   | 容器级可以包含任何标签   |
| 行内元素                          | 一行可以放多个行内元素                       | 不可以直接设置宽度高度                 | 它本身内容的宽度             | 容纳文本或则其他行内元素 |
| 行内块元素  **(img /input / td)** | 和相邻 行内块 在一行上, 但是之间会有空白缝隙 | 高度，行高、外边距以及内边距都可以控制 | 默认宽度就是它本身内容的宽度 |                          |



```
        flex(弹性盒、伸缩盒)
            - 是CSS中的又一种布局手段，它主要用来代替浮动来完成页面的布局
            - flex可以使元素具有弹性，让元素可以跟随页面的大小的改变而改变
            - 弹性容器
                - 要使用弹性盒，必须先将一个元素设置为弹性容器
                - 我们通过 display 来设置弹性容器
                    display:flex  设置为块级弹性容器
                    display:inline-flex 设置为行内的弹性容器

            - 弹性元素
                - 弹性容器的子元素是弹性元素（弹性项）
                - 弹性元素可以同时是弹性容器
```





**---------!--------- p 标签/ h标题标签/ dt      中 不能放 div --------------**



#### 模式切换

```html
<style>
        .display_mode_01{
            /* 行内元素inline：多个元素显示在一行，不能设置宽度、高度，大小等于自己内容的大小。 */
            display: inline;
        }
        .display_mode_02{
            /* 行内块元素inline-block，多个元素显示在一行，可以设置宽度、高度。 */
            display: inline-block;
        }
        .display_mode_03{
            /* 块级元素block：单个元素单独占一行， 可以设置宽度、高度。 */
            display: block;
        }
        .display_mode_04{
            /* 隐藏元素，不占有位置 */
            display: none;
        }
        .display_mode_05{
            /* 隐藏元素， 占有位置 */
            visibility: hidden;
        }
</style>
```



## 3. 元素的显示与隐藏

在CSS中有三个显示和隐藏的单词比较常见，我们要区分开，他们分别是 display visibility 和 overflow。

他们的主要目的是让一个元素在页面中消失，但是不在文档源码中删除。 最常见的是网站广告，当我们点击类似关闭不见了，但是我们重新刷新页面，它们又会出现和你玩躲猫猫！！

#### display 显示

display 设置或检索对象是否及如何显示。

```
display : none;   隐藏对象
display:block;    除了转换为块级元素之外，同时还有显示元素的意思。
特点： 隐藏之后，不再保留位置。
```

#### visibility 可见性

设置或检索是否显示对象。

```
visibility: visible;  　对象可视
visibility: hidden;     对象隐藏
特点： 隐藏之后，继续保留原有位置。
```

#### overflow 溢出

检索或设置当对象的内容超过其指定高度及宽度时如何管理内容。

```
overflow: visible;  不剪切内容也不添加滚动条。
overflow: auto;     超出自动显示滚动条，不超出不显示滚动条
overflow: hidden;   不显示超过对象尺寸的内容，超出的部分隐藏掉
overflow: scroll;   不管超出内容否，总是显示滚动条
```



------

:smile:  **快捷创建 使用了类选择器的多个div标签**

<1>   .box01+.box02+.box03  加Tab键

<2>   .con>.box01+.box02+.box03  加Tab键

------



## 4 权重

CSS 三大特性:  层叠 继承  优先级

```
a 当使用的选择器相同时, 按层叠性(后写的属性会覆盖先写的属性)
b 当使用的选择器不同时, 按权重值
```

#### 权重值比较

| 继承或者* 的贡献值       | 0,0,0,0  |
| ------------------------ | -------- |
| 每个元素（标签）贡献值为 | 0,0,0,1  |
| 每个类，伪类贡献值为     | 0,0,1,0  |
| 每个ID贡献值为           | 0,1,0,0  |
| 每个行内样式贡献值       | 1,0,0,0  |
| 每个 !important 贡献值   | ∞ 无穷大 |

```
1、行内式，如：style=””，权重值为1000 ---> 1,0,0,0
2、ID选择器，如：#content，权重值为100  ---> 0,1,0,0
3、类，伪类，如：.content、:hover 权重值为10 ---> 0,0,1,0
4、标签选择器，如：div、p 权重值为1 ---> 0,0,0,1
5  继承 或 *通配符选择器, 权重为0 ---> 0,0,0,0

-- 权重值相同：对于权重值相同的同种选择器，后写的会覆盖先写的
-- 权重值比较：按位比较---- (0 0 0 0), 不是简单地将各个选择器的权重值相加的和来比较
	0(行内式)  0(id选择器)  0(类选择器)  0(标签选择器)

---!import---的使用:
	在样式属性后面添加  权重最高, 为 无穷大
	
```

#### 权重叠加

```
按位相加
每一位上, 进行简单的十进制加法, 且不会进位
> 比如说： 0,0,0,5 + 0,0,0,5 =0,0,0,10 而不是 0,0, 1, 0， 所以不会存在10个div能赶上一个类选择器的情况。
比较之下, 只要最高位值更大的, 权重值就更大

实例:
	div ul li	---->  0,0,0,3
	.cls ul li	---->  0,0,1,2
	a:hover		---->  0,0,1,1
    .cls a		---->  0,0,1,1
    
```

#### 继承的权重为0

![Alt text](/images/继承的权重为0.png)



最终颜色是: blue



![Alt text](/images/计算权重值的步骤.png)



## 5 背景 - background

CSS 可以添加背景颜色和背景图片，以及来进行图片设置。

| background-color                                            | 背景颜色         |
| ----------------------------------------------------------- | ---------------- |
| background-image                                            | 背景图片地址     |
| background-repeat                                           | 是否平铺         |
| background-position                                         | 背景位置         |
| background-attachment                                       | 背景固定还是滚动 |
| 背景的合写（复合属性）                                      |                  |
| background:背景颜色 背景图片地址 背景平铺 背景滚动 背景位置 |                  |

背景颜色

```
background-color: apparent | "具体颜色"
"具体颜色"可以是: 英文单词 | #号+16进制数 | rgb(num1,num2,num3) | rgba(num1,num2,num3,0.5)
```

背景图片

```
background-image: none | url(images/1.png)
文字会显示在图片上层
```

背景平铺

```
background-repeat : repeat | no-repeat | repeat-x | repeat-y 

repeat : 　背景图像在纵向和横向上平铺（默认的）
no-repeat : 　背景图像不平铺
repeat-x : 　背景图像在横向上平铺
repeat-y : 　背景图像在纵向平铺 
```

背景位置

```
background-position : length || length
background-position : position || position 

length : 　百分数 | 由浮点数字和单位标识符组成的长度值。请参阅长度单位 
position : 　top | center | bottom | left | center | right 
```

背景附着

```
background-attachment : scroll | fixed 

scroll : 　背景图像是随对象内容滚动
fixed : 　背景图像固定 
```

背景简写

```
background: transparent url(image.jpg) repeat-y  scroll 50% 0 ;
```

背景透明

```
background: rgba(0,0,0,0.3);

注:
背景半透明是指盒子背景半透明， 盒子里面的内容不收影响,
同样, 可以给 文字和边框透明,  都是 rgba 的格式来写:
color:rgba(0,0,0,0.3);
border: 1px solid rgba(0,0,0,0.3);
```

多背景

```
background-image: url('images/gyt.jpg'),url('images/robot.png');
```



###### 

###### 

# (三) CSS重点

1. 盒子模型 
2. 浮动
3. 定位



## 1.盒子模型 

所谓盒子模型就是把HTML页面中的元素看作是一个矩形的盒子。

盒子的组成:

1. 内容区 (content)
2. 内边距 (padding)
3. 边框 (border)
4. 外边距 (margin)



#### 内边距 - padding

边框与内容之间的距离。

```
padding: 上左右下内边距
padding-top: 上内边距
padding-right: 右内边距
padding-left: 左内边距
padding-bottom: 下内边距
```

> 注意：  padding 后面跟几个数值表示的意思是不一样的。

| 值的个数 | 表达意思                                                     |
| -------- | ------------------------------------------------------------ |
| 1个值    | padding：上下左右边距 比如 padding: 3px; 表示上下左右都是3像素 |
| 2个值    | padding: 上下边距 左右边距 比如 padding: 3px 5px; 表示 上下3像素 左右 5像素 |
| 3个值    | padding：上边距 左右边距 下边距 比如 padding: 3px 5px 10px; 表示 上是3像素 左右是5像素 下是10像素 |
| 4个值    | padding:上内边距 右内边距 下内边距 左内边距 比如: padding: 3px 5px 10px 15px; 表示 上3px 右是5px 下 10px 左15px **顺时针** |





#### 边框 - border

```
border : border-width || border-style || border-color 
border-style: 	
    none：无边框
    solid：单实线
    dashed：虚线
    dotted：点线
    double：双实线

圆角边框:
    border-radius: 水平半径/垂直半径;
    一般我们垂直半径都是省略的默认和水平半径一样:
    border-radius: 左上角  右上角  右下角  左下角;
```

> 盒子边框总结表:

|              |                                                              |                                                              |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 设置内容     | 样式属性                                                     | 常用属性值                                                   |
| 上边框       | border-top-style:样式; border-top-width:宽度;border-top-color:颜色;border-top:宽度 样式 颜色; |                                                              |
| 下边框       | border-bottom-style:样式;border- bottom-width:宽度;border- bottom-color:颜色;border-bottom:宽度 样式 颜色; |                                                              |
| 左边框       | border-left-style:样式; border-left-width:宽度;border-left-color:颜色;border-left:宽度 样式 颜色; |                                                              |
| 右边框       | border-right-style:样式;border-right-width:宽度;border-right-color:颜色;border-right:宽度 样式 颜色; |                                                              |
| 样式         | border-style:上边 [右边 下边 左边];                          | none无（默认）、solid单实线、dashed虚线、dotted点线、double双实线 |
| 宽度         | border-width:上边 [右边 下边 左边];                          | 像素值                                                       |
| 颜色         | border-color:上边 [右边 下边 左边];                          | 颜色值、#十六进制、rgb(r,g,b)、rgb(r%,g%,b%)                 |
| 边框综合设置 | border:四边宽度 四边样式 四边颜色;                           |                                                              |





#### 外边距 - margin

设置外边距会在元素之间创建“空白”， 这段空白通常不能放置其他内容。

```
margin-top: 上外边距
margin-right: 右外边距
margin-bottom: 下外边距
margin-left: 上外边距
margin: 上外边距 右外边距  下外边距  左外边
```

#### + 外边距实现盒子水平居中

可以让一个盒子实现水平居中，需要满足一下两个条件：

1. 必须是块级元素。
2. 盒子必须指定了宽度（width）

然后就给左右的外边距都设置为auto，就可使块级元素水平居中。

实际工作中常用这种方式进行网页布局，示例代码如下：

~~~css
.header{ 
    width: 960px; 
    margin:0 auto;
}
~~~

#### + 清除默认内外边距

为了更方便地控制网页中的元素，制作网页时，可使用如下代码清除元素的默认内外边距： 

~~~css
* {
   padding:0;         /* 清除内边距 */
   margin:0;          /* 清除外边距 */
}
~~~

注意：  行内元素是只有左右内外边距的，是没有上下内外边距的。

#### + 外边距合并

使用 margin 定义块元素的垂直外边距时，可能会出现外边距的合并。

1. 相邻块元素垂直外边距的合并

当上下相邻的两个块元素相遇时，如果上面的元素有下外边距 margin-bottom，下面的元素有上外边距 margin-top，则他们之间的垂直间距不是 margin-bottom 与 margin-top 之和，而是两者中的较大者。这种现象被称为相邻块元素垂直外边距的合并（也称 **外边距塌陷**）。

2. 嵌套块元素垂直外边距的合并

对于两个嵌套关系的块元素，如果父元素没有上内边距及边框，则父元素的上外边距会与子元素的上外边距发生合并，合并后的外边距为两者中的较大者，即使父元素的上外边距为0，也会发生合并。解决方案：

```
1. 可以为父元素定义1像素的上边框或上内边距。
2. 可以为父元素添加 overflow:hidden。
```



#### + 盒子的总宽度&总高度

width 和 height 的属性值可以为不同单位的数值或相对于父元素的百分比%，实际工作中最常用的是像素值。

```
盒子的总宽度 = width + 左右内边距之和 + 左右边框宽度之和 + 左右外边距之和
	即:
	margin-left + border-left-width + padding-left 
	+ width 
	+ border-right-width + padding-right + margin-right

盒子的总高度 = height + 上下内边距之和 + 上下边框宽度之和 + 上下外边距之和

注:
1、宽度属性width和高度属性height仅适用于块级元素，对行内元素无效（ img 标签和 input除外）。
2、计算盒子模型的总高度时，还应考虑上下两个盒子垂直外边距合并的情况。
```

三个计算题

```
1. .demo{width:200px;height:200px;border:1px solid red; padding:20px;}， 盒子最终占有的空间是多大？
2. 一个盒子需要占用的空间是 400像素， 但是盒子又有 padding:25px, border: 1px solid red; 问，我们需要改动盒子宽度为多少？
3. 如何让一个200 * 200像素的盒子， 在一个400 * 400的盒子里面水平居中，垂直居中。
```



#### + 盒子布局稳定性

什么情况下使用内边距，什么情况下使用外边距？

```
根据稳定性来分，建议如下：
按照 优先使用  宽度 （width） 其次 使用内边距（padding） 再次  外边距（margin）。 
  width >  padding  >  margin
```



#### + CSS3盒模型

CSS3中可以通过 `box-sizing` 来指定盒模型，即可指定为 content-box、border-box，这样我们计算盒子大小的方式就发生了改变。

可以分成两种情况：

1. box-sizing: border-box  盒子大小为 width

2. box-sizing: content-box  盒子大小为 width + padding + border

```
div {
  width: 100px;
  height: 100px;
  background: skyblue;
  margin: 0 auto;
  border: 1px solid gray;

  /* 
  默认的设置 如果我们添加了 border属性 该容器的大小会发生改变
  因为他要优先保证内部的内容所占区域 不变
  */

  /*  
  box-sizing  如果不设置 默认的值 就是 
  content-box: 优先保证内容的大小 对盒子进行缩放;
  border-box: 让 盒子 优先保证自己所占区域的大小,对内容进行压缩;
  */
  box-sizing: border-box;
}
```

#### + 盒子阴影

```
box-shadow: 水平阴影 垂直阴影 模糊距离(可选) 阴影尺寸(可选) 阴影颜色(可选)  内/外阴影(可选)；
```

1. 前两个属性是必须写的。其余的可以省略。
2. 外阴影 (outset) 但是不能写    默认      想要内阴影  inset 

```
img {
  border:10px solid orange;
  box-shadow:3px 3px 5px 4px rgba(0,0,0,1);
}
```



## 2.浮动 - float

CSS的定位机制有3种：

1. 普通流（标准流）
2. 浮动
3. 定位

#### 浮动

**浮动**:  元素的浮动是指设置了浮动属性的元素会脱离标准普通流的控制，移动到其父元素中指定位置的过程。

```
选择器 {
	float: 属性值;
}

left: 元素向左浮动
right: 元素向右浮动
none: 元素不浮动（默认值）
```

#### 浮动的特性

- 浮动首先创建包含块的概念（包裹）。就是说， 浮动的元素总是找离它最近的父级元素对齐。但是不会超出内边距的范围。 

- 浮动的元素排列位置，跟上一个元素（块级）有关系。如果上一个元素有浮动，则A元素顶部会和上一个元素的顶部对齐；如果上一个元素是标准流，则A元素的顶部会和上一个元素的底部对齐。

- 一个父盒子里面的子盒子，如果其中一个子级有浮动的，则其他子级都需要浮动。这样才能一行对齐显示。

- 浮动脱离标准流，不占位置，会影响标准流。浮动只有左右浮动。
- 元素添加浮动后，元素会具有行内块元素的特性。元素的大小完全取决于定义的大小或者默认的内容多少

> 总结：  浮动 --->  浮漏特 
>
> 浮：    加了浮动的元素盒子是浮起来的，漂浮在其他的标准流盒子上面。
> 漏：    加了浮动的盒子，不占位置的，它浮起来了，它原来的位置漏 给了标准流的盒子。
> 特：    特别注意，这是特殊的使用，有很多的不好处，使用要谨慎。



#### 清除浮动的 方法

由于浮动元素不再占用原文档流的位置，所以它会对后面的元素排版产生影响，为了解决这些问题，此时就需要在该元素中清除浮动。

清除浮动主要为了解决父级元素因为子级浮动引起内部高度为0 的问题。

1. 内联式 clear 方法

```
选择器 {
    clear: 属性值;
}

left: 不允许左侧有浮动元素（清除左侧浮动的影响）
right: 不允许右侧有浮动元素（清除右侧浮动的影响）
both: 同时清除左右两侧浮动的影响
```

2. 行内式 额外标签法

```
<div style="clear:both"></div>
```

3. 父级添加 overflow 属性方法

可以给父级添加： overflow为 hidden|auto|scroll  都可以实现。

4. 使用 after 伪元素清除浮动

> 代表网站： 百度、淘宝网、网易等

```
 .clearfix:after {  
 	content: ".";    # 注意： content:"."  里面尽量跟一个小点，或者其他，尽量不要为空，否则再firefox 7.0前的版本会有生成空格。
 	display: block; 
 	height: 0; 
 	clear: both; 
 	visibility: hidden;  
 	}   
 	
 .clearfix {
 	*zoom: 1;
 }   /* IE6、7 专有 */
```

5. 使用before和after双伪元素清除浮动

> 代表网站： 小米、腾讯等

```
.clearfix:before,.clearfix:after { 
  content:".";
  display:table;
}
.clearfix:after {
 clear:both;
}
.clearfix {
  *zoom:1;
}
```





## 3.定位 - position

CSS离不开定位，js 特效也离不开定位

定位用处:

1. 突出显示某个元素
2. 轮播图切换
3. ...

元素的定位属性主要包括:

1. 定位模式
2. 边偏移





#### 1.定位模式

```
选择器 {
	position: 属性值;
}
```

position 属性的常用值

| 值       | 描述                                             |
| -------- | ------------------------------------------------ |
| static   | 自动定位（默认定位方式）                         |
| relative | 相对定位，相对于其原文档流的位置进行定位         |
| absolute | 绝对定位，相对于其上一个已经定位的父元素进行定位 |
| fixed    | 固定定位，相对于浏览器窗口进行定位               |



##### > 静态定位 - static

- 网页中所有元素都默认的是静态定位,   其实就是标准流的特性。

- 在静态定位状态下，无法通过边偏移属性（top、bottom、left或right）来改变元素的位置。

##### > 相对定位 - relative

- 相对定位是将元素相对于它在标准流中的位置进行定位，当 position:  relative 时，可以将元素定位于相对位置。

- 对元素设置相对定位后，可以通过边偏移属性改变元素的位置，但是它在文档流中的位置仍然保留,  继续占有。

##### > 绝对定位 - absolute

- 绝对定位最重要的一点是，它可以通过边偏移移动位置，但是它完全脱标，完全不占位置。

绝对定位分一下几种情况:

1. 父级没有定位: 若所有父元素都没有定位，以浏览器为准对齐(document文档)。
2. 父级有定位:  绝对定位是将元素依据最近的已经定位（绝对、固定或相对定位）的父元素（祖先）进行定位。 
3. 绝对定位的盒子如果没有边偏移:  如果只是给盒子指定了 定位，但是没有给与边偏移，则改盒子以标准流来显示排序，和上一个盒子的底边对齐，但是不占有位置。
4. **子绝父相**:  子级是绝对定位的话， 父级要用相对定位。因为子级是绝对定位，不会占有位置， 可以放到父盒子里面的任何一个地方。父盒子布局时，需要占有位置，因此父亲只能是 相对定位. 

##### > 固定定位 - fixed

固定定位是绝对定位的一种特殊形式，它以浏览器窗口作为参照物来定义网页元素。当 position 属性的取值为 fixed 时，即可将元素的定位模式设置为固定定位。

当对元素设置固定定位后，它将脱离标准文档流的控制，始终依据浏览器窗口来定义自己的显示位置。不管浏览器滚动条如何滚动也不管浏览器窗口的大小如何变化，该元素都会始终显示在浏览器窗口的固定位置。

固定定位有两点：

1. 固定定位的元素跟父亲没有任何关系，只认浏览器。
2. 固定定位完全脱标，不占有位置，不随着滚动条滚动。



##### > 吸附定位 - sticky

查资料



##### + 叠放次序 - z-index

当对多个元素同时设置定位时，定位元素之间有可能会发生重叠。

在CSS中，要想调整重叠定位元素的堆叠顺序，可以对定位元素应用 z-index 层叠等级属性，其取值可为正整数、负整数和 0。比如：  z-index: 2;

注意：

1. z-index的默认属性值是0，取值越大，定位元素在层叠元素中越居上。

2. 如果取值相同，则根据书写顺序，后来居上。

3. 只有相对定位、绝对定位、固定定位有此属性，其余标准流、浮动、静态定位都无此属性，亦不可指定此属性。

##### + 定位总结

| 定位模式         | 是否脱标占有位置     | 是否可以使用边偏移 | 移动位置基准           |
| ---------------- | -------------------- | ------------------ | ---------------------- |
| 静态static       | 不脱标，正常模式     | 不可以             | 正常模式               |
| 相对定位relative | 不脱标，占有位置     | 可以               | 相对自身位置移动       |
| 绝对定位absolute | 完全脱标，不占有位置 | 可以               | 相对于定位父级移动位置 |
| 固定定位fixed    | 完全脱标，不占有位置 | 可以               | 相对于浏览器移动位置   |

##### + 定位模式自动转换

跟 浮动一样， 元素添加了 绝对定位和固定定位之后， 元素模式也会发生转换， 都转换为 **行内块模式**， 因此 比如 行内元素 如果添加了 绝对定位或者 固定定位后，可以不用转换模式，直接给高度和宽度就可以了。



#### 2.边偏移

| 边偏移属性 | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| top        | 顶端偏移量，定义元素相对于其父元素上边线的距离， 如 top: 100px; |
| bottom     | 底部偏移量，定义元素相对于其父元素下边线的距离               |
| left       | 左侧偏移量，定义元素相对于其父元素左边线的距离               |
| right      | 右侧偏移量，定义元素相对于其父元素右边线的距离               |

定位要和边偏移搭配使用。



###### 

###### 

# (四) CSS 高级技巧

## 用户界面样式

#### 鼠标样式 - cursor

 设置或检索在对象上移动的鼠标指针采用何种系统预定义的光标形状。 

```html
cursor: default  小白 | pointer  小手  | move  移动  |  text  文本
```

#### 轮廓  - outline

 是绘制于元素周围的一条线，位于边框边缘的外围，可起到突出元素的作用。

~~~css
 outline : outline-color ||outline-style || outline-width 
~~~

但是我们都不关心可以设置多少，我们平时都是去掉的。

最直接的写法是：  outline: 0; 

```html
<input type="text" style="outline: 0;" />
```

#### 防止拖拽文本域 - resize

resize：none    这个单词可以防止 火狐 谷歌等浏览器随意的拖动 文本域。

右下角可以拖拽： 

<textarea></textarea>
右下角不可以拖拽： 

```html
<textarea  style="resize: none;"></textarea>
```

## 



## 字体和图标

#### 阿里 icon font字库

http://www.iconfont.cn/

可以引用在线字体,  如:   

1. 字体查看地址:  https://www.iconfont.cn/webfont?spm=a313x.7781069.1998910419.12&puhui=1#!/webfont/index 
2. webfont前端使用帮助:   https://www.zybuluo.com/cherishpeace/note/46809?spm=a313x.7781068.0.0 







## 计算函数

calc

```
div {
    height: calc(100% - 100px);
}
```

