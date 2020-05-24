# ==== jinja2 ====

Flask的Jinja2模板引擎 — 全局函数

-  http://www.ttlsa.com/python/flask-jinja2-template-engine-global-function/ 



# flask 向模板引擎中增加全局变量/方法



```python
from flask import Flask, render_template

app = Flask(__name__)

# 方法1
app.context_processor(lambda: {'my_var2': 'my_var2 value'})
app.context_processor(lambda: {'my_func2': lambda : 'Hello my_func2'})

# 方法2
@app.template_global()
def double(num):  # {{ double(100) }}
    return 2 * num

@app.route('/jinja2')
def jinja2():
	# 方法3
    app.jinja_env.globals['my_var'] = 'hahaha'
    app.jinja_env.globals['my_func'] = lambda: 'Hello my_func'

    return render_template('temp.html')
```

templates/temp.html

```html
(a) app.jinja_env.globals 字典   <br/>
变量: {{ my_var }}
方法: {{ my_func() }}
<br/><br/>
(b) app.context_processor 函数   <br/>
变量: {{ my_var2 }}
方法: {{ my_func2() }}
<br/><br/>
(c) @app.template_global() 装饰器   <br/>
方法: {{ double(100) }}
```



