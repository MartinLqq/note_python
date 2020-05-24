from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import View


def index(request):
    if request.method.lower() == 'get':
        print(request.__dict__)
        return HttpResponse('Hello django!')
    else:
        return HttpResponse('Not found', status=404)

def login(request):
    if request.method.lower() == 'get':
        login_form = """
        <form action='/blog/login/' method='post'>
            用户名: <input type='text' name='username' /> <br/>
            密 码: <input type='password' name='password' /> <br/>
            <input type='submit' value='提交' />
        </form>
        """
        return HttpResponse(login_form)

    if request.method.lower() == 'post':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return HttpResponse('参数不全')
        print(username)
        print(password)
        if request.session.get('username') == username:
            return HttpResponse('已登录')
        if username != 'Martin':
            return HttpResponse('用户不存在')
        if password != '123456':
            return HttpResponse('密码错误')

        request.session['username'] = username
        return HttpResponse('login success')


def logout(request):
    if request.method.lower() != 'post':
        return HttpResponseNotFound()
    username = request.POST.get('username')
    sess_uname = request.session.get('username')
    if sess_uname and sess_uname == username:
        del request.session['username']
        return HttpResponse('退出成功')
    return HttpResponse('退出成功')


class RegisterView(View):

    def get(self, request):

        # return render(request, 'register.html')
        register = """
        <form action='/blog/register/' method='post'>
            用户名: <input type='text' name='username' /> <br/>
            密码: <input type='password' name='password' /> <br/>
            确认密码: <input type='password' name='password1' /> <br/>
            <input type='submit' value='提交' />
        </form>
        """
        return HttpResponse(register)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if not all([username, password, password1]):
            return HttpResponse('参数不全')
        if password != password1:
            return HttpResponse('两次输入的密码不一致')

        # 注册...
        # 注册成功, 设置 session
        request.session['username'] = username

        return HttpResponse('注册成功')



def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了,  请求路径:　%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper

class DemoView(View):

    @method_decorator(my_decorator)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        assert 0
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')
