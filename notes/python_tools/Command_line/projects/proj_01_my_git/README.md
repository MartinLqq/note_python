2020-2-20 ~ 2020-2-21

An example for setuptools and command-line:
- 包含setup.py怎么写
- 包含argparse库怎么实现命令行, 包括子命令
- setp.py在项目根目录下
- 命令行代码入口在 src\mygit\__init__.py, 对应setup.py中指定的entry_points



功能：

- 模仿git命令， 实现几个git命令的基本格式

使用的CLI工具： 

- argparse

未实现：

- 参数组



测试效果:

> cd进入到项目目录(proj_01_my_git)下

1.安装命令行工具mygit
```bash
pip install -e .

# 开发模式不要用 python setup.py install
```
2.命令帮助
```bash
mygit
mygit -h
mygit --help
```
3.子命令帮助
```bash
mygit clone -h
mygit clone --help
```

**注:**
```
1.argparse库的详细用法见笔记
2.多看笔记
3.多看开源项目
```
