from sqlalchemy import Column, String, Integer
from test_sqlalchemy_without_flask.db import DB

url = 'mysql+pymysql://root:123456@localhost:3306/web_flask'
db = DB(url)


class Role(db.Model):
    __tablename__ = 'roles'  # 表名

    # 表结构
    id = Column(Integer, primary_key=True)
    role = Column(String(50), unique=True)

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.id, self.role)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return "<User %d %s %s>" % (self.id, self.username, self.email)


if __name__ == '__main__':
    # db.session.drop_all()
    # db.session.create_all()

    # role = Role(role='学生')
    # db.session.add(role)
    # db.session.commit()

    roles = db.session.query(Role).all()
    # 注: 没有实现 Role.query.xxx
    print(roles)

    db.session.close()
