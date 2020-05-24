from flask import Flask, jsonify, redirect, url_for, abort, request, make_response, session, render_template, \
    render_template_string
from flask_script import Manager
from flask.ctx import copy_current_request_context, after_this_request
from flask_wtf import FlaskForm, CSRFProtect
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.secret_key = 'something_secret'
# app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 10  # 测试 CSRF 过期时间
CSRFProtect(app)


@app.route('/', methods=['GET'])
def index():
    print(app.url_map)
    print(app.config)
    print(app.default_config)

    # ======== ctx.py::after_this_request ========
    @after_this_request
    def add_header(response):
        response.headers['X-Foo'] = 'Parachute'
        return response
    return 'Hello Index.'


# ========= jinja env =========
app.context_processor(lambda: {'my_var2': 'my_var2 value'})
app.context_processor(lambda: {'my_func2': lambda : 'Hello my_func2'})
@app.template_global()
def double(num):  # {{ double(100) }}
    return 2 * num


# ========= app.errorhandler =========
@app.errorhandler(404)
def not_found_error(e):
    return 'not_found_error'

# ========= 请求钩子 =========
@app.before_first_request
def step_0(): print('@app.before_first_request')
@app.before_request
def step_1(): print('@app.before_request')
@app.after_request
def step_2(response):
    print('@app.after_request. response=%s' % response)
    return response
@app.teardown_request
def step_3(exc):
    if exc is not None:
        print('Error occured: %s' % exc)
    print('@app.teardown_request. exc=%s' % exc)


@app.route('/json', methods=['GET'])
def json():
    return jsonify({'a': 3, 'b': 4}, c=5)

@app.route('/to/<url>', methods=['GET'])
def redirect_to(url):
    # return redirect('https://' + url)
    return redirect(url_for('foo'))


# ========= cookie & session ==========
@app.route('/login', methods=['POST'])
def login_cookie():

    user = request.form.get('user')
    passwd = request.form.get('password')
    info = {'Martin': '123456', 'John': '112233'}
    if user in info and passwd == info[user]:
        # 登录成功
        res = make_response('登录成功')
        res.set_cookie('user', user)
    else:
        # 登录失败
        res = '登录失败'
    return res

@app.route('/login/session', methods=['POST'])
def login_session():
    session['user'] = 'Martin'
    return 'Success'

# ========== multi_threads_out_of_ctx ========
@app.route('/multi_threads')
def multi_threads_out_of_ctx():
    @copy_current_request_context
    def background_task():
        import time
        time.sleep(10)
        print(request.method)

    from threading import Thread
    th = Thread(target=background_task)
    th.start()
    th.join()
    return 'multi_threads done'



# ======== CombinedMultiDict ======
@app.route('/register', methods=['POST'])
def register():
    print(request.json)
    form = RegisterForm(CombinedMultiDict([MultiDict(request.json)]))
    if form.validate():
        return jsonify({'code': 2000, 'message': '校验通过, 执行注册...'})
    print(form.errors)
    return jsonify({'error_code': 4000, 'error_msg': form.errors})

class RegisterForm(FlaskForm):
    username = StringField("用户名：", validators=[DataRequired("请输入用户名")])
    password = PasswordField("密码：", validators=[DataRequired("请输入密码")])
    password2 = PasswordField("确认密码：", validators=[DataRequired("请输入确认密码"), EqualTo("password", "两次密码不一致")])
    # submit = SubmitField("注册")


# ========= jinja env =========
@app.route('/jinja2')
def jinja2():
    app.jinja_env.globals['my_var'] = 'hahaha'
    app.jinja_env.globals['my_func'] = lambda: 'Hello my_func'

    return render_template('temp.html')


# ========= CSRF =========
@app.route('/csrf', methods=['GET', 'POST'])
def csrf_get():
    if request.method.upper() == 'GET':
        form = "<input hidden name='csrf_token' value='{{ csrf_token() }}'>"
        return render_template_string(form)
    elif request.method.upper() == 'POST':
        # 获取加盐加密前的 哈希值
        print(session.get('csrf_token'))
        return 'csrf_token validates success!'
    else:
        return 'My Page Not Found!', 404


# ======= class Module(Blueprint) ======
from views import admin, news
app.register_module(admin, url_prefix='/admin')
app.register_module(news, url_prefix='/news')
# print(app.url_map)


# ======== MethodView ========
from views.method_view import MyView
app.add_url_rule('/method_view', view_func=MyView.as_view('method_view'))
print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
