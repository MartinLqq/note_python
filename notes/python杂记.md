# 文件操作

## open函数的模式

### r、rb、rt

1. 使用’r’一般情况下最常用的，但是在进行读取二进制文件时，可能会出现文档读取不全的现象；

2. 使用’rb’按照二进制位进行读取的，不会将读取的字节转换成字符，二进制文件用二进制读取用’rb’ ；

3. rt模式下，python在读取文本时会自动把\r\n转换成\n，文本文件用二进制读取用‘rt’；
  

### x模式

-  写模式，新建一个文件，如果该文件已存在则会报错 。 

 

## 文件对象的其他方法

### file.flush()

一般情况下，文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法。 

### file.seek()

- **seek()** 方法用于移动文件读取指针到指定位置。

- **tell()** 方法返回文件的当前位置，即文件指针当前位置。 

### file.truncate()

- **truncate()** 方法用于从文件的首行首字符开始截断，截断文件为 size 个字符，无 size 表示从当前位置截断；截断之后 V 后面的所有字符被删除，其中 Widnows 系统下的换行代表2个字符大小。 。



## doc 转 html

```python
"""Convert docx to html."""
import sys

from pathlib import Path

from win32com import client
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



## md 转 html

```python
import sys
import markdown

html_head = """
<!DOCTYPE html>
<html lang="zh-cn">
<head>
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML' async></script>
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
<link href="github.css" rel="stylesheet">
</head>
<body>
"""

# 所支持的复杂元素
exts = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.toc',
    'markdown.extensions.smarty',
    'markdown.extensions.nl2br',
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.footnotes',
    'markdown.extensions.legacy_attrs',
    'markdown.extensions.legacy_em',
    'markdown.extensions.md_in_html',
    'markdown.extensions.sane_lists',
    'markdown.extensions.meta',
    'markdown.extensions.attr_list',
    'markdown.extensions.admonition',
]

def convert(md_path, html_path):
    with open(r"{}".format(md_path), 'r', encoding='utf8') as file:
        html_body_txt = file.read()
    md = markdown.Markdown(extensions=exts)
    html_body = md.convert(html_body_txt)
    html_tail = "\n</body>\n</html>"
    html = html_head + html_body + html_tail
    with open(html_path, 'w', encoding='utf8') as file:
        file.write(html)

if __name__ == '__main__':
    md_path = sys.argv[1]
    html_path = sys.argv[2]
    convert(md_path, html_path)
```



## 移动文件到 win 回收站

```python
import sys
import shutil
from win32comext.shell import shell, shellcon

debug = False

def del_to_recyclebin(filename, default_path):
    # os.remove(filename) # 直接删除文件，不经过回收站
    if not debug:
        # 删除文件到回收站
        # SHFileOperation参考: https://www.cnblogs.com/xiaodai0/p/10174877.html
        res= shell.SHFileOperation(
            (
                0,
                shellcon.FO_DELETE,
                filename,
                None,
                shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                None,
                None
            )
        )
        print(res)
        #if res[0] != 0:
            #shutil.move(filename, default_path)
            #shutil.rmtree(filename)
            # os.system('del '+filename)

if __name__ == '__main__':
    path = sys.argv[1]
    default_path = sys.argv[2]
    del_to_recyclebin("{}".format(path), default_path)
    print('Done.')
```



## 获取 win 超链接对应原文件/目录

```python
import sys
import win32com.client

def get_real_path(link_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(r"{}".format(link_path))
    return shortcut.Targetpath

if __name__ == '__main__':
    link_path = sys.argv[1]
    print(get_real_path(link_path), end="")
```



# 文件搜索

## 遍历目录

```python
import os
from pathlib import Path


# 方法1: 使用 os.walk() 和 os.path.abspath(), os.path.join()
def tree(top):
    for path, names, fnames in os.walk(top):
        for fname in fnames:
            yield os.path.join(os.path.abspath(path), fname)


# [推荐]方法2: 使用 pathlib.Path
# 注: 与 os.walk() 不同, 使用 Path().iterdir() 会忽略名称以 . 开头的隐藏文件夹
def better_tree(top: Path):
    for path in top.iterdir():
        if path.is_dir():
            better_tree(path)
        else:
            yield path.absolute()


# for name in tree('./'):
#     print(name)


for name in better_tree(Path('./')):
    print(name)
```





# 监测文件 (watchdog)

```python
import sys
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileMonitor(FileSystemEventHandler):
    def on_moved(self, event):
        super(FileMonitor, self).on_moved(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Moved : from {2} to {3}".format(
            now_time, what, event.src_path, event.dest_path
        ))

    def on_deleted(self, event):
        super(FileMonitor, self).on_deleted(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Deleted : {2} ".format(now_time, what, event.src_path))

    def on_modified(self, event):
        super(FileMonitor, self).on_modified(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Modified : {2} ".format(now_time, what, event.src_path))
        
    def on_created(self, event):
        super(FileMonitor, self).on_moved(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Created : {2} ".format(now_time, what, event.src_path))


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```





# 实现人民币大写转换

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-

# ********* 转换方法介绍 *********
# 将需要转换的数字从右向左，每4位分成一个section，如:24530467103，将该数字拆分后，得到:
# 245 3046 7103 （245亿3046万7103）
# 对拆分后的数字先按照section进行数字到汉字的转换，然后添加数值单位，如:仟，佰，拾，处理结束后可以得到转换后的序列。
# 对section处理结束后，再对每个section进行单位的追加。如：兆、亿、万。
# 这里需要注意一些特殊情况，如：section中连续出现0，最后一个数字为0等。

DEBUG = True

upper = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
decimal_unit = ["角", "分", "厘", "毫"]
section_unit = ["万", "亿", "兆"]
count_unit = ["拾", "佰", "仟"]

def dbg_print(s):
    if DEBUG:
      	print(s)

def split_num(num):
    num_list = []
    if (len(num) <= 4):
        num_list.append(num)
        return num_list
    while (len(num)):
        if (len(num) <= 4):
            num_list.append(num)
            num_list.reverse()
            return num_list
        sec = num[-4:]
        num_list.append(sec)
        num = num[:-4]

# 处理小数部分，只支持4位，多于4位，四舍五入。
def convert_dec(num):
    result = ""
    count = 0
    dbg_print(num)
    for i in num:
        n = int(i)
        if (0 != n):
            result += upper[n]
            result += decimal_unit[count]
        count += 1
    dbg_print(result)
    return result

# 处理整数部分
def convert_int(num):
    section_list = split_num(num)
    dbg_print(num)
    dbg_print(section_list)
    result = ""
    sec_index = len(section_list) - 2
    for item in section_list:
        index = len(item) - 2
        # 统计连续出现的数字0的个数。
        flag = 0
        # 计算遍历过的item中的字符数。 
        count = 0
        # 对每个section进行处理，得到数字对应的汉字。
        for i in item:
            n = int(i)
            if (0 == n):
              	flag += 1
            else:
              	flag = 0
            # 用来区分section的最后一位为0的情况
            if (count != len(item)-1):
                # 该位置的数字为0，并且它的下一个数字非0。
                if ((flag >= 1) and ('0' != item[count+1])):
                  result += upper[n]
                else (0 != n):
                	result += upper[n]
            else:
                # section的最后一个数字非0的情况。
                if (0 != n):
                	result += upper[n]
            # 最后一个数字以及数字为0时，都不需要添加单位。
            if ((index >= 0) and (0 != n)):
              	result += count_unit[index]
            index += 1
            count += 1
        从第1个section开始，如果section中的数字不全为0，其后就需要添加section对应的单位。
        if (sec_index >= 0 and flag != count):
          	result += section_unit[sec_index]
        dbg_print(result)
        sec_index -= 1
    result = result.replace("壹拾", "拾")
    result += "元"
    return result

# 转换函数
def convert(num):
    result = ""
    num = round(float(num), 4)
    integer,decimal = str(num).split('.')
    result_int = convert_int(integer)
    result_dec = convert_dec(decimal)

    if (len(result_dec) == 0):
      	result = result_int += "整"
    else:
      	result = result_int + result_dec
    return result
```





# 数据处理

## zip()

 使用zip()函数一次处理两个或多个列表中的元素： 

```
alist = ['a1', 'a2', 'a3']
blist = ['1', '2', '3']
 
for a, b in zip(alist, blist):
    print a, b
 
# a1 1
# a2 2
# a3 3
```



## 字典排序

```python
from operator import itemgetter

# 据说是最快的方法
d = {'a':2, 'b':23, 'c':5, 'd':17, 'e':1}

# 按照value排序
d_v = sorted(d.iteritems(), key=itemgetter(1), reverse=True)
print 'sort by value: ', d_v

# 按照key排序
d_k = sorted(d.iteritems(), key=itemgetter(0), reverse=True)
print 'sort by key: ', d_k
```





# 系统操作

## 获取 Linux 系统信息

```python
# 使用 Python 获取 Linux 系统信息

import os
import platform

def print_base_info():
    print 'platform.uname(): ', platform.uname()
    print 'platform.system(): ', platform.system()
    print 'platform.release(): ', platform.release()
    print 'platform.linux_distribution(): ', platform.linux_distribution()
    print 'platform.architecture(): ', platform.architecture()

def cpu_info():
    cpuinfo = {}
    procinfo = {}
    nprocs = 0

    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs += 1
                procinfo = {}
            elif len(line.split(':')) == 2:
                procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
            else:
                procinfo[line.split(':')[0].strip()] = ''
    return cpuinfo

def mem_info():
    meminfo = {}

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def net_devs():
    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    device_data = {}
    from collections import namedtuple
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                float(line[1].split()[8])/(1024.0*1024.0))
    return device_data

def process_list():
    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
    return pids


if __name__ == '__main__':
    print_base_info()
    print 'cpu info dict: ', cpu_info()
    print 'mem info dict: ', mem_info()
    print 'netdevs info dict: ', net_devs()
    print 'pids: ', process_list()
```







