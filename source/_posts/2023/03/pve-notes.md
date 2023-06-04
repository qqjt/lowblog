---
title: PVE After Install Notes
date: 2023-06-02 14:59:10
tags: ['PVE']
---
## 软件源
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

## 网络

`/etc/network/interfaces`:

```
auto lo
iface lo inet loopback

iface enp86s0 inet manual

auto vmbr0
iface vmbr0 inet dhcp
	# address 192.168.1.111/24
	# gateway 192.168.1.1
	bridge-ports enp86s0
	bridge-stp off
	bridge-fd 0
```

## 存储

- local - 
- local-lvm - 

## guest OS
```shell
sudo apt update && sudo apt install qemu-guest-agent
```
## 硬件直通

https://pve.proxmox.com/wiki/PCI_Passthrough

### BIOS 设置

Chipset -> System Agent(SA) Configuration:

VT-d: enabled
X2APIC Opt Out: disabled

### Enable the IOMMU

`/etc/default/grub`:
```shell
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"
```

`update-grup` then reboot

```shell
root@pve:~# dmesg | grep -e DMAR -e IOMMU
[    0.087000] DMAR: IOMMU enabled
[    0.610275] pci 0000:00:02.0: DMAR: Skip IOMMU disabling for graphics
```

### Required Modules
`/etc/modules`:
```
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```

### IOMMU Interrupt Remapping

```shell
root@pve:~# dmesg | grep 'remapping'
[    0.211970] DMAR-IR: Queued invalidation will be enabled to support x2apic and Intr-remapping.
[    0.213499] DMAR-IR: Enabled IRQ remapping in x2apic mode
```

`find /sys/kernel/iommu_groups/ -type l`:

```shell
root@pve:~# find /sys/kernel/iommu_groups/ -type l
/sys/kernel/iommu_groups/7/devices/0000:00:14.3
/sys/kernel/iommu_groups/15/devices/0000:01:00.0
/sys/kernel/iommu_groups/5/devices/0000:00:0d.0
/sys/kernel/iommu_groups/5/devices/0000:00:0d.3
/sys/kernel/iommu_groups/5/devices/0000:00:0d.2
/sys/kernel/iommu_groups/13/devices/0000:00:1e.0
/sys/kernel/iommu_groups/13/devices/0000:00:1e.3
/sys/kernel/iommu_groups/3/devices/0000:00:07.0
/sys/kernel/iommu_groups/11/devices/0000:00:19.0
/sys/kernel/iommu_groups/11/devices/0000:00:19.1
/sys/kernel/iommu_groups/1/devices/0000:00:02.0
/sys/kernel/iommu_groups/8/devices/0000:00:15.1
/sys/kernel/iommu_groups/8/devices/0000:00:15.0
/sys/kernel/iommu_groups/16/devices/0000:56:00.0
/sys/kernel/iommu_groups/6/devices/0000:00:14.2
/sys/kernel/iommu_groups/6/devices/0000:00:14.0
/sys/kernel/iommu_groups/14/devices/0000:00:1f.0
/sys/kernel/iommu_groups/14/devices/0000:00:1f.5
/sys/kernel/iommu_groups/14/devices/0000:00:1f.3
/sys/kernel/iommu_groups/14/devices/0000:00:1f.4
/sys/kernel/iommu_groups/4/devices/0000:00:07.2
/sys/kernel/iommu_groups/12/devices/0000:00:1c.0
/sys/kernel/iommu_groups/2/devices/0000:00:06.0
/sys/kernel/iommu_groups/10/devices/0000:00:17.0
/sys/kernel/iommu_groups/0/devices/0000:00:00.0
/sys/kernel/iommu_groups/9/devices/0000:00:16.0
```

`lspci`:

```shell
root@pve:~# lspci
00:00.0 Host bridge: Intel Corporation Device 4621 (rev 02)
00:02.0 VGA compatible controller: Intel Corporation Device 46a6 (rev 0c)
00:06.0 PCI bridge: Intel Corporation Device 464d (rev 02)
00:07.0 PCI bridge: Intel Corporation Device 463f (rev 02)
00:07.2 PCI bridge: Intel Corporation Device 462f (rev 02)
00:0d.0 USB controller: Intel Corporation Device 461e (rev 02)
00:0d.2 USB controller: Intel Corporation Device 463e (rev 02)
00:0d.3 USB controller: Intel Corporation Device 466d (rev 02)
00:14.0 USB controller: Intel Corporation Device 51ed (rev 01)
00:14.2 RAM memory: Intel Corporation Device 51ef (rev 01)
00:14.3 Network controller: Intel Corporation Device 51f0 (rev 01)
00:15.0 Serial bus controller [0c80]: Intel Corporation Device 51e8 (rev 01)
00:15.1 Serial bus controller [0c80]: Intel Corporation Device 51e9 (rev 01)
00:16.0 Communication controller: Intel Corporation Device 51e0 (rev 01)
00:17.0 SATA controller: Intel Corporation Device 51d3 (rev 01)
00:19.0 Serial bus controller [0c80]: Intel Corporation Device 51c5 (rev 01)
00:19.1 Serial bus controller [0c80]: Intel Corporation Device 51c6 (rev 01)
00:1c.0 PCI bridge: Intel Corporation Device 51be (rev 01)
00:1e.0 Communication controller: Intel Corporation Device 51a8 (rev 01)
00:1e.3 Serial bus controller [0c80]: Intel Corporation Device 51ab (rev 01)
00:1f.0 ISA bridge: Intel Corporation Device 5182 (rev 01)
00:1f.3 Multimedia audio controller: Intel Corporation Device 51c8 (rev 01)
00:1f.4 SMBus: Intel Corporation Device 51a3 (rev 01)
00:1f.5 Serial bus controller [0c80]: Intel Corporation Device 51a4 (rev 01)
01:00.0 Non-Volatile memory controller: Device 1dbe:5220 (rev 01)
56:00.0 Ethernet controller: Intel Corporation Ethernet Controller I225-V (rev 03)
```

```shell
root@pve:~# lspci -knn | grep -i -A 2 vga
00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:46a6] (rev 0c)
        DeviceName: Onboard - Video
        Subsystem: Device [1e50:8012]
```

添加 PCI 设备：`00:02.0`

### vm 配置文件

`/etc/pve/nodes/pve/qemu-server/100.conf`

