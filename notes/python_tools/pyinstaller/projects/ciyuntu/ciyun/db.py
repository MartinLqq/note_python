from sys import exit as sys_exit
from msvcrt import getch, putch
from pymysql import connect, MySQLError

CONFIGS = dict(
    host='localhost',
    user='root',
    password='jian19980501',
    database='renming',
    table='renming_data',
    table_created=False
)


def update_config():
    global CONFIGS
    CONFIGS.update(
        host=input('数据库地址(默认%s): ' % CONFIGS['host']) or CONFIGS['host'],
        user=input('数据库用户名(默认%s): ' % CONFIGS['user']) or CONFIGS['user'],
        # password=input('数据库密码(默认%s): ' % CONFIGS['password']) or CONFIGS['password'],
    )
    enter_password()


def enter_password():
    global CONFIGS
    print('数据库密码(默认%s): ' % CONFIGS['password'], end='', flush=True)
    li = list()
    while 1:
        char = getch()
        if char == b'\r':
            # 回车
            putch(b'\n')
            CONFIGS['password'] = b''.join(li).decode() or CONFIGS['password']
            break

        elif char == b'\x08':
            # 退格
            if li:
                li.pop()
                putch(b'\b')
                putch(b' ')
                putch(b'\b')
        elif char == b'\x1b':
            # Esc
            print('Bye.')
            sys_exit(0)
        else:
            li.append(char)
            putch(b'*')


class Connection:
    """Database API."""
    __connection = None

    def __init__(self):
        self.database = CONFIGS['database']
        self.table = CONFIGS['table']
        if self.__connection is None:
            try:
                self.db = connect(
                    host=CONFIGS['host'],
                    user=CONFIGS['user'],
                    password=CONFIGS['password'],
                    # database=""
                )
            except MySQLError as error:
                print('数据库连接失败. ', error)
                sys_exit(1)

            self.cursor = self.db.cursor()
            if not CONFIGS['table_created']:
                self.create_table()
        self.cursor.execute("use %s;" % self.database)

    def create_table(self):
        self.cursor.execute("drop database if exists `%s`;" % self.database)
        self.cursor.execute("create database `%s`;" % self.database)
        # create table
        self.cursor.execute("use %s;" % self.database)
        self.cursor.execute(
            """create table %s (
                `id` int unsigned auto_increment,
                `title` varchar(1000) not null,
                `content` varchar(10000),
                primary key (`id`)
            ) default charset=UTF8MB4;""" % self.table
        )
        global CONFIGS
        CONFIGS['table_created'] = True

    def insert(self, title, content=""):
        sql = """insert into {table}
            (title, content)
            values
            ('{title}', '{content}');
            """.format(table=self.table, title=title, content=content)
        self.cursor.execute(sql)
        self.db.commit()

    def query(self):
        sql = 'select title from %s' % self.table
        self.cursor.execute(sql)
        words_list = []
        for item in self.cursor.fetchall():
            words_list.append(item[0])
        return words_list

    def close(self):
        self.__connection = None
        self.cursor.close()
        self.db.close()
