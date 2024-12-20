---
title: 上赞 R200C 5G CPE 小玩一下
date: "2024-11-11"
tags: ["CPE"]
---

最近临时需要搞个流量上网，需要个可以插流量卡的路由器，我在闲鱼找了一圈，买了个 5G CPE 试试。型号叫 上赞 R200C，入手价格是 ￥340。

![r200c-front.jpg](r200c-front-small.jpg)

## 外观与硬件参数

据说是与超能犇一样的硬件配置，也都是品速的贴牌货。同级别是 R200S，高级一点的型号是 R200，价格都要贵一些。

芯片是高通 QCX315，应该比展锐的芯片发热低一些。

![r200c-ports.jpg](r200c-ports-small.jpg)

接口包括一个USB Type-C 口，供电和刷机都靠它，一个LAN口可以插网线上网。

机身上还有一个 Nano SIM 卡槽，一个重置孔。附带的电源是5V2A。

![r200c-bottom.jpg](r200c-bottom-small.jpg)

## 刷机&刷WEBUI

加了 QQ 群 WEBUI交流群2：993033024，群文件有刷机工具和刷机包。另附上固件下载网盘：<https://www.123pan.com/s/kPC6Vv-denR.html>

刷固件是用高通 9008 模式，和安卓手机刷机差不多，R200C 最新的固件版本是 `6.00.9`，我不小心刷了 R200S 的 `R200S-6.0.11`，结果指示灯有问题，后面重新刷了 `R200C-6.00.9`。

刷完固件刷 WEBUI，群里下载了`WEBUI_V3.1.3_FULL.zip`，照着教程操作就行。因为我机器的型号是`R200C`, `WEBUI刷入工具_1.2.9.exe` 提示里选的 `1、不区分机型`。

我用电信的卡简单跑了下，可以达到 300+ Mbps 的下载速度，差不多够用了：

![r200c-china-telecom.png](r200c-china-telecom.png)