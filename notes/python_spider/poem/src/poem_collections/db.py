import pymysql

from .config import DBConfig


class DBClient:

    def __init__(self, **kwargs):
        self._host = kwargs.get('host', DBConfig.HOST)
        self._port = kwargs.get('port', DBConfig.PORT)
        self._user = kwargs.get('user', DBConfig.USER)
        self._password = kwargs.get('password', DBConfig.PASSWORD)
        self._db_name = kwargs.get('db_name', DBConfig.DB_NAME)
        self._conn = self._get_conn()
        self._cursor = self._get_cursor()

    def _get_conn(self):
        return pymysql.connect(
            host=self._host,
            port=self._port,
            database=self._db_name,
            user=self._user,
            password=self._password,
            charset='utf8',
        )

    def _get_cursor(self):
        return self._conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql):
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        self._conn.commit()
        return result

    def exec(self, sql):
        result = self._cursor.execute(sql)
        return result

    def close(self):
        self._cursor.close()
        self._conn.close()
