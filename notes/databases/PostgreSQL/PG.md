# PostgreSQL

# PG 中文社区

 http://www.postgres.cn/v2/document 

# docker 运行 PG

```
docker pull postgres
docker run --name my_postgres -v dv_pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=123456 -p 5432:5432 -d postgres:latest
```

# 基本操作

### 连接数据库

接入PostgreSQL数据库: 

```bash
$ psql -h IP地址 -p 端口 -U 数据库名
```

之后会要求输入数据库密码

### 访问数据库

1. 列举数据库：\l
2. 选择数据库：\c 数据库名
3. 查看该某个库中的所有表：\dt
4. 切换数据库：\c interface
5. 查看某个库中的某个表结构：\d 表名
6. 查看某个库中某个表的记录：select * from apps limit 1;
7. 显示字符集：\encoding
8. 退出psgl：\q





