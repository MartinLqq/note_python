



# git基础

### 集中式vs分布式

- 集中式的版本控制系统:  `CVS`,  `SVN`

  ```
  版本库是集中存放在中央服务器的，而干活的时候，用的都是自己的电脑，所以要先从中央服务器取得最新的版本，然后开始干活，干完活了，再把自己的活推送给中央服务器。
  
  集中式版本控制系统最大的毛病就是必须联网才能工作.
  ```

-  分布式版本控制系统:  `Git`

  ```
  分布式版本控制系统根本没有“中央服务器”，每个人的电脑上都是一个完整的版本库.
  
  安全性更高:
  和集中式版本控制系统相比，分布式版本控制系统的安全性要高很多，因为每个人电脑里都有完整的版本库，某一个人的电脑坏掉了不要紧，随便从其他人那里复制一个就可以了。而集中式版本控制系统的中央服务器要是出了问题，所有人都没法干活了。
  
  "交换"修改:
  在实际使用分布式版本控制系统的时候，其实很少在两人之间的电脑上推送版本库的修改，因为可能你们俩不在一个局域网内，两台电脑互相访问不了。因此，分布式版本控制系统通常也有一台充当“中央服务器”的电脑，但这个服务器的作用仅仅是用来方便“交换”大家的修改，没有它大家也一样干活，只是交换修改不方便而已。
  ```

分布式版本控制系统除了Git以及促使Git诞生的`BitKeeper`外，还有类似Git的`Mercurial`和`Bazaar`等。这些分布式版本控制系统各有特点，但最快、最简单也最流行的依然是Git！ 



理解:

```
本地、服务器、中央服务器（远程服务器）。

每一次commit是提交到本本机的服务器，这个不需要联网，正所谓的版本管理，就是要方便我们知道每一个版本，比如回到之前的某个版本（这是其一），而且回退到某个之前的版本，也是从本机的服务器拿的数据，这些都不需要联网。而 SVN 的每一次 commit 都需要联网，这就需要网络的等待。 Git只有在Push、pull 的时候需要联网，而我们平时更多的操作应是commit。

再有就是，断网的情况下，SVN也能工作，但是由于没有版本控制的记录，当多人修改后就比较难以快速的合并，但是Git都在本地保存了版本记录，所以大家合并起来就方便得多了。
```



### 只跟踪文本文件

- 所有的版本控制系统，其实只能跟踪文本文件的改动，比如TXT文件，网页，所有的程序代码等等.
- 版本控制系统可以告诉你每次的改动，比如在第5行加了一个单词“Linux”，在第8行删了一个单词“Windows”。
- 而图片、视频这些二进制文件，虽然也能由版本控制系统管理，但没法跟踪文件的变化，只能把二进制文件每次改动串起来，也就是只知道图片从100KB改成了120KB，但到底改了啥，版本控制系统不知道，也没法知道。 

### 基本操作

git init: 初始化一个Git仓库

git add: 把工作区的修改，提交到暂存区

git status: 查看当前仓库的状态

git diff: 查看修改的内容 

git commit: 把暂存区的修改，保存至本地库

git push: 把本地库的记录，推送至远程库

git log:  查看从最近到最远的提交日志

```
git add <file> 可反复多次使用，添加多个文件；可一次添加多个文件

git log时只查看简短信息:
	git log --oneline
	git log --pretty=oneline
```



### 版本回退









# git使用技巧

- Git 官方 Pro Git文档: https://git-scm.com/book/zh/v1

- Git的三种Workflow及相关概念: https://note.qidong.name/2019/04/git-workflow/





### 本地修改暂存与恢复

```bash
# 暂存本地修改的内容
git stash
# 拉远程新代码
git pull origin master
# 恢复本地修改的内容
git stash pop
```

`git stash` 暂存的内容,  可 `git check other_branch` 切换到另一分支下 `git stash pop`



### 关闭 Merge 的自动提交

```bash
git config --global pull.rebase true
```



### 反转某次提交

只撤销指定commit_ID那次提交

```bash
git revert commit commit_ID
```



### 回到指定提交

撤销到指定commit_ID的所有提交

```bash
git reset --hard commit_ID
```

撤销上面的 `撤销到指定commit_ID的所有提交`

```bash
git reflog  # 找到commit_ID
git reset --hard commit_ID
```



### git pull

```shell
git pull --rebase   # rebase只适合解决一次冲突中只涉及少次数的提交???
```



### git log

```shell
# 查看简版commit记录
git log --oneline
# 查看图形化commit记录
git log --oneline --graph
```



### git commit

```shell
git commit -a
```







# git配置

## git pull push 免密码

方法一

```
1： 进入当前用户目录下；
2： vi .git-credentials 文件
3：输入：https://{username}：{password}@github.com
4：保存退出后执行:git config --global credential.helper store
执行完后
/home/用户名/.gitconfig 会新增一项
helper = store
这时再执行git push/pull的时候就不需要输入密码
```

方法二

```
git config --global credential.helper store
git pull /git push (这里需要输入用户名和密码，以后就不需要)
```



## git SSH 配置

Git安装完之后，需要做最后一步配置，如果你没有做这项配置，是没有 git 公钥和私钥的，而上传代码到远程仓库的时候需要秘钥进行验证是否本人上传的，想要创建可以使用下面的方法：

分别执行以下两句命令

```csharp
git config --global user.name “用户名”
git config --global user.email “邮箱”
```

SSH配置

1. 查看是否已配置SSH:  `cd ~/.ssh`
2. 生成公钥和私钥:  `ssh-keygen -t rsa`   回车3下
3. 上一步会在一个 `~/.ssh/` 下生成一个私钥 id_rsa 和一个公钥 id_rsa.pub
4. 查看公钥并复制:  `cat ~/.ssh/id_rsa.pub`  
5. 粘贴到 github / gitee 上的配置中



## 添加远程地址

```shell
git remote add [name] [ssh/https...xx.git]
# 默认的远程name是origin, 新增地址可设置为source, new, ...

# 查看远程地址
git remote -v
```



## 3种级别的 config

1. 仓库级

   ```shell
   配置路径:	.git/config
   查看命令:	git config --local -l
   ```

2. 全局级

   ```shell
   配置路径:	~/.gitconfig
   查看命令:	git config --global -l
   ```

3. 系统级

   ```shell
   配置路径:	/etc/gitconfig
   查看命令:	git config --system -l
   ```

查看当前生效的配置:

```shell
git config -l
```

配置搜索顺序:

```
系统级 -> 全局级 -> 仓库级
```

配置权重:

```
仓库级 > 全局级 > 系统级
```



# git fork解决冲突工作流

```shell
git log
git reset --hard [commit_id]
git status
git remote -v  # 查看远程地址
# 从主线上的仓地址 rebase (fork后的远程仓地址的name是 `origin`)
* git rebase [name]/master   # 如 git rebase source/master
git status
循环执行:
    ------------------------
    | 查找被标记有冲突的代码, 保留需要的内容(交叉时各取所需)
    | git add [...]
    | git rebase --continue
    | 若完成解冲突, 会提示一些: Applying: commit `commit msg1`
    | 若未完成, 重复此循环
    ------------------------
解决冲突后, 若还需要改代码, 修改好后三步走:
    git add [...]
    git commit -m "Fix conflix."
    git push origin HEAD:master
若提示分支无更新, 导致无法push, 则强制 push:
	git push origin HEAD:master -f
```



# 在任意路径下执行git

```shell
# 如 git status
git --git-dir xxx/proj/.git --work-tree xxx/proj status
```





# python库操作git

`< From yanqidong >`

## GitPython

**GitPython简介**

[GitPython](https://github.com/gitpython-developers/GitPython)是一个与Git库交互的Python库，包括底层命令（Plumbing）与高层命令（Porcelain）。 它可以实现绝大部分的Git读写操作，避免了频繁与Shell交互的畸形代码。 它并非是一个纯粹的Python实现，而是有一部分依赖于直接执行`git`命令，另一部分依赖于[GitDB](https://github.com/gitpython-developers/gitdb)。

[GitDB](https://github.com/gitpython-developers/gitdb)也是一个Python库。 它为`.git/objects`建立了一个数据库模型，可以实现直接的读写。 由于采用流式（stream）读写，所以运行高效、内存占用低。

**GitPython安装**

```sh
pip3 install GitPython
```

其依赖[GitDB](https://github.com/gitpython-developers/gitdb)会自动安装，不过可执行的`git`命令需要额外安装。

**基本用法**

- init

```python
import git
repo = git.Repo.init(path='.')
```

这样就在当前目录创建了一个Git库。 当然，路径可以自定义。

由于`git.Repo`实现了`__enter__`与`__exit__`，所以可以与`with`联合使用。

```python
with git.Repo.init(path='.') as repo:
    # do sth with repo
```

不过，由于只是实现了一些清理操作，关闭后仍然可以读写，所以使用这种形式的必要性不高。



- clone

clone分两种。 一是从当前库clone到另一个位置：

```python
new_repo = repo.clone(path='../new')
```

二是从某个URL那里clone到本地某个位置：

```python
new_repo = git.Repo.clone_from(url='git@github.com:USER/REPO.git', to_path='../new')
```



- commit

```python
with open('test.file', 'w') as fobj:
    fobj.write('1st line\n')
repo.index.add(items=['test.file'])
repo.index.commit('write a line into test.file')

with open('test.file', 'aw') as fobj:
    fobj.write('2nd line\n')
repo.index.add(items=['test.file'])
repo.index.commit('write another line into test.file')
```



- status

[GitPython](https://github.com/gitpython-developers/GitPython)并未实现原版`git status`，而是给出了部分的信息。

```python
>>> repo.is_dirty()
False
>>> with open('test.file', 'aw') as fobj:
>>>     fobj.write('dirty line\n')
>>> repo.is_dirty()
True
>>> repo.untracked_files
[]
>>> with open('untracked.file', 'w') as fobj:
>>>     fobj.write('')
>>> repo.untracked_files
['untracked.file']
```



- checkout（清理所有修改）

```python
>>> repo.is_dirty()
True
>>> repo.index.checkout(force=True)
<generator object <genexpr> at 0x7f2bf35e6b40>
>>> repo.is_dirty()
False
```



- branch

获取当前分支：

```python
head = repo.head
```

新建分支：

```python
new_head = repo.create_head('new_head', 'HEAD^')
```

切换分支：

```python
new_head.checkout()
head.checkout()
```

删除分支：

```python
git.Head.delete(repo, new_head)
# or
git.Head.delete(repo, 'new_head')
```



- merge

以下演示如何在一个分支（`other`），merge另一个分支（`master`）。

```python
master = repo.heads.master
other = repo.create_head('other', 'HEAD^')
other.checkout()
repo.index.merge_tree(master)
repo.index.commit('Merge from master to other')
```



- remote, fetch, pull, push

创建remote：

```python
remote = repo.create_remote(name='gitlab', url='git@gitlab.com:USER/REPO.git')
```

远程交互操作：

```python
remote = repo.remote()
remote.fetch()
remote.pull()
remote.push()
```

删除remote：

```python
repo.delete_remote(remote)
# or
repo.delete_remote('gitlab')
```



- 其它

其它还有Tag、Submodule等相关操作，不是很常用。

[GitPython](https://github.com/gitpython-developers/GitPython)的优点是 `在做读操作时可以方便地获取内部信息`，缺点是`在做写操作时会感觉很不顺手`。 当然，它还支持直接执行`git`操作。

```python
git = repo.git
git.status()
git.checkout('HEAD', b="my_new_branch")
git.branch('another-new-one')
git.branch('-D', 'another-new-one')
```



## 其它操作Git的方法

- subprocess

这就是所谓『老路』。 在另一个进程，执行Shell命令，并通过stdio来解析返回结果。

```python
import subprocess
subprocess.call(['git', 'status'])

subprocess.Popen()
```



- dulwich

[dulwich](https://github.com/jelmer/dulwich)是一个纯Python实现的Git交互库。

官方网站：https://www.dulwich.io/



- pygit2

[pygit2](https://github.com/libgit2/pygit2)是基于[libgit2](https://libgit2.github.com/)实现的一个Python库。 底层是C，而上层Python只是接口，运行效率应该是最高的。 其缺点是，需要环境中预先安装[libgit2](https://libgit2.github.com/)。 相比之下，[GitPython](https://github.com/gitpython-developers/GitPython)只需要环境预置Git，简单多了。

官方网站：http://www.pygit2.org/

