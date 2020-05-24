


# 网站优化三大标签

title  |  description  |  Keywords
(1) 网页标题 title

```html
<title>京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！</title>
```

(2) 网站说明 description
```html
<meta name="description" content="京东JD.COM-专业的综合网上购物商城,销售家电、数码通讯、电脑、家居百货、服装服饰、母婴、图书、食品等数万个品牌优质商品.便捷、诚信的服务，为您提供愉悦的网上购物体验!" />
```

(3) 关键词 Keywords
```html
<meta name="Keywords" content="网上购物,网上商城,手机,笔记本,电脑,MP3,CD,VCD,DV,相机,数码,配件,手表,存储卡,京东" />
```







# 前端问题

## 001   单选框的value提交



ajax提交请求时radio取值的坑

![02](.\images\002.png)

![01](.\images\001.png)



#### Jquery 获取 radio选中值

![03_redio](.\images\003_redio.jpg)

```javascript
// 1.获取选中值，三种方法都可以：

$('input:radio:checked').val()；
$("input[type='radio']:checked").val();
$("input[name='rd']:checked").val();


// 2.设置第一个Radio为选中值：

    $('input:radio:first').attr('checked', 'checked');
或者
	$('input:radio:first').attr('checked', 'true');

注：attr("checked",'checked')= attr("checked", 'true')= attr("checked", true)


// 3.设置最后一个Radio为选中值：

	$('input:radio:last').attr('checked', 'checked');
或者
	$('input:radio:last').attr('checked', 'true');


// 4.根据索引值设置任意一个radio为选中值：

	$('input:radio').eq(索引值).attr('checked', 'true');索引值=0,1,2....
或者
	$('input:radio').slice(1,2).attr('checked', 'true');


// 5.根据Value值设置Radio为选中值

	$("input:radio[value=http://www.2cto.com/kf/201110/'rd2']").attr('checked','true');
或者
	$("input[value=http://www.2cto.com/kf/201110/'rd2']").attr('checked','true');


// 6.删除Value值为rd2的Radio

	$("input:radio[value=http://www.2cto.com/kf/201110/'rd2']").remove();


// 7.删除第几个Radio

	$("input:radio").eq(索引值).remove();索引值=0,1,2....
	如删除第3个Radio:$("input:radio").eq(2).remove();


// 8.遍历Radio

    $('input:radio').each(function(index,domEle){
         //写入代码
    });
```



#### Jquery 获取下拉列表选中值



```javascript
// 1.   获取选中项：

	// 获取选中项的Value值：
	$('select#sel option:selected').val();
或者
    $('select#sel').find('option:selected').val();

	// 获取选中项的Text值：
	$('select#seloption:selected').text();
或者
	$('select#sel').find('option:selected').text();


// 2.   获取当前选中项的索引值：

	$('select#sel').get(0).selectedIndex;


// 3.   获取当前option的最大索引值：

	$('select#sel option:last').attr("index")

    
// 4.   获取DropdownList的长度：

	$('select#sel')[0].options.length;
或者
	$('select#sel').get(0).options.length;


// 5.  设置第一个option为选中值：

	$('select#sel option:first').attr('selected','true')
或者
	 $('select#sel')[0].selectedIndex = 0;
```





