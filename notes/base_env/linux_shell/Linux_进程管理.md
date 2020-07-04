# Linux 进程管理

### 查看进程
```
查看进程:   ps
查看进程树:  pstree
查找与指定条件匹配的进程: pgrep
    ps -ef | grep python
    pgrep -f python   # 不指定其他选项时, 只返回进程号 (pgrep --help)
实时监控进程占用资源状况: top
    -c - 显示进程的    整个路径。
    -d - 指定两次刷屏之间的间隔时间（秒为单位）。
    -i - 不显示闲置进程或僵尸进程。
    -p - 显示指定进程的信息。
```


### 终止进程
1- 通过进程号终止进程: kill
```
[root ~]$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
[root ~]# kill 1234
[root ~]# kill -9 1234
```
2- 通过进程名终止进程: pkill
```
结束名为mysqld的进程。
 [root ~]# pkill mysqld
结束hellokitty用户的所有进程。
 [root ~]# pkill -u hellokitty
 说明：这样的操作会让hellokitty用户和服务器断开连接。
```


### 进程切换到前台/后台

1-将进程置于后台运行/停止
```
Ctrl+Z - 快捷键，用于停止进程并置于后台。
& - 将进程置于后台运行。
[root ~]# mongod &
[root ~]# redis-server
...
^Z
[4]+  Stopped                 redis-server
```

2- 查询后台进程: jobs
```
[root ~]# jobs
[2]   Running                 mongod &
[3]-  Stopped                 cat
[4]+  Stopped                 redis-server
```

3- 让进程在后台继续运行: bg
```
[root ~]# bg %4
[4]+ redis-server &
[root ~]# jobs
[2]   Running                 mongod &
[3]+  Stopped                 cat
[4]-  Running                 redis-server &
```

4-将后台进程置于前台: fg
```
[root ~]# fg %4
redis-server
说明：置于前台的进程可以使用Ctrl+C来终止它。
```

