# ==== flas_wtf ====

# form.py

## FlaskForm

- 继承自 wtforms.form.Form

```python
class FlaskForm(Form):
    """
    If ``formdata`` is not specified, this will use :attr:`flask.request.form`
    and :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to
    prevent this.
    """
    # 重写父类 Form 的类属性 Meta, 原Meta=DefaultMeta
    class Meta(DefaultMeta):
        # csrf_class 重写为 flask_wtf 的 _FlaskFormCSRF
        csrf_class = _FlaskFormCSRF
        csrf_context = session  # not used, provided for custom csrf_class

        @cached_property
        def csrf(self):
            return current_app.config.get('WTF_CSRF_ENABLED', True)

        @cached_property
        def csrf_secret(self):
            return current_app.config.get(
                'WTF_CSRF_SECRET_KEY', current_app.secret_key
            )

        @cached_property
        def csrf_field_name(self):
            return current_app.config.get('WTF_CSRF_FIELD_NAME', 'csrf_token')

        # 获取 csrf_token 过期时间
        @cached_property
        def csrf_time_limit(self):
            return current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)
		
        # 重写 Meta 的 wrap_formdata 方法
        def wrap_formdata(self, form, formdata):
            if formdata is _Auto:
                if _is_submitted():
                    if request.files:
                        return CombinedMultiDict((request.files, request.form))
                    elif request.form:
                        return request.form
                    elif request.get_json():
                        return ImmutableMultiDict(request.get_json())
                return None
            return formdata
	
    	# 重写 Meta 的 get_translations 方法
        def get_translations(self, form):
            if not current_app.config.get('WTF_I18N_ENABLED', True):
                return None
            return translations

    def __init__(self, formdata=_Auto, **kwargs):
        pass

    def is_submitted(self):
        return _is_submitted()

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()

    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.
        """
	    pass
```

## _is_submitted

```python
def _is_submitted():
    """判断是否是表单提交. 结合两个条件判断:
    	1. bool(request) 为True
    	2. 当前请求方式属于 SUBMIT_METHODS 列表中的一个.
    	SUBMIT_METHODS = set(('POST', 'PUT', 'PATCH', 'DELETE'))
    """
    return bool(request) and request.method in SUBMIT_METHODS
```

# csrf.py

## CSRFProtect

用于自动进行 CSRF 校验

```python
class CSRFProtect(object):
    """开启 flask app 全局 CSRF 保护.
	用法:
        app = Flask(__name__)
        csrf = CsrfProtect(app)
	
	前端请求时携带 csrf_token 的两种途径:
        a.通过一个隐藏表单携带, name为`csrf_token`;
        b.通过请求头 `X-CSRFToken`
    
    渲染模板时获取csrf_token的方式:
    	`{{ csrf_token() }}`
    """

    def __init__(self, app=None):
        self._exempt_views = set()  # 记录豁免视图, 这些视图不需要 CSRF 保护
        self._exempt_blueprints = set()  # 记录豁免蓝图, 这些篮图下的视图不需要 CSRF 保护
        if app:
            self.init_app(app)

    def init_app(self, app):
        # 1. 向 flask app 注册一个扩展, flask.Flask中指明了 key 如何取名:
        """
        The key must match the name of the `flaskext` module.  For example in
        case of a "Flask-Foo" extension in `flaskext.foo`, the key would be
        ``'foo'``.
        但是下面这个貌似不符合key的命名...  这是 flask_wtf.
        """
        app.extensions['csrf'] = self

        # 2. 使用 app.config.setdefault() 方式定义了一些默认配置项, 如:
        # WTF_CSRF_ENABLED, WTF_CSRF_METHODS, WTF_CSRF_FIELD_NAME, WTF_CSRF_HEADERS,
        # WTF_CSRF_TIME_LIMIT, ...
        # ... 此处请看源码 
		
        # 3.向模板那上下文中注入变量/方法, 有两种方法:
        # 向 jinja2 模板引擎中加入 csrf_token 的全局变量, generate_csrf是一个函数, 用于生成 csrf_token值
        app.jinja_env.globals['csrf_token'] = generate_csrf
        # 向模板上下文中注入一个变量或方法,
        # app.context_processor 一般作为装饰器使用, 被装饰函数需要返回一个字典, 最终变量或方法名就是其key.
        app.context_processor(lambda: {'csrf_token': generate_csrf})
        # 源码这里为什么使用 app.context_processor 重复注入 csrf_token 方法 ??
		
        # 添加请求钩子, 在处理每次请求之前校验 csrf_token
        @app.before_request
        def csrf_protect():
            if not app.config['WTF_CSRF_ENABLED']:
                return
            if not app.config['WTF_CSRF_CHECK_DEFAULT']:
                return
            if request.method not in app.config['WTF_CSRF_METHODS']:
                return
            if not request.endpoint:
                return
			
            # 获取当前请求上下文对应的的视图函数
            view = app.view_functions.get(request.endpoint)
            if not view:
                return
			# 过滤豁免蓝图
            if request.blueprint in self._exempt_blueprints:
                return
			# 过滤豁免视图
            dest = '%s.%s' % (view.__module__, view.__name__)
            if dest in self._exempt_views:
                return

            self.protect()

    def _get_csrf_token(self):
        # find the ``csrf_token`` field in the subitted form
        # if the form had a prefix, the name will be
        # ``{prefix}-csrf_token``
        
        # a.尝试从form表单中获取 csrf_token
        field_name = current_app.config['WTF_CSRF_FIELD_NAME']
        for key in request.form:
            if key.endswith(field_name):
                csrf_token = request.form[key]
                if csrf_token:
                    return csrf_token
    	# a.从请求头中获取 csrf_token
        for header_name in current_app.config['WTF_CSRF_HEADERS']:
            csrf_token = request.headers.get(header_name)
            if csrf_token:
                return csrf_token
        return None

    def protect(self):
        # 一些请求方式不需要进行 CSRF 保护
        if request.method not in current_app.config['WTF_CSRF_METHODS']:
            return

        try:
            # 调用 validate_csrf 函数校验 csrf_token
            validate_csrf(self._get_csrf_token())
        except ValidationError as e:
            logger.info(e.args[0])
            self._error_response(e.args[0])

        if request.is_secure and current_app.config['WTF_CSRF_SSL_STRICT']:
            if not request.referrer:
                self._error_response('The referrer header is missing.')

            good_referrer = 'https://{0}/'.format(request.host)
		
            # same_origin是一个简单函数，用于判断两个URL是否是同一个源，即：
            # scheme相同 & hostname相同 & port相同
            if not same_origin(request.referrer, good_referrer):
                self._error_response('The referrer does not match the host.')
		
        # 标记该请求为 CSRF 合法
        g.csrf_valid = True

    def exempt(self, view):
        """标记一个视图或蓝图不进行 CSRF 保护
		用法1：
            @app.route('/some-view', methods=['POST'])
            @csrf.exempt
            def some_view(): ...
		用法2：
            bp = Blueprint(...)
            csrf.exempt(bp)
        """
        if isinstance(view, Blueprint):
            self._exempt_blueprints.add(view.name)
            return view

        if isinstance(view, string_types):
            view_location = view
        else:
            view_location = '%s.%s' % (view.__module__, view.__name__)

        self._exempt_views.add(view_location)
        # 返回被装饰的视图函数
        return view

    def _error_response(self, reason):
        raise CSRFError(reason)

    # 下面这个方法不要用， 应使用 @app.errorhandler(CSRFError)
    def error_handler(self, view):
        """Register a function that will generate the response for CSRF errors.
        """
        warnings.warn(FlaskWTFDeprecationWarning(
            '"@csrf.error_handler" is deprecated. Use the standard Flask error '
            'system with "@app.errorhandler(CSRFError)" instead. This will be'
            'removed in 1.0.'
        ), stacklevel=2)

        @wraps(view)
        def handler(reason):
            response = current_app.make_response(view(reason))
            raise CSRFError(response.get_data(as_text=True), response=response)
        self._error_response = handler
        return view
```



## _get_config

此方法用于获取配置,  代码虽少,  但考虑挺多.

```python
def _get_config(
    value, config_name, default=None,
    required=True, message='CSRF is not configured.'
):
    """Find config value based on provided value, Flask config, and default value.

    :param value: already provided config value
    :param config_name: Flask ``config`` key
    :param default: default value if not provided or configured
    :param required: whether the value must not be ``None``
    :param message: error message if required config is not found
    :raises KeyError: if required config is not found
    """
    # a.如果传入的 value 不为 None, 直接返回这个 value
    # b.如果传入的 value 为 None, 尝试从 current_app.config 中获取配置, 同时设置默认值.
    if value is None:
        value = current_app.config.get(config_name, default)
    if required and value is None:
        raise KeyError(message)
    return value
```



## generate_csrf

```python
def generate_csrf(secret_key=None, token_key=None):
    """Generate a CSRF token. The token is cached for a request, so multiple
    calls to this function will generate the same token.

    During testing, it might be useful to access the signed token in
    ``g.csrf_token`` and the raw token in ``session['csrf_token']``.

    :param secret_key: Used to securely sign the token. Default is
        ``WTF_CSRF_SECRET_KEY`` or ``SECRET_KEY``.
    :param token_key: Key where token is stored in session for comparision.
        Default is ``WTF_CSRF_FIELD_NAME`` or ``'csrf_token'``.
    """

    secret_key = _get_config(
        secret_key, 'WTF_CSRF_SECRET_KEY', current_app.secret_key,
        message='A secret key is required to use CSRF.'
    )
    field_name = _get_config(
        token_key, 'WTF_CSRF_FIELD_NAME', 'csrf_token',
        message='A field name is required to use CSRF.'
    )

    # 如果 g 变量中已经保存了 csrf_token, 直接return它.
    if field_name not in g:
        if field_name not in session:
            # 在 session 中存储一串 由sha1安全哈希算法生成的加密数据
            session[field_name] = hashlib.sha1(os.urandom(64)).hexdigest()

        # 使用 itsdangerous 模块的 URLSafeTimedSerializer, 
        # URLSafeTimedSerializer生成的 payload 会携带时间戳.
        # 根据上面的 sha1加密数据, 生成一个 csrf_token.  携带时间戳.
        # 将 csrf_token 存入 g 变量中.
        s = URLSafeTimedSerializer(secret_key, salt='wtf-csrf-token')
        setattr(g, field_name, s.dumps(session[field_name]))

    return g.get(field_name)
```



## validate_csrf

```python
def validate_csrf(data, secret_key=None, time_limit=None, token_key=None):
    """将传入的csrf_token (即data), 与存储在 session 中的 csrf_token 进行对比.
    :raises ValidationError
    	思考: CSRF token验证失败有哪些情况 ?
    """
    secret_key = _get_config(
        secret_key, 'WTF_CSRF_SECRET_KEY', current_app.secret_key,
        message='A secret key is required to use CSRF.'
    )
    field_name = _get_config(
        token_key, 'WTF_CSRF_FIELD_NAME', 'csrf_token',
        message='A field name is required to use CSRF.'
    )
    time_limit = _get_config(
        time_limit, 'WTF_CSRF_TIME_LIMIT', 3600, required=False
    )

    if not data:
        raise ValidationError('The CSRF token is missing.')

    if field_name not in session:
        raise ValidationError('The CSRF session token is missing.')

    s = URLSafeTimedSerializer(secret_key, salt='wtf-csrf-token')
    try:
        token = s.loads(data, max_age=time_limit)
    except SignatureExpired:
        raise ValidationError('The CSRF token has expired.')
    except BadData:
        raise ValidationError('The CSRF token is invalid.')

	# werkzeug\security.py::safe_str_cmp 函数: 用于安全比较两个字符串是否相同
    if not safe_str_cmp(session[field_name], token):
        raise ValidationError('The CSRF tokens do not match.')
```



## 测试 flask_wtf 的 CSRFProtect

```python
# ======== 测试 =========
from flask import Flask, request, session, render_template_string
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'something_secret'
# app.config['WTF_CSRF_ENABLED'] = True  # 默认为True, 开启 csrf 保护
app.config['WTF_CSRF_TIME_LIMIT'] = 10   # 测试 CSRF 过期时间
CSRFProtect(app)


@app.route('/csrf', methods=['GET', 'POST'])
def csrf_get():
    if request.method.upper() == 'GET':
        form = "<input hidden name='csrf_token' value='{{ csrf_token() }}'>"
        return render_template_string(form)
    elif request.method.upper() == 'POST':
        # 获取在 session 中存储的sha1加密数据
        print(session.get('csrf_token'))
        return 'csrf_token validates success!'
    else:
        return 'My Page Not Found!', 404
    
# ====== csrf_token非法时会返回什么? ========
"""The CSRF token is invalid."""
# ====== csrf_token不带上时会返回什么? ========
"""The CSRF token is missing."""
# ======= cerf_token 过期时 ==========
"""The CSRF token has expired."""
```



## _FlaskFormCSRF

- 继承自 wtforms 的 CSRF,  重写了 CSRF 的三个方法:  setup_form、generate_csrf_token、validate_csrf_token。
- _FlaskFormCSRF 用于 **flask_wtf\form.py**

```python
class _FlaskFormCSRF(CSRF):
    def setup_form(self, form):
        self.meta = form.meta
        return super(_FlaskFormCSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token_field):
        return generate_csrf(
            secret_key=self.meta.csrf_secret,
            token_key=self.meta.csrf_field_name
        )

    def validate_csrf_token(self, form, field):
        # 在 CSRFProtect::protect 方法中, 成功校验 csrf_token 后, 设置了 g.csrf_valid = True.
        if g.get('csrf_valid', False):  
            # already validated by CSRFProtect
            return
        try:
            validate_csrf(
                field.data,
                self.meta.csrf_secret,
                self.meta.csrf_time_limit,
                self.meta.csrf_field_name
            )
        except ValidationError as e:
            logger.info(e.args[0])
            raise
```





## same_origin

```python
def same_origin(current_uri, compare_uri):
    current = urlparse(current_uri)  # from urllib.parse import urlparse
    compare = urlparse(compare_uri)
    return (
        current.scheme == compare.scheme
        and current.hostname == compare.hostname
        and current.port == compare.port
    )

```



# ==== wtforms ====

资源

- flask之源码解读wtforms执行流程:   https://blog.csdn.net/qq_33733970/article/details/79027984 

# 模块顶层文件概览

```
csrf
ext
fields
locale
widgets
__init__.py
compat.py
form.py
i18n.py
meta.py
utils.py
validators.py
```



# fields\core.py 接口概览

```
Field
UnboundField
Flags
Label
SelectFieldBase
SelectField
SelectMultipleField
RadioField
StringField
LocaleAwareNumberField
IntegerField
DecimalField
FloatField
BooleanField
DateTimeField
DateField
TimeField
FormField
FieldList
```



## Field

Field 接口概览

```
__new__
__init__
__unicode__
__str__
__html__
__call__
gettext
ngettext
validate
_run_validation_chain
pre_validate
post_validate
process
process_data
process_formdata
populate_obj
_formfield
_translations
data
default
description
do_not_call_in_templates
errors
filters
flags
id
label
meta
name
object_data
process_errors
raw_data
render_kw
short_name
type
validators
widget
```



# widgets\core.py



# form.py

## BaseForm

- BaseForm(object)

## FormMeta

- FormMeta(type)

## Form

- Form(with_metaclass(FormMeta, BaseForm))

  

# ==== itsdangerous ====

