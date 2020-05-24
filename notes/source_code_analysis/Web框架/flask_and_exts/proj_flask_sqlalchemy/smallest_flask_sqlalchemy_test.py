from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost:3306/web_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
"""
create table user(
  id int unsigned not null auto_increment primary key,
  username varchar(30),
  email varchar(100)
)
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return "<User %d %s %s>" % (self.id, self.username, self.email)


# 创建表
db.create_all()

name = "Flask"
query_obj = User.query.filter(User.username == name)
print(query_obj)
if not query_obj.first():  # 不存在
    user = User(username=name, email="example@example.com")
    # 增
    db.session.add(user)
db.session.commit()

# 查
users = User.query.all()
print(users)
