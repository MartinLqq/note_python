db_url_formats = dict(

    # 使用 pymysql 进行连接
    mysql='mysql+pymysql://{username}:{password}@{server}/{dbname}',

    # 使用 psycopg2 进行连接
    postgresql='postgresql://{username}:{passwrod}@{server}/{dbname}',
)


def connect(db, *args, **kwargs):
    try:
        db_url = db_url_formats[db.lower()].format(
            username=kwargs['username'],
            password=kwargs['password'],
            server=kwargs['server'],
            dbname=kwargs['db'],
        )
    except KeyError:
        print('do sth.')
        raise
    return db_url
