[TOC]

# linux bash

命令解析器

shell -- unix操作系统

bash -- linux操作系统



# bash快捷键

```
历史命令切换
	- 向上遍历: ctrl + P	# Previous
	- 向下遍历: ctrl + N	# Next
光标移动
	- 向后:   ctrl + B	# Backward
	- 向前:   ctrl + F	# Forward
	- 向行首: ctrl + A	# Ahead
	- 向行末: ctrl + E	# End
删除字符
	- 删除光标前 一个字符: ctrl + H	# Backspace
	- 删除光标后 一个字符: ctrl + D	# Delete
	- 删除光标前 一个单词: ctrl + W  # Word
	- 删除光标前 所有字符: ctrl + U  # 在某些设置下,删除全行
	
匹配最相近的一个文件，然后输出:
	ctrl + R
```



# path

## linux 主要目录

```
/		根目录
/bin	存放bash命令
/boot	系统启动所需文件
/dev	存放根据硬件信息虚拟化后的文件
/etc	配置文件
/home	所有用户的主目录
/lib	存放linux系统需要用到的动态库(共享库), 类似windows的 .dll 文件
/media	linux将识别的U盘,光驱等设备挂载到 /media 目录下
/mnt	用于挂载临时文件系统, 用户可将光驱挂载到 /mnt 下, 进入 /mnt 查看光驱内容
/opt	存放第三方软件
/proc	虚拟目录, 是系统内存的映射, 内容在内存中, 存放系统信息
/root	超级用户的家目录
/usr	User Software Resource, 存放用户应用程序和文件, 类似windows的 program files 目录
/sys
/tmp	存放临时文件
```



## linux定时任务存放路径

```
/var/spool/cron/<xx>
如: root用户的定时任务路径 xx --> root
```

## linux环境变量自动配置

```
A. 启动帐号后自动执行的是 文件为 ~/.profile， 通过这个文件可设置自己的环境变量;
B. 或者将环境变量配置到 ~/.bashrc 中, source ~/.bashrc 使之生效

安装的软件路径一般需要加入到path中:
vim ~/.bashrc
	PATH=$APPDIR:/opt/app/soft/bin:$PATH:/usr/local/bin:$TUXDIR/bin:$ORACLE_HOME/bin;
	export PATH
```

## ssh配置文件路径

```
cd ~/.ssh/    # `~` 对应为root用户 或 自建用户
# 目录内容:
    authorized_keys
    id_rsa
    id_rsa.pub
    known_hosts
```

### 配置ssh远程登录时免密码

```
# 配置ssh远程登录时免密码
1. 获取客户主机的 publickey:  cat id_rsa.pub
2. 将客户主机的 publickey 添加到目标主机的 authorized_keys 文件中.
```

## vim配置文件路径

```
1. 系统配置文件：/etc/vim/vimrc	(更改会影响所有的用户）
2. 用户配置文件：～/.vimrc			(更改只会影响自己使用）

如何查找配置文件
	打开vim 输入 ':version'
	找到如下的代码，即vim的配置文件位置:
        系统 vimrc 文件: "$VIM/vimrc"
        用户 vimrc 文件: "$HOME/.vimrc"
        用户 exrc 文件: "$HOME/.exrc"
        系统 gvimrc 文件: "$VIM/gvimrc"
        用户 gvimrc 文件: "$HOME/.gvimrc"
        系统菜单文件: "$VIMRUNTIME/menu.vim"
        $VIM 预设值: "/usr/share/vim"
```

大牛 `~/.vimrc` 配置

```
map <F9> :call SaveInputData()<CR>
func! SaveInputData()
	exec "tabnew"
	exec 'normal "+gP'
	exec "w! /tmp/input_data"
endfunc


"colorscheme torte
"colorscheme murphy
"colorscheme desert 
"colorscheme desert 
"colorscheme elflord
colorscheme ron


"set fencs=utf-8,ucs-bom,shift-jis,gb18030,gbk,gb2312,cp936
"set termencoding=utf-8
"set encoding=utf-8
"set fileencodings=ucs-bom,utf-8,cp936
"set fileencoding=utf-8

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 显示相关  
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"set shortmess=atI   " 启动的时候不显示那个援助乌干达儿童的提示  
"winpos 5 5          " 设定窗口位置  
"set lines=40 columns=155    " 设定窗口大小  
set go=             " 不要图形按钮  
"color asmanian2     " 设置背景主题  
"set guifont=Courier_New:h10:cANSI   " 设置字体  
"syntax on           " 语法高亮  
autocmd InsertLeave * se nocul  " 用浅色高亮当前行  
autocmd InsertEnter * se cul    " 用浅色高亮当前行  
"set ruler           " 显示标尺  
set showcmd         " 输入的命令显示出来，看的清楚些  
"set cmdheight=1     " 命令行（在状态行下）的高度，设置为1  
"set whichwrap+=<,>,h,l   " 允许backspace和光标键跨越行边界(不建议)  
"set scrolloff=3     " 光标移动到buffer的顶部和底部时保持3行距离  
set novisualbell    " 不要闪烁(不明白)  
set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]\ %{strftime(\"%d/%m/%y\ -\ %H:%M\")}   "状态行显示的内容  
set laststatus=1    " 启动显示状态行(1),总是显示状态行(2)  
set foldenable      " 允许折叠  
set foldmethod=manual   " 手动折叠  
"set background=dark "背景使用黑色 
set nocompatible  "去掉讨厌的有关vi一致性模式，避免以前版本的一些bug和局限  
" 显示中文帮助
if version >= 603
	set helplang=cn
	set encoding=utf-8
endif
" 设置配色方案
"colorscheme murphy
"字体 
"if (has("gui_running")) 
"   set guifont=Bitstream\ Vera\ Sans\ Mono\ 10 
"endif 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""新文件标题
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"新建.c,.h,.sh,.java文件，自动插入文件头 
autocmd BufNewFile *.cpp,*.[ch],*.sh,*.java exec ":call SetTitle()" 
""定义函数SetTitle，自动插入文件头 
func SetTitle() 
	"如果文件类型为.sh文件 
	if &filetype == 'sh' 
		call setline(1,"\#########################################################################") 
		call append(line("."), "\# File Name: ".expand("%")) 
		call append(line(".")+1, "\# Author: ma6174") 
		call append(line(".")+2, "\# mail: ma6174@163.com") 
		call append(line(".")+3, "\# Created Time: ".strftime("%c")) 
		call append(line(".")+4, "\#########################################################################") 
		call append(line(".")+5, "\#!/bin/bash") 
		call append(line(".")+6, "") 
	else 
		call setline(1, "/*************************************************************************") 
		call append(line("."), "	> File Name: ".expand("%")) 
		call append(line(".")+1, "	> Author: ma6174") 
		call append(line(".")+2, "	> Mail: ma6174@163.com ") 
		call append(line(".")+3, "	> Created Time: ".strftime("%c")) 
		call append(line(".")+4, " ************************************************************************/") 
		call append(line(".")+5, "")
	endif
	if &filetype == 'cpp'
		call append(line(".")+6, "#include<iostream>")
		call append(line(".")+7, "using namespace std;")
		call append(line(".")+8, "")
	endif
	if &filetype == 'c'
		call append(line(".")+6, "#include<stdio.h>")
		call append(line(".")+7, "")
	endif
	"	if &filetype == 'java'
	"		call append(line(".")+6,"public class ".expand("%"))
	"		call append(line(".")+7,"")
	"	endif
	"新建文件后，自动定位到文件末尾
	autocmd BufNewFile * normal G
endfunc 
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"键盘命令
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

nmap <leader>w :w!<cr>
nmap <leader>f :find<cr>

" 映射全选+复制 ctrl+a
map <C-A> ggVGY
map! <C-A> <Esc>ggVGY
map <F12> gg=G
" 选中状态下 Ctrl+c 复制
vmap <C-c> "+y
"去空行  
nnoremap <F2> :g/^\s*$/d<CR> 
"比较文件  
nnoremap <C-F2> :vert diffsplit 
"新建标签  
map <M-F2> :tabnew<CR>  
"列出当前目录文件  
map <F3> :tabnew .<CR>  
"打开树状文件目录  
map <C-F3> \be  
"C，C++ 按F5编译运行
map <F5> :call CompileRunGcc()<CR>
func! CompileRunGcc()
	exec "w"
	if &filetype == 'c'
		exec "!g++ % -o %<"
		exec "! ./%<"
	elseif &filetype == 'cpp'
		exec "!g++ % -o %<"
		exec "! ./%<"
	elseif &filetype == 'java' 
		exec "!javac %" 
		exec "!java %<"
	elseif &filetype == 'sh'
		:!./%
	elseif &filetype == 'py'
		exec "!python %"
		exec "!python %<"
	endif
endfunc
"C,C++的调试
map <F8> :call Rungdb()<CR>
func! Rungdb()
	exec "w"
	exec "!g++ % -g -o %<"
	exec "!gdb ./%<"
endfunc


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""实用设置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 设置当文件被改动时自动载入
set autoread
" quickfix模式
autocmd FileType c,cpp map <buffer> <leader><space> :w<cr>:make<cr>
"代码补全 
set completeopt=preview,menu 
"允许插件  
filetype plugin on
"共享剪贴板  
set clipboard+=unnamed 
"从不备份  
set nobackup
"make 运行
:set makeprg=g++\ -Wall\ \ %
"自动保存
set autowrite
set ruler                   " 打开状态栏标尺
set cursorline              " 突出显示当前行
set magic                   " 设置魔术
set guioptions-=T           " 隐藏工具栏
set guioptions-=m           " 隐藏菜单栏
"set statusline=\ %<%F[%1*%M%*%n%R%H]%=\ %y\ %0(%{&fileformat}\ %{&encoding}\ %c:%l/%L%)\
" 设置在状态行显示的信息
set foldcolumn=0
set foldmethod=indent 
set foldlevel=3 
set foldenable              " 开始折叠
" 不要使用vi的键盘模式，而是vim自己的
set nocompatible
" 语法高亮
set syntax=on
" 去掉输入错误的提示声音
set noeb
" 在处理未保存或只读文件的时候，弹出确认
set confirm
" 自动缩进
set autoindent
set cindent
" Tab键的宽度
set tabstop=4
" 统一缩进为4
set softtabstop=4
set shiftwidth=4
" 不要用空格代替制表符
set noexpandtab
" 在行和段开始处使用制表符
set smarttab
" 显示行号
set number
" 历史记录数
set history=1000
"禁止生成临时文件
set nobackup
set noswapfile
"搜索忽略大小写
set ignorecase
"搜索逐字符高亮
set hlsearch
set incsearch
"行内替换
set gdefault
"编码设置
set enc=utf-8
set fencs=utf-8,ucs-bom,shift-jis,gb18030,gbk,gb2312,cp936
"语言设置
set langmenu=zh_CN.UTF-8
set helplang=cn
" 我的状态行显示的内容（包括文件类型和解码）
"set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]\ %{strftime(\"%d/%m/%y\ -\ %H:%M\")}
"set statusline=[%F]%y%r%m%*%=[Line:%l/%L,Column:%c][%p%%]
" 总是显示状态行
set laststatus=2
" 命令行（在状态行下）的高度，默认为1，这里是2
set cmdheight=2
" 侦测文件类型
filetype on
" 载入文件类型插件
filetype plugin on
" 为特定文件类型载入相关缩进文件
filetype indent on
" 保存全局变量
set viminfo+=!
" 带有如下符号的单词不要被换行分割
set iskeyword+=_,$,@,%,#,-
" 字符间插入的像素行数目
set linespace=0
" 增强模式中的命令行自动完成操作
set wildmenu
" 使回格键（backspace）正常处理indent, eol, start等
set backspace=2
" 允许backspace和光标键跨越行边界
set whichwrap+=<,>,h,l
" 可以在buffer的任何地方使用鼠标（类似office中在工作区双击鼠标定位）
set mouse=a
set selection=exclusive
set selectmode=mouse,key
" 通过使用: commands命令，告诉我们文件的哪一行被改变过
set report=0
" 在被分割的窗口间显示空白，便于阅读
set fillchars=vert:\ ,stl:\ ,stlnc:\
" 高亮显示匹配的括号
set showmatch
" 匹配括号高亮的时间（单位是十分之一秒）
set matchtime=1
" 光标移动到buffer的顶部和底部时保持3行距离
set scrolloff=3
" 为C程序提供自动缩进
set smartindent
" 高亮显示普通txt文件（需要txt.vim脚本）
au BufRead,BufNewFile *  setfiletype txt
"自动补全
:inoremap ( ()<ESC>i
:inoremap ) <c-r>=ClosePair(')')<CR>
":inoremap { {<CR>}<ESC>O
":inoremap } <c-r>=ClosePair('}')<CR>
:inoremap [ []<ESC>i
:inoremap ] <c-r>=ClosePair(']')<CR>
:inoremap " ""<ESC>i
:inoremap ' ''<ESC>i
function! ClosePair(char)
	if getline('.')[col('.') - 1] == a:char
		return "\<Right>"
	else
		return a:char
	endif
endfunction
filetype plugin indent on 
"打开文件类型检测, 加了这句才可以用智能补全
set completeopt=longest,menu
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



"NERDtee设定
let NERDChristmasTree=1
let NERDTreeAutoCenter=1
let NERDTreeBookmarksFile=$VIM.'\Data\NerdBookmarks.txt'
let NERDTreeMouseMode=2
let NERDTreeShowBookmarks=1
let NERDTreeShowFiles=1
let NERDTreeShowHidden=1
let NERDTreeShowLineNumbers=1
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
nnoremap f :NERDTreeToggle
map <F7> :NERDTree<CR>  

```



## hosts配置路径

```
/etc/hosts or C:\Windows\system32\drivers\etc\hosts
```



# command

## 命令帮助

```
whatis		命令的简要说明
info		命令更详细的说明
man			命令的具体参数及使用方法

which		命令的位置 (程序的binary文件所在路径), 不适用内建命令如:cd
whereis		命令的搜索路径 (当系统中安装了同一软件的多个版本时，不确定使用的是哪个版本时可用)

查看参数	[command] -h

总结:		whatis info man which whereis
```



## 文件及目录管理

```
创建和删除
	mkdir
	rm, rm -r	( find ./ -name "a.txt" -exec rm {}; )
	mv, mv -r
	cp, cp -r
目录切换:  cd
查看当前目录:  pwd

给文件增加别名 (创建符号链接/硬链接)
- 硬链接
	ln name1 name2
- 软连接
    ln -s name1 name2
    
管道和重定向
- 批处理命令连接执行使用 |
- 串联使用分号 ;
- 前面成功，则执行后面一条，否则，不执行:  &&
- 前面失败，则后一条执行: ||
	ls /proc && echo  suss! || echo failed.
	等价于:  if ls /proc; then echo suss; else echo fail; fi
- 将标准输出和标准错误重定向到同一文件；
	ls  proc/*.c > list 2> &l
	等价于: ls  proc/*.c &> list
- 清空文件
	> a.txt
- 重定向
	echo aa >> a.txt

综合应用
- 查找record.log中包含AAA，但不包含BBB的记录的总数:
	cat -v record.log | grep AAA | grep -v BBB | wc -l
```



### 查看文件内容

```
[ cat / vi / head / tail / more / less ] -h
- 显示行号
	cat -n
- 只看前10行
	head -10 **
- 显示文件倒数第五行
	tail -5 xxx
- 动态显示文本最新内容
	tail -f xxx
- 查看两个文件差别
	diff xxx yyy
	
查找文件内容:  egrep --help
```

### 文件与目录权限修改

```
改变文件的所有者:`
	sudo chown user1 FILE
改变文件的所属组:`
	sudo chgrp grp1 FILE
改变文件所有者和所属组:
	sudo chown user1:grp1 FILE
- 递归子目录修改： 
	sudo chown -R tuxapp source/
	
改变读、写、执行等权限:
	A.文字设定法:  chmod [who][+|-|=][mode] FILE
		[who]:
            文件所有者: u
            文件所属组: g
            其他人:	o
            所有人:	a
        [+|-|=]:
        	+:	添加权限
        	-:	减少权限
        	=:	覆盖之前的权限
        [mode]:
        	r:	可读
        	w:	可写
        	x:	可执行
	B.数字设定法:  chmod [+|-|=][?] FILE
		-:	没有权限
		r: 4
		w: 2
		x: 1
		chmod 765 FILE: 		# 默认为 =
			7: rwx -- 文件所有者
			6: rw  -- 文件所属组
			5: rx  -- 其他人
- 增加脚本可执行权限： 
	chmod a+x myscript
	
目录在创建后默认都带有可执行权限, 否则cd/ls时无法查看, 会提示权限不够
```



## 文件及目录属性

### wc, od

```
统计文本行数和字符:  wc [文本文件路径]
统计目录下文件个数:  find ./ | wc -l

$ wc hello.py
3  4  45  hello.py    # 行数  字数  字符数  文件名,  字数是以空格分开来计算

查看二进制文件
	- od [二进制文件路径]
```

### du, df

```
查看文件大小
	du -h		# Human, 以人类可理解的方式显示
查看磁盘大小
	df -h
```



## 文本处理

find、grep、xargs、sort、uniq、tr、cut、paste、wc、sed、awk

### find/locate文件查找

```
find/locate
- 查看当前目录下文件个数:  
	find ./ | wc -l
- 查看时给每项文件前面增加一个id编号:
	ll | cat -n
- 递归当前目录及子目录删除所有.o文件:
	find ./ -name "*.o" -exec rm {} \;
- 更快的查询:
	locate -h
	locate会为文件系统建立索引数据库，如果有文件更新，需要定期执行更新命令来更新索引库, 命令为 updatedb


查找txt和pdf文件:
	find . \( -name "*.txt" -o -name "*.pdf" \) -print
正则查找
	find . -regex  ".*\(\.txt|\.pdf\)$"
正则忽略大小写
	-iregex
反向查找
	find . ! -name "*.txt" -print
指定深度
	find . -maxdepth 1 -type f
```



**定制搜索**

```
按类型搜索  -type
	find . -type d -print  //只列出所有目录
	-type f  # 文件
	-type l  # 符号链接
	-type d  # 目录
	二进制文件和文本文件无法直接通过find的类型区分出来

检查文件具体类型（二进制或文本）
	file
	file redis-cli  # 二进制文件
- 查找本地目录下的所有二进制文件
	ls -lrt | awk '{print $9}'|xargs file|grep  ELF| awk '{print $1}'|tr -d ':'

按时间搜索
	-atime 访问时间 (单位:天，分钟单位则是-amin，以下类似）
	-mtime 修改时间 （内容被修改）
	-ctime 变化时间 （元数据或权限变化）
- 最近第7天被访问过的所有文件
	find . -atime 7 -type f -print
- 最近7天内被访问过的所有文件
	find . -atime -7 -type f -print
- 7天前被访问过的所有文件
	find . -atime +7 type f -print

按大小搜索   -size
- 寻找大于2k的文件
	find . -type f -size +2k

按权限查找   -perm
- 找具有可执行权限的所有文件
	find . -type f -perm 644 -print
	
按用户查找   -user
- 找用户weber所拥有的文件
	find . -type f -user weber -print
```



**查找的后续动作**

```
删除
- 删除当前目录下所有的swp文件:
	find . -type f -name "*.swp" -delete
	另一种语法:
	find . type f -name "*.swp" | xargs rm
执行动作（强大的exec）
- 将当前目录下的所有权变更为weber:
	find . -type f -user root -exec chown weber {} \;
	注：{}是一个特殊的字符串，对于每一个匹配的文件，{}会被替换成相应的文件名；
- 将找到的文件全都copy到另一个目录:
	find . -type f -mtime +10 -name "*.txt" -exec cp {} OLD \;
- 结合多个命令
	如果需要后续执行多个命令，可以将多个命令写成一个脚本。然后 -exec 调用时执行脚本即可:
	-exec ./commands.sh {} \;

-print的定界符
默认使用’\n’作为文件的定界符；
-print0 使用’\0’作为文件的定界符，这样就可以搜索包含空格的文件；
```



### grep 文本内容搜索

```
grep -r "查找的字符串" 查找路径		# 与find不同: find 查找路径 "文件名字符串"
```



### xargs 命令行参数转换

### sort 排序

env | sort

### uniq 消除重复行

### 用tr进行转换

### cut 按列切分文本

### paste 按列拼接文本

### sed 文本替换利器

### awk 数据流处理工具





# Ubuntu软件的安装和卸载

## a 在线安装

```
A. apt-get 安装 tree 软件
    安装	sudo apt-get install tree
    卸载	sudo apt-get remove tree
    更新软件列表	sudo apt-get update		(从下载源更新本地软件列表)
    清理所有安装包 sudo apt-get clean		(清理的是 /var/cache/apt/archives/ 下的 .deb)

B. aptitude 安装 tree 软件
	安装	sudo aptitude install tree
	重装	sudo aptitude reinstall tree
	更新	sudo apt-get update
	移除	sudo aptitude remove tree
	显示状态  sudo aptitude show tree
```

## b deb包安装

```
下载deb包到本地	xxx.deb
安装	sudo dpkg -i xxx.deb
删除	sudo dpkg -r xxx
```

## c 源码安装

```
1. 解压缩
2. 进入安装目录
3. 检测编译环境 & 创建Makefile: ./configure
4. 编译源码, 生成库和可执行程序: make
5. 把库和可执行程序 安装到系统目录下: sudo make install
6. 删除和卸载软件:  sudo make distclean
以上安装过程不是绝对的, 需要先看源码附带的 README 文件, 如 ./configure 执行时加参数
```





# 磁盘管理

## 磁盘信息

```
设备都保存在 /dev 中, 磁盘设备种类:
    sd: SCSI Device, 如: /dev/sda1
    hd: Hard Disk, 硬盘
    fd: Floppy Disk, 软盘

磁盘1: sda
	主分区:   最多允许有 4 个, 主分区1~4: sda1~sda4
	扩展分区: 第一个逻辑分区从 sda5 开始, 主分区5~xx: sda5~...
	
磁盘2: sdb
磁盘3: sdc
磁盘4: sdd
```

## mount 挂载

系统默认挂载目录:   `/media`

手动挂载目录: `/mnt`

挂载方式:

```
mount 设备名 挂载目录
	- 查看设备名: sudo fdisk -l
	- 挂载目录: 默认手动挂载到 /mnt, 如果手动挂载到非 /mnt 目录下, 挂载成功后会临时覆盖目录中原有内容, 卸载设备后能恢复目录中原有数据.
	- 例: sudo mount  /dev/sdb1  /home/lqq
```

````
mount [deviceName] [path]

fdisk -l
````

## umount 卸载

卸载时,  用户的当前位置不能在 `/mnt`  `/media` 或其子目录下,  否则无法卸载

```
sudo umount /mnt
sudo umount /home/lqq
```





# 压缩包管理

## tar

参数

```
c	创建 -- 打包
x	释放 -- 解包
v	提示
f	指定打包后的文件名

z	使用 gzip 方式压缩  -- .gz
j	使用 bizp2 方式压缩 -- .bz2
```

压缩

```
tar zcvf xxx.tar.gz *.txt dir/
tar jcvf xxx.tar.bz2 *.txt dir/
```

解压

```
tar zxvf xxx.tar.gz
tar zxvf xxx.tar.gz TargetPath
tar jxvf xxx.tar.bz2
tar jxvf xxx.tar.bz2 TargetPath
```

## rar

需要先手动安装 rar 软件:  `sudo apt-get install rar`

```
参数
    a	压缩
    x	解压
压缩
	rar a xx TargetFile
解压
	rar x xx.rar
	rar x xx.rar TargetPath
```

## zip

```
zip xx TargetFile
zip xx -r 目录	# 压缩目录要加 -r 参数
unzip xx.zip
unzip xx.zip -d TargetPath
```

 



# 用户管理

## 创建用户--useradd

```
groupadd g1
useradd -s /bin/bash -g g1 -d /home/Tom -m Tom
su - Tom
passwd Tom  # 或passwd, 直接修改当前用户密码
```

## 创建用户--adduser

```
adduser tom # 自动创建用户组(如果组不存在), 自动创建用户目录
			# adduser不支持用户名包含大写, 如Tom

root@ubuntu:~#  adduser temp-user
Adding user temp-user' ...
Adding new grouptemp-user' (1001) ...
Adding new user temp-user' (1001) with grouptemp-user' ...
Creating home directory /home/temp-user' ...
Copying files from/etc/skel' ...
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
Changing the user information for temp-user
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] y
```

## 删除用户--userdel

```
userdel -r Tom  # -r: 将用户的主目录一起删除
```

## 删除用户--deluser

```
deluser Tom    # 自动将用户的主目录一起删除
```





# ftp服务器搭建 - vsftpd

提供文件的上传和下载服务

安装:

```
apt install vsftpd
```

## 服务端

修改配置文件

```
/etc/vsftpd.conf

anonymous_enable=YES	# 允许匿名用户登录
write_enable=YES		# 实名登录用户拥有写权限(上传)
local_umask=022			# 设置本地掩码 022
anon_upload_enable=YES	# 匿名用户可上传数据
anon_mkdir_write_enable=YES	# 匿名用户可创建目录
```

重启服务

```
service vsftpd restart
```

## 客户端

实名用户登录

```
ftp IP
输入用户名, 密码

文件上传:  put FILE
文件下载:  get FILE
ftp不允许操作目录, 需要先打包
```

匿名用户登录

```
不允许匿名用户在任意目录下切换,  需要在ftp服务器上创建一个匿名用户的根目录, 不能切换到根目录外的其他目录
vim /etc/vsftpd.conf
anon_root=/home/temp/	# 匿名用户登录ftp时, 会显示为 /
service vsftpd restart

ftp IP
输入用户名: anonymous
密码: 回车
```

lftp客户端访问ftp服务器

```
apt-get install lftp

mget
mput
mirror 		下载整个目录及其子目录
mirror -R	上传整个目录及其子目录
```



# nfs服务器搭建

net file system 网络文件系统, 允许网络中的计算机之间通过Tcp/IP网络共享资源

## 服务器

安装

```
apt-get install nfs-kernel-server
```

创建共享目录

```
/home/share
```

修改配置

```
vim /etc/exports

写入共享目录的绝对路径 和 对应权限
/home/share *(ro, sync, no_root_squash)
    # ro: 可读写
    # sync: 实时更新本地数据
```

重启

```
sudo service nfs-kernel-server restart
```

## 客户端

挂载服务器共享目录

```
sudo mount IP:/home/share /mnt
```



# ssh服务器

## 服务器

安装 ssh

```
apt-get install openssh-server
```

查看是否安装

```
aptitude show openssh-server
```

## 客户端

远程登录

```
ssh IP
ssh 用户名@IP
ssh root@IP
```

退出登录:  logout



# vim分屏

末行模式下:

`sp`  以水平分割线将屏幕分为两部分, 显示两个相同文件的内容

`vsp` 以垂直分割线将屏幕分为两部分, 显示两个相同文件的内容

`sp/vsp 文件名`,  分屏,  显示两个不同文件的内容

`wqall` 保存并退出所有屏幕

`wq` 保存并退出光标所在屏幕

`Ctrl + ww`  在屏幕之间切换



`!ls`  执行bash下的 ls 命令









































