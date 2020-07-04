# py文件打包成so

可参考资源：https://blog.csdn.net/qq_44714134/article/details/100703907



1. 环境：Centos7 + python3

2. 安装 gcc、c++ 编译器以及内核文件：yum -y install gcc gcc-c++ kernel-devel

3. 安装 python3-devel： yum install python3-devel

4. 安装 Cython： pip3 install Cython

5. 编写好 setup.py，指定将哪些文件打包成 so

6. 打包： python3 setup.py build_ext

7. 查看打包结果

   ```
   # 打包结果在 build/ 目录下
   
   py2so/
   ├── build
   │   ├── lib.linux-x86_64-3.6
   │   │   └── py2so
   │   │       └── src
   │   │           └── foo.cpython-36m-x86_64-linux-gnu.so  # 最终需要的 so 文件
   │   └── temp.linux-x86_64-3.6    # 可删除
   │       └── src
   │           └── foo.o
   ├── __init__.py
   ├── main.py       # 程序入口
   ├── README.md
   ├── requirements.txt
   ├── setup.py      # 重要， 打包必备
   └── src
       ├── foo.c     # 可删除
       ├── foo.py
       └── __init__.py
   ```

8. 把 foo.cpython-36m-x86_64-linux-gnu.so 复制到 py2so/src 目录下， 重命名之前的 foo.py 为 foo.py_bak

9. 进入 py2so/ 目录下,  测试

   ```bash
   $ python3 main.py
   ```



> 注意:  
>
> 在与 python 版本有关的步骤中，必须正确指明版本， 包括
>
> - yum install python3-devel
> - pip3 install Cython -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
> - python3 setup.py build_ext
> - python3 main.py
>
> 对应 python2 下：
>
> - yum install python-devel
> - pip install Cython  （或 pip2 ...）
> - python setup.py build_ext （或 python2 ...）
> - python main.py  （或python2 ...）



setup.py 的最简单内容

```python
from distutils.core import setup
from Cython.Build import cythonize


# [] 内是要打包的文件名，可指定多个文件
setup(
    ext_modules=cythonize(["src/foo.py"]),   # 支持 "src/*.py"
)
```





# py2sec - 开源的代码加密脚本 

[py2sec](https://github.com/cckuailong/py2sec)





