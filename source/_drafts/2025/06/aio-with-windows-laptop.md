---
title: Windows 笔记本电脑用作 All-In-One
tags: ["AIO", "NAS"]
---

## 1. 硬件配置

神舟战神 TX9-CA5DP，一款傻大黑粗的游戏本，使用的是 11 代桌面级 CPU，还和台式机一样的可更换，搭配 RTX3070 Laptop 独显，比较可惜的是没有独显直连。

主要硬件参数：

- CPU：i5-11400
- 显卡：Nvidia RTX3070 Laptop
- 内存：16G × 2 DDR4 笔记本内存
- 硬盘接口：1 × SATA3 + 2 × m.2
- 网卡：1 × 千兆有线 + 1 × Intel 9462 无线网卡带蓝牙

机身接口：

- USB Type-C × 1
- USB-A 3.0 × 2 + 2.0 × 1
- Mini DisplayPort × 2 + HDMI × 1
- RJ45 千兆网口
- 耳机耳麦口 × 1
- 读卡器 × 1

## 2. 操作系统安装

选择的是 Windows Server 2025 版本，主要是 Windows 系统的图形界面比较好，可以搭配笔记本屏幕做二奶机。

使用 Hyper-V 做虚拟化，硬件直通可以用 Discrete Device Assignment(DDA)。

## 3. 虚拟机

## 4. 软件安装

- Jellyfin Server：媒体管理
- qBittorrent：bt/pt 下载