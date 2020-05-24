# Mongodb数据库

- 安装
- 基本操作
- 数据查询
- 聚合
- 索引和备份
- 与python交互





[官方文档](https://docs.mongodb.com/manual/)

[菜鸟教程  MongoDB ](https://www.runoob.com/mongodb/mongodb-tutorial.html) 



#一 mongodb的介绍和安装

**NoSQL的介绍**

- NoSQL最常⻅的解释是“non-relational”， “Not Only SQL”也被很多⼈接受， 指的是⾮关系型的数据库
- 菜鸟教程:  
  -  http://www.runoob.com/mongodb/nosql.html
    - NoSQL 简介
    - 分布式系统
    - RDBMS vs NoSQL
    - NoSQL 数据库分类
    - ACID vs BASE



**关系型和非关系型**

- 对于关系型数据库，存储数据的时候需要提前建表建库，随着数据的复杂度越来越高，所建的表的数量也越来越多；
  - MySQL 扩展性差, 大数据下IO压力大, 表结构更改困难


- 非关系型不需要提前建表建库,  易扩展,  大数据下性能高,  灵活的数据模型,  高可用
  - mongodb易扩展： NoSQL数据库种类繁多， 但是⼀个共同的特点都是去掉关系数据库的关系型特性。 数据之间⽆关系， 这样就⾮常容易扩展
  - mongodb ⼤数据量， ⾼性能： NoSQL数据库都具有⾮常⾼的读写性能， 尤其在⼤数据量下， 同样表现优秀。 这得益于它的⽆关系性， 数据库的结构简单
  - mongodb 灵活的数据模型： NoSQL⽆需事先为要存储的数据建⽴字段， 随时可以存储⾃定义的数据格式。 ⽽在关系数据库⾥， 增删字段是⼀件⾮常麻烦的事情。 如果是⾮常⼤数据量的表， 增加字段简直就是⼀个噩梦



**mongodb的安装**

```python
# 通过命令安装 / 也可通过源码安装
sudo apt-get install -y mongodb-org

各平台安装文档说明	https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
若此命令无法安装, 往后看
```



**mongodb的启动**

>  **服务端mongodb** 的启动

- 查看帮助：mongod –help
- 启动：sudo service mongod start
- 停止：sudo service mongod stop
- 重启：sudo service mongod restart
- 查看是否启动成功：ps -ef|grep mongod
- 配置文件的位置：/etc/mongod.conf
- 默认端⼝：27017
- 日志的位置：/var/log/mongodb/mongod.log

> 服务端mongodb无法启动的解决方法

```
sudo mongod --config /etc/mongod.conf &
```



**&符号** 是让命令执行后不占用当前终端



>  **客户端mongo**

- 启动本地客户端: mongo
- 查看帮助：mongo –help
- 退出：exit或者ctrl+c




## Ubuntu中安装mongodb的问题

1- 在终端上运行"sudo apt-get install mongo-org"后出现错误：

```
Reading package lists... Done
Building dependency tree 
Reading state information... Done
E: Unable to locate package mongodb-org  //This is the error
```

并且在运行"apt-get update"后依然是这个错误提示。

2- 结果按下面步骤设置后安装成功：

​	Step 1:  Import the MongoDB public key

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
```

​	Step 2: Generate a file with the MongoDB repository url

```
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
```

​	Step 3: Refresh the local database with the packages

```
sudo apt-get update
```

​	Step 4: Install the last stable MongoDB version and all the necessary packages on our system

```
sudo apt-get install mongodb-org
```

3- 这时装好以后应该会自动运行mongod程序，查看进程是否已经启动：

```
pgrep mongo -l
```



## Windows 平台安装 MongoDB

菜鸟教程	http://www.runoob.com/mongodb/mongodb-window-install.html

> 假设安装目录为 E:\MongoDB

1 开启服务端:  `E:\MongoDB\bin\mongod.exe`   或切换到mongod.exe目录下:  `mongod`

2 开启客户端:  `E:\MongoDB\bin\mongo.exe`     或切换到mongo.exe目录下:  `mongo`



## 文档的概念

文档是一组键值(key-value)对(即BSON)。MongoDB 的文档不需要设置相同的字段，并且相同的字段不需要相同的数据类型，这与关系型数据库有很大的区别，也是 MongoDB 非常突出的特点。

一个简单的文档例子如下：

```
{"site":"www.runoob.com", "name":"菜鸟教程"}
```

下表列出了 RDBMS 与 MongoDB 对应的术语：

| RDBMS | MongoDB                     |
| ----- | --------------------------- |
| 数据库   | 数据库                         |
| 表格    | 集合  ( MongoDB 文档组)          |
| 行     | 文档                          |
| 列     | 字段                          |
| 表联合   | 嵌入文档                        |
| 主键    | 主键 (MongoDB 提供了 key 为 _id ) |

需要注意的是：

1. 文档中的键/值对是有序的。
2. 文档中的值不仅可以是在双引号里面的字符串，还可以是其他几种数据类型（甚至可以是整个嵌入的文档)。
3. MongoDB区分类型和大小写。
4. MongoDB的文档不能有重复的键。
5. 文档的键是字符串。除了少数例外情况，键可以使用任意UTF-8字符。

文档键命名规范：

- 键不能含有\0 (空字符)。这个字符用来表示键的结尾。
- .和$有特别的意义，只有在特定环境下才能使用。
- 以下划线"_"开头的键是保留的(不是严格要求的)。





#二 mongodb的基本使用


## 1.数据库的命令

- 数据库不需要提前创建, 插入数据时自动创建
- 查看当前的数据库：db
- 查看所有的数据库：show dbs  /  show databases
- 切换数据库：use db_name
- 删除当前的数据库：db.dropDatabase()




数据库也通过名字来标识。数据库名可以是满足以下条件的任意UTF-8字符串。

- 不能是空字符串（"")。
- 不得含有' '（空格)、.、$、/、\和\0 (空字符)。
- 应全部小写。
- 最多64字节。

有一些数据库名是保留的，可以直接访问这些有特殊作用的数据库。

- **admin**： 从权限的角度来看，这是"root"数据库。要是将一个用户添加到这个数据库，这个用户自动继承所有数据库的权限。一些特定的服务器端命令也只能从这个数据库运行，比如列出所有的数据库或者关闭服务器。
- **local:** 这个数据永远不会被复制，可以用来存储限于本地单台服务器的任意集合
- **config**: 当Mongo用于分片设置时，config数据库在内部使用，用于保存分片的相关信息。



## 2. 集合的命令

- 集合不需要提前创建： 向不存在的集合中第⼀次加⼊数据时， 集合会自动创建
- 也可以手动创建集合：
  - db.createCollection(name,options)
  - db.createCollection("stu")
  - db.createCollection("sub", { capped : true, size : 10 } )
    - 参数capped： 是否设置上限,  默认值为false
    - 参数size： capped值为true时需要指定此参数,  表示上限字节⼤⼩,  当⽂档达到上限时会将之前的数据覆盖
- 查看集合：show collections
- 删除集合：db.集合名称.drop()




**注意: ** 在 MongoDB 中，集合只有在内容插入后才会创建!   就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建。



## 3. 常见数据类型

### 3.1 常见类型

- Object ID： ⽂档ID
- String： 字符串， 最常⽤， 必须是有效的UTF-8
- Boolean： 存储⼀个布尔值， true或false
- Integer： 整数可以是32位或64位， 这取决于服务器
- Double： 存储浮点值
- Arrays： 数组或列表， 多个值存储到⼀个键
- Object： ⽤于嵌⼊式的⽂档， 即⼀个值为⼀个⽂档
- Null： 存储Null值
- Timestamp： 时间戳， 表示从1970-1-1 (Unix新纪元) 到现在的总秒数
- Date： 存储当前⽇期或时间的UNIX时间格式

### 3.2 注意点

- 创建⽇期语句如下 ：参数的格式为'YYYY-MM-DD' 	如: new Date('2017-12-20')	


- 每个⽂档都有⼀个属性， 为 _id， 保证每个⽂档的唯⼀性

  可以⾃⼰去设置 \_id插⼊⽂档，如果没有提供， 那么MongoDB为每个⽂档提供了⼀个独特的_id， 类型为objectID

- objectID是⼀个12字节的⼗六进制数,  每个字节两位，一共是24 位的字符串

  - 4字节当前时间戳   ⼗   3字节机器ID    ⼗   2字节MongoDB服务进程id组成 PID   ⼗   3字节简单的增量值
  - 当前时间戳: 格林尼治时间 **UTC** 时间，比北京时间晚了 8 个小时


### 3.3 more

**ObjectId 对象**

ObjectId 对象中保存了创建的时间戳,  通过 getTimestamp 函数来获取文档的创建时间:

```
> var newObject = ObjectId()
> newObject.getTimestamp()
ISODate("2017-11-25T07:21:10Z")
```

ObjectId 转为字符串

```
> newObject.str
5a1919e63df83ce79df8b38f
```



**日期**

表示当前距离 Unix新纪元（1970年1月1日）的毫秒数。日期类型是有符号的, 负数表示 1970 年之前的日期。

```javascript
> var mydate1 = new Date()     //格林尼治时间
> mydate1
ISODate("2018-03-04T14:58:51.233Z")
> typeof mydate1
object
```

```javascript
> var mydate2 = ISODate() //格林尼治时间
> mydate2
ISODate("2018-03-04T15:00:45.479Z")
> typeof mydate2
object
```

这样创建的时间是**日期类型**，可以使用 JS 中的 Date 类型的方法。

返回一个**时间类型的字符串**：

```javascript
> var mydate1str = mydate1.toString()
> mydate1str
Sun Mar 04 2018 14:58:51 GMT+0000 (UTC) 
> typeof mydate1str
string
```

或者

```
> Date()
Sun Mar 04 2018 15:02:59 GMT+0000 (UTC)
```



## 4. 增删改查

### 4.1 插入

- db.集合名称.insert(document)

- document 为   字典 / 字典组成的列表

  ```javascript
  db.col_name.insert({name:'gj',gender:1})
  db.col_name.insert({_id:"20170101",name:'gj',gender:1})
  ```

  插⼊⽂档时， 如果不指定_id参数， MongoDB会为⽂档分配⼀个唯⼀的ObjectId



### 4.2 保存

命令：`db.集合名称.save(document)` \_id 存在则修改，_id不存在则添加

**insert 与 save 区别:**

```javascript
insert ------- _id 存在则报错,  不存在会插入
save  ------- _id 存在则更新,  不存在会插入
```



### 4.3 简单查询

命令：`db.集合名称.find()`		`db.集合名称.find().pretty()`



### 4.4 更新

命令：`db.集合名称.update(<query> ,<update>,{multi: <boolean>})`

- 参数query: 查询条件
- 参数update: 更新操作符
- 参数multi: 可选， 默认是false，表示只更新找到的第⼀条记录， 值为true表示把满⾜条件的⽂档全部更新

### >  3 种更新

<1> 更新满足条件的第一条  的整个document

```javascript
db.col_name.update({name:'hr'},{name:'mnc'})
$set 的使用
db.col_name.update({name:'hr'},{$set:{name:'hys'}})    # 单独用$set,  效果与不用时不一样
```

<2> $set 的使用**-------**更新满足条件的第一条document的对应键值对

```javascript
db.col_name.update({name:'hr'},{$set:{name:'hys'}})    # 单独用$set,  效果与不用时不一样
```

<3> $set 配合 {multi:true}**-------**更新满足条件  的全部document  的对应键值对

```javascript
db.col_name.update({gender:1},{$set:{gender:0}},{multi:true})  # $set配合{multi:true},  更新满足条件的全部
```

注意:  multi update only works with $ operators

​	无效操作: db.col_name.update({gender:1},{gender:0},{multi:true})



### > 更新的示例

```javascript
# ------------------------1-------------------------不使用$set
插入一条document
db.col.insert({
    title: 'MongoDB 教程', 
    description: 'MongoDB 是一个 Nosql 数据库',
    by: '菜鸟教程',
    url: 'http://www.runoob.com',
    tags: ['mongodb', 'database', 'NoSQL'],
    likes: 100
})
更新			db.col.update({'title':'MongoDB 教程'},{'title':'MongoDB'})
更新结果	  { "_id" : ObjectId("5ba9d54ec4695d055f3fbbc2"), "title" : "MongoDB" }


# ------------------------2-------------------------使用$set
再插入一条document
...
更新			db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
更新结果       {
                      "_id" : ObjectId("5ba9d5cdc4695d055f3fbbc3"),
                      "title" : "MongoDB",
                      "description" : "MongoDB 是一个 Nosql 数据库",
                      "by" : "菜鸟教程",
                      "url" : "http://www.runoob.com",
                      "tags" : [
                              "mongodb",
                              "database",
                              "NoSQL"
                      ],
                      "likes" : 100
              }
              
# ------------------------3-------------------------使用$set, 最后指明 {multi:true}
插入第三条document
...
更新			 db.col.update({'by':'菜鸟教程'},{$set:{'by':'菜鸟'}},{multi:true})
更新结果	   第二条和第三条document都更新了by键对应的值
```





### 4.5 删除文档

命令：`db.集合名称.remove(<query>,{justOne: <boolean>})`

- 满足条件**默认删除多条**
- 参数query: 必须，删除的⽂档的条件
- 参数**justOne**: 可选， 如果设为true或1， 则**只删除⼀条**， 默认false， 表示删除多条




## 5. 高级查询

### 5.1 数据查询

- ⽅法find()： 查询

  `db.集合名称.find({条件⽂档})`

- ⽅法findOne()：查询，只返回第⼀个

  `db.集合名称.findOne({条件⽂档})`

- ⽅法pretty()： 将结果格式化

  `db.集合名称.find({条件⽂档}).pretty()`



### 5.2 比较运算符

可以使用以下数据进行练习

```json
[{"name" : "郭靖", "hometown" : "蒙古", "age" : 20, "gender" : true },
{"name" : "⻩蓉", "hometown" : "桃花岛", "age" : 18, "gender" : false },
{"name" : "华筝", "hometown" : "蒙古", "age" : 18, "gender" : false },
{"name" : "⻩药师", "hometown" : "桃花岛", "age" : 40, "gender" : true },
{"name" : "段誉", "hometown" : "⼤理", "age" : 16, "gender" : true },
{"name" : "段王爷", "hometown" : "⼤理", "age" : 45, "gender" : true },
{"name" : "洪七公", "hometown" : "华⼭", "age" : 18, "gender" : true }]
```

- 等于： 默认是等于判断， 没有运算符

- ⼩于：`$lt （less than）`

- ⼩于等于：`$lte （less than equal）`

- ⼤于：`$gt （greater than）`

- ⼤于等于：`$gte`

- 不等于：`$ne`

  例如：

  ```javascript
    查询年龄大于18的所有学生
    db.stu.find({  age:{$gte:18}  })
  ```



### 5.3 逻辑运算符

- $and：在json中写多个条件即可

  {     $and: [ {}, {} ]     }

  ```javascript
  查询年龄⼤于或等于18， 并且性别为true的学⽣
  db.stu.find({   age:{$gte:18},gender:true   })
  db.test.find({  $and:[{age:{$gte:18}}, {gender:true}]  })
  ```

- $or:  值为数组， 数组中每个元素为json

  {     $or: [ {}, {} ]     }

  ```
  查询年龄⼤于18， 或性别为false的学⽣
  db.stu.find({   $or:[{age:{$gt:18}},{gender:false}]    })

  查询年龄⼤于18或性别为男⽣， 并且姓名是郭靖
  db.stu.find({    $or:[{age:{$gte:18}},{gender:true}],name:'郭靖'    })
  ```



### 5.4 范围运算符

使⽤`$in`， `$nin` 判断数据是否在某个数组内

``` 
 查询年龄为18、 28的学⽣
 db.stu.find({  age:{$in:[18,28,38]}  })
```



### 5.5 ⽀持正则表达式

使⽤  **/.../**  或  **$regex**  编写正则表达式

```
查询sku以abc开头的数据
db.products.find({  sku:/^abc/  })		# -----不能加引号-----

查询sku以789结尾的数据
db.products.find({  sku:{$regex:'789$'}  })  # -----要加引号-----
```

```json
[{ "_id" : 100, "sku" : "abc123", "description" : "Single line description." },
{ "_id" : 101, "sku" : "abc789", "description" : "First line\nSecond line" },
{ "_id" : 102, "sku" : "xyz456", "description" : "Many spaces before     line" },
{ "_id" : 103, "sku" : "xyz789", "description" : "Multiple\nline description" }]
```



### 5.6 skip和limit

- ⽅法limit()： ⽤于读取指定数量的⽂档

  ```
  db.集合名称.find().limit(NUMBER)
  查询2条学⽣信息
  db.stu.find().limit(2)
  ```

- ⽅法skip()： ⽤于跳过指定数量的⽂档

  ```
  db.集合名称.find().skip(NUMBER)
  db.stu.find().skip(2)
  ```

- 同时使用

  ```
  db.stu.find().skip(5).limit(4)	# 先使用skip再使用limit的效率更高
  或
  db.stu.find().limit(4).skip(5)
  ```

  ​



### 5.7 自定义js函数来查询

由于mongo的shell是一个js的执行环境 使⽤$where后⾯写⼀个函数， 返回满⾜条件的数据

```
 查询年龄⼤于30学⽣
 db.stu.find({
     $where:function({
         return this.age>3;}
})
```



### 5.8 投影 (指定返回字段)

查询时只返回指定的字段

命令：`db.集合名称.find({},{字段名称:1,...})`

参数为字段与值，值为1表示显示，值为0不显 

特别注意： 对于\_id列默认是显示的， 如果不显示需要明确设置为0   `db.stu.find({},{_id:0,name:1,gender:1})`



### 5.9 排序

⽅法sort()， ⽤于对 集合进⾏排序

命令：`db.集合名称.find().sort({字段:1,...})`

参数 1 为升序排列 参数 -1 为降序排列

```
 先根据性别降序， 再根据年龄升序
 db.stu.find().sort({gender:-1,age:1})
```



### 5.10 统计个数

⽅法count()⽤于统计结果集之中⽂档条数,  返回文档条数

命令：`db.集合名称.find({条件}).count()` 

命令：`db.集合名称.count({条件})`

```
 db.stu.find({gender:true}).count()
 db.stu.count({age:{$gt:20},gender:true})

```



### 5.11 消除重复

⽅法`distinct()`对数据进⾏去重:   指定去重字段(键),  返回去重后该键的值数组

命令：`db.集合名称.distinct('去重字段',{条件})`

```
db.stu.distinct('hometown',{age:{$gt:18}})
```





# 三 mongodb的聚合操作

## 1 聚合(aggregate)

聚合(aggregate) 是基于数据处理的聚合管道，每个文档通过一个由多个阶段（stage）组成的管道，可以对每个阶段的管道进行分组、过滤等功能，然后经过一系列的处理，输出相应的结果。

语法：`db.集合名称.aggregate({管道:{表达式}})`

使用一个/多个管道的语法:  

```
db.col_name.aggregate( [   {管道:{表达式}},   {管道:{表达式}}   ] )
db.col_name.aggregate(     {管道:{表达式}},   {管道:{表达式}}     )
```



![mongodb的聚合](.\03_Mongodb数据库_images\mongodb的聚合.png) 





## 2 常用管道和表达式

### 2.1 常用管道命令

在mongodb中，⽂档处理完毕后， 通过管道进⾏下⼀次处理 常用管道命令如下：

- `$group`： 将集合中的⽂档分组， 可⽤于统计结果
- `$match`： 过滤输出
- `$project`： 修改输⼊⽂档的结构， 如重命名、 增加、 删除字段、 创建计算结果
- `$sort`：排序输出
- `$limit`： 限制聚合管道返回的⽂档数
- `$skip`：跳过指定数量的⽂档， 并返回余下的⽂档

### 2.2 常用表达式

表达式：处理输⼊⽂档并输出 语法：`表达式:'$列名'` 常⽤表达式:

- `$sum`：	计算总和， $sum:1 表示以⼀倍计数 (统计组中数据个数 ,  非求和)
- `$avg`： 计算平均值
- `$min`：获取最⼩值
- `$max`： 获取最⼤值
- `$push`：在结果⽂档中插⼊值到⼀个数组中




## 3. 管道命令之 `$group`

### 3.1 按照某个字段进行分组

`$group`是所有聚合命令中用的最多的一个命令，用来将集合中的文档分组，可用于统计结果

使用示例:

```
db.stu.aggregate(
    {$group:
        {_id:"$gender", counter:{$sum:1}}
    }
)
```

注意点：

- `db.db_name.aggregate()`是语法，所有的管道命令都需要写在其中
- `_id` 表示**分组的依据**，按照哪个字段进行分组，需要使用`$gender`表示选择这个字段进行分组
- `$sum:1` 表示把每条数据作为1进行统计，统计的是该分组下面数据的条数

### 3.2 把整个文档分为一组进行统计

当我们需要统计整个文档的时候，`$group` 的另一种用途就是把整个文档分为一组进行统计

使用实例：

```
db.stu.aggregate(
    {$group:
        {_id:null, counter:{$sum:1}}
    }
)
```

其中注意点：

- `_id:null` 表示不指定分组的字段，即统计整个文档，此时获取的`counter`表示整个文档的个数

### 3.3 数据透视

正常情况在统计的不同性别的数据的时候，需要知道所有的name，需要逐条观察，如果通过某种方式把所有的name放到一起，那么此时就可以理解为数据透视

使用示例如下：

1. 使用 `$push` 统计姓名列表

   ```
   不统计个数, 而是显示数据列表
    db.stu.aggregate(
        {$group:
            {_id:null, name:{$push:"$name"}}
        }
    )
   ```

2. 使用`$$ROOT`可以将整个文档放入数组中

   ```
    db.stu.aggregate(
        {$group:
            {_id:null, name:{$push:"$$ROOT"}}
        }
    )
   ```

### 3.4 练习

对于如下数据，需要统计出每个country/province下的userid的数量（同一个userid只统计一次）

```
[{ "country" : "china", "province" : "sh", "userid" : "a" }, 
{  "country" : "china", "province" : "sh", "userid" : "b" }, 
{  "country" : "china", "province" : "sh", "userid" : "a" }, 
{  "country" : "china", "province" : "sh", "userid" : "c" }, 
{  "country" : "china", "province" : "bj", "userid" : "da" }, 
{  "country" : "china", "province" : "bj", "userid" : "fa" }]
```

参考写法

```
db.user.aggregate(
--------------- 多个管道, 是单独的字典 ---------------
  {$group:{_id:{country:'$country',province:'$province',userid:'$userid'}}},
  {$group:{_id:{country:'$_id.country',province:'$_id.province'}, count:{$sum:1}}}
  )
```



## 4.管道命令之`$match`

`$match`用于进行数据的过滤，是在能够在聚合操作中使用的命令，和`find`区别在于`$match` 操作可以把结果交给下一个管道处理，而`find`不行

使用示例如下：

1. 查询年龄大于20的学生

   ```
    db.stu.aggregate(
        {$match:
            {age:{$gt:20}}
        )
   ```

2. 查询年龄大于20的男女学生的人数

   ```
    db.stu.aggregate(
        {$match:{age:{$gt:20}},
        {$group:{_id:"$gender",counter:{$sum:1}}}
        )
   ```



## 5. 管道命令之 `$project`

`$project`用于修改文档的输入输出结构，例如 **重命名，增加，删除字段**

使用示例：

1. 查询学生的年龄、姓名，仅输出年龄姓名

   ```
    db.stu.aggregate(
        {$project:{_id:0,name:1,age:1}}		# $project单独用时
        )
   ```

2. 查询男女生人生，输出人数

   ```
    db.stu.aggregate(
        {$group:{_id:"$gender",counter:{$sum:1}}},
        {$project:{_id:0,counter:1}}	`		# $project配合用时
        )
   ```

### 5.1 练习

对于如下数据：统计出每个country/province下的userid的数量（同一个userid只统计一次），结果中的字段为{country:"\*\*"，province:"\**"，counter:"\*\*"}

```
{ "country" : "china", "province" : "sh", "userid" : "a" },
{  "country" : "china", "province" : "sh", "userid" : "b" },
{  "country" : "china", "province" : "sh", "userid" : "a" },
{  "country" : "china", "province" : "sh", "userid" : "c" },
{  "country" : "china", "province" : "bj", "userid" : "da" }, 
{  "country" : "china", "province" : "bj", "userid" : "fa" }
```

参考写法

```
db.user.aggregate(
	------------ 注: 多个分组依据_id 用字典表示 ------------
  {$group:{_id:{country:'$country',province:'$province',userid:'$userid'}}},
  {$group:{_id:{country:'$_id.country',province:'$_id.province'},count:{$sum:1}}},
  {$project:{_id:0,country:'$_id.country',province:'$_id.province',counter:'$count'}}
  )
```



## 6. 管道命令之 `$sort`

`$sort`用于将输入的文档排序后输出

使用示例如下：

1. 查询学生信息，按照年龄升序

   ```
    db.stu.aggregate({$sort:{age:1}})
   ```

2. 查询男女人数，按照人数降序

   ```
    db.stu.aggregate(
        {$group:{_id:"$gender",counter:{$sum:1}}},		# 按男/女分组, 统计每组个数
        {$sort:{counter:-1}}							# 按每组个数 降序
    )
   ```




## 7. 管道命令之`$skip` 和 `$limit`

- `$limit`限制返回数据的条数
- `$skip` 跳过指定的文档数，并返回剩下的文档数
- 同时使用时先使用skip在使用limit

使用示例如下：

1. 查询2条学生信息

   ```
    db.stu.aggregate(
        {$limit:2}
    )
   ```

2. 查询从第三条开始的学生信息

   ```
    db.stu.aggregate(
        {$skip:3}
    )
   ```

3. 统计男女生人数，按照人数升序，返回第二条数据

   ```
    db.stu.aggregate(
        {$group:{_id:"$gender",counter:{$sum:1}}},
        {$sort:{counter:-1}},
        {$skip:1},
        {$limit:1}
    )
   ```








# 四 mongodb的 索引 / 备份



## 1. mongodb的索引

知识点

- 掌握mongodb索引的创建，删除操作
- 掌握mongodb查看索引的方法
- 掌握mongodb创建联合索引的方法
- 掌握mongodb创建唯一索引的方法

### 1.1 为什么mongdb需要创建索引

- 加速查询
- 唯一索引还可以 数据去重

### 1.2 创建简单索引的方法

- 语法：
  - `db.集合.ensureIndex({属性:1})`，1表示升序， -1表示降序
  - `db.集合.createIndex({属性:1})`
  - 上面两个命令效果等价
- 具体操作：db.col_name.ensureIndex({name:1})



### 1.3 创建索引前后查询速度对比

**JS语句添加测试数据**

```
for(i=0;i<100000;i++){db.test_index.insert({name:'test'+i,age:i})}
```

创建索引前：

```
db.test_index.find({name:'test10000'})
db.test_index.find({name:'test10000'}).explain('executionStats')
```

创建索引后：

```
db.test_index.ensureIndex({name:1})
db.test_index.find({name:'test10000'}).explain('executionStats')
```

前后速度对比

![创建索引速度对比](.\03_Mongodb数据库_images\创建索引速度对比.png)



### 1.4 索引的查看

**默认情况下_id是集合的索引**

查看方式：`db.col_name.getIndexes()`

添加索引前：

```
> db.test2000.insert({"name":"hello",age:20})
WriteResult({ "nInserted" : 1 })
> db.test2000.find()
{ "_id" : ObjectId("5ae0232f625b9ddd91a0e7ae"), "name" : "hello", "age" : 20 }
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    }
]
```

添加name为索引后:

```
> db.test2000.ensureIndex({name:1})
{
    "createdCollectionAutomatically" : false,
    "numIndexesBefore" : 1,
    "numIndexesAfter" : 2,
    "ok" : 1
}
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "key" : {
            "name" : 1
        },
        "name" : "name_1",
        "ns" : "test2000.test2000"
    }
]
```



### 1.5 创建唯一索引

在默认情况下mongdb的索引字段的值是可以相同的,  仅仅能够提高查询速度

添加唯一索引的语法：

```
db.collection_name.ensureIndex({"name":1},{"unique":true})
```

使用普通索引的效果如下：

```
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "key" : {
            "name" : 1
        },
        "name" : "name_1",
        "ns" : "test2000.test2000"
    }
]
> db.test2000.insert({name:"hello",age:40})
WriteResult({ "nInserted" : 1 })
> db.test2000.find()
{ "_id" : ObjectId("5ae0232f625b9ddd91a0e7ae"), "name" : "hello", "age" : 20 }
{ "_id" : ObjectId("5ae02421625b9ddd91a0e7af"), "name" : "hello", "age" : 30 }
{ "_id" : ObjectId("5ae02432625b9ddd91a0e7b0"), "name" : "hello", "age" : 40 }

```

添加age为唯一索引之后：

```
> db.test2000.createIndex({age:1},{unique:true})
{
    "createdCollectionAutomatically" : false,
    "numIndexesBefore" : 2,
    "numIndexesAfter" : 3,
    "ok" : 1
}
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "key" : {
            "name" : 1
        },
        "name" : "name_1",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "unique" : true,
        "key" : {
            "age" : 1
        },
        "name" : "age_1",
        "ns" : "test2000.test2000"
    }
]
> db.test2000.insert({"name":"world",age:20})
WriteResult({
    "nInserted" : 0,
    "writeError" : {
        "code" : 11000,
        "errmsg" : "E11000 duplicate key error collection: test2000.test2000 index: age_1 dup key: { : 20.0 }"
    }
})

```



### 1.6 删除索引

语法：`db.col_name.dropIndex({'索引名称':1})`

```
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "key" : {
            "name" : 1
        },
        "name" : "name_1",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "unique" : true,
        "key" : {
            "age" : 1
        },
        "name" : "age_1",
        "ns" : "test2000.test2000"
    }
]
> db.test2000.dropIndex({age:1})
{ "nIndexesWas" : 3, "ok" : 1 }
> db.test2000.dropIndex({name:1})
{ "nIndexesWas" : 2, "ok" : 1 }
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    }
]
```



### 1.6 建立复合索引

在进行数据去重的时候，可能用一个字段来保证数据的唯一性，这个时候可以考虑建立复合索引来实现。

**例如：**抓全贴吧信息，如果把帖子的名字作为唯一索引对数据进行去重是不可取的，因为可能有很多帖子名字相同

**建立复合索引的语法**：`db.collection_name.ensureIndex({字段1:1,字段2:1})`

```
> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    }
]

> db.test2000.createIndex({name:1,age:1})
{
    "createdCollectionAutomatically" : false,
    "numIndexesBefore" : 1,
    "numIndexesAfter" : 2,
    "ok" : 1
}

> db.test2000.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "test2000.test2000"
    },
    {
        "v" : 2,
        "key" : {
            "name" : 1,
            "age" : 1
        },
        "name" : "name_1_age_1",
        "ns" : "test2000.test2000"
    }
]
```



### 1.7 建立索引注意点

- 根据需要选择是否需要建立唯一索引

- 索引字段是 升序还是降序 在单个索引的情况下不影响查询效率，但是带复合索引的条件下会有影响

  > 例如：在进行查询的时候如果字段1需要升序的方式排序输出，字段2需要降序的方式排序输出，那么此时复合索引的建立需要把字段1设置为1，字段2设置为-1





## 2. mongodb的备份和恢复

### 2.1 备份

  ```
  mongodump -h dbhost -d dbname -o dbdirectory
  ```

- `-h`： 服务器地址， 也可以指定端⼝号

- `-d`： 需要备份的数据库名称

- `-o`： 备份的数据存放位置， 此⽬录中存放着备份出来的数据

示例：`mongodump -h 192.168.196.128:27017 -d test1 -o ~/Desktop/test1bak`



### 2.2 恢复

```
mongorestore -h dbhost -d dbname --dir dbdirectory
```

- `-h`： 服务器地址
- `-d`： 需要恢复的数据库实例
- `--dir`： 备份数据所在位置

示例：`mongorestore -h 192.168.196.128:27017 -d test2 --dir ~/Desktop/test1bak/test1`







# 五 mongodb和python交互

## 1. pymongo模块入门

`pymongo` 提供了mongdb和python交互的所有方法 

0. 安装

      ```
      pip install pymongo
      ```


1. 连接数据库服务器获取客户端对象,   获取数据库对象再获取集合对象

   ```python
    from pymongo import MongoClient
       
    client = MongoClient(host=, port=)
    # client = MongoClient()   # 默认本地连接
       
    collection = client['db名']['集合名']	 # 数据库和集合没有同样会自动创建
   ```

2. 添加一条数据

   ```python
   ret = collection.insert_one({"name":"test10010","age":33})
   print(ret)
   ```

3. 添加多条数据

   ```python
    item_list = [{"name":"test1000{}".format(i)} for i in range(10)]
    #insert_many接收一个列表，列表中为所有需要插入的字典
    t = collection.insert_many(item_list)
   ```

4. 查找一条数据

   ```python
    #find_one查找并且返回一个结果,接收一个字典形式的条件
    t = collection.find_one({"name":"test10005"})
    print(t)
   ```

5. 查找全部数据

   结果是一个Cursor游标对象，是一个可迭代对象，可以类似读文件的指针，但是只能够进行一次读取

   ```python
    #find返回所有满足条件的结果，如果条件为空，则返回数据库的所有
    t = collection.find({"name":"test10005"})
    	#结果是一个Cursor游标对象，是一个可迭代对象，可以类似读文件的指针，
    for i in t:
        print(i)
    for i in t: #此时t中没有内容
        print(i)
   ```

6. 更新一条数据 注意使用`$set`命令

   ```python
    # update_one 更新一条数据
    collection.update_one({"name":"test10005"},{"$set":{"name":"new_test10005"}})
   ```

7. 更新全部数据

   ```python
    # update_many 更新全部数据
    collection.update_many({"name":"test10005"},{"$set":{"name":"new_test10005"}})
   ```

8. 删除一条数据

   ```python
    # delete_one 删除一条数据
    collection.delete_one({"name":"test10010"})
   ```

9. 删除全部数据

   ```python
    # delete_may 删除所有满足条件的数据
    collection.delete_many({"name":"test10010"})
   ```






```python
import pymongo

# 创建mongo客户端, 链接mongo服务器
client = pymongo.MongoClient()

# 指定/创建集合
collection = client['shendiao']['shendiao']

# 插入一条数据
# collection.insert_one({"name": "杨过", "hometown": "襄阳", "age": 20, "gender": True})

# 插入多条数据
# collection.insert_many([
#     {"name": "白相", "hometown": "地狱公寓公寓103", "age": 32, "gender": True},
#     {"name": "凌玲", "hometown": "地狱公寓公寓104", "age": 23, "gender": False},
# ])

# 查找一条数据
ret1 = collection.find_one({'gender': True})
print(ret1)

# 查找多条数据
ret2 = collection.find({'gender': False, 'age': {'$lte': 25}})  # 返回可迭代对象Cursor
print(ret2)
for item in ret2:
    print(item)

# 更新一条数据
collection.update_one({'name': '杨过'}, {'$set': {'name': '杨过007'}})

# 更新多条数据
collection.update_many({'name': '杨过'}, {'$set': {'name': '杨过000007'}})

# 删除一条数据
# collection.delete_one({'name': '杨过000007'})
print(collection.find({'name': '杨过000007'}).count())

# 删除多条数据
collection.delete_many({'name': '凌玲'})
```

