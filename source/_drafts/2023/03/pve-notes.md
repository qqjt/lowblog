---
title: PVE 配置记录
date: 2023-06-02 14:59:10
tags: ['PVE']
---
## 1. 软件源
https://mirrors.ustc.edu.cn/help/proxmox.html

```shell
cp /etc/apt/sources.list /etc/apt/sources.list.bak
mv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak

sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

source /etc/os-release
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve $VERSION_CODENAME pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

apt update && apt upgrade -y
```

## 备忘

- vm 配置文件位置：`/etc/pve/nodes/pve/qemu-server/<vm>.conf`

