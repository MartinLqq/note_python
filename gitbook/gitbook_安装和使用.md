# 安装和使用 GitBook

-  http://gitbook.hushuang.me/setup.html 



```bash
# 安装 gitbook-cli,  指定淘宝镜像地址
npm install gitbook-cli -g  --registry=https://registry.npm.taobao.org

# 在当前目录创建一本书 (会先下载 GitBook)
gitbook init

# 在指定路径下创建一本书
gitbook init ./directory
# gitbook init 会生成两个文件: README.md 和 SUMMARY.md

# 本地预览
gitbook serve
# 或构建静态网站
gitbook build

# 调试模式预览/构建静态网站
# gitbook serve ./ --log=debug --debug
gitbook build ./ --log=debug --debug

# gitbook 卸载
gitbook uninstall 3.2.3
```



 列出可用于安装的远程版本:   gitbook ls-remote 