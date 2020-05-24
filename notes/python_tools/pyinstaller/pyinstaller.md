# Windows 使用 pyinstaller

## 文档

- 官方文档:  https://pyinstaller.readthedocs.io/en/stable/spec-files.html#using-spec-files
- 使用 pyinstaller 打包多文件和目录的 python 项目: https://www.cnblogs.com/shiyongge/p/10582552.html





## 注意

1. pyinstaller 指定的 python 解释器路径中, 最好不能带中文,  避免出现不可预知错误
2. Windows上路径分隔符是反斜杠 `\`,  进入虚拟环境时须注意.
3. 要想打包时能将所有依赖包一起打包,  首先保证在当前环境下,  要打包的脚本可以成功执行
4. 要想打包时能将所有数据一起打包,  包括图片和其他配置等,  需要修改自动生成的 .spec 文件
5. pyinstaller打包后程序体积太大，如何解决？   https://www.zhihu.com/question/268397385



创建虚拟环境:

```bash
python3 -m venv myenv1
```

进入虚拟环境:

```bash
# 注意用反斜杠`\`
.\myenv\Scripts\activate.bat
```

在虚拟环境下安装 pyinstaller

```bash
pip install pyinstaller
```

安装项目所有必须的依赖,  如:

```bash
pip install requests bs4 jieba matplotlib pillow wordcloud pymysql
```

携带额外数据

```
# 在 ciyun.spec 中增加:

from wordcloud.wordcloud import FILE

added_files = [
    ("icon.ico", "."),
    #("images", "images"),
    ("fonts", "fonts"), 
    (os.path.join(FILE, 'stopwords'), "wordcloud"),
]
```



在虚拟环境下打包

```bash
pyinstaller -F ciyun.spec --distpath packed/ 
# -p 可以指定imports的目录
```

