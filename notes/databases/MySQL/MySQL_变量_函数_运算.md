

# MySQL 进阶

# 定义变量

### `select @var := val`

 ```mysql
mysql> SELECT @min_price:=MIN(price),@max_price:=MAX(price) FROM shop;
+------------------------+------------------------+
| @min_price:=MIN(price) | @max_price:=MAX(price) |
+------------------------+------------------------+
|                   1.25 |                  19.95 |
+------------------------+------------------------+

mysql> SELECT * FROM shop WHERE price=@min_price OR price=@max_price;
+---------+--------+-------+
| article | dealer | price |
+---------+--------+-------+
|    0003 | D      |  1.25 |
|    0004 | D      | 19.95 |
+---------+--------+-------+
 ```

### `set @var = val`

```
SET @j = '{"a": 1, "b": 2, "c": {"d": 4}}'
```





# 函数

官网文档,  函数与运算符的文档索引:    https://dev.mysql.com/doc/refman/5.7/en/func-op-summary-ref.html 



### 类型转换

```mysql
# 加法自动转换类型
mysql> SELECT 1+'1';
        -> 2

# concat() 转为 CHAR
mysql> SELECT CONCAT(2,' test');
        -> '2 test'
mysql> SELECT 38.8, CONCAT(38.8);
        -> 38.8, '38.8'

# CAST(value as <type>) 转为指定类型
mysql> SELECT 38.8, CAST(38.8 AS CHAR);
        -> 38.8, '38.8'
        
BINARY str	  # Cast a string to a binary string
CONVERT()	  # Cast a value as a certain type

# CAST()  与  CONVERT() 对比:
CONVERT(string, CHAR[(N)] CHARACTER SET charset_name)
CAST(string AS CHAR[(N)] CHARACTER SET charset_name)
# 如:
SELECT CONVERT('test', CHAR CHARACTER SET utf8);
SELECT CAST('test' AS CHAR CHARACTER SET utf8);
```



##### `CAST()`

Cast(字段名 as 转换的类型 )，其中类型可以为：

```
CHAR[(N)] 字符型 
DATE  日期型
DATETIME  日期和时间型
DECIMAL  float型
SIGNED  int
TIME  时间型
```



例如表 table1

```
date
2015-11-03 15:31:26
```

select cast(date as signed) as date from  table1;

结果如下：

```
date
20151103153126
```

select cast(date as char) as date from  table1;

结果如下：

```
date
2015-11-03 15:31:26
```

select cast(date as datetime) as date from  table1;

结果如下：

```
date
2015-11-03 15:31:26
```

select cast(date as date) as date from  table1;

结果如下：

```
date
2015-11-03
```

select cast(date as time) as date from  table1;

结果如下：

```
date
15:31:26
```



### 流程控制

| Name                                                         | Description                  |
| ------------------------------------------------------------ | ---------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case) | Case operator                |
| [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if) | If/else construct            |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) | Null if/else construct       |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_nullif) | Return NULL if expr1 = expr2 |



##### `CASE`

`CASE  [val]  WHEN  val  THEN  val   [ WHEN  val  THEN  val ]  ELSE  val  END`

```mysql
mysql> SELECT CASE 1 WHEN 1 THEN 'one'
    ->     WHEN 2 THEN 'two' ELSE 'more' END;
        -> 'one'
mysql> SELECT CASE WHEN 1>0 THEN 'true' ELSE 'false' END;
        -> 'true'
mysql> SELECT CASE BINARY 'B'
    ->     WHEN 'a' THEN 1 WHEN 'b' THEN 2 END;
        -> NULL
```

##### `IF()`

`IF(布尔条件, 条件真时的值, 条件假时的值)`

```mysql
mysql> SELECT IF(1>2,2,3);
        -> 3
mysql> SELECT IF(1<2,'yes','no');
        -> 'yes'
mysql> SELECT IF(STRCMP('test','test1'),'no','yes');
        -> 'no'
```

##### `IFNULL()`

`IFNULL( 值1, 值2 )`    返回两个值中 第一个不为 NULL 的值

```mysql
mysql> SELECT IFNULL(1,0);
        -> 1
mysql> SELECT IFNULL(NULL,10);
        -> 10
mysql> SELECT IFNULL(1/0,10);
        -> 10
mysql> SELECT IFNULL(1/0,'yes');
        -> 'yes'
```

##### `NULLIF()`

```mysql
mysql> SELECT NULLIF(1,1);
        -> NULL
mysql> SELECT NULLIF(1,2);
        -> 1
```

### 数学函数

```
ABS()    # 返回绝对值
CEIL()   # 向上取整,  同 CEILING()
FLOOR()  # 向下取整
ROUND()  # 四舍五入
TRUNCATE(2.33333, 1)  # 保留指定位数的小数
DIV      # 整除, SELECT 7 DIV 3; 返回 2
MOD(2, 3)   # 取余
POW(2, 3)   # 次方, 同 POWER(2, 3)
SQRT(4)     # 二次方根 4^(-2)

RAND()      # 随机返回一个 0-1 之间的浮点数
SIGN()


# 三角函数
ACOS()   # 返回 arc cosine 值, 类似 ASIN, ATAN
COS()    # 类似 SIN(), TAN(), COT()
PI()     # 返回 π 的值
RADIANS()


# 对数
EXP()
LN()    # 返回数值的自然对数
LOG()
LOG10()
LOG2()
```



### 日期和时间函数

##### 汇总

```
ADDDATE('2020-01-01', 5)   # 给一个日期增加一个天数间隔
	ADDDATE('2020-01-01', -1)   # 减一天
	ADDDATE('2020-01-01', INTERVAL 5 MONTH)  # 加 5 个月
ADDTIME('6:10:00', 3)      # 给一个时间 增加/减少 一个秒数间隔

CONVERT_TZ(日期时间, 时区1, 时区2)    # 从一个时区转到另一个时区

CURDATE()       # 返回当前日期字符串 (年-月-日), 同 CURRENT_DATE(), CURRENT_DATE
	SELECT CURDATE() + 0; ---> 20200510
CURTIME()       # 返回当前时间字符串 (时:分:秒), 同 CURRENT_TIME(), CURRENT_TIME
NOW()           # 返回当前日期时间, 同 CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP

DATE(日期/日期时间)	Extract the date part of a date or datetime expression
DATE_ADD()	Add time values (intervals) to a date value
	DATE_ADD(NOW(), INTERVAL 3 DAY)  # 3 天后
DATE_FORMAT()	Format date as specified
DATE_SUB()	Subtract a time value (interval) from a date
DATEDIFF()	Subtract two dates
DAY()	Synonym for DAYOFMONTH()
DAYNAME()	Return the name of the weekday
DAYOFMONTH()	Return the day of the month (0-31)
DAYOFWEEK()	Return the weekday index of the argument
DAYOFYEAR()	Return the day of the year (1-366)
EXTRACT()	Extract part of a date
FROM_DAYS()	Convert a day number to a date
FROM_UNIXTIME()	Format Unix timestamp as a date
GET_FORMAT()	Return a date format string
HOUR()	Extract the hour
LAST_DAY()	Return the last day of the month for the argument
LOCALTIME(), LOCALTIME	Synonym for NOW()
LOCALTIMESTAMP, LOCALTIMESTAMP()	Synonym for NOW()
MAKEDATE()	Create a date from the year and day of year
MAKETIME()	Create time from hour, minute, second
MICROSECOND()	Return the microseconds from argument
MINUTE()	Return the minute from the argument
MONTH()	Return the month from the date passed
MONTHNAME()	Return the name of the month
NOW()	Return the current date and time
PERIOD_ADD()	Add a period to a year-month
PERIOD_DIFF()	Return the number of months between periods
QUARTER()	Return the quarter from a date argument
SEC_TO_TIME()	Converts seconds to 'hh:mm:ss' format
SECOND()	Return the second (0-59)
STR_TO_DATE()	Convert a string to a date
SUBDATE()	Synonym for DATE_SUB() when invoked with three arguments
SUBTIME()	Subtract times
SYSDATE()	Return the time at which the function executes
TIME()	Extract the time portion of the expression passed
TIME_FORMAT()	Format as time
TIME_TO_SEC()	Return the argument converted to seconds
TIMEDIFF()	Subtract time
TIMESTAMP()	With a single argument, this function returns the date or datetime expression; with two arguments, the sum of the arguments
TIMESTAMPADD()	Add an interval to a datetime expression
TIMESTAMPDIFF()	Subtract an interval from a datetime expression
TO_DAYS()	Return the date argument converted to days
TO_SECONDS()	Return the date or datetime argument converted to seconds since Year 0
UNIX_TIMESTAMP()	Return a Unix timestamp
UTC_DATE()	Return the current UTC date
UTC_TIME()	Return the current UTC time
UTC_TIMESTAMP()	Return the current UTC date and time
WEEK()	Return the week number
WEEKDAY()	Return the weekday index
WEEKOFYEAR()	Return the calendar week of the date (1-53)
YEAR()	Return the year
YEARWEEK()	Return the year and week
```



##### ` DATEDIFF()`

> - ` TIMEDIFF()`
> - ` TIMESTAMPDIFF()`
> - `PERIOD_DIF()`

```mysql
mysql> SELECT DATEDIFF('2007-12-31 23:59:59','2007-12-30');
        -> 1
mysql> SELECT DATEDIFF('2010-11-30 23:59:59','2010-12-31');
        -> -31
```



##### `DATE_ADD(),DATE_SUB()`

```mysql
mysql> SELECT DATE_ADD('2018-05-01',INTERVAL 1 DAY);
        -> '2018-05-02'
mysql> SELECT DATE_SUB('2018-05-01',INTERVAL 1 YEAR);
        -> '2017-05-01'
mysql> SELECT DATE_ADD('2020-12-31 23:59:59',
    ->                 INTERVAL 1 SECOND);
        -> '2021-01-01 00:00:00'
mysql> SELECT DATE_ADD('2018-12-31 23:59:59',
    ->                 INTERVAL 1 DAY);
        -> '2019-01-01 23:59:59'
mysql> SELECT DATE_ADD('2100-12-31 23:59:59',
    ->                 INTERVAL '1:1' MINUTE_SECOND);
        -> '2101-01-01 00:01:00'
mysql> SELECT DATE_SUB('2025-01-01 00:00:00',
    ->                 INTERVAL '1 1:1:1' DAY_SECOND);
        -> '2024-12-30 22:58:59'
mysql> SELECT DATE_ADD('1900-01-01 00:00:00',
    ->                 INTERVAL '-1 10' DAY_HOUR);
        -> '1899-12-30 14:00:00'
mysql> SELECT DATE_SUB('1998-01-02', INTERVAL 31 DAY);
        -> '1997-12-02'
mysql> SELECT DATE_ADD('1992-12-31 23:59:59.000002',
    ->            INTERVAL '1.999999' SECOND_MICROSECOND);
        -> '1993-01-01 00:00:01.000001'
```





##### ` DATE_FORMAT()`

> - `STR_TO_DATE()`
> - `TIME_FORMAT()`
> - `UNIX_TIMESTAMP()`

| Specifier | Description                                                  |
| --------- | ------------------------------------------------------------ |
| `%a`      | Abbreviated weekday name (`Sun`..`Sat`)                      |
| `%b`      | Abbreviated month name (`Jan`..`Dec`)                        |
| `%c`      | Month, numeric (`0`..`12`)                                   |
| `%D`      | Day of the month with English suffix (`0th`, `1st`, `2nd`, `3rd`, …) |
| `%d`      | Day of the month, numeric (`00`..`31`)                       |
| `%e`      | Day of the month, numeric (`0`..`31`)                        |
| `%f`      | Microseconds (`000000`..`999999`)                            |
| `%H`      | Hour (`00`..`23`)                                            |
| `%h`      | Hour (`01`..`12`)                                            |
| `%I`      | Hour (`01`..`12`)                                            |
| `%i`      | Minutes, numeric (`00`..`59`)                                |
| `%j`      | Day of year (`001`..`366`)                                   |
| `%k`      | Hour (`0`..`23`)                                             |
| `%l`      | Hour (`1`..`12`)                                             |
| `%M`      | Month name (`January`..`December`)                           |
| `%m`      | Month, numeric (`00`..`12`)                                  |
| `%p`      | `AM` or `PM`                                                 |
| `%r`      | Time, 12-hour (*`hh:mm:ss`* followed by `AM` or `PM`)        |
| `%S`      | Seconds (`00`..`59`)                                         |
| `%s`      | Seconds (`00`..`59`)                                         |
| `%T`      | Time, 24-hour (*`hh:mm:ss`*)                                 |
| `%U`      | Week (`00`..`53`), where Sunday is the first day of the week; [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) mode 0 |
| `%u`      | Week (`00`..`53`), where Monday is the first day of the week; [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) mode 1 |
| `%V`      | Week (`01`..`53`), where Sunday is the first day of the week; [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) mode 2; used with `%X` |
| `%v`      | Week (`01`..`53`), where Monday is the first day of the week; [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) mode 3; used with `%x` |
| `%W`      | Weekday name (`Sunday`..`Saturday`)                          |
| `%w`      | Day of the week (`0`=Sunday..`6`=Saturday)                   |
| `%X`      | Year for the week where Sunday is the first day of the week, numeric, four digits; used with `%V` |
| `%x`      | Year for the week, where Monday is the first day of the week, numeric, four digits; used with `%v` |
| `%Y`      | Year, numeric, four digits                                   |
| `%y`      | Year, numeric (two digits)                                   |
| `%%`      | A literal `%` character                                      |
| `%*`x`*`  | *`x`*, for any “*`x`*” not listed above                      |

```mysql
mysql> SELECT DATE_FORMAT('2009-10-04 22:23:00', '%W %M %Y');
        -> 'Sunday October 2009'
mysql> SELECT DATE_FORMAT('2007-10-04 22:23:00', '%H:%i:%s');
        -> '22:23:00'
mysql> SELECT DATE_FORMAT('1900-10-04 22:23:00',
    ->                 '%D %y %a %d %m %b %j');
        -> '4th 00 Thu 04 10 Oct 277'
mysql> SELECT DATE_FORMAT('1997-10-04 22:23:00',
    ->                 '%H %k %I %r %T %S %w');
        -> '22 22 10 10:23:00 PM 22:23:00 00 6'
mysql> SELECT DATE_FORMAT('1999-01-01', '%X %V');
        -> '1998 52'
mysql> SELECT DATE_FORMAT('2006-06-00', '%d');
        -> '00'
```



##### `DAYOFxxx()`

- `DAYOFYEAR`   一年中的第几天  (1 ~ 366)
- `DAYOFMONTH`   一个月中的第几天  (1 ~ 31)
- `DAYOFWEEK`    一个星期中的第几天  (1 ~ 7)

##### `WEEKOFYEAR()`

返回一年中的第几周



##### ` LAST_DAY()`

返回一个月的最后一天



##### ` EXTRACT()`

```mysql
mysql> SELECT EXTRACT(YEAR FROM '2019-07-02');
        -> 2019
mysql> SELECT EXTRACT(YEAR_MONTH FROM '2019-07-02 01:02:03');
        -> 201907
mysql> SELECT EXTRACT(DAY_MINUTE FROM '2019-07-02 01:02:03');
        -> 20102
mysql> SELECT EXTRACT(MICROSECOND FROM '2003-01-02 10:30:00.000123');
        -> 123
```

有点类似于

```
# 提取一个 日期/时间/日期时间 中的指定部分
YEAR()
MONTH()
WEEK()
DAY()
HOUR()
MINUTE()
SECOND()
MICROSECOND()
TIME()
```



YEAR( )



##### ` GET_FORMAT()`

```mysql
GET_FORMAT(DATE,'USA')	'%m.%d.%Y'
GET_FORMAT(DATE,'JIS')	'%Y-%m-%d'
GET_FORMAT(DATE,'ISO')	'%Y-%m-%d'
GET_FORMAT(DATE,'EUR')	'%d.%m.%Y'
GET_FORMAT(DATE,'INTERNAL')	'%Y%m%d'
GET_FORMAT(DATETIME,'USA')	'%Y-%m-%d %H.%i.%s'
GET_FORMAT(DATETIME,'JIS')	'%Y-%m-%d %H:%i:%s'
GET_FORMAT(DATETIME,'ISO')	'%Y-%m-%d %H:%i:%s'
GET_FORMAT(DATETIME,'EUR')	'%Y-%m-%d %H.%i.%s'
GET_FORMAT(DATETIME,'INTERNAL')	'%Y%m%d%H%i%s'
GET_FORMAT(TIME,'USA')	'%h:%i:%s %p'
GET_FORMAT(TIME,'JIS')	'%H:%i:%s'
GET_FORMAT(TIME,'ISO')	'%H:%i:%s'
GET_FORMAT(TIME,'EUR')	'%H.%i.%s'
GET_FORMAT(TIME,'INTERNAL')	'%H%i%s'
```



##### ` STR_TO_DATE()`

```mysql
mysql> SELECT STR_TO_DATE('01,5,2013','%d,%m,%Y');
        -> '2013-05-01'
mysql> SELECT STR_TO_DATE('May 1, 2013','%M %d,%Y');
        -> '2013-05-01'
        
mysql> SELECT STR_TO_DATE('a09:30:17','a%h:%i:%s');
        -> '09:30:17'
mysql> SELECT STR_TO_DATE('a09:30:17','%h:%i:%s');
        -> NULL
mysql> SELECT STR_TO_DATE('09:30:17a','%h:%i:%s');
        -> '09:30:17'
        
mysql> SELECT STR_TO_DATE('abc','abc');
        -> '0000-00-00'
mysql> SELECT STR_TO_DATE('9','%m');
        -> '0000-09-00'
mysql> SELECT STR_TO_DATE('9','%s');
        -> '00:00:09'
        
mysql> SELECT STR_TO_DATE('00/00/0000', '%m/%d/%Y');
        -> '0000-00-00'
mysql> SELECT STR_TO_DATE('04/31/2004', '%m/%d/%Y');
        -> '2004-04-31'
```

更多转换见官网文档





### 字符串函数

```
CHAR_LENGTH(), CHARACTER_LENGTH()  # 返回字符串的长度
CONCAT()     # 将传入的参数作为字符串进行合并, 存在 NULL 时结果为 NULL
CONCAT_WS()  # 以指定内容将其他参数连接起来, CONCAT_WS('---', 1, 2, 3)

FROM_BASE64()  # 对 base64编码的字符串进行解码
TO_BASE64()

INSTR('abac', 'a')  # 返回子串第一次出现时的索引 (从 1 开始)
LOCATE('abac', 'a'), POSITION() # 返回子串第一次出现时的位置 (从 0 开始)

LCASE(), LOWER()
UCASE(), UPPER()

LIKE
REGEXP, NOT REGEXP, RLIKE

LOAD_FILE()

LEFT(str, num)   # 返回指定字符串左侧的 num 个字符
RIGHT(str, num)

LPAD()    # 在字符串的左侧填充内容, LPAD('hi',4,'??') -> '??hi'
RPAD()
LTRIM(), RTRIM(), TRIM()
REPEAT(str, num)
SPACE(num)  # 返回一个由指定个数空格组成的字符串
REPLACE()
REVERSE()
STRCMP()
SUBSTR()
```



##### `CONCAT(),CONCAT_WS()`

```mysql
mysql> SELECT CONCAT('My', 'S', 'QL');
        -> 'MySQL'
mysql> SELECT CONCAT('My', NULL, 'QL');
        -> NULL
mysql> SELECT CONCAT(14.3);
        -> '14.3'
        
mysql> SELECT CONCAT_WS(',','First name','Second name','Last Name');
        -> 'First name,Second name,Last Name'
mysql> SELECT CONCAT_WS(',','First name',NULL,'Last Name');
        -> 'First name,Last Name'
```



##### `RIGHT(),LEFT()`

```mysql
mysql> SELECT RIGHT('foobarbar', 4);
        -> 'rbar'
```

##### `RPAD(),LPAD()`

```mysql
mysql> SELECT RPAD('hi',5,'?');
        -> 'hi???'
mysql> SELECT RPAD('hi',1,'?');
        -> 'h'
```





##### `SUBSTR(),SUBSTRING()`

```mysql
mysql> SELECT SUBSTRING('Quadratically',5);
        -> 'ratically'
mysql> SELECT SUBSTRING('foobarbar' FROM 4);
        -> 'barbar'
mysql> SELECT SUBSTRING('Quadratically',5,6);
        -> 'ratica'
mysql> SELECT SUBSTRING('Sakila', -3);
        -> 'ila'
mysql> SELECT SUBSTRING('Sakila', -5, 3);
        -> 'aki'
mysql> SELECT SUBSTRING('Sakila' FROM -4 FOR 2);
        -> 'ki'
```



### 加密和压缩函数

```
# 一些
COMPRESS()	Return result as a binary string
MD5()	Calculate MD5 checksum
RANDOM_BYTES()	Return a random byte vector
SHA1(), SHA()	Calculate an SHA-1 160-bit checksum
SHA2()	Calculate an SHA-2 checksum
UNCOMPRESS()	Uncompress a string compressed
```



### 信息函数

```
CHARSET()	返回参数的字符集
CURRENT_USER()， CURRENT_USER	经过身份验证的用户名和主机名
DATABASE()	返回默认（当前）数据库名称, SCHEMA()
FOUND_ROWS()	对于带有LIMIT子句的SELECT，如果没有LIMIT子句，则将返回的行数
LAST_INSERT_ID()	最后一个INSERT的AUTOINCREMENT列的值
ROW_COUNT()	更新的行数
USER()	客户端提供的用户名和主机名, SESSION_USER(), SYSTEM_USER()
VERSION()	返回指示MySQL服务器版本的字符串
```



### JSON 函数

```
创建JSON值
搜索JSON值
修改JSON值
返回JSON值属性
```



```mysql
->	    评估路径后从JSON列返回值；等效于JSON_EXTRACT()
->>     评估路径并取消引用结果后，从JSON列返回值；等效于JSON_UNQUOTE(JSON_EXTRACT())
JSON_ARRAY()	创建JSON数组
JSON_ARRAY_APPEND()	将数据附加到JSON文档
JSON_ARRAY_INSERT()	插入JSON数组
JSON_CONTAINS()	    JSON文档是否在路径中包含特定对象
JSON_CONTAINS_PATH()	JSON文档是否在路径中包含任何数据
JSON_DEPTH()	JSON文档的最大深度
JSON_EXTRACT()	从JSON文档返回数据
JSON_INSERT()	将数据插入JSON文档
JSON_KEYS()	JSON文档中的键数组
JSON_LENGTH()	JSON文档中的元素数
JSON_MERGE_PATCH() 合并JSON文档，替换重复键的值
JSON_MERGE_PRESERVE() 合并JSON文档，保留重复的键
JSON_OBJECT()	创建JSON对象
JSON_PRETTY()   以易于阅读的格式打印JSON文档
JSON_QUOTE()	生成有效的 JSON 字符串,  CAST(val AS JSON)
JSON_REMOVE()	从JSON文档中删除数据
JSON_REPLACE()	替换JSON文档中的值
JSON_SEARCH()	JSON文档中值的路径
JSON_SET()	    将数据插入JSON文档
JSON_STORAGE_SIZE()  用于存储JSON文档的二进制表示形式的空间
JSON_TYPE()	    JSON值类型
JSON_UNQUOTE()	取消引用JSON值
JSON_VALID()	JSON值是否有效
```

##### `JSON_ARRAY()`

```mysql
mysql> SELECT JSON_ARRAY(1, "abc", NULL, TRUE, CURTIME());
# [1, "abc", null, true, "11:30:24.000000"] 
```

`JSON_OBJECT()`

```mysql
mysql> SELECT JSON_OBJECT('id', 87, 'name', 'carrot');
# {"id": 87, "name": "carrot"}
```

##### `JSON_QUOTE()`

```mysql
mysql> SELECT JSON_QUOTE('null'), JSON_QUOTE('"null"');
# "null", "\"null\""

mysql> SELECT JSON_QUOTE('[1, 2, 3]');
# "[1, 2, 3]"
```

##### `JSON_CONTAINS()`

```mysql
# JSON_CONTAINS(target, candidate[, path])

mysql> SET @j = '{"a": 1, "b": 2, "c": {"d": 4}}';
mysql> SET @j2 = '1';
mysql> SELECT JSON_CONTAINS(@j, @j2, '$.a');  # 1
mysql> SELECT JSON_CONTAINS(@j, @j2, '$.b');  # 0

mysql> SET @j2 = '{"d": 4}';
mysql> SELECT JSON_CONTAINS(@j, @j2, '$.a');  # 0
mysql> SELECT JSON_CONTAINS(@j, @j2, '$.c');  # 1
```

##### `JSON_CONTAINS_PATH()`

```mysql
# JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)

# 'one'：如果文档中至少存在一个路径，则为1，否则为0。
# 'all'：如果文档中存在所有路径，则为1，否则为0。

mysql> SET @j = '{"a": 1, "b": 2, "c": {"d": 4}}';
mysql> SELECT JSON_CONTAINS_PATH(@j, 'one', '$.a', '$.e');  # 1
mysql> SELECT JSON_CONTAINS_PATH(@j, 'all', '$.a', '$.e');  # 0
mysql> SELECT JSON_CONTAINS_PATH(@j, 'one', '$.c.d');  # 1
mysql> SELECT JSON_CONTAINS_PATH(@j, 'one', '$.a.d');  # 0
```

##### `JSON_EXTRACT()`

 从JSON文档中返回数据，该数据是从与*`path`* 参数匹配的文档部分中选择的 

```mysql
# JSON_EXTRACT(json_doc, path[, path] ...)

mysql> SELECT JSON_EXTRACT('[10, 20, [30, 40]]', '$[1]');  # 20
mysql> SELECT JSON_EXTRACT('[10, 20, [30, 40]]', '$[1]', '$[0]');  # [20, 10]
mysql> SELECT JSON_EXTRACT('[10, 20, [30, 40]]', '$[2][*]');  # [30, 40]
```

##### ` column->path`

在MySQL 5.7.9及更高版本中，与两个参数一起使用时，该 `->` 运算符充当 `JSON_EXTRACT()` 函数的别名 ，两个参数分别是左侧的列标识符和右侧的JSON路径（针对JSON文档进行评估）（列值）。您可以使用此类表达式代替SQL语句中出现的列标识符。 

```mysql
mysql> SELECT c, JSON_EXTRACT(c, "$.id"), g
     > FROM jemp
     > WHERE JSON_EXTRACT(c, "$.id") > 1
     > ORDER BY JSON_EXTRACT(c, "$.name");
+-------------------------------+-----------+------+
| c                             | c->"$.id" | g    |
+-------------------------------+-----------+------+
| {"id": "3", "name": "Barney"} | "3"       |    3 |
| {"id": "4", "name": "Betty"}  | "4"       |    4 |
| {"id": "2", "name": "Wilma"}  | "2"       |    2 |
+-------------------------------+-----------+------+

mysql> SELECT c, c->"$.id", g
     > FROM jemp
     > WHERE c->"$.id" > 1
     > ORDER BY c->"$.name";
+-------------------------------+-----------+------+
| c                             | c->"$.id" | g    |
+-------------------------------+-----------+------+
| {"id": "3", "name": "Barney"} | "3"       |    3 |
| {"id": "4", "name": "Betty"}  | "4"       |    4 |
| {"id": "2", "name": "Wilma"}  | "2"       |    2 |
+-------------------------------+-----------+------+
```

 此功能不限于 `SELECT` 

```mysql
mysql> ALTER TABLE jemp ADD COLUMN n INT;

mysql> UPDATE jemp SET n=1 WHERE c->"$.id" = "4";

mysql> SELECT c, c->"$.id", g, n
     > FROM jemp
     > WHERE JSON_EXTRACT(c, "$.id") > 1
     > ORDER BY c->"$.name";
+-------------------------------+-----------+------+------+
| c                             | c->"$.id" | g    | n    |
+-------------------------------+-----------+------+------+
| {"id": "3", "name": "Barney"} | "3"       |    3 | NULL |
| {"id": "4", "name": "Betty"}  | "4"       |    4 |    1 |
| {"id": "2", "name": "Wilma"}  | "2"       |    2 | NULL |
+-------------------------------+-----------+------+------+

mysql> DELETE FROM jemp WHERE c->"$.id" = "4";

mysql> SELECT c, c->"$.id", g, n
     > FROM jemp
     > WHERE JSON_EXTRACT(c, "$.id") > 1
     > ORDER BY c->"$.name";
+-------------------------------+-----------+------+------+
| c                             | c->"$.id" | g    | n    |
+-------------------------------+-----------+------+------+
| {"id": "3", "name": "Barney"} | "3"       |    3 | NULL |
| {"id": "2", "name": "Wilma"}  | "2"       |    2 | NULL |
+-------------------------------+-----------+------+------+
```

 也适用于JSON数组值 

```mysql
mysql> CREATE TABLE tj10 (a JSON, b INT);

mysql> INSERT INTO tj10
     > VALUES ("[3,10,5,17,44]", 33), ("[3,10,5,17,[22,44,66]]", 0);

mysql> SELECT a->"$[4]" FROM tj10;
+--------------+
| a->"$[4]"    |
+--------------+
| 44           |
| [22, 44, 66] |
+--------------+

mysql> SELECT * FROM tj10 WHERE a->"$[0]" = 3;
+------------------------------+------+
| a                            | b    |
+------------------------------+------+
| [3, 10, 5, 17, 44]           |   33 |
| [3, 10, 5, 17, [22, 44, 66]] |    0 |
+------------------------------+------+

mysql> SELECT * FROM tj10 WHERE a->"$[4][1]" IS NOT NULL;
+------------------------------+------+
| a                            | b    |
+------------------------------+------+
| [3, 10, 5, 17, [22, 44, 66]] |    0 |
+------------------------------+------+
```

##### `column->>path`

 给定一个 JSON 列值 *`column`*和一个路径表达式 *`path`*，以下三个表达式返回相同的值 

1. `JSON_UNQUOTE( JSON_EXTRACT(column, path) )`
2. `JSON_UNQUOTE(column -> path)`
3. `column->>path`

```mysql
mysql> SELECT * FROM jemp WHERE g > 2;
+-------------------------------+------+
| c                             | g    |
+-------------------------------+------+
| {"id": "3", "name": "Barney"} |    3 |
| {"id": "4", "name": "Betty"}  |    4 |
+-------------------------------+------+

mysql> SELECT c->'$.name' AS name
    ->     FROM jemp WHERE g > 2;
+----------+
| name     |
+----------+
| "Barney" |
| "Betty"  |
+----------+

mysql> SELECT JSON_UNQUOTE(c->'$.name') AS name
    ->     FROM jemp WHERE g > 2;
+--------+
| name   |
+--------+
| Barney |
| Betty  |
+--------+

mysql> SELECT c->>'$.name' AS name
    ->     FROM jemp WHERE g > 2;
+--------+
| name   |
+--------+
| Barney |
| Betty  |
+--------+

# 此运算符也可以与JSON数组一起使用
```

##### `JSON_KEYS()`

 从JSON对象的顶级值作为JSON数组返回键，或者，如果*`path`* 给定了参数，则从所选路径返回顶级键。 

```mysql
# JSON_KEYS(json_doc[, path])
```

##### `JSON_SEARCH()`

-  返回JSON文档中给定字符串的路径 
-  *`one_or_all`*参数影响搜索 
  - `'one'`：搜索在第一个匹配项后终止，并返回一个路径字符串。
  - `'all'`：搜索将返回所有匹配的路径字符串，因此不包括重复的路径。如果有多个字符串，它们将自动包装为一个数组。数组元素的顺序是不确定的。
- 匹配搜索:
  - 在*`search_str`*搜索字符串参数中，`%`和`_` 字符与 LIKE 运算符的作用相同：`%`匹配任意数量的字符（包括零个字符），并且 `_`恰好匹配一个字符。
  - 要在搜索字符串中指定文字`%`或 `_`字符，请在其前面加上转义字符。默认值是 `\`，如果 *`escape_char`*参数丢失或 `NULL`。否则， *`escape_char`*必须为空或一个字符的常量。

```mysql
# JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])

mysql> SET @j = '["abc", [{"k": "10"}, "def"], {"x":"abc"}, {"y":"bcd"}]';

mysql> SELECT JSON_SEARCH(@j, 'one', 'abc');
+-------------------------------+
| JSON_SEARCH(@j, 'one', 'abc') |
+-------------------------------+
| "$[0]"                        |
+-------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', 'abc');
+-------------------------------+
| JSON_SEARCH(@j, 'all', 'abc') |
+-------------------------------+
| ["$[0]", "$[2].x"]            |
+-------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', 'ghi');
+-------------------------------+
| JSON_SEARCH(@j, 'all', 'ghi') |
+-------------------------------+
| NULL                          |
+-------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10');
+------------------------------+
| JSON_SEARCH(@j, 'all', '10') |
+------------------------------+
| "$[1][0].k"                  |
+------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$');
+-----------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$') |
+-----------------------------------------+
| "$[1][0].k"                             |
+-----------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$[*]');
+--------------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$[*]') |
+--------------------------------------------+
| "$[1][0].k"                                |
+--------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$**.k');
+---------------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$**.k') |
+---------------------------------------------+
| "$[1][0].k"                                 |
+---------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$[*][0].k');
+-------------------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$[*][0].k') |
+-------------------------------------------------+
| "$[1][0].k"                                     |
+-------------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$[1]');
+--------------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$[1]') |
+--------------------------------------------+
| "$[1][0].k"                                |
+--------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '10', NULL, '$[1][0]');
+-----------------------------------------------+
| JSON_SEARCH(@j, 'all', '10', NULL, '$[1][0]') |
+-----------------------------------------------+
| "$[1][0].k"                                   |
+-----------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', 'abc', NULL, '$[2]');
+---------------------------------------------+
| JSON_SEARCH(@j, 'all', 'abc', NULL, '$[2]') |
+---------------------------------------------+
| "$[2].x"                                    |
+---------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%a%');
+-------------------------------+
| JSON_SEARCH(@j, 'all', '%a%') |
+-------------------------------+
| ["$[0]", "$[2].x"]            |
+-------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%');
+-------------------------------+
| JSON_SEARCH(@j, 'all', '%b%') |
+-------------------------------+
| ["$[0]", "$[2].x", "$[3].y"]  |
+-------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%', NULL, '$[0]');
+---------------------------------------------+
| JSON_SEARCH(@j, 'all', '%b%', NULL, '$[0]') |
+---------------------------------------------+
| "$[0]"                                      |
+---------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%', NULL, '$[2]');
+---------------------------------------------+
| JSON_SEARCH(@j, 'all', '%b%', NULL, '$[2]') |
+---------------------------------------------+
| "$[2].x"                                    |
+---------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%', NULL, '$[1]');
+---------------------------------------------+
| JSON_SEARCH(@j, 'all', '%b%', NULL, '$[1]') |
+---------------------------------------------+
| NULL                                        |
+---------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%', '', '$[1]');
+-------------------------------------------+
| JSON_SEARCH(@j, 'all', '%b%', '', '$[1]') |
+-------------------------------------------+
| NULL                                      |
+-------------------------------------------+

mysql> SELECT JSON_SEARCH(@j, 'all', '%b%', '', '$[3]');
+-------------------------------------------+
| JSON_SEARCH(@j, 'all', '%b%', '', '$[3]') |
+-------------------------------------------+
| "$[3].y"                                  |
+-------------------------------------------+
```



### 聚合（GROUP BY）

常用聚合函数

```
AVG()	返回参数的平均值
COUNT()	返回返回的行数的计数
COUNT(DISTINCT)	返回多个不同值的计数
GROUP_CONCAT()	返回串联的字符串
JSON_ARRAYAGG()  将结果集作为单个JSON数组返回
JSON_OBJECTAGG()  将结果集作为单个JSON对象返回
MAX()	最大值
MIN()	最小值
SUM()	总和
```

##### `AVG()`

```mysql
# AVG([DISTINCT] expr)
# 返回一组数据的平均值. 可以使用 DISTINCT 选项先将字段去重, 然后求平均

mysql> SELECT student_name, AVG(test_score)
       FROM student
       GROUP BY student_name;
```

##### `COUNT()`

- `COUNT(expr)`     
  - 返回由 语句检索的行中非`NULL` 值的数量的计数 
  - 注:  `COUNT(*)`  返回的计数会算上 非 `NULL` 值
- `COUNT(DISTINCT expr,[expr...])`

```mysql
mysql> SELECT student.student_name,COUNT(*)
       FROM student,course
       WHERE student.student_id=course.student_id
       GROUP BY student_name;

mysql> SELECT COUNT(DISTINCT results) FROM student;
```

##### `GROUP_CONCAT()`

```mysql
GROUP_CONCAT([DISTINCT] expr [,expr ...]
             [ORDER BY {unsigned_integer | col_name | expr}
                 [ASC | DESC] [,col_name ...]]
             [SEPARATOR str_val])
             
mysql> SELECT student_name,
         GROUP_CONCAT(test_score)
       FROM student
       GROUP BY student_name;
       
mysql> SELECT student_name,
         GROUP_CONCAT(DISTINCT test_score
                      ORDER BY test_score DESC SEPARATOR ' ')
       FROM student
       GROUP BY student_name;
```

##### `JSON_ARRAYAGG()`

```mysql
# JSON_ARRAYAGG(col_or_expr)
# 将结果集聚合为单个 JSON数组，其元素由行组成。

mysql> SELECT o_id, attribute, value FROM t3;
+------+-----------+-------+
| o_id | attribute | value |
+------+-----------+-------+
|    2 | color     | red   |
|    2 | fabric    | silk  |
|    3 | color     | green |
|    3 | shape     | square|
+------+-----------+-------+

mysql> SELECT o_id, JSON_ARRAYAGG(attribute) AS attributes
     > FROM t3 GROUP BY o_id;
+------+---------------------+
| o_id | attributes          |
+------+---------------------+
|    2 | ["color", "fabric"] |
|    3 | ["color", "shape"]  |
+------+---------------------+
```

##### `JSON_OBJECTAGG`

```mysql
# JSON_OBJECTAGG(key, value)
# 将两个列名或表达式作为参数，其中第一个用作键，第二个用作值，并返回包含键值对的JSON对象。

mysql> SELECT o_id, attribute, value FROM t3;
+------+-----------+-------+
| o_id | attribute | value |
+------+-----------+-------+
|    2 | color     | red   |
|    2 | fabric    | silk  |
|    3 | color     | green |
|    3 | shape     | square|
+------+-----------+-------+

mysql> SELECT o_id, JSON_OBJECTAGG(attribute, value) FROM t3 GROUP BY o_id;
+------+----------------------------------------+
| o_id | JSON_OBJECTAGG(attribute, name)        |
+------+----------------------------------------+
|    2 | {"color": "red", "fabric": "silk"}     |
|    3 | {"color": "green", "shape": "square"}  |
+------+----------------------------------------+
```



##### `MAX(), MIN()`

##### `SUM()`

```mysql
SUM([DISTINCT] expr)
```



### 其他函数

一些

```mysql
ANY_VALUE()	Suppress ONLY_FULL_GROUP_BY value rejection
DEFAULT()	Return the default value for a table column
SLEEP()	Sleep for a number of seconds
UUID()	Return a Universal Unique Identifier (UUID)
UUID_SHORT()	Return an integer-valued universal identifier
VALUES()	Define the values to be used during an INSERT
```





# 运算符

```
赋值运算:   := (赋值)
比较运算:   >   <   >=   <=   <>,!=   =   <=> (NULL-safe equal)
           BETWEEN ... AND ..., NOT BETWEEN ... AND ...
           IN(), NOT IN
           IS, IS NOT
           IS NULL, IS NOT NULL, ISNULL()
           LIKE, NOT LIKE
           REGXP, NOT REGXP
           RLIKE
           SOUNDS LIKE
           GREATEST(), LEAST()   # 最大值, 最小值.  select GREATEST(1, 2, 8);
           STRCMP()   # 比较两个 strings
           COALESCE()
           INTERVAL()
算术运算:   +   -   *   /   %,MOD
逻辑运算:   &&,AND   ||,OR    XOR   !,NOT
按位运算:   &   |   ~   ^   >>   <<

JSON运算:   ->    ->>

其他运算:   
            BINARY
            CASE
            DIV
```



### `BETWEEN ... AND ...`

> **注意:** 
>
> 1. 范围的上下限 **有顺序要求**,  **and 的左侧值必须小于等于右侧值**,  比较的结果才可能为 1
> 2. 比较时包含上下限的值,  既可以相等,  **但**仍然是 and 左侧的值必须小于右侧值, 才有可能返回 1
> 3. 相反:  NOT BETWEEN ... AND ...

```mysql
mysql> SELECT 2 BETWEEN 1 AND 3, 2 BETWEEN 3 and 1;
        -> 1, 0
mysql> SELECT 'b' BETWEEN 'a' AND 'c';
        -> 1
mysql> SELECT 2 BETWEEN 2 AND '3';
        -> 1
mysql> SELECT 2 BETWEEN 2 AND 'x-3';
        -> 0     # 此处结果为 0, 是因为 and 左侧的 2, 大于右侧的 'x-3', 拿任何值来比都是返回 0
```



### `COALESCE()`

返回列表中第一个 非 NULL 的值,  或当没有 NULL 时,  返回 NULL

```mysql
mysql> SELECT COALESCE(NULL, 5);
        -> 1
mysql> SELECT COALESCE(NULL, NULL, NULL);
        -> NULL
```

### `GREATEST()`

返回列表中最大值

> 相反:  LEAST()
>
> 注:  NULL 永远是最小的

```mysql
mysql> SELECT GREATEST(2,0);
        -> 2
mysql> SELECT GREATEST(34.0,3.0,5.0,767.0);
        -> 767.0
mysql> SELECT GREATEST('B','A','C');
        -> 'C'
```

### `IN`

> IN 指向的列表中的值个数 由  [`max_allowed_packet`](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_max_allowed_packet)   配置
>
> 相反:  NOT IN

```mysql
mysql> SELECT 2 IN (0,3,5,7);
        -> 0
mysql> SELECT 'wefwf' IN ('wee','wefwf','weg');
        -> 1
        
mysql> SELECT (3,4) IN ((1,2), (3,4));
        -> 1
        
# 应该避免在 IN 指向的列表中混合写入 带引号 和 不带引号的数值, 避免出现不可预知的错误
mysql> SELECT 'a' IN (0), 0 IN ('b');
        -> 1, 1   # 'a'会被转为 0.0,  'b' 会被转为 0.0
SELECT val1 FROM tbl1 WHERE val1 IN ('1','2','a');
```



### `IS`

测试一个值的布尔值,   布尔值可以是  `TRUE`, `FALSE`, or `UNKNOWN`.

> 类似:  IS NOT,  IS NULL,  IS NOT NULL,  ISNULL()
>
> 注意:  对于 DATE、DATETIME 类型的 '0000-00-00'  属于 NULL

```sql
mysql> SELECT 1 IS TRUE, 0 IS FALSE, NULL IS UNKNOWN;
        -> 1, 1, 1
        
mysql> SELECT 1 IS NULL, 0 IS NULL, NULL IS NULL;
        -> 0, 0, 1
        
SELECT * FROM tbl_name WHERE date_column IS NULL

mysql> SELECT ISNULL(1/0);
        -> 1
        
mysql> SELECT -10 IS TRUE;
-> 1
```





### `AND, NOT, OR, XOR`

不同于 python 中的逻辑运算,   mysql 的逻辑运算只会返回 1 或 0

XOR:  两个值一真一假 则返回 1



### `:=`

赋值运算,  用于定义变量时赋值

```mysql
mysql> SELECT @var1, @var2;
        -> NULL, NULL
mysql> SELECT @var1 := 1, @var2;
        -> 1, NULL
mysql> SELECT @var1, @var2;
        -> 1, NULL
mysql> SELECT @var1, @var2 := @var1;
        -> 1, 1

mysql> SELECT @var1:=COUNT(*) FROM t1;
        -> 4
mysql> SELECT @var1;
        -> 4
```

可以不紧接着 select 使用 `:=`

```mysql
mysql> SELECT * FROM t1;
        -> 1, 3, 5, 7

mysql> UPDATE t1 SET c1 = 2 WHERE c1 = @var1:= 1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT @var1;
        -> 1
mysql> SELECT * FROM t1;
        -> 2, 3, 5, 7
```

