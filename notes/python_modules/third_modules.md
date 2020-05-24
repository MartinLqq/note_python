# celery

celery排队机制

# chardet



# kombu

消息框架,  Python的消息库

https://github.com/celery/kombu



# ffmpeg

视频转码





# qrcode

```
import qrcode

# 不管那种方案都要装第三方模块，qrcode 模块 和  Image  模块
# 第一种方案
img = qrcode.make("tangjie")
img.save("xinxing.jpg")

# 第二种方案

# version 表示二维码的版本号，二维码总共有1到40个版本，最小的版本号是1，对应的尺寸是21×21，每增加一个版本会增加4个尺寸。这里说的尺寸不是只生成图片的大小，而是值二维码的长宽被平均分为多少份。
#
# error_correction指的是纠错容量，这就是为什么二维码上面放一个小图标也能扫出来，纠错容量有四个级别，分别是
#
# ERROR_CORRECT_L L级别，7%或更少的错误能修正
#
# ERROR_CORRECT_M M级别，15%或更少的错误能修正，也是qrcode的默认级别
#
# ERROR_CORRECT_Q Q级别，25%或更少的错误能修正
#
# ERROR_CORRECT_H H级别，30%或更少的错误能修正
#
# box_size 指的是生成图片的像素
#
# border 表示二维码的边框宽度，4是最小值

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data('xinxingzhaojhgfddfghj')
qr.make(fit=True)

img = qr.make_image()
img.save('xinxingzhao.png')

```







# psutil

```bash
pip install psutil

# get help on package psutil
python -c "import psutil; help(psutil)" > psutil_help.txt
```





# Pillow



# python-docx

- 0.8.10 Document:  https://python-docx.readthedocs.io/en/latest/

# pydocx

- 文档: [python docx文档转html页面](https://www.cnblogs.com/taixiang/p/9978456.html)
-  pip3 install pydocx 



## 处理docx

```python
from pydocx import PyDocX
html = PyDocX.to_html("test.docx")
f = open("test.html", 'w', encoding="utf-8")
f.write(html)
f.close()
```



## 处理doc、wps

针对doc 的文档，可以手动改成docx后缀名，进行上传使用。 尝试用代码转换成docx，window平台下有相应的库:   **pypiwin32**

```python
"""Convert docx to html."""
import sys

from pathlib import Path

from win32com import client  // pypiwin32
from pydocx import PyDocX


def convert(docx_path: str, html_path: str):
    """
    docx  -->  html
    doc   -->  docx  -->  html
    wps   -->  docx  -->  html
    """
    ext = Path(docx_path).suffix
    if ext in ['.doc', '.wps']:
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(docx_path)
        docx_path = docx_path.replace(ext, '.docx')
        doc.SaveAs(docx_path, 16)
        doc.Close()
        word.Quit()
    html = PyDocX.to_html(docx_path)
    with open(html_path, 'w', encoding="utf-8") as file:
        file.write(html)


if __name__ == '__main__':
    docx_path = r"{}".format(sys.argv[1])
    html_path = r"{}".format(sys.argv[2])
    convert(docx_path, html_path)
```







# pypiwin32

- pip3 install pypiwin32





# setuptools





# tempfile

## TemporaryFile

## NamedTemporaryFile

## TemporaryDirectory

## gettempdir



# werkzueg

werkzueg.local 模块

> http://python.jobbole.com/87738/





# wordcloud

```python
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

titles = "".join(
    ['高层领导人报道集地方领导资料库 历次党代会', '历届人大政协会议 外交部发言人中央重拳打击腐败 人事任免',
     '开国将帅名录 党史人物纪念馆 历年访谈汇总 2019两会访谈录高考 考公务员 图解新闻 证监会答复投资者信息检索库']
)

wordcloud = WordCloud(
    background_color='white',
    scale=1.5,
    width=1200,
    height=800,
    # max_words=50,
    font_path=r"C:\Windows\Fonts\STSONG.TTF"
)
words = jieba.lcut(titles)
wordcloud.generate(" ".join(words))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

wordcloud.to_file("outfile.png")
```





# shlex

安全切分shell命令中的空白字符

```
cmdargs = shlex.split(cmd)
```