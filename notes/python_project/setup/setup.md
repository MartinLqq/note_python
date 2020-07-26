

# 项目打包成 wheel

> 可参考链接:
>
> https://blog.csdn.net/T_NULL/article/details/89967641

1. 检查

```shell
python3 setup.py check
```

2. 打包

```shell
python3 setup.py sdist bdist_wheel || True
```

3. 查看

```shell
1> build/lib/
2> dist/xxx.tar.gz
3> dist/xxx-py3-none-any.whl
```

4. 安装

```shell
cd dist
pip3 install xxx-py3-none-any.whl
```

5. 查看已安装

```shell
pip3 show xxx
```





# python 项目辅助配置文件

资源

- [cookiecutter-flask](https://github.com/cookiecutter-flask/cookiecutter-flask)
- [pipy - Python Packages Index](https://pypi.org/)



除了框架自动生成的文件,  项目根目录一般有很多其他文件. 

1. 这些文件用在什么场景?
2. 有的有必要使用吗?
3. 如果能完成同样的需求,  选择使用哪个?



### > 编码风格相关

> 注:  
>
> 1. 以下很多工具,  在 pytest 中有集成, 名称对应为 pytest-xxx, 如 pytest-pylint, 在运行 pytest 测试命令时,  也会自动查找代码风格

```
.editorconfig
.pylintrc
.yapfignore
.pep8    (支持此文件, 但官方强烈不建议用, 而建议配置在 setup.cfg 或 tox.ini 中)
.flake8  (同样可以用 setup.cfg 或 tox.ini 替代)
.pydocstyle  (配置文件有多种, 具体往后看)
```

##### `.editorconfig`

- Editorconfig 可以用于多种开语言,  前端也基本会使用到.
- 光有 `.editorconfig` 配置不行,  需要 IDE 上有插件支持
- Pycahrm 在默认情况下支持 `.editorconfig` 

较通用的配置

```ini
# http://editorconfig.org
root = true

[*]
indent_style = space  # 缩进风格：空格
indent_size = 2       # 缩进大小2
charset = utf-8       # 字符集utf-8
trim_trailing_whitespace = true  # 是否删除每行行尾的空格

end_of_line = lf
insert_final_newline = true  # 是否在文件的最后插入一个空行

[*.md]
trim_trailing_whitespace = false

[Makefile]    # 针对 Makefile 的配置
indent_style = tab
```

##### `.pylintrc`

- [官方文档](http://pylint.pycqa.org/en/latest/)

```bash
$ pip install pylint
```



##### `.yapfignore`

- [pypi 文档](https://pypi.org/project/yapf/)

```bash
$ pip install  yapf
```

##### `.pep8`

- [官方文档](http://pep8.readthedocs.org/)

```bash
$ pip install pep8
```



##### `.flake8`

- [官方文档](http://flake8.pycqa.org/en/latest/)

```bash
$ pip install flake8
```



##### `.pydocstyle`

python  docstring 的静态分析工具

- [官方文档](http://www.pydocstyle.org/en/latest/index.html)

```bash
$ pip install pydocstyle
```

支持多种配置文件

- `setup.cfg`
- `tox.ini`
- `.pydocstyle`
- `.pydocstyle.ini`
- `.pydocstylerc`
- `.pydocstylerc.ini`





### > 测试相关

>  PS:  可以集成编码风格相关的工具配置

```
.coveragerc
pytest.ini
```

##### `.coveragerc`

- [官方文档](https://coverage.readthedocs.io/en/latest/config.html)

```bash
$ pip install coverage
```



##### `pytest.ini`

- [官方文档](https://docs.pytest.org/)
- pytest 插件有多少?
  - 通过 classifier 在 pypi.org 上搜索 pytest 插件:  [Framework :: Pytest](https://pypi.org/search/?q=&o=&c=Framework+::+Pytest)

pytest  `rootdir` 和 `inifile` 的查找顺序:

```
# first look for pytest.ini files
path/pytest.ini
path/tox.ini    # must also contain [pytest] section to match
path/setup.cfg  # must also contain [tool:pytest] section to match
pytest.ini
... # all the way down to the root

# now look for setup.py
path/setup.py
setup.py
... # all the way down to the root
```



### >  docker 相关

```
.dockerignore
docker-support
	Dockerfile            # 描述一个 docker 镜像的构建过程
	entrypoint.sh         # 指定为 docker 容器启动时会执行的脚本
	docker-compose.yaml   # 管理多个 docker 容器
```



##### `.dockerignore`

- [官方文档](https://docs.docker.com/engine/reference/builder/#dockerignore-file)

执行 docker build 命令时,  默认会把指定上下文目录的所有内容打包, 发送给 docker 引擎,  一般会用 `.dockerignore` 配置忽略一些文件,  提升 build 速度.



### > git 相关

```
.gitattributes
.gitignore
.gitmodules
```



### > 项目信息

```
LICENSE
README.md
```



### > 打包与安装

```
setup.cfg
setup.py

requirements.txt
# 或 requirements/dev.txt   requirements/prod.txt
```

##### `setup.py`, `setup.cfg`

- [官方文档](https://docs.python.org/3/distutils/setupscript.html)
- CSDN:  [python setup](https://blog.csdn.net/zhaole524/article/details/51772586)


### > CI/CD
```
.travis.yml    # 用来描述如何持续构建，支持各种语言和系统环境
.gitlab-ci.yml
```

`.travis.yml`: [官方网档](https://docs.travis-ci.com/user/tutorial/)
`.gitlab-ci.yml`: 持续集成之.gitlab-ci.yml篇, https://segmentfault.com/a/1190000019540360

### > 未分类

```
MANIFEST.in
MAKEFILE
tox.ini       # 通用的虚拟环境管理和测试命令行工具。tox能够让我们在同一个Host上自定义出多套相互独立且隔离的python环境
```



