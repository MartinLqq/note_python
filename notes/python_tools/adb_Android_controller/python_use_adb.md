# python与adb交互

1. 使用python的 `subprocess模块 + adb原始命令`

2. 使用python的 `PyADB` 模块,   **貌似不支持python3**

   Pip (Not always the latest version)

   ```bash
   $ sudo easy_install pyadb
   ```

   From source

   ```bash
   $ pytho3n setup.py build
   $ sudo python3 setup.py install
   ```

   Usage:

   ```python
   >>> from pyadb import ADB
   >>> adb = ADB('/home/chema/.android-sdks/platform-tools/adb')
   >>> adb.pyadb_version()
   '0.1.4'
   >>> adb.get_version()
   '1.0.32'
   ```



# adb-Android远程调控工具

Android Debug Bridge



## windows安装adb

1. 安装 ADB：
   http://adbshell.com/downloads, 下载ADB Kits, 得到 `adb.exe`  `AdbWinApi.dll`  `AdbWinUsbApi.dll` .
   将这三个文件都放到 `C:\Windows\System32` , 保险起见，同时拷贝这三个文件到 `C:\Windows\System`  及 `C:\Windows\SysWOW64`
   如果不拷贝到 `System/` 目录下有可能执行adb时会出错："找不到AdbWinApi.dll文件"
   如果不拷贝到 `Windows/SysWOW64/` 有可能执行adb时会出错: "CreateProcess failure. error 2"

2. 安装Android USB 驱动
   用usb连接pc机,  正常设备开启adb server后，连接上pc机时，pc机会自动装驱动,
   如果在设备管理器中没有找到 Android Phone设备则就手动装驱动,

   > 手动安装步骤如下:
   > 驱动下载路径：http://dl.adbdriver.com/upload/adbdriver.zip
   > 配置好工具和安装好驱动后，如有问题可拔掉usb重新连接，或者重新启动一下电脑。

3. 如果安装了驱动后，adb 连接不上，可尝试adb kill-server 再adb start-server下，还有就是检查手机端adb server是否正确开启。



## adb—命令大全

https://github.com/mzlogin/awesome-adb

或 https://www.cnblogs.com/zhuminghui/p/10457316.html

### 以 root 权限运行 adbd

1. 获取android root权限.  以魅蓝note1 (m1 note)为例,  在[设置]-[安全]-[ROOT 权限]中开启root用户权限

2. adb shell

3. shell@m1note:/ $ su

4. 在手机端点击允许root,  电脑cmd提示:

   enter main
   start command :am start -a android.intent.action.MAIN -n com.android.settings/com.meizu.settings.root.FlymeRootRequestActivity --ei uid 2000 --ei pid 11354 > /dev/null
   shell@m1note:/ #

完成.



### 模拟按键输入

> 基本命令

　　adb 模拟按键输入的命令主要通过 input 进行

```
Usage: input [<source>] <command> [<arg>...]
```

```
The sources are:
      mouse
      keyboard
      joystick
      touchnavigation
      touchpad
      trackball
      stylus
      dpad
      gesture
      touchscreen
      gamepad

The commands and default sources are:
      text <string> (Default: touchscreen)
      keyevent [--longpress] <key code number or name> ... (Default: keyboard)
      tap <x> <y> (Default: touchscreen)
      swipe <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen)
      press (Default: trackball)
      roll <dx> <dy> (Default: trackball)
```



> 常用命令

#### 物理键

```
adb shell input keyevent 26 # 电源键
adb shell input keyevent 82 # 菜单键
adb shell input keyevent 3 # HOME 键
adb shell input keyevent 4 # 返回键
adb shell input keyevent 24 # 音量+
adb shell input keyevent 25 # 音量-
adb shell input keyevent 164 # 静音 
```

#### 媒体控制

```
adb shell input keyevent 85 # 播放/暂停
adb shell input keyevent 86 # 停止播放
adb shell input keyevent 87 # 播放下一首
adb shell input keyevent 88 # 播放上一首
adb shell input keyevent 126 # 恢复播放
adb shell input keyevent 127 # 暂停播放
```

#### 点亮/熄灭屏幕

可以通过上 模拟电源键 来切换点亮和熄灭屏幕，但如果明确地想要点亮或者熄灭屏幕，那可以使用如下方法。

```
adb shell input keyevent 224 # 点亮屏幕
adb shell input keyevent 223 # 熄灭屏幕
```

#### 触击屏幕

```
adb shell input tap <X> <Y> # x，y为坐标位置
```

#### 滑动屏幕

划动屏幕用到了 swipe 命令，它有四个参数，分别是起始点x坐标 起始点y坐标 结束点x坐标 结束点y坐标。

如果锁屏没有密码，是通过滑动手势解锁，那么可以通过 `input swipe` 来解锁。

```
# 四个参数：起始点x坐标 起始点y坐标 结束点x坐标 结束点y坐标。
adb shell input swipe 300 1000 300 500 # 向上滑动
adb shell input swipe 300 100 300 1000 # 向下滑动
adb shell input swipe 1000 500 200 500 # 向左滑动
adb shell input swipe 200 500 1000 500 # 向右滑动
```

#### 输入文本

　　在焦点处于某文本框时，可以通过 input 命令来输入文本。

```
adb shell input text hello  # 输入hello
```

 



#### keyevent 命令大全

　　官方文档地址：[*https://developer.android.com/reference/android/view/KeyEvent*](https://developer.android.com/reference/android/view/KeyEvent)

　　中文keycode大全：*adb——keyevent命令大全*



### 查看手机设备信息

手机设备信息可以包括如下信息：

- 手机型号
- 电池状况
- 分辨率
- 屏幕密度
- 显示屏参数
- Android_id
- IMEI
- Android系统版本
- IP地址
- Mac地址
- CPU信息
- 内存信息



#### 查看手机型号

```
adb shell getprop ro.product.model
```

#### 查看电池状况

```
adb shell dumpsys battery

'''
Current Battery Service state:
  AC powered: false
  USB powered: true
  Wireless powered: false
  status: 2
  health: 2
  present: true
  level: 44
  scale: 100
  voltage: 3872
  temperature: 280
  technology: Li-poly
其中 scale 代表最大电量，level 代表当前电量。上面的输出表示还剩下 44% 的电量。
'''
```

#### 查看分辨率

```
adb shell wm size
'''
Physical size: 1080x1920    该设备屏幕分辨率为 1080px * 1920px。

如果使用命令修改过，那输出可能是：
Physical size: 1080x1920
Override size: 480x1024
表明设备的屏幕分辨率原本是 1080px * 1920px，当前被修改为 480px * 1024px。
'''
```

#### 查看屏幕密度

```
adb shell wm density
'''
Physical density: 420
该设备屏幕密度为 420dpi。

如果使用命令修改过，那输出可能是：
Physical density: 480
Override density: 160
表明设备的屏幕密度原来是 480dpi，当前被修改为 160dpi。
'''
```

#### 查看显示屏参数

```
adb shell dumpsys window displays
'''
WINDOW MANAGER DISPLAY CONTENTS (dumpsys window displays)
  Display: mDisplayId=0
    init=1080x1920 420dpi cur=1080x1920 app=1080x1794 rng=1080x1017-1810x1731
    deferred=false layoutNeeded=false
其中 mDisplayId 为 显示屏编号，init 是初始分辨率和屏幕密度，app 的高度比 init 里的要小，表示屏幕底部有虚拟按键，高度为 1920 - 1794 = 126px 合 42dp。
'''
```

#### 查看android_id

```
adb shell settings get secure android_id # 51b6be48bac8c569
```

#### 查看IMEI

在 Android 4.4 及以下版本可通过如下命令获取 IMEI：

```
adb shell dumpsys iphonesubinfo
'''
Phone Subscriber Info:
  Phone Type = GSM
  Device ID = 860955027785041
其中的 Device ID 就是 IMEI。
'''
```

而在 Android 5.0 及以上版本里这个命令输出为空，得通过其它方式获取了（需要 root 权限）：

```
adb shell
su
service call iphonesubinfo 1
'''
Result: Parcel(
  0x00000000: 00000000 0000000f 00360038 00390030 '........8.6.0.9.'
  0x00000010: 00350035 00320030 00370037 00350038 '5.5.0.2.7.7.8.5.'
  0x00000020: 00340030 00000031                   '0.4.1...        ')
'''
```

把里面的有效内容提取出来就是 IMEI 了，比如这里的是 860955027785041。参考：*[adb shell dumpsys iphonesubinfo not working since Android 5.0 Lollipop](http://stackoverflow.com/questions/27002663/adb-shell-dumpsys-iphonesubinfo-not-working-since-android-5-0-lollipop)*

#### 查看系统版本

```
adb shell getprop ro.build.version.release # 5.0.2
```

#### 查看IP地址

可从手机的「设置」-「关于手机」-「状态信息」-「IP地址」查看

```
adb shell ifconfig | grep Mask
'''
inet addr:10.130.245.230  Mask:255.255.255.252
inet addr:127.0.0.1  Mask:255.0.0.0
那么 10.130.245.230 就是设备 IP 地址。
'''
```

在有的设备上这个命令没有输出，如果设备连着 WiFi，可以使用如下命令来查看局域网 IP：

```
adb shell ifconfig wlan0
'''
wlan0: ip 10.129.160.99 mask 255.255.240.0 flags [up broadcast running multicast]
或

wlan0     Link encap:UNSPEC
          inet addr:10.129.168.57  Bcast:10.129.175.255  Mask:255.255.240.0
          inet6 addr: fe80::66cc:2eff:fe68:b6b6/64 Scope: Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:496520 errors:0 dropped:0 overruns:0 frame:0
          TX packets:68215 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:3000
          RX bytes:116266821 TX bytes:8311736
'''
```

如果以上命令仍然不能得到期望的信息，那可以试试以下命令（部分系统版本里可用）：

```
adb shell netcfg
'''
ip6tnl0  DOWN                                   0.0.0.0/0   0x00000080 00:00:00:00:00:00
sit0     DOWN                                   0.0.0.0/0   0x00000080 00:00:00:00:00:00
p2p0     UP                                     0.0.0.0/0   0x00001003 3a:bc:1a:e2:8a:2a
ifb1     DOWN                                   0.0.0.0/0   0x00000082 be:b8:dd:d8:b2:b1
ifb0     DOWN                                   0.0.0.0/0   0x00000082 72:72:60:9b:b1:86
lo       UP                                   127.0.0.1/8   0x00000049 00:00:00:00:00:00
wlan0    UP                             192.168.199.142/24  0x00001043 38:bc:1a:e2:8a:2a
tunl0    DOWN                                   0.0.0.0/0   0x00000080 00:00:00:00:00:00
ccmni1   DOWN                                   0.0.0.0/0   0x00000080 ae:d0:58:13:a9:80
ccmni0   DOWN                                   0.0.0.0/0   0x00000080 be:50:b4:7b:54:e9
ccmni2   DOWN                                   0.0.0.0/0   0x00000080 56:77:bb:5b:11:60
可以看到网络连接名称、启用状态、IP 地址和 Mac 地址等信息。
'''
```

#### 查看Mac地址

```
adb shell cat /sys/class/net/wlan0/address # f8:a9:d0:17:42:4d
# 这查看的是局域网 Mac 地址，移动网络或其它连接的信息可以通过前面的 查看IP 地址 里提到的 adb shell netcfg 命令来查看。
```

#### 查看CPU信息

```
adb shell cat /proc/cpuinfo
'''
Processor       : ARMv7 Processor rev 0 (v7l)
processor       : 0
BogoMIPS        : 38.40

processor       : 1
BogoMIPS        : 38.40

processor       : 2
BogoMIPS        : 38.40

processor       : 3
BogoMIPS        : 38.40

Features        : swp half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt
CPU implementer : 0x51
CPU architecture: 7
CPU variant     : 0x2
CPU part        : 0x06f
CPU revision    : 0

Hardware        : Qualcomm MSM 8974 HAMMERHEAD (Flattened Device Tree)
Revision        : 000b
Serial          : 0000000000000000
这是 Nexus 5 的 CPU 信息，我们从输出里可以看到使用的硬件是 Qualcomm MSM 8974，processor 的编号是 0 到 3，所以它是四核的，采用的架构是 ARMv7 Processor rev 0 (v71)。
'''
```

#### 查看内存信息

```
adb shell cat /proc/meminfo
'''
MemTotal:        1027424 kB
MemFree:          486564 kB
Buffers:           15224 kB
Cached:            72464 kB
SwapCached:        24152 kB
Active:           110572 kB
Inactive:         259060 kB
Active(anon):      79176 kB
Inactive(anon):   207736 kB
Active(file):      31396 kB
Inactive(file):    51324 kB
Unevictable:        3948 kB
Mlocked:               0 kB
HighTotal:        409600 kB
HighFree:         132612 kB
LowTotal:         617824 kB
LowFree:          353952 kB
SwapTotal:        262140 kB
SwapFree:         207572 kB
Dirty:                 0 kB
Writeback:             0 kB
AnonPages:        265324 kB
Mapped:            47072 kB
Shmem:              1020 kB
Slab:              57372 kB
SReclaimable:       7692 kB
SUnreclaim:        49680 kB
KernelStack:        4512 kB
PageTables:         5912 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:      775852 kB
Committed_AS:   13520632 kB
VmallocTotal:     385024 kB
VmallocUsed:       61004 kB
VmallocChunk:     209668 kB
'''
# 其中，MemTotal 就是设备的总内存，MemFree 是当前空闲内存。
```

#### 查看硬件与系统属性

```
adb shell cat /system/build.prop
```

这会输出很多信息，包括前面提到的「型号」和「Android 系统版本」等。

输出里还包括一些其它有用的信息，它们也可通过命令单独查看，列举一部分属性如下：

```
adb shell getprop <属性名>  # 单独查看属性
```

 

| 属性名                          | 含义                          |
| ------------------------------- | ----------------------------- |
| ro.build.version.sdk            | SDK 版本                      |
| ro.build.version.release        | Android 系统版本              |
| ro.build.version.security_patch | Android 安全补丁程序级别      |
| ro.product.model                | 型号                          |
| ro.product.brand                | 品牌                          |
| ro.product.name                 | 设备名                        |
| ro.product.board                | 处理器型号                    |
| ro.product.cpu.abilist          | CPU 支持的 abi 列表[*节注一*] |
| persist.sys.isUsbOtgEnabled     | 是否支持 OTG                  |
| dalvik.vm.heapsize              | 每个应用程序的内存上限        |
| ro.sf.lcd_density               | 屏幕密度                      |

*注：*

一些小厂定制的 ROM 可能修改过 CPU 支持的 abi 列表的属性名，如果用ro.product.cpu.abilist属性名查找不到，可以这样试试：

```
adb shell cat /system/build.prop | grep ro.product.cpu.abi
'''
ro.product.cpu.abi=armeabi-v7a
ro.product.cpu.abi2=armeabi
'''
```



1. 下载

https://down.xiazaidb.com/2_25504

2. 安装

```
adb install C:\Users\Administrator\Downloads\chaoji_16172.apk
```

3. 手机端配置

在手机启动adbd.apk, 并勾选【启动超级adbd】项

4. 关闭cmd窗口，拔掉usb数据线

5. 重新开启一个cmd窗口，再输入adb root命令,  查看是否获取root权限

### 管理手机文件

　　这里只列出手机和电脑之间的互相复制文件的功能

#### 复制手机的文件到电脑

```
adb pull <设备里的文件路径> [电脑上的目录] # 电脑上的目录参数可忽略，默认为当前目录
# 例：
adb pull /sdcard/sr.mp4 ~/tmp/ # 将手机中的/sdcard/sr.mp4文件复制到电脑的~/tmp/ 所在的文件夹中# 设备上的文件路径可能需要root权限才能访问，如果你的设备已经root过，可以先使用adb shell和su命令在adb shell里获取root 限后，先cp /path/on/device /sdcard/filename将文件复制到sdcard，然后adb pull /sdcard/filename /path/on/pc
```

#### 复制电脑上的文件到手机

```
adb push <电脑上的文件路径> <设备里的目录>
# 例
adb push ~/sr.mp4 /sdcard/
 # 设备上的文件路径普通权限可能无法直接写入，如果设备已经root过，可以先adb push /path/on/pc /sdcard/filename，然后adb shell和su在 adb shell里获取root权限后，cp /sdcard/filename /path/on/device。
```



### 应用管理

- 查看应用列表
- 安装应用
- 卸载应用
- 清楚应用数据与缓存
- 查看前台Activity
- 查看应用信息
- 查看安装路径等等 

主要操作有查看应用列表、安装应用、卸载应用、清楚应用数据与缓存、查看前台Activity、查看应用信息及安装路径等等

#### 查看应用列表

```
adb shell pm list packages [-f] [-d] [-e] [-s] [-3] [-i] [-u] [--user USER_ID] [FILTER]
```

　　即在adb shell pm list packages的基础上可以加一些参数进行过滤查看不同的列表，支持的过滤参数如下：

| 参数     | 显示列表                 |
| -------- | ------------------------ |
| 无       | 所有应用                 |
| -f       | 显示应用关联的 apk 文件  |
| -d       | 只显示 disabled 的应用   |
| -e       | 只显示 enabled 的应用    |
| -s       | 只显示系统应用           |
| -3       | 只显示第三方应用         |
| -i       | 显示应用的 installer     |
| -u       | 包含已卸载应用           |
| <FILTER> | 包名包含<FILTER>的字符串 |

- 查看所有应用

  ```
  adb shell pm list packages
  '''
  package:com.android.smoketest
  package:com.example.android.livecubes
  package:com.android.providers.telephony
  package:com.google.android.googlequicksearchbox
  package:com.android.providers.calendar
  package:com.android.providers.media
  package:com.android.protips
  package:com.android.documentsui
  package:com.android.gallery
  package:com.android.externalstorage
  ...
  // other packages here
  ...
  '''
  ```

- 查看系统应用

  ```
  adb shell pm list packages -s
  ```

- 查看第三方应用

  ```
  adb shell pm list packages -3
  ```

- 查看某个包名中包含指定字符的应用

  ```
  # 比如要查看包名包含字符串 python 的应用列表
  adb shell pm list packages python
  
  # 也可以使用 grep 来过滤：
  adb shell pm list packages | grep python
  ```

#### 安装应用

```
adb install [-lrtsdg] <path_to_apk>
```

实际上 adb install 是分三步完成：

1. push apk 文件到 /data/local/tmp。
2. 调用 pm install 安装。
3. 删除 /data/local/tmp 下的对应 apk 文件。

　　所以，必要的时候也可以根据这个步骤，手动分步执行安装过程。

　　adb install后面可以跟一些可选参数来控制安装 APK 的行为，可用参数及含义如下：

| 参数 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| -l   | 将应用安装到保护目录 /mnt/asec                               |
| -r   | 允许覆盖安装                                                 |
| -t   | 允许安装 AndroidManifest.xml 里 application 指定android:testOnly="true"的应用 |
| -s   | 将应用安装到 sdcard                                          |
| -d   | 允许降级覆盖安装                                             |
| -g   | 授予所有运行时权限                                           |

　　运行命令后如果见到类似如下输出（状态为Success）代表安装成功：

```
# 当前最新版 v1.0.36 的 adb 的输出，会显示 push apk 文件到手机的进度百分比。
[100%] /data/local/tmp/1.apk
    pkg: /data/local/tmp/1.apk
Success

# 使用旧版本 adb 的输出则是这样的：
12040 KB/s (22205609 bytes in 1.801s)
        pkg: /data/local/tmp/SogouInput_android_v8.3_sweb.apk
Success

# 如果状态为 Failure 则表示安装失败，比如：
[100%] /data/local/tmp/map-20160831.apk
        pkg: /data/local/tmp/map-20160831.apk
Failure [INSTALL_FAILED_ALREADY_EXISTS]
```

常见安装失败输出代码、含义及可能的解决办法如下：

| 输出                                                         | 含义                                                         | 解决办法                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| INSTALL_FAILED_ALREADY_EXISTS                                | 应用已经存在，或卸载了但没卸载干净                           | adb install使用 -r 参数，或者先adb uninstall <packagename>再安装 |
| INSTALL_FAILED_INVALID_APK                                   | 无效的 APK 文件                                              |                                                              |
| INSTALL_FAILED_INVALID_URI                                   | 无效的 APK 文件名                                            | 确保 APK 文件名里无中文                                      |
| INSTALL_FAILED_INSUFFICIENT_STORAGE                          | 空间不足                                                     | 清理空间                                                     |
| INSTALL_FAILED_DUPLICATE_PACKAGE                             | 已经存在同名程序                                             |                                                              |
| INSTALL_FAILED_NO_SHARED_USER                                | 请求的共享用户不存在                                         |                                                              |
| INSTALL_FAILED_UPDATE_INCOMPATIBLE                           | 以前安装过同名应用，但卸载时数据没有移除；或者已安装该应用，但签名不一致 | 先 adb uninstall <packagename> 再安装                        |
| INSTALL_FAILED_SHARED_USER_INCOMPATIBLE                      | 请求的共享用户存在但签名不一致                               |                                                              |
| INSTALL_FAILED_MISSING_SHARED_LIBRARY                        | 安装包使用了设备上不可用的共享库                             |                                                              |
| INSTALL_FAILED_REPLACE_COULDNT_DELETE                        | 替换时无法删除                                               |                                                              |
| INSTALL_FAILED_DEXOPT                                        | dex 优化验证失败或空间不足                                   |                                                              |
| INSTALL_FAILED_OLDER_SDK                                     | 设备系统版本低于应用要求                                     |                                                              |
| INSTALL_FAILED_CONFLICTING_PROVIDER                          | 设备里已经存在与应用里同名的content provider                 |                                                              |
| INSTALL_FAILED_NEWER_SDK                                     | 设备系统版本高于应用要求                                     |                                                              |
| INSTALL_FAILED_TEST_ONLY                                     | 应用是 test-only 的，但安装时没有指定 -t 参数                |                                                              |
| INSTALL_FAILED_CPU_ABI_INCOMPATIBLE                          | 包含不兼容设备 CPU 应用程序二进制接口的 native code          |                                                              |
| INSTALL_FAILED_MISSING_FEATURE                               | 应用使用了设备不可用的功能                                   |                                                              |
| INSTALL_FAILED_CONTAINER_ERROR                               | 1. sdcard 访问失败; 2. 应用签名与 ROM 签名一致，被当作内置应用。 | 1. 确认 sdcard 可用，或者安装到内置存储; 2. 打包时不与 ROM 使用相同签名。 |
| INSTALL_FAILED_INVALID_INSTALL_LOCATION                      | 1. 不能安装到指定位置; 2. 应用签名与 ROM 签名一致，被当作内置应用。 | 1. 切换安装位置，添加或删除 -s 参数; 2. 打包时不与 ROM 使用相同签名。 |
| INSTALL_FAILED_MEDIA_UNAVAILABLE                             | 安装位置不可用                                               | 一般为 sdcard，确认 sdcard 可用或安装到内置存储              |
| INSTALL_FAILED_VERIFICATION_TIMEOUT                          | 验证安装包超时                                               |                                                              |
| INSTALL_FAILED_VERIFICATION_FAILURE                          | 验证安装包失败                                               |                                                              |
| INSTALL_FAILED_PACKAGE_CHANGED                               | 应用与调用程序期望的不一致                                   |                                                              |
| INSTALL_FAILED_UID_CHANGED                                   | 以前安装过该应用，与本次分配的 UID 不一致                    | 清除以前安装过的残留文件                                     |
| INSTALL_FAILED_VERSION_DOWNGRADE                             | 已经安装了该应用更高版本                                     | 使用 -d 参数                                                 |
| INSTALL_FAILED_PERMISSION_MODEL_DOWNGRADE                    | 已安装 target SDK 支持运行时权限的同名应用，要安装的版本不支持运行时权限 |                                                              |
| INSTALL_PARSE_FAILED_NOT_APK                                 | 指定路径不是文件，或不是以 .apk 结尾                         |                                                              |
| INSTALL_PARSE_FAILED_BAD_MANIFEST                            | 无法解析的 AndroidManifest.xml 文件                          |                                                              |
| INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION                    | 解析器遇到异常                                               |                                                              |
| INSTALL_PARSE_FAILED_NO_CERTIFICATES                         | 安装包没有签名                                               |                                                              |
| INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES               | 已安装该应用，且签名与 APK 文件不一致                        | 先卸载设备上的该应用，再安装                                 |
| INSTALL_PARSE_FAILED_CERTIFICATE_ENCODING                    | 解析 APK 文件时遇到CertificateEncodingException              |                                                              |
| INSTALL_PARSE_FAILED_BAD_PACKAGE_NAME                        | manifest 文件里没有或者使用了无效的包名                      |                                                              |
| INSTALL_PARSE_FAILED_BAD_SHARED_USER_ID                      | manifest 文件里指定了无效的共享用户 ID                       |                                                              |
| INSTALL_PARSE_FAILED_MANIFEST_MALFORMED                      | 解析 manifest 文件时遇到结构性错误                           |                                                              |
| INSTALL_PARSE_FAILED_MANIFEST_EMPTY                          | 在 manifest 文件里找不到找可操作标签（instrumentation 或 application） |                                                              |
| INSTALL_FAILED_INTERNAL_ERROR                                | 因系统问题安装失败                                           |                                                              |
| INSTALL_FAILED_USER_RESTRICTED                               | 用户被限制安装应用                                           | 在开发者选项里将「USB安装」打开，如果已经打开了，那先关闭再打开。 |
| INSTALL_FAILED_DUPLICATE_PERMISSION                          | 应用尝试定义一个已经存在的权限名称                           |                                                              |
| INSTALL_FAILED_NO_MATCHING_ABIS                              | 应用包含设备的应用程序二进制接口不支持的 native code         |                                                              |
| INSTALL_CANCELED_BY_USER                                     | 应用安装需要在设备上确认，但未操作设备或点了取消             | 在设备上同意安装                                             |
| INSTALL_FAILED_ACWF_INCOMPATIBLE                             | 应用程序与设备不兼容                                         |                                                              |
| INSTALL_FAILED_TEST_ONLY                                     | APK 文件是使用 Android Studio 直接 RUN 编译出来的文件        | 通过 Gradle 的 assembleDebug 或 assembleRelease 重新编译，或者 Generate Signed APK |
| does not contain AndroidManifest.xml                         | 无效的 APK 文件                                              |                                                              |
| is not a valid zip file                                      | 无效的 APK 文件                                              |                                                              |
| Offline                                                      | 设备未连接成功                                               | 先将设备与 adb 连接成功                                      |
| unauthorized                                                 | 设备未授权允许调试                                           |                                                              |
| error: device not found                                      | 没有连接成功的设备                                           | 先将设备与 adb 连接成功                                      |
| protocol failure                                             | 设备已断开连接                                               | 先将设备与 adb 连接成功                                      |
| Unknown option: -s                                           | Android 2.2 以下不支持安装到 sdcard                          | 不使用 -s 参数                                               |
| No space left on device                                      | 空间不足                                                     | 清理空间                                                     |
| Permission denied ... sdcard ...                             | sdcard 不可用                                                |                                                              |
| signatures do not match the previously installed version; ignoring! | 已安装该应用且签名不一致                                     | 先卸载设备上的该应用，再安装                                 |



#### 卸载应用

```
adb uninstall [-k] <packagename>
# <packagename> 表示应用的包名，-k 参数可选，表示卸载应用但保留数据和缓存目录。

adb uninstall com.qihoo360.mobilesafe # 卸载 360 手机卫士。
```

#### 清除应用数据与缓存

```
adb shell pm clear <packagename>
# <packagename> 表示应用名包，这条命令的效果相当于在设置里的应用信息界面点击了「清除缓存」和「清除数据」。

adb shell pm clear com.qihoo360.mobilesafe # 表示清除 360 手机卫士的数据和缓存。
```

#### 查看前台Activity

```
adb shell dumpsys activity activities | grep mFocusedActivity
# mFocusedActivity: ActivityRecord{8079d7e u0 com.cyanogenmod.trebuchet/com.android.launcher3.Launcher t42}
# 其中的com.cyanogenmod.trebuchet/com.android.launcher3.Launcher 就是当前处于前台的 Activity。
```

#### 查看运行的services

```
adb shell dumpsys activity services [<packagename>]
# <packagename> 参数不是必须的，指定 <packagename> 表示查看与某个包名相关的 Services，不指定表示查看所有 Services。
# <packagename> 不一定要给出完整的包名，比如运行adb shell dumpsys activity services org.xxx，那么包名org.xxx.demo1、org.xxx.demo2 和 org.xxx123 等相关的Services都会列出来。
```

#### 查看应用信息

```
adb shell dumpsys package <packagename> # <packagename> 表示应用包名。
# 输出中包含很多信息，包括 Activity Resolver Table、Registered ContentProviders、包名、userId、安装后的文件资源代码等路径、版本信息、权限信息和授予状态、签名版本信息等。
```

#### 查看应用安装路径

```
adb shell pm path <PACKAGE>
# 如
adb shell pm path ecarx.weather # package:/data/app/ecarx.weather-1.apk
```





### 应用交互

应用交互的操作包括：启动应用 / 调起Activity、调起Services、停止Service、发送广播、强行停止应用

#### 基本命令

```
am <command> 
```

常用的command如下：

| command                         | 用途                        |
| ------------------------------- | --------------------------- |
| start [options] <INTENT>        | 启动<INTENT>指定的 Activity |
| startservice [options] <INTENT> | 启动<INTENT>指定的services  |
| broadcast [options] <INTENT>    | 发送<INTENT>指定的广播      |
| force-stop <packagename>        | 停止<packgame> 相关的进程   |

　　<INTENT>参数很灵活，和写 Android 程序时代码里的 Intent 相对应。

　　用于决定 intent 对象的选项如下：

| 参数           | 含义                                                         |
| -------------- | ------------------------------------------------------------ |
| -a <ACTION>    | 指定 action，比如android.intent.action.VIEW                  |
| -c <CATEGORY>  | 指定 category，比如android.intent.category.APP_CONTACTS      |
| -n <COMPONENT> | 指定完整 component 名，用于明确指定启动哪个 Activity，如com.example.app/.ExampleActivity |

　　<INTENT>里还能带数据，就像写代码时的 Bundle 一样：

|                                                             |                                        |
| ----------------------------------------------------------- | -------------------------------------- |
| 参数 含义 --esn <EXTRA_KEY>                                 | null 值（只有 key 名）                 |
| `-e                                                         | --es <EXTRA_KEY> <EXTRA_STRING_VALUE>` |
| --ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE>                      | boolean 值                             |
| --ei <EXTRA_KEY> <EXTRA_INT_VALUE>                          | integer 值                             |
| --el <EXTRA_KEY> <EXTRA_LONG_VALUE>                         | long 值                                |
| --ef <EXTRA_KEY> <EXTRA_FLOAT_VALUE>                        | float 值                               |
| --eu <EXTRA_KEY> <EXTRA_URI_VALUE>                          | URI                                    |
| --ecn <EXTRA_KEY> <EXTRA_COMPONENT_NAME_VALUE>              | component name                         |
| --eia <EXTRA_KEY> <EXTRA_INT_VALUE>[,<EXTRA_INT_VALUE...]   | integer 数组                           |
| --ela <EXTRA_KEY> <EXTRA_LONG_VALUE>[,<EXTRA_LONG_VALUE...] | long 数组                              |

#### 启动应用 / 调起Activity：

```
adb shell am start [options] <INTENT>
```

例如：

```
# 调起微信主界面。
adb shell am start -n com.tencent.mm/.ui.LauncherUI

# 调起 org.mazhuang.boottimemeasure/.MainActivity 并传给它 string 数据键值对 toast - hello, world。
adb shell am start -n org.mazhuang.boottimemeasure/.MainActivity --es "toast" "hello, world"
```

#### 调起Services

```
adb shell am startservice [options] <INTENT>
```

例如：

```
# 调起微信的某 Service。
adb shell am startservice -n com.tencent.mm/.plugin.accountsync.model.AccountAuthenticatorService

# 另外一个典型的用例是如果设备上原本应该显示虚拟按键但是没有显示，可以试试这个
adb shell am startservice -n com.android.systemui/.SystemUIService
```

#### 停止Service

```
adb shell am stopservice [options] <INTENT>
```

#### 发送广播

```
adb shell am broadcast [options] <INTENT>
```

　　可以向所有组件广播，也可以只向指定组件广播。

　　例如

```
# 向所有组件广播 BOOT_COMPLETED：
adb shell am broadcast -a android.intent.action.BOOT_COMPLETED

# 只向 org.mazhuang.boottimemeasure/.BootCompletedReceiver 广播 BOOT_COMPLETED：
adb shell am broadcast -a android.intent.action.BOOT_COMPLETED -n org.mazhuang.boottimemeasure/.BootCompletedReceiver
```

　　这类用法在测试的时候很实用，比如某个广播的场景很难制造，可以考虑通过这种方式来发送广播。

　　既能发送系统预定义的广播，也能发送自定义广播。如下是部分系统预定义广播及正常触发时机：

| action                                          | 触发时机                                      |
| ----------------------------------------------- | --------------------------------------------- |
| android.net.conn.CONNECTIVITY_CHANGE            | 网络连接发生变化                              |
| android.intent.action.SCREEN_ON                 | 屏幕点亮                                      |
| android.intent.action.SCREEN_OFF                | 屏幕熄灭                                      |
| android.intent.action.BATTERY_LOW               | 电量低，会弹出电量低提示框                    |
| android.intent.action.BATTERY_OKAY              | 电量恢复了                                    |
| android.intent.action.BOOT_COMPLETED            | 设备启动完毕                                  |
| android.intent.action.DEVICE_STORAGE_LOW        | 存储空间过低                                  |
| android.intent.action.DEVICE_STORAGE_OK         | 存储空间恢复                                  |
| android.intent.action.PACKAGE_ADDED             | 安装了新的应用                                |
| android.net.wifi.STATE_CHANGE                   | WiFi 连接状态发生变化                         |
| android.net.wifi.WIFI_STATE_CHANGED             | WiFi 状态变为启用/关闭/正在启动/正在关闭/未知 |
| android.intent.action.BATTERY_CHANGED           | 电池电量发生变化                              |
| android.intent.action.INPUT_METHOD_CHANGED      | 系统输入法发生变化                            |
| android.intent.action.ACTION_POWER_CONNECTED    | 外部电源连接                                  |
| android.intent.action.ACTION_POWER_DISCONNECTED | 外部电源断开连接                              |
| android.intent.action.DREAMING_STARTED          | 系统开始休眠                                  |
| android.intent.action.DREAMING_STOPPED          | 系统停止休眠                                  |
| android.intent.action.WALLPAPER_CHANGED         | 壁纸发生变化                                  |
| android.intent.action.HEADSET_PLUG              | 插入耳机                                      |
| android.intent.action.MEDIA_UNMOUNTED           | 卸载外部介质                                  |
| android.intent.action.MEDIA_MOUNTED             | 挂载外部介质                                  |
| android.os.action.POWER_SAVE_MODE_CHANGED       | 省电模式开启                                  |

*（以上广播均可使用 adb 触发）*

#### 强制停止应用

```
adb shell am force-stop <packagename>

# 停止 360 安全卫士的一切进程与服务。
adb shell am force-stop com.qihoo360.mobilesafe
```

#### 收紧内存

```
adb shell am send-trim-memory  <pid> <level>
# pid: 进程 ID level: HIDDEN、RUNNING_MODERATE、BACKGROUND、 RUNNING_LOW、MODERATE、RUNNING_CRITICAL、COMPLETE

# 向 pid=12345 的进程，发出 level=RUNNING_LOW 的收紧内存命令。
adb shell am send-trim-memory 12345 RUNNING_LOW
```



### 查看日志

　　Android 系统的日志分为两部分，底层的 Linux 内核日志输出到 /proc/kmsg，Android 的日志输出到 /dev/log。

#### 查看Android的日志

```
[adb] logcat [<option>] ... [<filter-spec>] ...
```

常用用法列举如下：

**一、按级别过滤日志**

　　Android 的日志分为如下几个优先级（priority）：

- V —— Verbose（最低，输出得最多）
- D —— Debug
- I —— Info
- W —— Warning
- E —— Error
- F —— Fatal
- S —— Silent（最高，啥也不输出）

　　按某级别过滤日志则会将该级别及以上的日志输出。

　　比如，下面命令会将 Warning、Error、Fatal 和 Silent 日志输出。

```
adb logcat *:W # 注： 在 macOS 下需要给 *:W 这样以 * 作为 tag 的参数加双引号，如 adb logcat "*:W"，不然会报错 no matches found: *:W
```



**二、按 tag 和级别过滤日志**

```
# <filter-spec> 可以由多个 <tag>[:priority] 组成。

# 比如，下面命令表示输出 tag ActivityManager 的 Info 以上级别日志，输出 tag MyApp 的 Debug 以上级别日志，及其它 tag 的 Silent 级别日志（即屏蔽其它 tag 日志）
adb logcat ActivityManager:I MyApp:D *:S
```



**三、日志格式**

　　可以用adb logcat -v <format>选项指定日志输出格式。

日志支持按以下几种<format>

- brief——默认格式。格式为

  ```
  <priority>/<tag>(<pid>): <message>
  # 示例
  D/HeadsetStateMachine( 1785): Disconnected process message: 10, size: 0
  ```

- process——格式为：

  ```
  <priority>(<pid>) <message>
  # 示例：
  D( 1785) Disconnected process message: 10, size: 0  (HeadsetStateMachine)
  ```

- tag——格式为：

  ```
  <priority>/<tag>: <message>
  # 示例：
  D/HeadsetStateMachine: Disconnected process message: 10, size: 0
  ```

- raw——格式为：

  ```
  <message>
  # 示例：
  Disconnected process message: 10, size: 0
  ```

- time——格式为：

  ```
  <datetime> <priority>/<tag>(<pid>): <message>
  # 示例：
  08-28 22:39:39.974 D/HeadsetStateMachine( 1785): Disconnected process message: 10, size: 0
  ```

- threadtime——格式为：

  ```
  <datetime> <pid> <tid> <priority> <tag>: <message>
  # 示例：
  08-28 22:39:39.974  1785  1832 D HeadsetStateMachine: Disconnected process message: 10, size: 0
  ```

- long——格式为：

  ```
  [ <datetime> <pid>:<tid> <priority>/<tag> ]
  <message>
  # 示例：
  [ 08-28 22:39:39.974  1785: 1832 D/HeadsetStateMachine ]
  Disconnected process message: 10, size: 0
  ```

　　指定格式可与上面的过滤同时使用。比如：

```
adb logcat -v long ActivityManager:I *:S
```

 

**四、清空日志**

```
adb logcat -c
```

 

#### 查看内核日志

　　通过内核日志我们可以做一些事情，比如衡量内核启动时间，在系统启动完毕后的内核日志里找到 Freeing init memory 那一行前面的时间就是。

```
adb shell dmesg
'''
<6>[14201.684016] PM: noirq resume of devices complete after 0.982 msecs
<6>[14201.685525] PM: early resume of devices complete after 0.838 msecs
<6>[14201.753642] PM: resume of devices complete after 68.106 msecs
<4>[14201.755954] Restarting tasks ... done.
<6>[14201.771229] PM: suspend exit 2016-08-28 13:31:32.679217193 UTC
<6>[14201.872373] PM: suspend entry 2016-08-28 13:31:32.780363596 UTC
<6>[14201.872498] PM: Syncing filesystems ... done.
'''
# 中括号里的 [14201.684016] 代表内核开始启动后的时间，单位为秒。
```



### 修改手机默认设置

　　修改设置的原理主要是通过 settings 命令修改 /data/data/com.android.providers.settings/databases/settings.db 里存放的设置值。

　　利用ADB的命令可以修改手机的一些默认设置，修改设置之后，运行恢复命令有可能显示仍然不太正常，可以运行 adb reboot 重启设备，或手动重启。

- 修改分辨率
- 修改屏幕密度
- 修改显示区域
- 关闭USB调试
- 允许 / 禁止访问非 SDK API：
- 状态栏和导航栏的显示隐藏



#### 修改分辨率

```
adb shell wm size 480x1024 # 表示将分辨率修改为 480px * 1024px。
E
# 恢复原分辨率
adb shell wm size reset
```

#### 修改屏幕密度

```
adb shell wm density 160 # 表示将屏幕密度修改为 160dpi。

# 恢复原屏幕密度
adb shell wm density reset
```

#### 修改显示区域

```
adb shell wm overscan 0,0,0,200 # 四个数字分别表示距离左、上、右、下边缘的留白像素，以上命令表示将屏幕底部 200px 留白。

# 恢复原显示区域
adb shell wm overscan reset
```

#### 关闭USB调试

```
adb shell settings put global adb_enabled 0
```

注意：用命令无法恢复，毕竟关闭了 USB 调试 adb 就连接不上 Android 设备了。去设备上手动恢复：「设置」-「开发者选项」-「Android 调试」。

#### 允许访问非 SDK API

```
adb shell settings put global hidden_api_policy_pre_p_apps 1
adb shell settings put global hidden_api_policy_p_apps 1
```

#### 禁止访问非 SDK API

```
adb shell settings delete global hidden_api_policy_pre_p_apps
adb shell settings delete global hidden_api_policy_p_apps
```

　　上述个功能不需要设备获得 Root 权限。

　　命令最后的数字的含义：

| 值   | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| 0    | 禁止检测非 SDK 接口的调用。该情况下，日志记录功能被禁用，并且令 strict mode API，即 detectNonSdkApiUsage() 无效。不推荐。 |
| 1    | 仅警告——允许访问所有非 SDK 接口，但保留日志中的警告信息，可继续使用 strick mode API。 |
| 2    | 禁止调用深灰名单和黑名单中的接口。                           |
| 3    | 禁止调用黑名单中的接口，但允许调用深灰名单中的接口。         |

#### 状态栏和导航栏的显示隐藏

命令：

```
adb shell settings put global policy_control <key-values>
```

<key-value> 可由如下几种键及其对应的值组成，格式<key1>=<value1>:<key2>=<value2>

|          key          | 含义       |
| :-------------------: | ---------- |
|    immersive.full     | 同时隐藏   |
|   immersive.status    | 隐藏状态栏 |
| immersive.navigation  | 隐藏导航栏 |
| immersive.preconfirms | ?          |

这些键对应的值可则如下值用逗号组合：

|    value     | 含义         |
| :----------: | ------------ |
|     apps     | 所有应用     |
|      *       | 所有界面     |
| packagename  | 指定应用     |
| -packagename | 排除指定应用 |

例如：

```
# 设置在所有界面下都同时隐藏状态栏和导航栏。
adb shell settings put global policy_control immersive.full=*

# 设置在包名为 com.package1 和 com.package2 的应用里隐藏状态栏，在除了包名为 com.package3 的所有应用里隐藏导航栏。
adb shell settings put global policy_control immersive.status=com.package1,com.package2:immersive.navigation=apps,-com.package3
```



### 其他实用功能 

#### 屏幕截图

```
adb exec-out screencap -p > sc.png # 截图保存到电脑# 实测如果指定文件名以 .png 结尾时可以省略 -p 参数；否则需要使用 -p 参数。如果不指定文件名，截图文件的内容将直接输出到 stdout。
# 如果 adb 版本较老，无法使用 exec-out 命令，建议更新 adb 版本。若无法更新使用如下步骤：
adb shell screencap -p /sdcard/sc.png # 先截图保存到设备里
adb pull /sdcard/sc.png # 然后将 png 文件导出到电脑：
```

　　可以使用 adb shell screencap -h 查看 screencap 命令的帮助信息，下面是两个有意义的参数及含义：

| 参数          | 含义                                       |
| ------------- | ------------------------------------------ |
| -p            | 指定保存文件为 png 格式                    |
| -d display-id | 指定截图的显示屏编号（有多显示屏的情况下） |

另外一种一行命令截图并保存到电脑的方法：

```
# Linux 和 Windows
adb shell screencap -p | sed "s/\r$//" > sc.png

# Mac OS X
adb shell screencap -p | gsed "s/\r$//" > sc.png
```

上述方法需要用到 gnu sed 命令，在 Linux 下直接就有，在 Windows 下 Git 安装目录的 bin 文件夹下也有。如果确实找不到该命令，可以下载 [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm) 并将 sed.exe 所在文件夹添加到 PATH 环境变量里。

而在 Mac 下使用系统自带的 sed 命令会报错：

```
sed: RE error: illegal byte sequence
# 需要安装 gnu-sed，然后使用 gsed 命令：
brew install gnu-sed
```

#### 录制屏幕

```
adb shell screenrecord /sdcard/filename.mp4 # 录制屏幕以 mp4 格式保存到 /sdcard
adb pull /sdcard/filename.mp4 # 导出到电脑：

# 需要停止时按 Ctrl-C，默认录制时间和最长录制时间都是 180 秒。
```

　　可以使用 adb shell screenrecord --help 查看 screenrecord 命令的帮助信息，下面是常见参数及含义：

| 参数                | 含义                                          |
| ------------------- | --------------------------------------------- |
| --size WIDTHxHEIGHT | 视频的尺寸，比如 1280x720，默认是屏幕分辨率。 |
| --bit-rate RATE     | 视频的比特率，默认是 4Mbps。                  |
| --time-limit TIME   | 录制时长，单位秒。                            |
| --verbose           | 输出更多信息。                                |

#### 重新挂载 system 分区为可写

注：需要 root 权限。

　　/system 分区默认挂载为只读，但有些操作比如给 Android 系统添加命令、删除自带应用等需要对 /system 进行写操作，所以需要重新挂载它为可读写。

步骤：

```
# 1.进入 shell 并切换到 root 用户权限。
adb shell
su
# 2.查看当前分区挂载情况。
mount
# 3.找到其中我们关注的带 /system 的那一行：/dev/block/platform/msm_sdcc.1/by-name/system /system ext4 ro,seclabel,relatime,data=ordered 0 0重新挂载。
mount -o remount,rw -t yaffs2 /dev/block/platform/msm_sdcc.1/by-name/system /system
# 这里的 /dev/block/platform/msm_sdcc.1/by-name/system 就是我们从上一步的输出里得到的文件路径。
# 如果输出没有提示错误的话，操作就成功了，可以对 /system 下的文件为所欲为了。
```

#### 查看连接过的 WiFi 密码

注：需要 root 权限。

```
adb shell
su
cat /data/misc/wifi/*.conf
'''
输出示例：
network={
    ssid="TP-LINK_9DFC"
    scan_ssid=1
    psk="123456789"
    key_mgmt=WPA-PSK
    group=CCMP TKIP
    auth_alg=OPEN
    sim_num=1
    priority=13893
}

network={
    ssid="TP-LINK_F11E"
    psk="987654321"
    key_mgmt=WPA-PSK
    sim_num=1
    priority=17293
}
ssid 即为我们在 WLAN 设置里看到的名称，psk 为密码，key_mgmt 为安全加密方式。
'''
```

#### 设置系统日期和时间

注：需要 root 权限。

```
adb shell
su
date -s 20160823.131500
# 表示将系统日期和时间更改为 2016 年 08 月 23 日 13 点 15 分 00 秒。
```

#### 重启手机

```
adb reboot
```

#### 检测设备是否已 root

```
adb shell
su
# 此时命令行提示符是 $ 则表示没有 root 权限，是 # 则表示已 root。
```

#### 使用 Monkey 进行压力测试

　　Monkey 可以生成伪随机用户事件来模拟单击、触摸、手势等操作，可以对正在开发中的程序进行随机压力测试。

简单用法：

```
adb shell monkey -p <packagename> -v 500 # 表示向 <packagename> 指定的应用程序发送 500 个伪随机事件。
```

 

Monkey 的详细用法参考 *[官方文档](https://developer.android.com/studio/test/monkey.html)*。

 

#### 开启/关闭 WiFi

注：需要 root 权限

```
adb shell
su

# 开启 WiFi：
svc wifi enable

# 关闭 WiFi：
svc wifi disable

# 若执行成功，输出为空；若未取得 root 权限执行此命令，将执行失败，输出 Killed。
```



### 其他ADB shell命令 

　　Android 系统是基于 Linux 内核的，所以 Linux 里的很多命令在 Android 里也有相同或类似的实现，在 adb shell 里可以调用。本文档前面的部分内容已经用到了 adb shell 命令。

#### 查看进程

```
adb shell ps
'''
输出示例：

USER     PID   PPID  VSIZE  RSS     WCHAN    PC        NAME
root      1     0     8904   788   ffffffff 00000000 S /init
root      2     0     0      0     ffffffff 00000000 S kthreadd
...
u0_a71    7779  5926  1538748 48896 ffffffff 00000000 S com.sohu.inputmethod.sogou:classic
u0_a58    7963  5926  1561916 59568 ffffffff 00000000 S org.mazhuang.boottimemeasure
...
shell     8750  217   10640  740   00000000 b6f28340 R ps
'''
```

各列含义：

| 列名 | 含义      |
| ---- | --------- |
| USER | 所属用户  |
| PID  | 进程 ID   |
| PPID | 父进程 ID |
| NAME | 进程名    |

#### 查看实时资源占用情况

```
adb shell top
'''
输出示例：

User 0%, System 6%, IOW 0%, IRQ 0%
User 3 + Nice 0 + Sys 21 + Idle 280 + IOW 0 + IRQ 0 + SIRQ 3 = 307

  PID PR CPU% S  #THR     VSS     RSS PCY UID      Name
 8763  0   3% R     1  10640K   1064K  fg shell    top
  131  0   3% S     1      0K      0K  fg root     dhd_dpc
 6144  0   0% S   115 1682004K 115916K  fg system   system_server
  132  0   0% S     1      0K      0K  fg root     dhd_rxf
 1731  0   0% S     6  20288K    788K  fg root     /system/bin/mpdecision
  217  0   0% S     6  18008K    356K  fg shell    /sbin/adbd
 ...
 7779  2   0% S    19 1538748K  48896K  bg u0_a71   com.sohu.inputmethod.sogou:classic
 7963  0   0% S    18 1561916K  59568K  fg u0_a58   org.mazhuang.boottimemeasure
'''
```

各列含义：

| 列名 | 含义                                                       |
| ---- | ---------------------------------------------------------- |
| PID  | 进程 ID                                                    |
| PR   | 优先级                                                     |
| CPU% | 当前瞬间占用 CPU 百分比                                    |
| S    | 进程状态（R=运行，S=睡眠，T=跟踪/停止，Z=僵尸进程）        |
| #THR | 线程数                                                     |
| VSS  | Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）      |
| RSS  | Resident Set Size 实际使用物理内存（包含共享库占用的内存） |
| PCY  | 调度策略优先级，SP_BACKGROUND/SPFOREGROUND                 |
| UID  | 进程所有者的用户 ID                                        |
| NAME | 进程名                                                     |

top 命令还支持一些命令行参数，详细用法如下：

Usage: top [ -m max_procs ] [ -n iterations ] [ -d delay ] [ -s sort_column ] [ -t ] [ -h ]

- -m num   最多显示多少个进程
- -n num 　刷新多少次后退出
- -d num    刷新时间间隔（单位秒，默认值 5）
- -s col      按某列排序（可用 col 值：cpu, vss, rss, thr）
- -t           显示线程信息
- -h           显示帮助文档

#### 查看进程 UID

```
# 第一种方案：
adb shell dumpsys package <packagename> | grep userId=

# 如：
$ adb shell dumpsys package org.mazhuang.guanggoo | grep userId=
   userId=10394

# 第二种：通过 ps 命令找到对应进程的 pid 之后 adb shell cat /proc/<pid>/status | grep Uid

# 如：
$ adb shell
gemini:/ $ ps | grep org.mazhuang.guanggoo
u0_a394   28635 770   1795812 78736 SyS_epoll_ 0000000000 S org.mazhuang.guanggoo
gemini:/ $ cat /proc/28635/status | grep Uid
Uid:    10394   10394   10394   10394
gemini:/ $
```

#### 其它

如下是其它常用命令的简单描述，前文已经专门讲过的命令不再额外说明：

| 命令  | 功能                        |
| ----- | --------------------------- |
| cat   | 显示文件内容                |
| cd    | 切换目录                    |
| chmod | 改变文件的存取模式/访问权限 |
| df    | 查看磁盘空间使用情况        |
| grep  | 过滤输出                    |
| kill  | 杀死指定 PID 的进程         |
| ls    | 列举目录内容                |
| mount | 挂载目录的查看和管理        |
| mv    | 移动或重命名文件            |
| ps    | 查看正在运行的进程          |
| rm    | 删除文件                    |
| top   | 查看进程的资源占用情况      |





