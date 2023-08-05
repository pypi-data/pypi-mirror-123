# pyadb_GUI

#### 介绍
使用 python 自带的 Tkinter 库编写一个通过GUI 界面操作 adb 设备的可执行文件。

#### 开发计划

1. 基础功能(0.1.0)
   - [x] 常用遥控器按键
   - [x] 一键直达 蓝牙配对/ wifi 连接
     - [x] 调整快捷键背景色
   - [x] 一键输入文字
     - [x] 输入后清除文字
2. 设备信息界面(1.0)
   - [x] 设备  
     - [x] 时间
     - [x] 版本
     - [x] 获取 DSN 号
   - [x] 网络
     - [x] ip 地址
     - [x] 联网状态
   - [x] 遥控器
     - [x] mac 地址
   - [x] TreeView (列表)视图
   - [x] NoteBook 分页
   - [x] 双击复制信息
3. 视频/截图
   - [ ] 截图功能
   - [ ] 屏幕录制功能
4. log 截取(关键字)
   - [ ] adb / picus / event log
   - [ ] get_log
   - [ ] 清理 log 缓存
5. adb push 文件
6. 刷机功能
7. 多设备
   - [ ] adb connect & adb disconnect
   - [ ] TV & SMP 的连接方式不同
   - [ ] 显示设备 adb kill-server + sudo adb devices -l
   - [ ] 常驻浮动条 显示多设备已连接的设备
8. 优化
   - [ ] 布局自适应缩放
   - [ ] 


#### 软件架构
软件架构说明


#### 安装教程

1.  `pip3 install --upgrade pyadb_gui`
2.  `pyadb`

#### 可能遇到的问题

1. `no module named tkinter`
   - `sudo apt update`
   - `sudo apt install python3-tk -y`
   - `pyadb`
2. 安装完 python3-tk 后无效
```
oem@ps-01:-$ pyadb
Traceback (most recent call last):
File "/home/oem/.local/bin/pyadb", line 5, in <module>
from pyadb_gui.main import main
File "/home/oem/.Local/lib/python3.7/site-packages/pyadb_gui/matn.py",line2,in<module>
     import tkinter as tk
ModuleNotFoundError: No module named tkinter'
```
   - 找到提示文字中的 python3.7
   - `sudo apt install python3.7-tk -y`



#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
