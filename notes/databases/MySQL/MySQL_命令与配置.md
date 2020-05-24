# mysql 系列命令/插件

更多见官网:  https://dev.mysql.com/doc/refman/5.7/en/programs.html



### 客户端

```shell
# 客户端
$ mysql — The MySQL Command-Line Client
$ mysqladmin — Client for Administering a MySQL Server
$ mysqlcheck — A Table Maintenance Program
$ mysqldump — A Database Backup Program
$ mysqlimport — A Data Import Program
$ mysqlpump — A Database Backup Program
$ mysqlshow — Display Database, Table, and Column Information
	# mysqlshow blog auth_user %user%
$ mysqlslap — Load Emulation Client
```

### 服务端

```bash
# 服务端
$ mysqld       # MySQL 服务, 主程序
$ mysqld_safe  # 服务启动脚本 (Unix)
$ mysql.server # 服务启动脚本 (Unix)
$ mysqld_multi # 管理多个 mysql 服务 (Unix)
```

mysqld 程序在启动时有非常多的选项,  可以通过以下命令查看

```bash
$ mysqld --verbose --help
```

`mysqld_safe` 是 Unix 上推荐使用的服务启动命令,  因为 `mysqld_safe` 增加一些安全特性,  例如发生错误时重启服务,  并记录运行信息到错误日志中.

`mysqld_safe`  程序会从配置文件的 `[mysqld]`, `[server]`, 和 `[mysqld_safe]` 部分读取配置

```ini
[mysqld]
log-error=error.log
```



### mysql>  输入框命令

```mysql
help   # 遇事不决, help 解决
help create  # 查看 create 命令帮助
help create table

help contents  # 查看服务端的命令帮助

# help 支持模糊查询
help %user%    # 查看包含 `user` 字符串的命令帮助
help %function%


# 一些常用的:
# 取消这一行已输入的内容, 可以在行尾输入 \c, 再回车
# 执行一个 .sql 文件的内容
source xx.sql
# 运行一个当前系统的命令 (仅支持 Unix)
system ls
# 切换数据库
use db_name
```



# 选项/配置

配置项包括:

- 命令行连接服务端时的选项
- 命令行连接服务端时指定的配置文件
- mysql 服务运行时的配置

### 配置文件的路径

通过执行 mysql 系列命令加 --help 可以找到关于配置文件的说明,  如

```bash
$ mysql --help
```

返回信息中关于配置文件的说明,  举例如下:

```
Default options are read from the following files in the given order:
C:\Windows\my.ini 
C:\Windows\my.cnf 
C:\my.ini 
C:\my.cnf 
C:\Program Files (x86)\MySQL\MySQL Server 5.5\my.ini 
C:\Program Files (x86)\MySQL\MySQL Server 5.5\my.cnf
```

如果一个 mysql 程序启动时指定了 ` --no-defaults `,  那么不会读取除了 ` .mylogin.cnf `  文件之外的其他配置文件.



### 配置文件的类型

有两种内容类型的配置

1. 纯文本格式的配置文件
2. 由 [**mysql_config_editor**](https://dev.mysql.com/doc/refman/5.7/en/mysql-config-editor.html) 加密的配置文件:  ` .mylogin.cnf `,  由 `--login-path` 选项指定它的路径



### 配置加载顺序

##### Windows 上

| File Name                            | Purpose                                                      |
| ------------------------------------ | ------------------------------------------------------------ |
| `%WINDIR%\my.ini`, `%WINDIR%\my.cnf` | Global options                                               |
| `C:\my.ini`, `C:\my.cnf`             | Global options                                               |
| `BASEDIR\my.ini`, `BASEDIR\my.cnf`   | Global options                                               |
| `defaults-extra-file`                | The file specified with [`--defaults-extra-file`](https://dev.mysql.com/doc/refman/5.7/en/option-file-options.html#option_general_defaults-extra-file) |
| `%APPDATA%\MySQL\.mylogin.cnf`       | Login path options (clients only)                            |

```bash
> echo %WINDIR%
C:\Windows

> echo %APPDATA%
C:\Users\Administrator\AppData\Roaming
```





##### Unix 上

| File Name             | Purpose                                                      |
| --------------------- | ------------------------------------------------------------ |
| `/etc/my.cnf`         | Global options                                               |
| `/etc/mysql/my.cnf`   | Global options                                               |
| `SYSCONFDIR/my.cnf`   | Global options                                               |
| `$MYSQL_HOME/my.cnf`  | Server-specific options (server only)                        |
| `defaults-extra-file` | The file specified with [`--defaults-extra-file `](https://dev.mysql.com/doc/refman/5.7/en/option-file-options.html#option_general_defaults-extra-file) |
| `~/.my.cnf`           | User-specific options                                        |
| `~/.mylogin.cnf`      | User-specific login path options (clients only)              |





### 配置文件的语法

纯文本配置文件的语法:

```ini
# 注释内容
; 注释内容

[group]

opt_name  # 与命令行指定 --opt_name 一致

opt_name=value  # 与命令行指定 --opt_name=value 一致
```

一个典型的全局配置文件例子:

```ini
[client]
port=3306
socket=/tmp/mysql.sock

[mysqld]     # 配置 mysqld 命令的选项, mysqld 是服务端命令
port=3306
socket=/tmp/mysql.sock
key_buffer_size=16M
max_allowed_packet=8M

[mysqldump]  # 配置 mysqldump 命令的选项
quick
```

一个典型的用户配置文件:

```ini
[client]
# The following password will be sent to all standard MySQL clients
password="my password"

[mysql]
no-auto-rehash
connect_timeout=2

prompt=(\\u@\\h) [\\d]>\\_   # 修改客户端的命令行提示符
# prompt="\\r:\\m:\\s> "     # `hh:mm:ss> `

[mysqld-5.7]  # 配置 mysqld-5.7 版本 mysqld 命令的选项
sql_mode=TRADITIONAL
```



##### 配置文件包含

在一个配置文件中,  可以包含另一个配置文件

```ini
# 包含另一个配置文件
!include /home/mydir/myopt.cnf

# 包含一个配置目录
# windows 上, 会去 mydir 下找 .init / .conf 文件
# unix 上, 会去 mydir 下找 .conf 文件
!includedir /home/mydir  
```



