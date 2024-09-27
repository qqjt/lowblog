---
title: windows 11 企业版多会话
tags: [ "PC", "Windows" ]
date: "2024-09-27 11:30:00"
---

# 体验 Windows 11 企业版多会话版操作系统

![winver.png](winver.png)

Windows 11 专业版和 Windows Server 版操作系统各有优缺点，最近发现了一个“企业版多会话”的操作系统，应该算是介于俩者之间的版本。

## 安装

我是先安装了 Windows 11 Pro，然后通过改密钥的方式换成了多会话版本：

```shell
slmgr /ipk VMKVQ-3MN6B-BVM9F-YWV97-R9FCX
slmgr /skms <kms服务器地址>
slmgr /ato
```

重启一下，会有一些系统更新操作。为了体验更完整，我重置了一下系统，结果重置完之后没有出现创建用户的引导，旧用户也登录不上去了。搜索了一番，通过进安全模式的方式启用了“Administrator”账号密码。

1. 在登录界面，键盘按住shift，鼠标点击重启。
2. 重启后，选择进入带网络的安全模式。
3. 进入系统后，使用快捷键“windows+r”打开运行指令框。
4. 在输入框中输入 compmgmt.msc，回车确定。
5. 展开系统工具-本地用户和组-用户。
6. 在“Administrator”用户上右键，设置密码。

## 使用体验

优点挺多的，比如：

- 可以先安装好 Windows 11 的驱动，再改成多会话版，比Server 版安装驱动更容易。
- 可以开启 Windows Server 的Discrete Device Assignment（DDA），也即硬件设备直通功能。
- 可以开启 WSL2 等 Windows 11 原有的功能，可以安装 Docker。

可以说是东食西宿，既要又要了。

缺点：

- 有些软件会把系统识别为 Windows Server，导致无法运行。