# [ ](https://hellogithub.com/periodical/category/Python 项目/?page=14#python-fire)[python-fire](https://github.com/google/python-fire) 

https://hellogithub.com/    ***第 12 期\* \*Star 17.3k\* \*Watch 383\* \*Fork 1.1k\***
Fire 是 Google 开源的 Python 库，可自动将您的代码转变成 CLI，无需您做任何额外工作。您不必定义参数，设置帮助信息，或者编写定义代码运行方式的 main 函数。相反，您只需从 main 模块调用“Fire”函数，其余工作全部交由 Python Fire 来完成。示例代码如下：

```python
import fire
class Example(object):
    def hello(self, name='world'):
        """Says hello to the specified name."""
        return 'Hello {name}!'.format(name=name)

def main():
    fire.Fire(Example)
if __name__ == '__main__':
    main()
```



```bash
# 在终端中调用效果如下：
$ ./example.py hello
Hello world!
$ ./example.py hello David
Hello David!
$ ./example.py hello --name=Google
Hello Google!
```

