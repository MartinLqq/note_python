# 综合案例 - 图书管理

- WTF表单
- 数据库操作
- 一对多关系演练



# 1 基本流程

## 1.1 定义模型

模型表示程序使用的数据实体，在Flask-SQLAlchemy中，模型一般是Python类，继承自db.Model，db是SQLAlchemy类的实例，代表程序使用的数据库。

<1> 创建表

​	authors表,  books表

<2> 添加测试数据



## 1.2 数据显示&表单添加

<1> 数据显示

- 定义路由函数，并将 Author 和 Book 的所有结果传到模板
- 模板文件



<2> 表单添加

- 定义表单类
- 通过render_template()传入至模版中
- 模板中写对应代码实现表单



<3> 表单验证

- 实例化FlaskForm表单对象
- 判断是否提交表单:  表单对象名.validate_on_submit()
- 重新编写html文件展示列表书籍
- 在form标签下添加 flash 消息的显示



## 1.3 删除数据

<1> 定义删除author和book的路由

<2> 在模版中添加删除的 a 标签链接



# 2 代码实现

## 2.1 .py文件

```python
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/my_flask_test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

app.config["SECRET_KEY"] = "affagg"

db = SQLAlchemy(app)


# 创建表单类
class AddBookForm(FlaskForm):
    """自定义添加书籍的表单"""
    author = StringField("作者",
                         validators=[InputRequired("请输入作者")],
                         render_kw={"placeholder": "请输入作者"})
    book = StringField("书名",
                       validators=[InputRequired("请输入书名")],
                       render_kw={"placeholder": "请输入书名"})
    submit = SubmitField("添加")


# 定义模型类 Author------一的一方
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 定义属性, 使Author模型可以直接通过该属性获取 书
    # backref 给 Book 添加一个author属性, 可以通过book.author获取书所对应的作者
    books = db.relationship("Book", backref="author")

    def __repr__(self):
        return self.name


# 定义模型类 Book------多的一方
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 给books表添加外键
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))

    def __repr__(self):
        return self.name


@app.route("/delete_author/<author_id>")
def delete_author(author_id):
    """删除作者 以及作者所有书籍"""

    # 提取 author_id
    author = None
    try:
        author = Author.query.get(author_id)
    except Exception as ret:
        print(ret)
        flash("查询错误！")
    if not author:
        """作者不存在, 不可以删除"""
        return "没有 %s 的信息, 无法删除！" % author
    try:
        """作者存在, 先删除 作者对应的书籍, 再删除作者"""
        # Query对象.delete()
        Book.query.filter(Book.author_id == author_id).delete()
        db.session.delete(author)
        db.session.commit()
    except Exception as ret:
        print(ret)
        db.session.rollback()
        return "删除失败！"

    # 删除成功, 则重定向到主页
    return redirect(url_for("index"))


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    """删除书籍"""

    # 提取 book_id
    book = None
    try:
        book = Book.query.get(book_id)
    except Exception as ret:
        print(ret)
        flash("查询错误！")
    if not book:
        """书籍不存在, 不可以删除"""
        return "没有《%s》这本书, 无法删除！" % book
    try:
        """书籍存在, 删除书籍"""
        db.session.delete(book)
        db.session.commit()
    except Exception as ret:
        print(ret)
        db.session.rollback()
        return "删除失败！"

    # 删除成功, 则重定向到主页
    return redirect(url_for("index"))


@app.route('/', methods=["GET", "POST"])
def index():
    """返回首页"""
    # 创建表单对象, 后面传入渲染模板中
    book_form = AddBookForm()

    # ———————————————————— 添加数据到数据库 start ————————————————————
    # 如果book_form可以被提交
    if book_form.validate_on_submit():
        # 1 提取表单数据
        # author_name = request.form.get("author")
        # book_name = request.form.get("book")
        author_name = book_form.author.data
        book_name = book_form.book.data

        # 2 添加数据到数据库
        # 查找是否有作者名
        # 如果不存在, 则添加作者名, 再添加书籍; 如果作者存在, 直接添加书籍
        author = Author.query.filter(Author.name == author_name).first()
        if not author:
            try:
                # 初始化Author模型对象 -- 添加作者名
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()

                # 添加书籍
                book = Book(name=book_name, author_id=author.id)
                db.session.add(book)
                db.session.commit()
            except Exception as ret:
                db.session.rollback()
                print(ret)
                flash("添加失败！")

        else:
            # 判断书籍是否存在, 不存在则直接添加
            book = Book.query.filter(Book.name == book_name).first()
            if not book:
                try:
                    # 添加书籍
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as ret:
                    db.session.rollback()
                    print(ret)
                    flash("添加失败！")
            else:
                return "《%s》已存在!" % book_name

    else:
        if request.method == "POST":
            flash("参数错误!")
    # ————————————————————————— end —————————————————————————————

    # 查询数据
    authors = Author.query.all()
    # 渲染模板
    return render_template("index.html", form=book_form, authors=authors)


if __name__ == '__main__':

    # db.drop_all()
    # db.create_all()
    #
    # # 添加测试数据
    #
    # # 生成数据
    # au1 = Author(name='老王')
    # au2 = Author(name='老尹')
    # au3 = Author(name='老刘')
    # # 把数据提交给用户会话
    # db.session.add_all([au1, au2, au3])
    # # 提交会话
    # db.session.commit()
    #
    # bk1 = Book(name='老王回忆录', author_id=au1.id)
    # bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    # bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    # bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    # bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # # 把数据提交给用户会话
    # db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # # 提交会话
    # db.session.commit()

    app.run(debug=True)
```





## 2.2 templates目录下的.html文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>图书管理</title>
</head>
<body>
    <h1>图书管理</h1>

    {# 注意设置表单提交方式: post #}
    <form method="post">
        {{ form.csrf_token() }}<br>
        {{ form.author.label }}{{ form.author }}
        {{ form.book.label }}{{ form.book }}
        {{ form.submit }}

        {% for msg in get_flashed_messages() %}
        {{ msg }} <br>
        {% endfor %}

    </form>

    <hr>
    <ul>
        {% for author in authors %}

        <li>{{ author }} &nbsp;&nbsp;<a href="/delete_author/{{ author.id }}">删除作者</a> </li>
            <ul>
                {% for book in author.books %}
                    <li>{{ book.name }} &nbsp;&nbsp;<a href="/delete_book/{{ book.id }}">删除书籍</a> </li>
                {% endfor %}
            </ul>
            <br>

        {% endfor %}
    </ul>

</body>
</html>
```



