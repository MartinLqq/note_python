# Tmux终端分屏

## Linux

### 下载安装

```bash
sudo apt-get install tmux
sudo apt-get remove tmux
```





## Windows

Windows上可以在 MSYS terminal 中使用 Tmux

源链接:  https://blog.pjsen.eu/?p=440

### 1.下载安装MSYS2

https://www.msys2.org/

### 2.更新源下载源

https://www.cnblogs.com/flyinggod/p/10841291.html

修改msys64\etc\pacman.d 目录下有三个文件的内容：mirrorlist.mingw32 、mirrorlist.mingw64 、mirrorlist.msys为中国科学技术大学开源软件镜像 

- mirrorlist.mingw32

```
`##``## 32-bit Mingw-w64 repository mirrorlist``##` `## Primary``## msys2.org` `Server = http:``//mirrors.ustc.edu.cn/msys2/mingw/i686/``Server = http:``//repo.msys2.org/mingw/i686``Server = http:``//downloads.sourceforge.net/project/msys2/REPOS/MINGW/i686``Server = http:``//www2.futureware.at/~nickoe/msys2-mirror/i686/`
```

- mirrorlist.mingw64

```
`##``## 64-bit Mingw-w64 repository mirrorlist``##` `## Primary``## msys2.org` `Server = http:``//mirrors.ustc.edu.cn/msys2/mingw/x86_64/``Server = http:``//repo.msys2.org/mingw/x86_64``Server = http:``//downloads.sourceforge.net/project/msys2/REPOS/MINGW/x86_64``Server = http:``//www2.futureware.at/~nickoe/msys2-mirror/x86_64/`
```

- mirrorlist.msys

```
`##``## MSYS2 repository mirrorlist``##` `## Primary``## msys2.org` `Server = http:``//mirrors.ustc.edu.cn/msys2/msys/$arch/``Server = http:``//repo.msys2.org/msys/$arch``Server = http:``//downloads.sourceforge.net/project/msys2/REPOS/MSYS2/$arch``Server = http:``//www2.futureware.at/~nickoe/msys2-mirror/msys/$arch/`
```





### 3.下载 tmux

1. 进入MSYS2安装目录,  运行`msys2.exe` 打开MSYS2命令行窗口
2. 下载 tmux : `pacman -S tmux` 
3. 在 MSYS terminal 下载好 tmux 命令后, 就可以直接在 MSYS terminal 使用.





## 常用操作

参考:  https://www.cnblogs.com/lizhang4/p/7325086.html

```bash
# 启动新会话
tmux [new -s 会话名 -n 窗口名]
# 恢复会话
tmux at [-t 会话名]
# 列出所有会话
tmux ls
# 关闭会话
tmux kill-session -t 会话名
# 关闭所有会话
tmux ls | grep : | cut -d. -f1 | awk '{print substr($1, 0, length($1)-1)}' | xargs kill
```



**在 Tmux 中，按下 Tmux 前缀 `ctrl+b`，然后：**

> **会话**

```
:new<回车>  启动新会话
s           列出所有会话
$           重命名当前会话
```

>  **窗口 (标签页)**

```
c  创建新窗口
w  列出所有窗口
n  后一个窗口
p  前一个窗口
f  查找窗口
,  重命名当前窗口
&  关闭当前窗口
```

>  **调整窗口排序**

```
swap-window -s 3 -t 1  交换 3 号和 1 号窗口
swap-window -t 1       交换当前和 1 号窗口
move-window -t 1       移动当前窗口到 1 号
```

>  **窗格（分割窗口）**

```
%  垂直分割
"  水平分割
o  交换窗格
x  关闭窗格
⍽  左边这个符号代表空格键 - 切换布局
q 显示每个窗格是第几个，当数字出现的时候按数字几就选中第几个窗格
{ 与上一个窗格交换位置
} 与下一个窗格交换位置
z 切换窗格最大化/最小化
```

>  **杂项**

```
d  退出 tmux（tmux 仍在后台运行）
t  窗口中央显示一个数字时钟
?  列出所有快捷键
:  命令提示符
```



# httpie

httpie是一个 http client 命令行工具，能帮助我们快速的进行 http 请求，类似于 curl 但是语法做了很多简写 

```bash
$ pip install --upgrade httpie
$ http --help
```

# vimdiff 文本文件比对
```bash
vimdiff test1.py test2.py
```
