import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DB:

    def __init__(self, url, auto_commit=False, **kwargs):
        if '?charset' not in url:  # 解决一个中文bug
            url += '?charset=utf8'
        # 初始化数据库连接
        self.__engine = create_engine(url, **kwargs)
        # 创建 Session 类
        self.__session_factory = sessionmaker(bind=self.__engine, autocommit=auto_commit)
        self.session = self.__session_factory()
        self.Model = declarative_base(
            # cls=object,
            name='Model',
            # metadata=None,
            # metaclass=DeclarativeMeta
        )

        self._compact()
        _include_sqlalchemy(self)

    def _compact(self):
        self.session.create_all = self.create_all
        self.session.drop_all = self.drop_all

    def create_all(self):
        self.Model.metadata.create_all(self.__engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.__engine)


def _include_sqlalchemy(obj):
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))

