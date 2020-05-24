# DDL

- 文档:   https://dev.mysql.com/doc/refman/5.7/en/sql-data-definition-statements.html 
- 帮助   `help XXX`

```
ALTER
    ALTER DATABASE
    ALTER EVENT
    ALTER FUNCTION
    ALTER INSTANCE
    ALTER LOGFILE GROUP
    ALTER PROCEDURE
    ALTER SERVER
    * ALTER TABLE
    ALTER TABLESPACE
    ALTER VIEW
CREATE
    * CREATE DATABASE
    CREATE EVENT
    CREATE FUNCTION
    CREATE INDEX
    CREATE LOGFILE GROUP
    CREATE PROCEDURE和CREATE FUNCTION
    CREATE SERVER
    * CREATE TABLE
    CREATE TABLESPACE
    CREATE TRIGGER
    CREATE VIEW
DROP
    DROP DATABASE
    DROP EVENT
    DROP FUNCTION
    DROP INDEX
    DROP LOGFILE GROUP
    DROP PROCEDURE, DROP FUNCTION
    DROP SERVER
    * DROP TABLE
    DROP TABLESPACE
    DROP TRIGGER
    DROP VIEW
RENAME
	RENAME TABLE
TRUNCATE
	TRUNCATE TABLE
```

# DML, DQL

- 文档:  https://dev.mysql.com/doc/refman/5.7/en/sql-data-manipulation-statements.html

```
    CALL
    * DELETE    用于从表中删除行
    HANDLER
    DO
    * INSERT
    LOAD DATA
    LOAD XML
    * SELECT  (DQL)
    REPLACE
    * 子查询   (DQL)
    * UPDATE
```



### `SELECT`

```mysql
SELECT
    [ALL | DISTINCT | DISTINCTROW ]
    [HIGH_PRIORITY]
    [STRAIGHT_JOIN]
    [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
    [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
    select_expr [, select_expr] ...
    [into_option]
    [FROM table_references
      [PARTITION partition_list]]
    [WHERE where_condition]
    [GROUP BY {col_name | expr | position}
      [ASC | DESC], ... [WITH ROLLUP]]
    [HAVING where_condition]
    [ORDER BY {col_name | expr | position}
      [ASC | DESC], ...]
    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
    [PROCEDURE procedure_name(argument_list)]
    [into_option]
    [FOR UPDATE | LOCK IN SHARE MODE]

into_option: {
    INTO OUTFILE 'file_name'
        [CHARACTER SET charset_name]
        export_options
  | INTO DUMPFILE 'file_name'
  | INTO var_name [, var_name] ...
}
```





# TPL