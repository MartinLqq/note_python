

# Chrome github 插件神器

- 不翻墙访问不了谷歌商店,  可以使用 收藏猫网页 来下载谷歌浏览器插件,   手动安装
- 收藏猫插件商店:   https://pictureknow.com/extensions 

Tip:  下载 Chrome插件 收藏猫,  就可以快速进入 收藏猫的插件商店 了.





## octotree / octotree pro

- github 侧边文件树 Chrome插件

直接下载 octotree 插件,  并进入 github 任意一个仓库使用时,  可能出现 `Error: Connection error`,

这是因为 github 在 API 访问时限制了访问速率,  解决 API 访问受限问题的方法:

```
github需要我们设置一个token作为访问令牌，提升访问速率, 设置路径:
Settings -> Developer settings -> Personal access tokens
生成一个 token 即可.
```

## sourcegraph

- 别样的 github 阅读体验

- sourcegraph插件安装好后会在github仓库页面中显示一个按钮,  点击按钮跳转到  sourcegraph.com

- sourcegraph插件做的事情简单来说就是 拼接一个 URL 并访问,  如

  ```
  https://sourcegraph.com/github.com/LQQXR/DjangoBlog
  
  # 1. https://sourcegraph.com/
  # 2. github.com/LQQXR/DjangoBlog
  ```



# Chrome 使用技巧

## 分屏

需求:  浏览某个页面时,  需要在当前页面下分屏 (两屏)

实现:

1. 打开一个新的标签页

2. 点击收藏按钮,  点击更多

3. 在弹框中的 URL 输入框中输入以下 JS 代码

   ```javascript
   javascript:document.write('<HTML><HEAD></HEAD><FRAMESET COLS=\'50%25,*\'><FRAME SRC=' + location.href + '><FRAME SRC=' + location.href + '></FRAMESET></HTML>')
   ```

4. 保存标签,  命名为 分屏

5. 打开目标页面,  点击一下新创建的 分屏 标签

6. 查看效果



# github高级搜索

## 资源

- [About searching on GitHub](https://help.github.com/en/github/searching-for-information-on-github/about-searching-on-github)
  - [Repositories](https://help.github.com/en/articles/searching-for-repositories)
  - [Topics](https://help.github.com/en/articles/searching-topics)
  - [Issues and pull requests](https://help.github.com/en/articles/searching-issues-and-pull-requests)
  - [Code](https://help.github.com/en/articles/searching-code)
  - [Commits](https://help.github.com/en/articles/searching-commits)
  - [Users](https://help.github.com/en/articles/searching-users)
  - [Packages](https://help.github.com/en/github/searching-for-information-on-github/searching-for-packages)
  - [Wikis](https://help.github.com/en/articles/searching-wikis) 

## 高级搜索页面

- 链接:  https://github.com/search/advanced
- 根据多种条件自动生成高级搜索的搜索方式,  入门学习时可参考

## 普通搜索框

- 在 github 普通搜索输入框中输入高级搜索条件,  

## 高级搜索指南

- 参考CSDN:  [高级搜索方式](https://blog.csdn.net/qq_15071263/article/details/86561562?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)

### in:name

项目名称

```
// 仓库名称 中包含你搜索的文本的仓库
// 关键词 可以放在条件之前
in:name 关键词
```

### in:descripton

项目描述

```
// 仓库描述 中包含你搜索的文本的仓库
in:descripton 关键词
```

### in:readme

readme文件

```
// readme 文件中包含你搜索的文本的仓库
in:readme 关键词
```

### in:path

### in:file

###  filename:*FILENAME*

###  extension:*FIEL_EXTENSION* 



### stars:>500

star 数量

```
// star 数量大于500的项目
stars: > 500
// star 数量在10-20之间的仓库
stars: 10..20 关键词
```

### fork:>500

fork 数量

```
// fork 数量大于500的项目
fork: > 500
// fork 数量在10-20之间的仓库
fork: 10..20 关键词
```

### size:>=5000

仓库大小

```
// 单位是KB
// 仓库大于5000KB的仓库
size:>=5000 关键词
```

### pushed:>2020-01-01

最近更新时间

```
// 最近一次提交在2019年以后的仓库
pushed:>2019-01-01 关键词
```

8、仓库创建时间

```
// 2019年以后创建的仓库
created:>2019-01-01 关键词
```

### license:apache-2.0

license

```
// 使用 apache-2.0 协议的仓库
license:apache-2.0 关键词
```

### language:python

仓库开发语言

```
// 用java 语言写的仓库
language:java 关键词
```

### user:kennethreitz

仓库持有者

```
// 用户google 上传的仓库
user:google 关键词
```

### org:spring-cloud

组织机构代码

```
// 列出org 的 spring-cloud  仓库
org:spring-cloud 
```

### 组合条件

```
// 多条件组合，中间加个空格就行
user:google language:java
language:python scrapy stars:>10000

// 一个条件有多个内容, 用逗号分隔
python in:file,path
```







# 百度高级搜索

## filetype:pdf

filetype加上冒号，后面跟上文档格式，可以搜索特定的文档。

```
filetype:pdf django
```

## intitle:菜鸟教程

搜索范围限定在网页标题

```
intitle:菜鸟教程 django
```

## site:python.org

搜索范围限定在特定站点中

```
site:python.org
site:python.org pathlib
```

## inurl:runoob

搜索范围限定在url链接中

```
inurl:runoob
inurl:runoob django
```

## +  和  -

+包含特定查询词，-不包含特定查询词

```
flask-socketio +中文
```

## |

或

```
flask|django
```

