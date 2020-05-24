# 资源

- 官方 doc:    [MySQL 5.7 doc](https://dev.mysql.com/doc/refman/5.7/en)
- 菜鸟教程  https://www.runoob.com/



# 一、数据库介绍

数据库存储 - 数据库就是一种特殊的文件，存储在硬盘上

持久化	读写快	查找快	有效性	易扩展

mysql 数据库文件存储路径： /var/lib/mysql

需要超级管理员权限进入 ----  防止随意修改

 

## RDBMS

RDBMS	一种软件的简称	Relational Database Management System

(Relational DBMS)  关系型数据库管理系统

MySQL是一套RDBMS软件，由 MySQL 生成的数据库叫 MySQL 数据库

 

C/S架构			客户端--服务器 模型	Client/Server

B/S架构			浏览器--服务器 模型	Browser/Server

 

RDBMS是用**C/S架构**，RDBMS-client与RDBMS-Server使用**SQL语句**来通信



![img](.\images\RDBMS.jpg) 

**常用数据库:**

MySQL		关系型数据库		开源，免费，使用最广泛

Redis			一般用于缓存

Mongodb	非关系型数据库	一般用于爬虫数据存储等，不需要先建表的数据库，容易扩展,  以字典(key-value)方式存储数据，查询效率高

 

**其他数据库：**

Oracle		关系型数据库		NO.1 一般用于大型网站，按用户量/CPU型号收费，

​					淘宝以前用Oracle，现在用自己开发的数据库

SQlite		关系型数据库		轻量级，用于移动平台

> 关系型数据库：在同一个数据库中的多个数据表之间具有一定的联系

Oracle公司---收费 Oracle 和免费 MySQL

 

## 关系型数据库核心元素

- 行	(记录)

- 列	(字段)

- 表	(行的集合)

- 库	(表的集合)

 

 

## SQL 语句

Structured Query Language，结构化查询语言，是一种用来操作RDBMS的数据库语言

 

SQL语句主要分为：

**DDL：数据定义语言，进行数据库、表的管理等，如create、drop**

**DML：数据操作语言，对数据进行增加、修改、删除，如insert、udpate、delete**

**DQL：数据查询语言，用于对数据进行查询，如select**

DCL：数据控制语言，进行授权与权限回收，如grant、revoke

TPL：事务处理语言，对事务进行处理，包括begin transaction、commit、rollback

CCL：指针控制语言，通过控制指针完成表的操作，如declare cursor

 

SQL语句分 类:

1. 数据定义语言DDL:  Data Definition Language
2. 数据操纵语言DML:  Data Manipulation Language
3. 数据查询语言DQL:  Data Query Language
4. 数据控制语言DCL:  Data Control Language
5. 事务处理语言TPL
6. 指针控制语言CCL



### DDL - 数据定义语言

- 建设者角度
- 建表、建库、建视图

| 命令   | 描述                                                   |
| :----- | :----------------------------------------------------- |
| CREATE | 创建一个新的表，一个表的视图，或者数据库中的其他对象。 |
| ALTER  | 修改数据库中的某个已有的数据库对象，比如一个表。       |
| DROP   | 删除整个表，或者表的视图，或者数据库中的其他对象。     |

　　对象： 数据库和表

（后文所有示例对应 SQL 为 MySQL）

　　关键词： create  alter  drop  truncate(删除当前表再新建一个一模一样的表结构)

　　创建数据库：create database school;

　　删除数据库：drop database school;

　　切换数据库：use school;



表级操作：

- 查看所有表:  show tables;
- 创建表： create table xx ...;
- 查看生成表的 sql: show create table xx;
- 查看表结构： desc xx;
- 重命名表： rename table xx to yy;
- 删除表： drop table xx;

字段级操作：

- 增加字段：alter table xx add  字段名  类型  约束;
- 修改字段类型和约束：alter table xx modify  字段名  类型  约束;
- 重命名字段：alter table xx change 原字段名  新字段名  新类型  新约束);
- 删除字段：alter table xx drop 字段名;



### DML - 数据操作语言

- 使用者角度
- 数据记录的 增、删、改

| 命令   | 描述           |
| :----- | :------------- |
| INSERT | 创建一条记录。 |
| UPDATE | 修改记录。     |
| DELETE | 删除记录。     |

　　对象：纪录(行)

　　关键词：insert  update  delete

　　插入：insert into student values(01,'tonbby',99); (插入所有的字段)

　　　　　insert into student(id,name) values(01,'tonbby'); (插入指定的字段)

　　更新：update student set name='tonbby',score='99' where id=1;

　　删除：delete from tonbby where id = 01;

　　注意:  开发中很少使用delete,删除有物理删除和逻辑删除，其中逻辑删除可以通过给表添加一个字段(isDel)，若值为1，代表删除；若值为0，代表没有删除。

　　　　　此时，对数据的删除操作就变成了update操作了。

　　truncate和delete的区别：

　　　　truncate是删除表，再重新创建这个表,  属于DDL，delete是一条一条删除表中的数据，属于DML。



### DQL - 数据查询语言

- 使用者角度
- 数据记录的 查询

| 命令   | 描述                           |
| :----- | :----------------------------- |
| SELECT | 从一个或多个表中检索某些记录。 |

　　select ... from student where 条件 group by 分组字段 having 条件 order by 排序字段

　　执行顺序：from->where->group by->having->order by->select

　　注意：group by 通常和聚合函数(avg(),count()...)一起使用 ,经常先使用group by关键字进行分组，然后再进行集合运算。

　　　　　group by与having 一起使用，可以限制输出的结果，只有满足条件表达式的结果才会显示。

　　having和where的区别：

　　　　两者起作用的地方不一样，where作用于表或视图，是表和视图的查询条件。having作用于分组后的记录，用于选择满足条件的组。



### DCL - 数据控制语言

- 管理员角度

- 用户，权限，事务。

- 数据控制语句 用于控制不同数据段直接的许可和访问级别的语句。这些语句定义了数据库、表、字段、用户的访问权限和安全级别。主要的语句关键字包括grant、revoke 等。 

#### 管理用户

通配符：% 表示可以在任意主机使用用户登录数据库

添加用户

```mysql
create user '用户名'@'主机名' identified by '密码';
```

删除用户

```mysql
drop user '用户名'@'主机名';
```

修改用户密码

```mysql
update user set password=password('新密码') where user='用户名';
set password for '用户名'@'主机名'=password('新密码');
```

查询用户

```mysql
user mysql；
desc user;
select * from user;
```

#### 授权

查询权限

```mysql
show grants for '用户名'@'主机名';
```

授予权限

```mysql
grant 权限列表 on 数据库.表名  to  '用户名'@'主机名';
```

给用户授予所有去权限，在所有数据库数据表上

```mysql
grant all on .  to  '用户名'@'主机名';
```

撤销权限

```mysql
revoke 权限列表  on  数据库.表名  to  '用户名'@'主机名';
```





 

# 二、使用 MySQL

## 安装服务端

 安装 mysql 服务器端：

```bash
# Ubuntu 安装 mysql 服务器端
sudo apt-get install mysql-server

# 查看进程中是否有mysql
ps -aux | grep mysql
```

服务管理

```bash
# 查看
sudo service mysql status
# 启动
sudo service mysql start
# 关闭
sudo service mysql stop
# 重启
sudo service mysql restart
```



## 配置服务端

```bash
cd /etc/mysql/conf.d  # 配置文件目录
vim mysql.cnf

# 注：mysql目录下也有个mysql.cnf文件，但没有配置

# 主要配置项
# bind-address 表示服务器绑定的ip，默认为 127.0.0.1
# port 表示端口，默认为 3306
# datadir 表示数据库目录，默认为 /var/lib/mysql
# general_log_file 表示普通日志，默认为 /var/log/mysql/mysql.log
# log_error 表示错误日志，默认为 /var/log/mysql/error.log
```

 

## CentOS 安装 mysql5.7

https://blog.csdn.net/wohiusdashi/article/details/89358071 

 

## 连接服务端

进入客户端,  连接服务端

### <1>  Linux命令行

```bash
mysql -uroot -pmysql 或 mysql -uroot -p

# 连接时指定数据库:
mysql mydb -uroot -p123456
```

### <2>  Navicat

- 图形化界面客户端navicat:  http://www.formysql.com/xiazai.html

- 图形界面有: Navicat、sqlyog、MySQL Workbench



1. 下载 Navicat：官网

2. 解压缩

3. 运行：终端切换到目标目录，输入 `./start_navicat`

4. 重置试用天数：（按天数计算试用期的，一定有一个文件记录天数）

   ```bash
   cd ~
   ls -a
   rm .navicat64 -rf  # 这个文件记录天数的就是 .navicat64
   ```

 

**Navicat 安装问题：**

1 菜单栏乱码

需要设置字体：

菜单栏---->工具(T)---->选项(工具菜单的最后一个)---->设置界面字体为Noto Sans CJK SC Regular

2 数据表中文乱码

<1> 需要修改配置：用vim打开启动Navicat的文件 start_navicat

<2> 看到 export LANG=”en_US.UTF-8”，改为export LANG=”zh_CN.UTF-8”，保存。

 

**Navicat查询功能：**

1 注释	同 sublimetext----> Ctrl + /

2 命令界面字体大小	鼠标左键 + 滚轮

3 Ctrl + R 执行所有语句（结合使用注释 ------> 将其他语句注释，执行当前语句）

4 导入SQL语句源文件：在界面左侧点击”表”，右键选择导入SQL文件





### <3> windows连接mysql

1. 配置环境变量

 ```bash
# a 若没有配置环境变量 ------> 切换工作目录到mysql目录下, 如:
cd C:\Program Files (x86)\MySQL\MySQL Server 5.5\bin

# b 配置环境变量后不需要在mysql路径下打开mysql, 
# *配置环境变量的方法* -----> 我的电脑右键属性---高级系统设置---环境变量---选中Path---编辑---新建---将mysql路径写入其中---确定
 ```

2. 连接 MySQL

```bash
mysql -hlocalhost -uroot -p  / mysql -uroot -p
# 输入密码...
```

 



 

## SQL 导入/导出

> 注:  以下所说的 sql 文件,  后缀不一定要是 `.sql`

在数据库终端中导入 sql 文件的内容:

1. 切换工作路径到 SQL文件路径
2. 终端进入mysql，如果导入的是只插入数据的SQL语句时，需要先创建好对应的table
3. 输入命令 source areas.sql;  （source  <sql文件名>）  

在 Linux 终端中导出 / 导入 sql 文件

```
备份
	mysqldump –uroot –p 数据库名 > python.sql;		# 按提示输入mysql的密码

恢复
    连接mysql，创建新的数据库
    退出连接，执行如下命令
	mysql -uroot –p 新数据库名 < python.sql			# 根据提示输入mysql密码 
	
    进入 mysql 终端执行 sql 文件的方式:
        source areas.sql
```

## LOAD DATA 指令

```mysql
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```

要求:

1. pet 表中定义好字段
2. pet.txt 中的每一行数据都是对应 pet 的一行,  第一行是字段名,  每一列都用特殊分隔符分开
3. LOAD DATA 导入数据时,   会默认以 `\t` 分开每列数据,  以 `\n` 分开每一行数据
4. 可以指定 列分隔符 和 行分隔符







## MySQL 常用指令

>  不区分大小写

```
select version();
select now();
select CURRENT_DATE;
select CURDATE();
select 1 + 1, sin( pi() * 2 );
select pi() * 2 as result;
select user();

SHOW WARNINGS;
```



# 三、数据类型和约束

##  数据类型

l 使用数据类型的原则是：够用就行，尽量使用取值范围小的，而不用大的，这样可以更多的节省存储空间

MySQL支持多种类型，大致可以分为三类：数值、日期/时间和字符串(字符)类型。



### 数值类型

| 类型         | 大小                                     | 范围（有符号）                                               | 范围（无符号）                                               | 用途            |
| :----------- | :--------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :-------------- |
| TINYINT      | 1 字节                                   | (-128，127)                                                  | (0，255)                                                     | 小整数值        |
| SMALLINT     | 2 字节                                   | (-32 768，32 767)                                            | (0，65 535)                                                  | 大整数值        |
| MEDIUMINT    | 3 字节                                   | (-8 388 608，8 388 607)                                      | (0，16 777 215)                                              | 大整数值        |
| INT或INTEGER | 4 字节                                   | (-2 147 483 648，2 147 483 647)                              | (0，4 294 967 295)                                           | 大整数值        |
| BIGINT       | 8 字节                                   | (-9,223,372,036,854,775,808，9 223 372 036 854 775 807)      | (0，18 446 744 073 709 551 615)                              | 极大整数值      |
| FLOAT        | 4 字节                                   | (-3.402 823 466 E+38，-1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38) | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                  | 单精度 浮点数值 |
| DOUBLE       | 8 字节                                   | (-1.797 693 134 862 315 7 E+308，-2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 双精度 浮点数值 |
| DECIMAL      | 对DECIMAL(M,D) ，如果M>D，为M+2否则为D+2 | 依赖于M和D的值                                               | 依赖于M和D的值                                               | 小数值          |

- 如decimal(5,2)表示共存5位数，小数占2位



### 日期和时间

- 每个时间类型有一个有效值范围和一个"零"值，当指定不合法的MySQL不能表示的值时使用"零"值。

- TIMESTAMP类型有专有的自动更新特性

| 类型      | 大小 (字节) | 范围                                                         | 格式                | 用途                     |
| :-------- | :---------- | :----------------------------------------------------------- | :------------------ | :----------------------- |
| DATE      | 3           | 1000-01-01/9999-12-31                                        | YYYY-MM-DD          | 日期值                   |
| TIME      | 3           | '-838:59:59'/'838:59:59'                                     | HH:MM:SS            | 时间值或持续时间         |
| YEAR      | 1           | 1901/2155                                                    | YYYY                | 年份值                   |
| DATETIME  | 8           | 1000-01-01 00:00:00/9999-12-31 23:59:59                      | YYYY-MM-DD HH:MM:SS | 混合日期和时间值         |
| TIMESTAMP | 4           | 1970-01-01 00:00:00/2038结束时间是第 **2147483647** 秒，北京时间 **2038-1-19 11:14:07**，格林尼治时间 2038年1月19日 凌晨 03:14:07 | YYYYMMDD HHMMSS     | 混合日期和时间值，时间戳 |



### 字符串、文本

| 类型       | 大小                | 用途                            |
| :--------- | :------------------ | :------------------------------ |
| CHAR       | 0-255字节           | 定长字符串                      |
| VARCHAR    | 0-65535 字节        | 可变长字符串                    |
| TINYBLOB   | 0-255字节           | 不超过 255 个字符的二进制字符串 |
| TINYTEXT   | 0-255字节           | 短文本字符串                    |
| BLOB       | 0-65 535字节        | 二进制形式的长文本数据          |
| TEXT       | 0-65 535字节        | 长文本数据                      |
| MEDIUMBLOB | 0-16 777 215字节    | 二进制形式的中等长度文本数据    |
| MEDIUMTEXT | 0-16 777 215字节    | 中等长度文本数据                |
| LONGBLOB   | 0-4 294 967 295字节 | 二进制形式的极大文本数据        |
| LONGTEXT   | 0-4 294 967 295字节 | 极大文本数据                    |

- CHAR 和 VARCHAR 类型类似，但它们保存和检索的方式不同。它们的最大长度和是否尾部空格被保留等方面也不同。在存储或检索过程中不进行大小写转换。
  - 如char(3)，如果填充'ab'时会补一个空格为'ab '
  - 如varchar(3)，填充'ab'时就会存储'ab'

- BINARY 和 VARBINARY 类似于 CHAR 和 VARCHAR，不同的是它们包含二进制字符串而不要非二进制字符串。也就是说，它们包含字节字符串而不是字符字符串。这说明它们没有字符集，并且排序和比较基于列值字节的数值值。

- BLOB 是一个二进制大对象，可以容纳可变数量的数据。有 4 种 BLOB 类型：TINYBLOB、BLOB、MEDIUMBLOB 和 LONGBLOB。它们区别在于可容纳存储范围不同。

- 有 4 种 文本类型：TINYTEXT、TEXT、MEDIUMTEXT 和 LONGTEXT。对应的这 4 种 BLOB 类型，可存储的最大长度不同，可根据实际情况选择。当字符大于4000时推荐使用 TEXT



### 位

- bit:  0/1

```sql
alter table students add is_delete bit default 0;  
```



l 特别说明：

- varchar 长度的限制：

  字符类型若为gbk，每个字符最多占2个字节，最大长度不能超过32766;
  字符类型若为utf8，每个字符最多占3个字节，最大长度不能超过21845。
  字符类型若为utf8mb4，每个字符最多占4个字节，最大长度不能超过16283。
  若定义的时候超过上述限制，则varchar字段会被强行转为text类型，并产生warning。

- 对于图片、音频、视频等文件，不存储在数据库中，而是上传到某个服务器上，然后在表中存储这个文件的保存路径

- MySQL 5.0 以上的版本：

  1、一个汉字占多少长度与编码有关：

  **UTF－8**：一个汉字＝3个字节

  **GBK**：一个汉字＝2个字节

  2、varchar(n) 表示 n 个字符，无论汉字和英文，Mysql 都能存入 n 个字符，仅是实际字节长度有所区别

  3、MySQL 检查长度，可用 SQL 语言来查看：

  ```
  select LENGTH(fieldname) from tablename
  ```

l 更全的数据类型可以参考http://blog.csdn.net/anxpp/article/details/51284106

 



### NULL 类型

```mysql
mysql> SELECT 1 IS NULL, 1 IS NOT NULL;
+-----------+---------------+
| 1 IS NULL | 1 IS NOT NULL |
+-----------+---------------+
|         0 |             1 |
+-----------+---------------+
```

NULL 的比较运算

```mysql
mysql> SELECT 1 = NULL, 1 <> NULL, 1 < NULL, 1 > NULL;
+----------+-----------+----------+----------+
| 1 = NULL | 1 <> NULL | 1 < NULL | 1 > NULL |
+----------+-----------+----------+----------+
|     NULL |      NULL |     NULL |     NULL |
+----------+-----------+----------+----------+
```

MySQL 中只有数字  `0` 和 `NULL` 类型的布尔值为 false (0)

```mysql
mysql> SELECT 0 IS NULL, 0 IS NOT NULL, '' IS NULL, '' IS NOT NULL;
+-----------+---------------+------------+----------------+
| 0 IS NULL | 0 IS NOT NULL | '' IS NULL | '' IS NOT NULL |
+-----------+---------------+------------+----------------+
|         0 |             1 |          0 |              1 |
+-----------+---------------+------------+----------------+
```



## 约束

- 主键 primary key：物理上存储的顺序
- 自增 auto_increment

- 非空 not null：此字段不允许填写空值

- 惟一 unique：此字段的值不允许重复

- 默认 default：当不填写此值时会使用默认值，如果填写时以填写为准

- 外键 foreign key：对关系字段进行约束，当为关系字段填写值时，会到关联的表中查询此值是否存在，如果存在则填写成功，如果不存在则填写失败并抛出异常
  - 说明：虽然外键约束可以保证数据的有效性，但是在进行数据的crud（增加、修改、删除、查询）时，都会降低数据库的性能，所以不推荐使用.
  - 可以在逻辑层控制数据的有效性

 



# 四、操作 database

```sql

    -- 链接数据库
    mysql -uroot -p
    mysql -uroot -pmysql

    -- 退出数据库
    exit / quit / ctrl + d

    -- sql语句最后需要有分号;结尾
    -- 显示数据库版本
    select version();

    -- 显示时间
    select now();

    -- 查看所有数据库 (对于当前用户有查看权限的数据库)
    show databases;

    -- 创建数据库
    -- create database 数据库名 charset=utf8;
    create database python04;
    -- 数据库、数据表都有编码格式，创建表时，默认按照数据库的编码格式
    create database python04new charset=utf8;
    -- 注：如果没有在创建数据库的时候指定编码的话，向数据库中插入中文后，会报错，那么需要修改数据库的编码集:
	alter database 数据库名 CHARACTER SET utf8;

    -- 查看 创建数据库的sql
    -- show crate database ....
    show create database python04;

    -- 查看当前数据库
    select database();

    -- 使用数据库
    -- use 数据库的名字
    use python04new;

    -- 删除数据库
    -- drop database 数据库名;
    drop database python04;
```



 

# 五、操作 table

表级操作：

- 查看所有表:  show tables;
- 创建表： create table xx ...;
- 查看生成表的 sql: show create table xx;
- 查看表结构： desc xx;   或  describe xx;
- 重命名表： rename table xx to yy;
- 删除表： drop table xx;

字段级操作：

- 增加字段：alter table xx add  字段名  类型  约束;
- 修改字段类型和约束：alter table xx modify  字段名  类型  约束;
- 重命名字段：alter table xx change 原字段名  新字段名  新类型  新约束);
- 删除字段：alter table xx drop 字段名;

```sql
-- 数据表的操作

    -- 查看当前数据库中所有表
    show tables;

    -- 创建表
    -- auto_increment 表示自动增长
    -- not null 表示不能为空
    -- primary key 表示主键
    -- default 默认值
    
    -- create table 表名 (字段 类型 约束[, 字段 类型 约束]);
    
    create table xxxxx(id int, name varchar(30));
    create table yyyyy(id int primary key not null auto_increment, name varchar(30));
    create table zzzzz(
        id int primary key not null auto_increment,
        name varchar(30)
    );

    -- 查看表结构(列出所有字段及其约束)
    -- desc 表名;
    desc xxxxx;

    -- 创建students表(id、name、age、high、gender、cls_id)
    create table students(
        id int unsigned not null auto_increment primary key,
        name varchar(30),
        age tinyint unsigned default 0,
        high decimal(5,2),
        gender enum("男", "女", "中性", "保密") default "保密",
        -- enumerate 枚举
        cls_id int unsigned
    );

    insert into students values(0, "老王", 18, 188.88, "男", 0);
    select * from students;

    -- 创建classes表(id、name)
    create table classes(
        id int unsigned not null auto_increment primary key,
        name varchar(30)
    );

    insert into classes values(0, "神");
    select * from classes;

    -- 查看 创建表的实际完整语句
    -- show create table 表名字;
    show create table students;


    -- 修改表-添加字段
    -- alter table 表名 add 列名 类型;
    alter table students add birthday datetime;
    

    -- 修改表-修改字段：修改类型和约束
    -- alter table 表名 modify 列名 类型及约束;
    alter table students modify birthday date;


    -- 修改表-修改字段：修改字段名
    -- alter table 表名 change 原名 新名 类型及约束;
    alter table students change birthday birth date default "2000-01-01";
    change需要重新指定字段的 数据类型、约束

    -- 修改类型和约束的另一种方式：使用change，字段名不变，只改类型和约束

    -- 修改表-删除字段
    -- alter table 表名 drop 列名;
    alter table students drop high;


    -- 删除表
    -- drop table 表名;
    -- drop database 数据库;
    -- drop table 数据表;
    drop table xxxxx;
    
    -- 数据表的重命名：
    rename table t1 to t2;
```



# 六、增删改查 curd

## curd

- curd的解释: 代表创建（Create）、更新（Update）、读取（Retrieve）和删除（Delete）

## 增 - insert

```sql
-- 全列插入
-- insert [into] 表名 values(...)
-- 主键字段 可以用 0  null   default 来占位

-- 向classes表中插入 一个班级
insert into classes values(0, "菜鸟班");

-- 向students表插入 一个学生信息
insert into students values(0, "小李飞刀", 20, "女", 1, "1990-01-01");
insert into students values(null, "小李飞刀", 20, "女", 1, "1990-01-01");
insert into students values(default, "小李飞刀", 20, "女", 1, "1990-01-01");

-- 失败
-- insert into students values(default, "小李飞刀", 20, "第4性别", 1, "1990-02-01");

-- 枚举中 的 下标从1 开始 1---“男” 2--->"女"....
insert into students values(default, "小李飞刀", 20, 1, 1, "1990-02-01");

-- 部分插入
-- insert into 表名(列1,...) values(值1,...)
insert into students (name, gender) values ("小乔", 2);

-- 多行插入
insert into students (name, gender) values ("大乔", 2),("貂蝉", 2);
insert into students values(default, "西施", 20, "女", 1, "1990-01-01"), (default, "王昭君", 20, "女", 1, "1990-01-01");
```



## 删 - delete

```sql
-- 物理删除
-- delete from 表名 where 条件
delete from students; -- 整个数据表中的所有数据全部删除
delete from students where name="小李飞刀";

-- 逻辑删除
-- 用一个字段来表示 这条信息是否已经不能再使用了
-- 给students表添加一个is_delete字段 bit 类型
alter table students add is_delete bit default 0;  -- bit ---> 1位二进制数0/1
update students set is_delete=1 where id=6;

-- 一个字节 --> 8个bit
-- is_delete、bit、0  都可以随便设置
```



## 改 - update

```sql
-- update 表名 set 列1=值1,列2=值2... where 条件;
    update students set gender=1; -- 全部都改
    update students set gender=1 where name="小李飞刀"; -- 只要name是小李飞刀的 全部的修改
    update students set gender=1 where id=3; -- 只要id为3的 进行修改
    update students set age=22, gender=1 where id=3; -- 只要id为3的 进行修改
    update students set gender="女" where name="貂蝉" or name="林轩";
```



## 查 - select

### 基本查询

```sql
-- 查询所有列
-- select * from 表名;
select * from students;

---定条件查询
select * from students where name="小李飞刀"; -- 查询 name为小李飞刀的所有信息
select * from students where id>3; -- 查询 name为小李飞刀的所有信息

-- 查询指定列
-- select 列1,列2,... from 表名;
select name,gender from students;

-- 可以使用as为列或表指定别名
-- select 字段[as 别名] , 字段[as 别名] from 数据表 where ....;
select name as "姓名", gender as "性别" from students;

-- as 可省略
-- 字段的顺序
select id as "序号", gender as "性别", name as "姓名" from students;

select id+1 "序号", 88 from students;
```



###  高级查询

- 条件查询:
  - 比较运算符
  - 逻辑运算符：and、or、not
  - 模糊查询：like、rlike
  - 范围查询：in、not in、between ... and ...、not between ... and ...
  - 空判断：is null、is not null
- 排序：order by ... asc、order by ... desc、order by ... asc, ... desc
- 聚合函数：count、max、min、avg、round、sum
- 分组：group by、group_concat(...)、having
- 分页：limit [start], [count]
- 链接查询：inner join、left join、right join
  - join 连接:  
    - select * from scores s1, scorces s2;
    - 结果行数是: 左表行数 * 右表行数
- 自关联
- 子查询

```sql
-- 数据的准备
    -- 创建一个数据库
    create database python_test charset=utf8;

    -- 使用一个数据库
    use python_test;

    --显示使用的当前数据库是哪个?
    select databases();

    --创建一个数据表
    -- students表
    create table students(
        id int unsigned primary key auto_increment not null,
        name varchar(20) default '',
        age tinyint unsigned default 0,
        height decimal(5,2),
        gender enum('男','女','中性','保密') default '保密',
        cls_id int unsigned default 0,
        is_delete bit default 0
    );

    -- classes表
    create table classes (
        id int unsigned auto_increment primary key not null,
        name varchar(30) not null
    );



-- 查询
    -- 查询所有字段
    -- select * from 表名;
    select * from students;
    select * from classes;
    select id, name from classes;

    -- 查询指定字段
    -- select 列1,列2,... from 表名;
    select name, age from classes;

    -- 使用 as 给字段起别名
    -- select 字段 as 名字.... from 表名;
    select name as 姓名, age as 年龄 from classes;

    -- select 表名.字段 .... from 表名;
    -- 用于多表区分
    select students.name, students.age from students;


    -- 可以通过 as 给表起别名
    --  select 别名.字段 .... from 表名 as 别名;
    select students.name, students.age from students;
    select s.name, s.age from students as s;
    -- 失败的select students.name, students.age from students as s;

    ————————————————————————————————————————————————————
    distinct
    -- 消除重复行
    -- distinct 字段
    select distinct gender from students;
    ————————————————————————————————————————————————————

-- 条件查询
    -- 比较运算符
        -- select .... from 表名 where .....
        -- >
        -- 查询大于18岁的信息
        select * from students where age>18;
        select id,name,gender from students where age>18;

        -- <
        -- 查询小于18岁的信息
        select * from students where age<18;

        -- >=
        -- <=
        -- 查询小于或等于18岁的信息

        -- =
        --查询年龄为18岁的所有学生的名字
        select * from students where age=18;


        -- != 或者 <> (<>在很多语言中不能用，如在pytho3.0中不可以用)


    -- 逻辑运算符
        -- and
        -- 18到28岁之间所有学生的信息
        select * from students where age>18 and age<28;
        -- 失败select * from students where age>18 and <28;


        --18岁以上的女性
        select * from students where age>18 and gender="女";
        select * from students where age>18 and gender=2;


        -- or
        --18岁以上或者身高查过180(包含)以上
        select * from students where age>18 or height>=180;


        -- not
        -- 不在 18岁以上的女性 这个范围内的信息
        -- and 优先级高于 not
        select * from students where not age>18 and gender=2;
        select * from students where not (age>18 and gender=2);

        -- 年龄不是小于或者等于18 并且是女性
        select * from students where (not age<=18) and gender=2;


    -- 模糊查询
        -- like
        -- % 替换1个或者多个
        -- _ 替换1个
        
        -- 查询姓名中 以 "小" 开始的名字
        select name from students where name="小";
        select name from students where name like "小%";

        -- 查询姓名中 有"小" 所有的名字
        select name from students where name like "%小%";

        -- 查询有2个字的名字
        select name from students where name like "__";

        -- 查询有3个字的名字
        select name from students where name like "___";

        -- 查询至少有2个字的名字
        select name from students where name like "__%";


        -- rlike 正则
        -- 查询以 周开始的姓名
        select name from students where name rlike "^周.*";

        -- 查询以 "周"开始、"伦"结尾的姓名
        select name from students where name rlike "^周.*伦$";
        select name from students where name rlike "^周" and name rlike "伦$";

        -- 查询不以则"周"开始的姓名
        -- select name from students where name not like "周%";




    -- 范围查询
        -- in（1, 3，8 ）表示在一个非连续的范围内
        -- 查询 年龄为18、34的名字
        select name,age from students where age=18 or age=34;
        select name,age from students where age=18 or age=34 or age=12;
        select name,age from students where age in (12, 18, 34);



        -- not in 不非连续的范围之内
        -- 年龄不是 18、34岁之间的信息
        select name,age from students where age not in (12, 18, 34);
  

        -- between ... and ...表示在一个连续的范围内
        -- 查询 年龄在18到34之间的信息
        select name,age from students where age between 18 and 34;


        -- not between ... and ...表示不在一个连续的范围内
        -- 查询 年龄不在在18到34之间的的信息
        select * from students where age not between 18 and 34;
        select * from students where not age between 18 and 34;
        -- 失败的select * from students where age not (between 18 and 34);
        -- 失败的select * from students where age (not between) 18 and 34;


    -- 空判断
        -- 判空is null
        -- 查询身高为空的信息
        select * from students where height is null;
        select * from students where height is NULL;
        select * from students where height is Null;

        -- 判非空is not null
        select * from students where height is not null;



-- 排序
    -- order by 字段
    -- asc从小到大排列，即升序 ----ascend
    -- desc从大到小排序，即降序----descend

    -- 查询年龄在18到34岁之间的男性，按照年龄从小到大排序
    select * from students where (age between 18 and 34) and gender=1;
    select * from students where (age between 18 and 34) and gender=1 order by age;
    select * from students where (age between 18 and 34) and gender=1 order by age asc;
   

    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序
    select * from students where (age between 18 and 34) and gender=2 order by height desc;

    
    -- order by 多个字段
    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序, 如果身高相同的情况下按照年龄从小到大排序
    select * from students where (age between 18 and 34) and gender=2 order by height desc, age asc;

    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序, 如果身高相同的情况下按照年龄从小到大排序,
    -- 如果年龄也相同那么按照id动大到小排序
    select * from students where (age between 18 and 34) and gender=2 order by height desc, age asc, id desc;

    -- 按照年龄从小到大、身高从高到矮的排序
    select * from students order by age asc, height desc;
    
    -- 按中文排序：不是按首字的拼音，一般不用中文排序
    -- 可以没有where，有 where 就一定接在表名之后



-- 聚合函数
    -- 总数
    -- count
    -- 查询男性有多少人，女性有多少人
    select *  from students where gender=1;
    select count(*)  from students where gender=1;
    select count(*) as 男性人数 from students where gender=1;
    select count(*) as 女性人数 from students where gender=2;


    -- 最大值
    -- max
    -- 查询最大的年龄
    select age from students;
    select max(age) from students;
    -- 查询年龄最大的学生的全部信息
    select * from students where age=(select max(age) from students);
    select * from students order by age desc limit 1;

    -- 查询女性的最高 身高
    select max(height) from students where gender=2;

    
    -- 最小值
    -- min
    
    -- 求和
    -- sum
    -- 计算所有人的年龄总和
    select sum(age) from students;

    
    -- 平均值
    -- avg
    -- 计算平均年龄   
    select avg(age) from students;
    -- 计算平均年龄 sum(age)/count(*)
    select sum(age)/count(*) from students;
    ---------  avg(age)只对age字段中不为null的所有age求平均， 如果age有null值，则avg(age)结果不同于 sum(age)/count(*)


    -- 四舍五入 round(123.23 , 1) 保留1位小数
    -- 计算所有人的平均年龄，保留2位小数
    select round(sum(age)/count(*), 2) from students;
    select round(sum(age)/count(*), 3) from students;

    -- 计算男性的平均身高 保留2位小数
    select round(avg(height), 2) from students where gender=1;
    -- 失败 select name, round(avg(height), 2) from students where gender=1;


-- 分组 (与聚合函数一起用)
    -- group by
    -- 按照性别分组, 查询所有的性别
    select gender from students group by gender;
    -- 失败 select name from students group by gender;
    -- 失败 select * from students group by gender;

    -- 计算每种性别中的人数
    select gender,count(*) from students group by gender;


    -- 计算男性的人数
    select gender,count(*) from students where gender=1 group by gender;
    -- 可以没有where，有 where 就一定在 group by 之前


    -- group_concat(...)
    -- 查询同种性别中的姓名
    select gender, group_concat(name) from students where gender=1 group by gender;
    select gender, group_concat(name, age, id) from students where gender=1 group by gender;
    select gender, group_concat(name, "_", age, " ", id) from students where gender=1 group by gender;

    -- having
    -- 查询平均年龄超过30岁的性别，以及姓名 having avg(age) > 30
    select gender, group_concat(name), avg(age) from students group by gender having avg(age)>30;

    -- 查询每种性别中的人数多于2个的信息
    select gender, group_concat(name) from students group by gender having count(*)>2;



-- 分页
    -- limit start, count

    -- 限制查询出来的数据格式
    select * from students where gender=1 limit 2;

    -- 查询前5个数据
    select * from students limit 0,5;

    -- 查询id6-10（包含）的书序
    select * from students limit 5,5;


    -- 每页显示2个，第1页
    select * from students limit 0,2;

    -- 每页显示2个，第2页
    select * from students limit 2,2;

    -- 每页显示2个，第3页
    select * from students limit 4,2;

    -- 每页显示2个，第4页
    select * from students limit 6,2; -- -----> limit (第N页-1)*每个的个数, 每页的个数;

    -- 每页显示2个，显示第6页的信息, 按照年龄从小到大排序
    -- 失败select * from students limit 2*(6-1),2;
    -- 失败select * from students limit 10,2 order by age asc;
    select * from students order by age asc limit 10,2;

    select * from students where gender=2 order by age desc limit 0,2;

    -- 注：where 紧接表名、limit 在最后
    -- 先排序再 limit 1 可以直接查询到最值


-- 链接查询
    -- inner join ... on

    -- select * from 表A inner join 表B;
    select * from students inner join classes;

    -- 查询 有能够对应班级的学生以及班级信息
    select * from students inner join classes on students.cls_id=classes.id;

    -- 按照要求显示姓名、班级
    select students.* classes.name from students inner join classes on students.cls_id=classes.id;
    select students.name classes.name from students inner join classes on students.cls_id=classes.id;

    -- 给数据表起名字
    select s.name c.name from students as s inner join classes as c on s.cls_id=c.id;  

    -- 查询 有能够对应班级的学生以及班级信息, 显示学生的所有信息, 只显示班级名称
    select s.*,c.name from students as s inner join classes as c on s.cls_id=c.id;

    -- 在以上的查询中，将班级姓名显示在第1列
    select c.name,s.* from students as s inner join classes as c on s.cls_id=c.id;

    -- 查询 有能够对应班级的学生以及班级信息, 按照班级进行排序
    -- select c.xxx s.xxx from student as s inner join clssses as c on .... order by ....;
    select c.name, s.* from students as s inner join classes as c on s.cls_id=c.id order by c.name;

    -- 当时同一个班级的时候, 按照学生的id进行从小到大排序
    select c.name, s.* from students as s inner join classes as c on s.cls_id=c.id order by c.name,s.id;

    -- left join
    -- 查询每位学生对应的班级信息
    select * from students as s left join classes as c on s.cls_id=c.id;

    -- 查询没有对应班级信息的学生
    -- select ... from xxx as s left join xxx as c on..... where .....
    -- select ... from xxx as s left join xxx as c on..... having .....
    select s.*, c.name from students as s left join classes as c on s.cls_id=c.id where c.name is null;
    select s.*, c.name from students as s left join classes as c on s.cls_id=c.id having c.name is null;

    -- right join
    -- 将数据表名字互换位置，用left join完成


-- 自关联
    -- 省级联动 url:http://demo.lanrenzhijia.com/2014/city0605/

    -- 查询所有省份
    select * from areas where pid is null;

    -- 查询出山东省有哪些市
    select * from areas as province inner join areas as city on city.pid=province.aid having province.atitle="山东省";
    select province.atitle, city.atitle from areas as province inner join areas as city on city.pid=province.aid having province.atitle="山东省";

    -- 查询出青岛市有哪些县城
    select * from areas as city inner join areas as province on city.pid=province.aid where province.atitle="青岛市";



-- 子查询
    -- 标量子查询
    -- 查询出高于平均身高的信息
    select * from students where height > (select avg(height) from students);

    -- 查询最高的男生信息
    select * from students where height = 188;

    select * from students where height = (select max(height) from students);
    

    -- 列级子查询
    -- 查询学生的班级号能够对应的学生信息
    select * from students where cls_id in (1, 2);
    select * from students where cls_id in (select id from classes);


    -- 查询某个市的县和县级市
    -- select * from arears where pid = (select pid from areas where atitle="南京市");
```



### where 和 having 的区别

```
where 是按条件对原表进行过滤
having 是按条件对 group by 分组后的表进行过滤
```



### inner, left, right 三种 join 的区别

```
inner join    取两张表的交集, 对于左表特有, 或右表特有的内容, 不会返回
left join     取两张表的交集, 同时对于左表特有的, 对应右表都填充为 NULL
right join    取两张表的交集, 同时对于右表特有的, 对应左表都填充为 NULL

在 left join 和 right join 的结果下增加以下任一条件, 可以实现 inner join 的效果:
	1. WHERE xxx IS NOT NULL
	2. HAVING xxx IS NOT NULL
```

当查询结果的列来源于多张表时，需要将多张表连接成一个大的数据集，再选择合适的列返回

mysql支持三种类型的连接查询，分别为：

- 内连接查询：查询的结果为两个表匹配到的数据

  ![img](images/inner_join.png)

- 右连接查询：查询的结果为两个表匹配到的数据，右表特有的数据，对于左表中不存在的数据使用null填充

  ![img](images/right_join.png)

- 左连接查询：查询的结果为两个表匹配到的数据，左表特有的数据，对于右表中不存在的数据使用null填充

  ![img](images/left_join.png)







###  练习

```
-- 数据库的操作

    -- 链接数据库
    -- 退出数据库
    
    -- sql语句最后需要有分号;结尾
    -- 显示数据库版本
    -- 显示时间
    -- 查看所有数据库
    -- 创建数据库
    -- 查看 创建数据库的完整语句
    -- 查看当前使用的数据库
    -- 使用数据库
    -- 删除数据库


-- 数据表的操作
    -- 查看当前数据库中所有表
    -- 创建表

    -- 查看表结构(列出所有字段及其约束)
    -- 创建students表(id、name、age、high、gender、cls_id)
    -- 创建classes表(id、name)
    -- 查看 创建表的实际完整语句

    -- 修改表-添加字段
    -- 修改表-修改字段：修改类型和约束
    -- 修改表-修改字段：修改字段名
    -- 修改表-删除字段
    -- 删除表

    
-- 表数据的增删改查(curd)

    -- 增加
        -- 全列插入
        -- 部分插入
        -- 多行插入
       
    -- 修改表中的数据

    -- 查询基本使用
        -- 查询所有列
        ---定条件查询
        -- 查询指定列
        -- 使用as为列或表指定别名
        -- 字段的顺序可以不同
    	
    -- 删除
        -- 物理删除
        -- 逻辑删除


-- 查询进阶

-- 数据的准备
    -- 创建一个数据库
    -- 使用一个数据库
    --显示使用的当前数据库是哪个?
    --创建一个数据表
    -- students表
    -- classes表

-- 查询
    -- 查询所有字段
    -- 查询指定字段
    -- 使用 as 给字段起别名

    -- 用于多表区分
    -- 可以通过 as 给表起别名
    -- 消除重复行


-- 条件查询
    -- 比较运算符
        -- 查询大于18岁的信息
        -- 查询小于18岁的信息
        -- 查询小于或等于18岁的信息
        -- 查询年龄为18岁的所有学生的名字
        -- != 或者 <> (<>在很多语言中不能用，如在pytho3.0中不可以用)
    -- 逻辑运算符
        -- 18到28岁之间所有学生的信息
        -- 18岁以上的女性
        
        -- 18岁以上或者身高查过180(包含)以上

        -- 不在 18岁以上的女性 这个范围内的信息

        -- 年龄不是小于或者等于18 并且是女性

    -- 模糊查询
        -- like
        -- 查询姓名中 以 "小" 开始的名字
        -- 查询姓名中 有"小" 所有的名字
        -- 查询有2个字的名字
        -- 查询有3个字的名字
        -- 查询至少有2个字的名字

        -- rlike 正则
        -- 查询以 周开始的姓名
        -- 查询以 "周"开始、"伦"结尾的姓名
        -- 查询不以则"周"开始的姓名


    -- 范围查询
        -- 查询 年龄为18、34的名字
        -- 年龄不是 18、34岁之间的信息
        -- 查询 年龄在18到34之间的信息
        -- 查询 年龄不在在18到34之间的的信息


    -- 空判断
        -- 查询身高为空的信息
        -- 查询身高不为空的信息


-- 排序
    -- 查询年龄在18到34岁之间的男性，按照年龄从小到到排序
    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序

    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序, 如果身高相同的情况下按照年龄从小到大排序
    -- 查询年龄在18到34岁之间的女性，身高从高到矮排序, 如果身高相同的情况下按照年龄从小到大排序,
    -- 如果年龄也相同那么按照id从大到小排序

    -- 按中文排序：不是按首字的拼音，一般不用中文排序

-- 聚合函数

    -- 查询男性有多少人，女性有多少人
    -- 查询最大的年龄
    -- 查询女性的最高 身高
    -- 计算所有人的年龄总和
    -- 计算平均年龄
    -- 计算平均年龄 另外一种方法
    -- 计算所有人的平均年龄，保留2位小数
    -- 计算男性的平均身高 保留2位小数


-- 分组 (与聚合函数一起用)
    -- 按照性别分组, 查询所有的性别
    -- 计算每种性别中的人数
    -- 计算男性的人数

    -- 查询同种性别中的姓名

    -- having
    -- 查询平均年龄超过30岁的性别，以及姓名 having avg(age) > 30
    -- 查询每种性别中的人数多于2个的信息


-- 分页

    -- 限制查询出来的数据格式
    -- 查询前5个数据
    -- 查询id 6-10（包含）的书序
    -- 每页显示2个，第1个页面
    -- 每页显示2个，第2个页面
    -- 每页显示2个，第3个页面
    -- 每页显示2个，第4个页面
    -- 每页显示2个，显示第6页的信息, 按照年龄从小到大排序


-- 链接查询
    
    -- 查询 有能够对应班级的学生以及班级信息
    -- 按照要求显示姓名、班级
    -- 给数据表起名字
    -- 查询 又能够对应班级的学生以及班级信息, 显示学生的所有信息, 只显示班级名称
    -- 在以上的查询中，将班级姓名显示在第1列
    -- 查询 有能够对应班级的学生以及班级信息, 按照班级进行排序
    -- 当时同一个班级的时候, 按照学生的id进行从小到大排序
    -- 查询每位学生对应的班级信息
    -- 查询没有对应班级信息的学生


-- 自关联
 
    -- 查询所有省份
    -- 查询出山东省有哪些市
    -- 查询出青岛市有哪些县城


-- 子查询
    -- 标量子查询
    -- 查询出高于平均身高的信息
    -- 查询最高的男生信息

    -- 列级子查询
    -- 查询学生的班级号能够对应的学生信息
    -- 查询某个市的县和县级市

```



 



# 概念总结

## 链接查询

**内连接查询**：查询的结果为两个表匹配到的数据

外链接-----左链接、右链接		

（用左链接、更换两个表名的顺序 也可以实现右链接 -----> 一般用left join）

**右连接查询**：查询的结果为两个表匹配到的数据，右表特有的数据，对于左表中不存在的数据使用null填充

**左连接查询**：查询的结果为两个表匹配到的数据，左表特有的数据，对于右表中不存在的数据使用null填充

 

## 主查询和子查询

标量子查询			select * from students where age > (select avg(age) from students);

列级子查询			select name from classes where id in (select cls_id from students);

行级子查询			select * from students where (height,age) = (select max(height),max(age) from students);

 

## select语法顺序

select 语法顺序：

```
select distinct * from 表名
    where ....
    group by ...
    having ...	# having 条件表达式：用来分组查询后指定一些条件来输出查询结果
                # having作用和where一样，但having只能用于group by
    order by ...
    limit start,count  # start索引是从 0 开始
```

**将 子查询的结果表格 起别名，并作为链接的一部分：**

```
select xx.?, yy.? 
    from (select .....) as xx 
    inner join (select .......) as yy
    on xx.?=yy.?
    order by ?;
```

## innodb 和 myisam 的区别

- mysql 中 engine=innodb 和 engine=myisam 的区别: https://www.cnblogs.com/avivahe/p/5427884.html







 

# Python 操作 MySQL

![img](.\images\pymysql.jpg) 

 

## pymysql

安装 pymysql

```
sudo pip3 install pymysql
```

### 使用步骤

```python
import pymysql

# 连接database
conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='renming',
    user='root',
    password='123456',
    charset='utf8'
)

# 得到一个可以执行SQL语句的光标对象
# 执行完毕返回的结果集默认以`元组`显示
# cursor = conn.cursor()
# 得到一个可以执行SQL语句并且将结果作为`字典`返回的游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# 定义要执行的SQL语句
sql = "select * from renming_data"

# 执行SQL语句
cursor.execute(sql)

# 获取结果集
data = cursor.fetchall()
print(data)

# 关闭光标对象
cursor.close()

# 关闭数据库连接
conn.close()
```



###  cursor.execute() 多种用法

```
# a.先拼接 sql, 再传给 execute
sql = 'select * from userinfo where user = "%s" and pwd="%s"' % (user, pwd)
print(sql)
res = cursor.execute(sql)

# b.不拼接 sql, 传给 execute 时指定替换数据,  可以有效防止 SQL 注入
# %s需要去掉引号，pymysql会自动加上
sql = "select * from userinfo where name=%s and password=%s"
res = cursor.execute(sql, [user, pwd])
```



### 添加多条数据

- cursor.executemany(sql, data)

```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='renming',
    user='root',
    password='123456',
    charset='utf8'
)
cursor = conn.cursor()
sql = "insert into renming_data(title, content) values(%s, %s);"
# 准备多条数据
data = [
    ('july', '147'),
    ('june', '258'),
    ('marin', '369')
]

cursor.executemany(sql, data)  # 返回受影响行数: 3

# 涉及写操作要注意提交
conn.commit()

# 关闭连接
cursor.close()
conn.close()

```

 

### 数据回滚

```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='renming',
    user='root',
    password='123456',
    charset='utf8'
)
cursor = conn.cursor()
sql1 = "insert into renming_data (id, title, content) values (%s, %s, %s);"
sql2 = sql1

try:
    cursor.execute(sql1, [210, 'title', 'content'])
    cursor.execute(sql2, [210, 'title', 'content'])  # id已存在, 执行该SQL语句会报错
    # 涉及写操作注意要提交
    conn.commit()
except Exception as e:
    print('Error: ', str(e))
    # 回滚
    conn.rollback()

cursor.close()
conn.close()

```





# MySQL高级

## 1 视图 view

视图就是一条SELECT语句执行后返回的结果集。所以我们在创建视图的时候，主要的工作就落在创建这条SQL查询语句上。

视图是对若干张基本表的引用，一张虚表，查询语句执行的结果，不存储具体的数据（基本表数据发生了改变，视图也会跟着改变）；

方便操作，特别是查询操作，减少复杂的SQL语句，增强可读性；

 

·虚拟的表，隔离数据库，数据库结构变化时，不需要改动程序中的sql语句

·使用sql查询语句的结果创建一个视图：

```
create view v_name as select语句;
```

删除视图:

```
drop view v_name;
```

·视图不能用来对数据进行增删改

·原数据表的改动 直接更新到视图中

 

- 方便查询数据（但不能提高查询效率）
- 提高了重用性，就像一个函数
- 对数据库重构，却不影响程序的运行
- 提高了安全性能，可以对不同的用户
- 让数据更加清晰

 

数据表的拆分 ---->  方便增删改

视图 (链接表---结果集)  ---->  方便查



## 2 事务 transcation

- 所谓事务,它是一个操作序列，这些操作要么都执行，要么都不执行，它是一个不可分割的工作单位。

- 事务是数据库维护数据一致性的单位，在每个事务结束时，都能保持数据一致性

- 事务广泛的运用于订单系统、银行系统等多种场景

- 表的引擎类型必须是 **innodb** 类型才可以使用事务，这是 mysql 表的默认引擎

 

**事务四大特性 ---------**  **ACID** **(重要)**

1 原子性(Atomicity)

- 一个事务必须被视为一个不可分割的最小工作单元，整个事务中的所有操作要么全部提交 (commit) 成功，要么全部失败回滚 (rollback)

2 一致性(Consistency)

- 数据库总是从一个一致性的状态转换到另一个一致性的状态。（在转账的例子中，一致性确保了，即使在执行第三、四条语句之间时系统崩溃，支票账户中也不会损失200美元，因为事务最终没有提交，所以事务中所做的修改也不会保存到数据库中。）

3 隔离性(Isolation)

- 一个事务所做的修改在最终提交以前，对其他事务是不可见的，其他事务会等待前面的事务先被提交**(堵塞)**。

4 持久性(Durability)

- 一旦事务提交，则其所做的修改会永久保存到数据库。（此时即使系统崩溃，修改的数据也不会丢失。）

 



·修改数据的命令会自动的触发事务，包括insert、update、delete；

·在mysql客户端中也可以手动开启事务、手动提交：

```sql
-- 开启事务
begin;
-- 或 start transaction;

-- 修改数据
update语句;

-- 回滚事务 ----  放弃缓存中变更的数据
rollback;

-- 提交事务 ----  将缓存中的数据变更维护到物理表中
commit;
```

**事务SQL的样本**

1  start transaction;

2  select balance from checking where customer_id = 10233276;

3  update checking set balance = balance - 200.00 where customer_id = 10233276;

4  update savings set balance = balance + 200.00 where customer_id = 10233276;

5  commit;

 

show variables;

查看mysql的默认设置

 

**其他主题:**

- **事务的隔离级别**

- **脏读、不可重复读、虚读(幻读)**



 

## 3 索引 index

- 索引是一种 特殊的文件 (InnoDB数据表上的索引是表空间的一个组成部分)，它们包含着对数据表里所有记录的引用指针。
- 数据库索引能加快数据库的 **查询** 速度
- 索引太多会影响 **更新和插入** 的速度，因为它需要同样更新每个索引文件。
- 对于一个经常需要更新和插入的表格，就没有必要为一个很少使用的where字句单独建立索引了，对于比较小的表，排序的开销不会很大，也没有必要建立另外的索引。

- 建立索引会占用磁盘空间
- 创建 主键、外键时自动创建索引，通过主键、外键查找效率高
- 索引类型
  - btree 索引
  - hash 索引

 

**索引的使用**

查看索引

```
show index from 表名;
```

创建索引

```
# 如果指定字段是字符串，需要指定长度，建议长度与定义字段时的长度一致
# 字段类型如果不是字符串，可以不填写长度部分
create index 索引名称 on 表名(字段名称(长度))
```

删除索引

```
drop index 索引名称 on 表名;
```





## 4 账户管理 account

修改mysql的密码：

1 sudo -s

2 mysql -uroot -p

3 直接回车进入mysql

4 

```
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
```





## 5 主从同步配置

主数据库 (主服务器 master)  x 1

从数据库 (从服务器 slave)  x n

 

·读写分离 (向从服务器请求读，向主服务器请求写)

为什么要分离读和写？

·自动同步 (数据备份) (主服务器的数据修改立即自动同步到从服务器)

·负载均衡

  

**配置主从同步**

·主从同步机制：基于 **二进制日志机制**，从服务器主动请求主服务器获取二进制log日志，采用轮询方式检查是否有数据更新

·一般主服务器运行一段时间后才需要建从服务器，此时需要先将主服务器现有的数据**备份**到所有从服务器，然后配置主从**同步** （先备份----->再配置同步）

 

·确定从服务器能正常连接主服务器

·在主服务器上将生成的**备份**文件用 scopy 发送到 从服务器（或反过来使用scopy获取**备份**文件）

 

<1> 备份 (将数据导出成sql文件)

```
mysqldump -uroot -p jing_dong > JD.sql
```

<2> 恢复 (将sql文件导入，执行)

多种方法恢复：

```
mysql -uroot -p new_JD < JD.sql
或 
source JD.sql
```

<3> 配置主服务器、配置从服务器 -- 使主从**同步**

在mysql文件中分别配置主从的  server_id、log_bin

在主服务器中分配一定权限 (读权限) 的账户给从服务器

 







