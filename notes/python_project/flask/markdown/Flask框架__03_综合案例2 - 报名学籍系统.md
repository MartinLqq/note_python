# 综合案例 - 报名学籍系统

> 前后端不分离

> 使用  一对多 和 多对多 的表关联,  创建外键 -便捷属性 -反向引用

> 使用 flask_wtf 表单和  html原生表单, 分别使用各自表单数据的获取方式

> 使用cookie进行会话状态保持

# 表模型

表的关联：

	Admin 班主任 (管理员)
	Student 学生
	MyClass 班级
	
	班级 ——1对1—— 学生
	班级 ——多对多—— 管理员




# 主程序 main.py

```python
from flask import Flask, render_template, flash, redirect, url_for, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length
# import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/sign_up_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "lqq"

db = SQLAlchemy(app)

# todo  班级 ————多对多———— 管理员
tb_MyClass_Admin = db.Table("myclass_admin",
                            # 添加外键
                            db.Column("cls_id", db.Integer, db.ForeignKey("classes.id")),
                            db.Column("admin_id", db.Integer, db.ForeignKey("admins.id"))
                            )


class MyClass(db.Model):
    __tablename__ = "classes"
    # id，name，is_delete
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    is_delete = db.Column(db.Boolean(create_constraint=True), default=0)

    # 给班级添加属性 使 <班级> 与 <学生> 互相直接获取信息
    get_stu = db.relationship("Student", backref="get_class", lazy="dynamic")

    # 给班级添加属性  使 <班级> 与 <管理员> 互相直接获取信息
    get_admin = db.relationship('Admin', secondary=tb_MyClass_Admin,
                                backref=db.backref('get_cls', lazy='dynamic'),
                                lazy='dynamic')

    # def __repr__(self):
    #     return "MyClass %s-%s" % (self.id, self.name)


class Admin(db.Model):
    # id，name，password，phone，is_delete

    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16), default="123456")
    phone = db.Column(db.String(11), unique=True)
    is_delete = db.Column(db.Boolean(create_constraint=True), default=0)

    # 添加 <班级id> 的外键
    # cls_id = db.Column(db.Integer, db.ForeignKey(MyClass.id))

    def __repr__(self):
        return "Admin %d-%s" % (self.id, self.name)


class Student(db.Model):
    # id，name，gender，age，phone，subject，cls_id，is_delete
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    age = db.Column(db.SmallInteger)
    phone = db.Column(db.String(11), unique=True)
    # -----改----删除学生表的subject字段
    # subject = db.Column(db.String(64))
    is_delete = db.Column(db.Boolean(create_constraint=True), default=False)

    # 添加 <班级id> 的外键
    cls_id = db.Column(db.Integer, db.ForeignKey(MyClass.id))

    def __repr__(self):
        return "Stu %d-%s-%s" % (self.id, self.name, self.subject)


class StuForm(FlaskForm):
    """自定义添加学生的表单"""
    stu_name = StringField("姓名: ",
                           validators=[InputRequired("请输入姓名")],
                           render_kw={"placeholder": "请输入学生姓名"})
    gender = StringField("性别: ",
                         validators=[InputRequired("请输入性别")],
                         render_kw={"placeholder": "请输入性别"})
    age = StringField("年龄: ",
                      validators=[InputRequired("请输入年龄")],
                      render_kw={"placeholder": "请输入年龄"})
    phone = StringField("电话: ",
                        validators=[InputRequired("请输入手机号")],
                        render_kw={"placeholder": "请输入手机号"})
    class_name = StringField("班级: ",
                             validators=[InputRequired("请输入班级")],
                             render_kw={"placeholder": "请输入班级"})
    # ----改----
    # subject_name = StringField("学科: ",
    #                            validators=[InputRequired("请输入学科")],
    #                            render_kw={"placeholder": "请输入学科"})
    submit = SubmitField("提交")


class RegisterForm(FlaskForm):
    name = StringField("姓名: ",
                       validators=[InputRequired("请输入姓名")],
                       render_kw={"placeholder": "请输入姓名"})
    class_name = StringField("班级: ",
                             validators=[InputRequired("请输入班级")],
                             render_kw={"placeholder": "请输入班级"})
    phone = StringField("手机号: ",
                        validators=[InputRequired("请输入手机号")],
                        render_kw={"placeholder": "请输入手机号"})
    password1 = PasswordField("密码: ",
                              validators=[InputRequired("请输入密码")],
                              render_kw={"placeholder": "请输入密码"})
    password2 = PasswordField("确认密码: ",
                              validators=[InputRequired("请输入确认密码"),
                                          EqualTo("password1", "两次密码不一致")],
                              render_kw={"placeholder": "请输入确认密码"})
    submit = SubmitField("注册")


@app.route("/delete_data/<student_id>")
def delete_data(student_id):
    stu = None
    try:
        stu = Student.query.get(student_id)
    except Exception as ret:
        print(ret)
        flash("查询错误！")
    if not stu:
        """学生不存在, 不可以删除"""
        return "没有该学生, 无法删除！"
    try:
        """学生存在, 删除学生"""
        stu.is_delete = 1
        # ----改---- 取消物理删除
        # db.session.delete(stu)
        db.session.commit()
    except Exception as ret:
        print(ret)
        db.session.rollback()
        return "删除失败！"

    # 删除成功, 则重定向到主页
    return redirect(url_for("admin_detail"))


@app.route("/submit_changed_data", methods=["POST", "GET"])
def submit_changed_data():
    if request.method == "POST":
        form = request.form
        stu_id = form.get("id")
        name = form.get("name")
        gender = form.get("gender")
        age = form.get("age")
        phone = form.get("phone")
        # subject = form.get("subject")
        cls_name = form.get("cls_name")

        if not all([name, gender, age, phone, cls_name]):
            flash("填写不完整!")
            return render_template(url_for("submit_changed_data"))

        # 更新数据到数据库
        my_class = MyClass.query.filter(MyClass.name == cls_name).first()
        if my_class:
            try:
                stu = Student.query.filter(Student.id == stu_id).first()
                stu.name = name
                stu.gender = gender
                stu.age = age
                stu.phone = phone
                # stu.subject = subject
                stu.cls_id = my_class.id
                # ----姓名不能重复----
                query_obj = Student.query.filter(Student.name == name)
                if len(query_obj.all()) > 1:
                    db.session.rollback()
                    return "学生姓名已存在"
                db.session.commit()
            except Exception as e:
                print(e)
                return "修改失败!"
        else:
            # 管理员没有发布过此班级
            return "没有此班级, 请重新输入!"
    return redirect(url_for("admin_detail"))


@app.route("/change_data/<stu_id>", methods=["POST", "GET"])
def change_data(stu_id):
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for("admin_login"))

    # 当请求方式为 POST时, 获取表单内容
    if request.method == "POST":
        form = request.form
        stu_id = form.get("id")
        name = form.get("name")
        gender = form.get("gender")
        age = form.get("age")
        phone = form.get("phone")
        subject = form.get("subject")
        cls_name = form.get("cls_name")

        if not all([name, gender, age, phone, subject, cls_name]):
            return "填写不完整!"
        # 添加数据到数据库
        my_class = MyClass.query.filter(MyClass.name == cls_name).first()
        # ----改----增加is_delete判断
        # if my_class:
        if my_class and (not my_class.is_delete):
            try:
                stu = Student.query.filter(Student.id == stu_id).first()
                stu.name = name
                stu.gender = gender
                stu.age = age
                stu.phone = phone
                stu.subject = subject
                stu.cls_id = my_class.id
                db.session.add(stu)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "修改失败"
        else:
            # 管理员没有发布过此班级
            return "没有此班级, 请重新输入!"

        # 修改成功后, 返回学生和班级信息页面
        return redirect(url_for("admin_detail"))

    # 当请求方式为GET时, 显示修改学生信息的页面
    student = Student.query.get(stu_id)
    return render_template("/change_data.html", student=student)


@app.route("/add_class", methods=["GET", "POST"])
def add_class():
    form = request.form
    cls_name = form.get("cls_name")
    subject = form.get("subject")

    print("------>%s<-------" % subject)

    if not all([cls_name, subject]):
        return "参数不足"
    my_class = MyClass.query.filter(MyClass.name == cls_name).first()
    if my_class and (not my_class.is_delete):
        flash("班级名称已存在")
    else:
        try:
            my_class = MyClass(name=cls_name, subject=subject)
            db.session.add(my_class)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return "添加失败"
    return redirect(url_for("admin_detail"))


@app.route("/change_class/<cls_id>", methods=["POST", "GET"])
def change_class(cls_id):
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for('admin_login'))

    # 当请求方式为 POST时, 获取表单内容
    if request.method == "POST":
        form = request.form
        cls_id = form.get("id")
        subject = form.get("subject")
        admin_list = form.getlist("admin_list")
        my_class = MyClass.query.filter(MyClass.id == cls_id).first()

        li = list()
        for admin_name in admin_list:
            admin = Admin.query.filter(Admin.name == admin_name).first()
            li.append(admin)
        try:
            cls_name = form.get("name")
            print("--------->班级名称:%s<---------" % cls_name)

            # 如果获取到班级name为空字符串"", 表示要删除这个班级
            if cls_name == "":
                print("------1-------")
                # 删除此班级id对应的所有学生
                student_list = Student.query.filter(Student.cls_id == cls_id).all()
                for student in student_list:
                    # db.session.delete(student)
                    student.is_delete = 1
                # 删除班级表中此班级id (与管理员id的对应关系也就不存在)
                # db.session.delete(my_class)
                my_class.is_delete = 1
                db.session.commit()

            # 获取到了班级名称
            else:
                print("------2-------")
                my_class.get_admin = li
                my_class.name = cls_name
                my_class.subject = subject
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return "修改班级失败!"

        # 修改成功, 返回学生和班级信息页面
        return redirect(url_for("admin_detail"))

    # 当请求方式为GET时, 显示修改班级的页面
    cls = MyClass.query.filter(MyClass.id == cls_id).first()
    admins = Admin.query.all()
    return render_template("/change_class.html", cls=cls, admins=admins)


@app.route("/baoming", methods=["POST", "GET"])
def baoming():
    student_form = StuForm()
    if student_form.validate_on_submit():
        # 1 提取表单数据
        stu_name = student_form.stu_name.data
        gender = student_form.gender.data
        age = student_form.age.data
        phone = student_form.phone.data
        cls_name = student_form.class_name.data
        # 学生表没有 subject
        # sub_name = student_form.subject_name.data

        # print(stu_name, gender, age, phone, cls_name, sub_name)

        # 2 添加数据到数据库
        # 由管理员发布班级, 学生填写本信息, 如果没有一致的班级名称, 提示没有这个班级, 且不能添加学生信息
        my_class = MyClass.query.filter(MyClass.name == cls_name).first()
        if my_class:
            # 查询是否有此学生
            stu = Student.query.filter(Student.name == stu_name).first()
            if stu:
                return "您的信息已经添加, 请不要再添加!"
            else:
                try:
                    stu = Student(name=stu_name, gender=gender, age=age, phone=phone,
                                  cls_id=my_class.id)
                    db.session.add(stu)
                    db.session.commit()
                except Exception as ret:
                    print(ret)
                    db.session.rollback()
                    flash("添加失败!")
                return "报名成功, 欢迎 %s 加入传智播客学习!" % stu_name
        else:
            # 管理员没有发布过此班级
            return "没有此班级, 请重新输入!"
    else:
        if request.method == "POST":
            flash("参数错误!")
    return render_template("baoming.html", form=student_form)


@app.route("/", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        # 取到表单中提交上来的参数
        username = request.form.get("username")
        password = request.form.get("password")

        if not all([username, password]):
            # 向前端界面弹出一条提示(闪现消息)
            flash("参数不足")
        else:
            have_ad_name = Admin.query.filter(Admin.name == username).first()
            if not have_ad_name:
                return "用户名错误!"

            have_pwd = Admin.query.filter(Admin.name == username).first()
            if not (have_pwd and have_pwd.password == password):
                return "密码错误!"

            # 状态保持，设置用户名到cookie中表示登录成功
            response = redirect(url_for('admin_detail'))
            response.set_cookie('username', username)
            return response

    return render_template('adminlogin.html')


@app.route('/admin_detail', methods=["POST", "GET"])
def admin_detail():
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for("admin_login"))

    # todo ------- send tag -------
    # 获取数据库所有班级的对象, 传入模板, 用于对应html的 form表单(select的第一项)
    all_class = MyClass.query.all()

    # 判断请求方式是否是POST
    if request.method == "POST":
        # 获取表单 form 提交的内容
        get_dict = request.form.to_dict()
        opt = get_dict["opt"]
        # 获取班级列表
        classes = MyClass.query.all()
        for a_class in classes:
            if opt == a_class.name:
                show_class = MyClass.query.filter(MyClass.name == opt).first()
                # 查询对象还可以连续用过滤器
                show_students = Student.query.filter(Student.cls_id == show_class.id)
                show_students = show_students.filter(Student.is_delete == 0)

                return render_template("admindetail.html",
                                       # form=student_form,
                                       students=show_students,
                                       # 这里传过去的show_class必须是可迭代的对象, 如列表
                                       classes=[show_class],
                                       # todo ------- get tag -------
                                       all_class=all_class,
                                       opt=opt)
        else:
            # 运行到这里, 说明 opt=="--所有班级--"
            # pass, 不return任何值, 与下方GET请求的代码合用
            pass

    # 请求方式为GET
    # ----改----根据is_delete决定学生/班级是否显示
    # students = Student.query.all()
    students = Student.query.filter(Student.is_delete == 0).all()
    # classes = MyClass.query.all()
    classes = MyClass.query.filter(MyClass.is_delete == 0).all()
    return render_template("admindetail.html",
                           # form=student_form,
                           students=students,
                           classes=classes,
                           all_class=all_class)


@app.route("/admin_register", methods=["POST", "GET"])
def admin_register():
    register_form = RegisterForm()
    if not request.method == "POST":
        return render_template("adminregister.html", register_form=register_form)

    register_data = request.form
    name = register_data.get("name")
    cls_name = register_data.get("class_name")
    phone = register_data.get("phone")
    pwd1 = register_data.get("password1")
    pwd2 = register_data.get("password2")
    if Admin.query.filter(Admin.name == name).first():
        flash("该用户名已经注册, 请登录")
        return render_template("adminregister.html", register_form=register_form)

    elif pwd1 != pwd2:
        flash("两次密码不一致!")
        return render_template("adminregister.html", register_form=register_form)

    elif Admin.query.filter(Admin.phone == phone).first():
        flash("该手机号已被注册, 请输入正确的手机号")
        return render_template("adminregister.html", register_form=register_form)

    my_class = MyClass.query.filter(MyClass.name == cls_name).first()
    if not my_class:
        return "此班级不存在!"
    try:
        admin = Admin(name=name, password=pwd1, phone=phone)
        my_class.get_admin.append(admin)
        db.session.add_all([admin])
        db.session.commit()

        # 注册成功, 转到登录界面
        return redirect(url_for("admin_login"))

    except Exception as e:
        print(e)
        db.session.rollback()
        return "注册失败!"


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 添加测试数据
    # 表的关联：    班级 ————1对1———— 学生
    #             班级 ————多对多———— 管理员

    # 数据添加顺序： 先有班级————>管理员(用到cls_id)  学生(用到cls_id)

    # 班级: id，name，is_delete
    my_class1 = MyClass(name="python一期", subject="python人工智能")
    my_class2 = MyClass(name="python二期", subject="python全栈")
    db.session.add_all([my_class1, my_class2])
    db.session.commit()

    # 管理员: id，name，password，phone，is_delete
    admin1 = Admin(name="星悦", password="111111", phone="15607021342")
    admin2 = Admin(name="徐韬", password="111111", phone="18745301231")
    admin3 = Admin(name="赵四", password="444444", phone="19898989898")

    # 班级1 由管理员1来管理
    my_class1.get_admin = [admin1]
    # 班级2 由管理员2 和 管理员3 来管理
    my_class2.get_admin = [admin2, admin3]

    db.session.add_all([admin1, admin2, admin3])
    db.session.commit()

    # 学生:  id，name，gender，age，phone，subject，cls_id，is_delete
    stu1 = Student(name="白离厌", gender="男", age=20, phone="110", cls_id=1)
    stu2 = Student(name="孙青竹", gender="女", age=18, phone="10086", cls_id=1)
    stu3 = Student(name="洛亦枫", gender="女", age=19, phone="10010", cls_id=2)
    stu4 = Student(name="凡雨琪", gender="男", age=21, phone="120", cls_id=2)
    db.session.add_all([stu1, stu2, stu3, stu4])
    db.session.commit()

    app.run(debug=True)
```



# 模板目录 templates

## 学生报名 baoming.py

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>学生端</title>
</head>
<body>
<div class="baoming_frame">
    <h3>学生报名登记</h3>
  
    {% include 'temp_form.html' %}<br>
  
    {{ get_flashed_messages()[0] }}
</div>
</body>
</html>
```



### 报名表单模板 temp_form.html

```html
<form method="POST">
    {{ form.csrf_token() }}<br>
    {{ form.stu_name.label }}{{ form.stu_name }}<br>
    {{ form.gender.label }}{{ form.gender }}<br>
    {{ form.age.label }}{{ form.age }}<br>
    {{ form.phone.label }}{{ form.phone }}<br>
    {{ form.class_name.label }}{{ form.class_name }}<br>
{#    {{ form.subject_name.label }}{{ form.subject_name }}<br>#}
    {{ form.submit }}<br>
</form>
```

## 管理员登录 adminlogin.html

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>管理员登录</title>
</head>
<body>
<h2>管理员登录</h2>

<form method="post">
    <label>用户名：</label><input type="text" name="username" placeholder="请输入用户名"><br/>
    <label>密码：</label><input type="password" name="password" placeholder="请输入密码"><br/>
    <input type="submit" value="登录"><br>
    {% for msg in get_flashed_messages() %}
        {{ msg }}
    {% endfor %}
</form>

</body>
</html>
```



## 管理员注册 admingregister.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>register</title>
</head>
<body>
    <h2>管理员注册</h2>
    <form method="POST">
        {{ register_form.name.label }}{{ register_form.name }}<br>
        {{ register_form.class_name.label }}{{ register_form.class_name }}<br>
        {{ register_form.phone.label }}{{ register_form.phone }}<br>
        {{ register_form.password1.label }}{{ register_form.password1 }}<br>
        {{ register_form.password2.label }}{{ register_form.password2 }}<br><br>
        {{ register_form.submit }} &nbsp;&nbsp;
        <a href="/">登录</a> <br><br>

        {% for msg in get_flashed_messages() %}
        {{ msg }}
        {% endfor %}
    </form>
</body>
</html>
```



## 学生和班级详情 admindetail.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>报名系统——管理员</title>
    <style>
        table {
            width: 666px;
            height: 66px;
            text-align: center;
            border-collapse: collapse;
        }
        td,th {
            border: 1px solid lightseagreen;
        }
        th {
            height: 32px;
        }
        select {
            height: 25px;
        }
    </style>
</head>
<body>

{#  学生信息  #}
    <table>
        <aption><h3>学生信息</h3></aption>
    <tr>

{#        <th>学号</th>#}
        <th>姓名</th>
        <th>性别</th>
        <th>年龄</th>
        <th>手机号</th>
        <th>
            <form action="/admin_detail" method="post">
                <select name="opt">

                        <option> --所有班级-- </option>

                    {#    提取all_class的班级名称, 组成下拉表单     #}
                    {% for cls in all_class %}
                        <option>{{ cls.name }}</option>
                    {% endfor %}
                    <input id="sub" type="submit" value="选择" >
                </select>
            </form>
        </th>
        <th>学科</th>
        <th>操作</th>
    </tr>

    {% for stu in students %}
    <tr>
{#        <td>{{ stu.id }}</td>#}
        <td>{{ stu.name }}</td>
        <td>{{ stu.gender }}</td>
        <td>{{ stu.age }}</td>
        <td>{{ stu.phone }}</td>
        <td>{{ stu.get_class.name }}</td>
        <td>{{ stu.get_class.subject }}</td>
        <td>
            <a href="/change_data/{{ stu.id }}">修改</a>
            <a href="/delete_data/{{ stu.id }}">删除</a>
        </td>
    </tr>
    {% endfor %}
    </table>
    <hr>
    <h3>班级信息</h3>
    <table>
        <tr>
            <th>序号</th>
            <th>班级名称</th>
            <th>管理员</th>
            <th>学科</th>
            <th>学生人数</th>
            <th>操作</th>
        </tr>

        {% for cls in classes %}
        <tr>
            <td>{{ cls.id }}</td>
            <td>{{ cls.name }}</td>
            <td>
                {%  for admin in cls.get_admin.all() %}
                    {{ admin.name }}&nbsp;&nbsp;
                    {% endfor %}
            </td>
            {#    -----------------------    #}
            <td>{{ cls.subject }}</td>
            <td>{{ cls.get_stu.count() }}</td>
            <td>
{#                <a href="#">修改</a>#}
                <a href="/change_class/{{ cls.id }}">修改</a>
            </td>
        </tr>
        {% endfor %}
    </table><br>
    <hr>
    <h4>发布新班级:</h4>
    <form action="/add_class" method="post">
        <label>班级:<input type="text" name="cls_name" placeholder="请输入班级名称"></label>

        {% for msg in get_flashed_messages() %}
            {{ msg }}
        {% endfor %}

        <br>
        <label>学科:<input type="text" name="subject" placeholder="请输入学科名称"></label><br>
        <input type="submit" value="提交"><br>
    </form>
    <br><br><br><br><br><br><br>
</body>
</html>
```



## 修改学生信息 change_data.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>修改学生信息</title>
</head>
<body>
<h3>修改学生信息</h3>
<form action="/submit_changed_data" method="post">

    <input type="hidden" name="id" value="{{ student.id }}">

    <label>姓名: <input type="text" name="name" value="{{ student.name }}"></label><br>
    <label>性别: <input type="text" name="gender" value="{{ student.gender }}"></label><br>
    <label>年龄: <input type="text" name="age" value="{{ student.age }}"></label><br>
    <label>电话: <input type="text" name="phone" value="{{ student.phone }}"></label><br>
{#    <label>学科: <input type="text" name="subject" value="{{ student.get_class.subject }}"></label><br>#}
    <label>班级: <input type="text" name="cls_name" value="{{ student.get_class.name }}"></label><br>
    <input type="submit" value="提交"><br>
</form>

</body>
</html>
```



## 修改班级信息 change_class.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>修改班级信息</title>
</head>
<body>
<h3>修改班级信息</h3>
<form action="/change_class/{{ cls.id }}" method="post">

    <input type="hidden" name="id" value="{{ cls.id }}">
    <label>班级: <input type="text" name="name" value="{{ cls.name }}"></label><br>
    <label>学科: <input type="text" name="subject" value="{{ cls.subject }}"></label><br>
    选择管理员:
    {% for admin in admins %}
            {#  todo ----------  #}
            {% if admin in cls.get_admin.all() %}
                {#        添加默认选项        #}
                <input type="checkbox" name="admin_list" value="{{ admin.name }}" checked="checked">{{ admin.name }}
            {% else %}
                <input type="checkbox" name="admin_list" value="{{ admin.name }}">{{ admin.name }}
            {% endif %}

    {% endfor %}<br>

    <input type="submit" value="提交">&nbsp;&nbsp;
        {% for msg in get_flashed_messages() %}
        {{ msg }}
        {% endfor %}

</form>
</body>
</html>
```























