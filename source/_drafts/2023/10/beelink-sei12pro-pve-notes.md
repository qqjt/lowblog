---
title: 零刻 SEi 12 Pro PVE 安装配置记录
date: 2023-10-24 14:59:10
tags: [ 'PVE' ]
---

在零刻 SEi 12 Pro 迷你主机上安装并配置 PVE 8.0。

## 1. BIOS 设置

- `Advanced` - `CPU Configuration`:

    ```
    Intel(VMX) Virtualization Technology: Enabled
    Active Efficient-cores: 0 # 关闭小核心保平安
    ```

- `Chipset` - `System Agent(SA) Configuration`:

    ```
    VT-d: Enabled
    X2APIC Opt Out: Disabled(default)
    ```

## 2. 系统安装

前往 <https://www.proxmox.com/downloads> （或者 <https://mirrors.ustc.edu.cn/proxmox/iso/>
）下载系统镜像，使用 `balenaEtcher` 软件写入到U盘里，再从U盘启动，照着向导安装即可。

由于之前发生过用 `Rufus` 软件做的U盘安装不了的情况，所以这次改用 `balenaEtcher` 了。

安装成功后可以通过浏览器或者 SSH 软件访问。

## 3. 硬盘与分区调整

默认安装成功后有俩个存储：`local` 与 `local-lvm`
，按照网上的博客建议（PVE的local和local-lvm：<https://foxi.buduanwang.vip/virtualization/pve/1434.html/>
），删掉了 `local-lvm`：

```shell
lvremove /dev/pve/data
lvextend -rl +100%FREE /dev/pve/root
```

在网页端 `Datacenter` - `Storage` 处，删掉 `local-lvm`，修改 `local` ，勾选上全部用途：

![storage.png](storage.png)

## 4. 修改软件源

https://mirrors.ustc.edu.cn/help/proxmox.html

```shell
cp /etc/apt/sources.list /etc/apt/sources.list.bak
mv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak

sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

source /etc/os-release
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve $VERSION_CODENAME pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

apt update && apt upgrade -y

# 安装软件
apt install git vim zsh
```

## 5. 硬件直通

先照着官方的文档操作，主要是这俩篇：

1. PCI Passthrough: <https://pve.proxmox.com/wiki/PCI_Passthrough>
2. PCI(e) Passthrough: <https://pve.proxmox.com/wiki/PCI(e)_Passthrough>

### 5.1 一些检查命令及输出

1. `dmesg | grep -e DMAR -e IOMMU`
    ```shell
    ➜  ~ dmesg | grep -e DMAR -e IOMMU          
    [    0.010200] ACPI: DMAR 0x00000000441D7000 000088 (v02 INTEL  EDK2     00000002      01000013)
    [    0.010230] ACPI: Reserving DMAR table memory at [mem 0x441d7000-0x441d7087]
    [    0.078238] DMAR: IOMMU enabled
    [    0.181322] DMAR: Host address width 39
    [    0.181323] DMAR: DRHD base: 0x000000fed90000 flags: 0x0
    [    0.181327] DMAR: dmar0: reg_base_addr fed90000 ver 4:0 cap 1c0000c40660462 ecap 29a00f0505e
    [    0.181329] DMAR: DRHD base: 0x000000fed91000 flags: 0x1
    [    0.181332] DMAR: dmar1: reg_base_addr fed91000 ver 5:0 cap d2008c40660462 ecap f050da
    [    0.181333] DMAR: RMRR base: 0x0000004b000000 end: 0x0000004f7fffff
    [    0.181335] DMAR-IR: IOAPIC id 2 under DRHD base  0xfed91000 IOMMU 1
    [    0.181336] DMAR-IR: HPET id 0 under DRHD base 0xfed91000
    [    0.181337] DMAR-IR: Queued invalidation will be enabled to support x2apic and Intr-remapping.
    [    0.182918] DMAR-IR: Enabled IRQ remapping in x2apic mode
    [    0.681712] pci 0000:00:02.0: DMAR: Skip IOMMU disabling for graphics
    [    0.761309] DMAR: No ATSR found
    [    0.761309] DMAR: No SATC found
    [    0.761310] DMAR: IOMMU feature fl1gp_support inconsistent
    [    0.761311] DMAR: IOMMU feature pgsel_inv inconsistent
    [    0.761311] DMAR: IOMMU feature nwfs inconsistent
    [    0.761312] DMAR: IOMMU feature dit inconsistent
    [    0.761312] DMAR: IOMMU feature sc_support inconsistent
    [    0.761313] DMAR: IOMMU feature dev_iotlb_support inconsistent
    [    0.761313] DMAR: dmar0: Using Queued invalidation
    [    0.761315] DMAR: dmar1: Using Queued invalidation
    [    0.761831] DMAR: Intel(R) Virtualization Technology for Directed I/O
    ```
2. `dmesg | grep 'remapping'`:

  ```shell
  ➜  ~ dmesg | grep 'remapping'
  [    0.182424] DMAR-IR: Queued invalidation will be enabled to support x2apic and Intr-remappin.
  [    0.184009] DMAR-IR: Enabled IRQ remapping in x2apic mode
  ```

`pvesh get /nodes/{nodename}/hardware/pci --pci-class-blacklist ""`(nodename 为节点名称):

```shell
➜  ~ pvesh get /nodes/pve/hardware/pci --pci-class-blacklist ""
┌──────────┬────────┬──────────────┬────────────┬────────┬──────────────────────────────────────
│ class    │ device │ id           │ iommugroup │ vendor │ device_name                          
╞══════════╪════════╪══════════════╪════════════╪════════╪══════════════════════════════════════
│ 0x010601 │ 0x51d3 │ 0000:00:17.0 │         10 │ 0x8086 │ Alder Lake-P SATA AHCI Controller    
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x010802 │ 0x5013 │ 0000:01:00.0 │         15 │ 0x1987 │ PS5013 E13 NVMe Controller           
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x020000 │ 0x15f3 │ 0000:56:00.0 │         16 │ 0x8086 │ Ethernet Controller I225-V           
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x028000 │ 0x51f0 │ 0000:00:14.3 │          7 │ 0x8086 │ Alder Lake-P PCH CNVi WiFi           
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x030000 │ 0x4626 │ 0000:00:02.0 │          0 │ 0x8086 │ Alder Lake-P Integrated Graphics Cont
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x040100 │ 0x51c8 │ 0000:00:1f.3 │         14 │ 0x8086 │ Alder Lake PCH-P High Definition Audi
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x050000 │ 0x51ef │ 0000:00:14.2 │          6 │ 0x8086 │ Alder Lake PCH Shared SRAM           
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060000 │ 0x4621 │ 0000:00:00.0 │          1 │ 0x8086 │                                      
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060100 │ 0x5182 │ 0000:00:1f.0 │         14 │ 0x8086 │ Alder Lake PCH eSPI Controller       
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060400 │ 0x464d │ 0000:00:06.0 │          2 │ 0x8086 │ 12th Gen Core Processor PCI Express x
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060400 │ 0x463f │ 0000:00:07.0 │          3 │ 0x8086 │ Alder Lake-P Thunderbolt 4 PCI Expres
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060400 │ 0x462f │ 0000:00:07.2 │          4 │ 0x8086 │ Alder Lake-P Thunderbolt 4 PCI Expres
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x060400 │ 0x51be │ 0000:00:1c.0 │         12 │ 0x8086 │                                      
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x078000 │ 0x51e0 │ 0000:00:16.0 │          9 │ 0x8086 │ Alder Lake PCH HECI Controller       
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x078000 │ 0x51a8 │ 0000:00:1e.0 │         13 │ 0x8086 │ Alder Lake PCH UART #0               
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c0330 │ 0x461e │ 0000:00:0d.0 │          5 │ 0x8086 │ Alder Lake-P Thunderbolt 4 USB Contro
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c0330 │ 0x51ed │ 0000:00:14.0 │          6 │ 0x8086 │ Alder Lake PCH USB 3.2 xHCI Host Cont
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c0340 │ 0x463e │ 0000:00:0d.2 │          5 │ 0x8086 │ Alder Lake-P Thunderbolt 4 NHI #0    
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c0340 │ 0x466d │ 0000:00:0d.3 │          5 │ 0x8086 │ Alder Lake-P Thunderbolt 4 NHI #1    
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c0500 │ 0x51a3 │ 0000:00:1f.4 │         14 │ 0x8086 │ Alder Lake PCH-P SMBus Host Controlle
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51e8 │ 0000:00:15.0 │          8 │ 0x8086 │ Alder Lake PCH Serial IO I2C Controll
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51e9 │ 0000:00:15.1 │          8 │ 0x8086 │ Alder Lake PCH Serial IO I2C Controll
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51c5 │ 0000:00:19.0 │         11 │ 0x8086 │ Alder Lake-P Serial IO I2C Controller
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51c6 │ 0000:00:19.1 │         11 │ 0x8086 │ Alder Lake-P Serial IO I2C Controller
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51ab │ 0000:00:1e.3 │         13 │ 0x8086 │                                      
├──────────┼────────┼──────────────┼────────────┼────────┼──────────────────────────────────────
│ 0x0c8000 │ 0x51a4 │ 0000:00:1f.5 │         14 │ 0x8086 │ Alder Lake-P PCH SPI Controller      
└──────────┴────────┴──────────────┴────────────┴────────┴──────────────────────────────────────
```

### 5.2 核显直通

`/etc/default/grub`

`intel_iommu=on` `iommu=pt`

`/etc/modules`

```shell
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```

`update-grub`

`update-initramfs -u -k all`

`find /sys/kernel/iommu_groups/ -type l`:

```shell
echo "blacklist i915" >> /etc/modprobe.d/blacklist.conf
```

## 6. 备忘

- vm 配置文件位置：`/etc/pve/nodes/pve/qemu-server/<vm>.conf`