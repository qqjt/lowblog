---
title: PVE 配置记录
date: 2023-06-02
updated: 2024-04-12
tags: ['PVE']
---
## 1. 软件源
https://mirrors.ustc.edu.cn/help/proxmox.html

```shell
cp /etc/apt/sources.list /etc/apt/sources.list.bak
mv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak
mv /etc/apt/sources.list.d/ceph.list /etc/apt/sources.list.d/ceph.list.bak

sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

source /etc/os-release
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve $VERSION_CODENAME pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

apt update && apt upgrade -y
```

## 2. 直通

### 2.1 单个硬盘直通
<https://pve.proxmox.com/wiki/Passthrough_Physical_Disk_to_Virtual_Machine_(VM)>
```shell
find /dev/disk/by-id/ -type l|xargs -I{} ls -l {}|grep -v -E '[0-9]$' |sort -k11|cut -d' ' -f9,10,11,12

qm set 592 -scsi2 /dev/disk/by-id/ata-ST3000DM001-1CH166_Z1F41BLC
```

## 3. 安装桌面环境
<https://forum.proxmox.com/threads/install-desktop-and-browser-on-proxmox-host-server.20515/>

mate：
```shell
apt install mate chromium lightdm
```

或者 gnome：
```shell
apt update
apt upgrade
adduser *USERNAME*
reboot
tasksel install desktop gnome-desktop
systemctl set-default graphical.target
reboot
```

## 4. 去除订阅提示
```shell
sed -i_orig "s/data.status === 'Active'/true/g" /usr/share/pve-manager/js/pvemanagerlib.js
sed -i_orig "s/if (res === null || res === undefined || \!res || res/if(/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
sed -i_orig "s/.data.status.toLowerCase() !== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

## 5. 删除 lvm-thin
```sh
lvremove /dev/pve/data
lvextend -rl +100%FREE /dev/pve/root
# 数据中心手动删除 local-lvm
```

## 6. 备忘

- vm 配置文件位置：`/etc/pve/nodes/pve/qemu-server/<vm>.conf`

