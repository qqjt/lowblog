---
title: 华硕 B550i 主板安装 windows server 2022 并更新驱动
tags: ['刷机', 'Armbian', '玩客云']
date: 2023-11-18
updated: 2023-11-18
---

记录下华硕 B550I 主板安装 Windows Server 2022 系统并打上各种驱动的过程。

## 1. 主要硬件配置

- 主板：ROG STRIX B550-I GAMING，板载：
    - Intel I225-V 2.5G有线网卡
    - Intel AX200 无线网卡带蓝牙

- CPU：AMD 3300X
- 显卡：Nvidia 2060 super

## 2. 系统安装

使用的系统 ISO 文件为 `zh-cn_windows_server_2022_updated_sep_2023_x64_dvd_892eeda9.iso`，用 Rufus 制作系统U盘，正常安装即可。
安装完成后没有网卡驱动上不了网，临时插了一个免驱的 usb 转千兆有线网卡，用来上网。打开 Windows Update 更新系统到最新。

## 3. 驱动安装

### 3.1 I225-V 2.5G 网卡驱动

在安装无线网卡驱动前，需要在“添加角色和功能”里，安装好 `无线LAN服务`，具体过程不赘述。

去 Intel 网站下载驱动包：<https://www.intel.cn/content/www/cn/zh/products/sku/184676/intel-ethernet-controller-i225v/downloads.html>，一个超级大包 `Release_28.2.1.zip`。

我解压后直接运行 `Autorun.exe` 安装失败，需要改 inf 文件后，手动安装。

参考 [Windows Server 2022安装Intel I225-V/I226-V驱动 - 夸克之书](https://www.quarkbook.com/?p=1414)，具体步骤为：

- 打开设备管理器，找到网卡设备，右键-属性-详细信息，下拉选择硬件ID，记录下值，我的为 `PCI\VEN_8086&DEV_15F3&SUBSYS_87D21043&REV_03`。
- 文本编辑器打开解压好的驱动程序 inf 文件：`Release_28.2.1\PRO2500\Winx64\WS2022\e2f.inf`，查找 `DEV_15F3`，在 `[Intel.NTamd64.10.0.1..17763]` 下有 3 处：
    ```
    [Intel.NTamd64.10.0.1..17763]
    ; DisplayName               Section                     DeviceID
    ; -----------               -------                     --------
    %E15F2NC.DeviceDesc%      = E15F2.10.0.1..17763,        PCI\VEN_8086&DEV_15F2&REV_01
    %E15F3NC.DeviceDesc%      = E15F3.10.0.1..17763,        PCI\VEN_8086&DEV_15F3&REV_01
    %E0D9FNC.DeviceDesc%      = E0D9F.10.0.1..17763,        PCI\VEN_8086&DEV_0D9F&REV_02
    %E5502NC.DeviceDesc%      = E5502.10.0.1..17763,        PCI\VEN_8086&DEV_5502&REV_02
    %E15F2_2NC.DeviceDesc%    = E15F2_2.10.0.1..17763,      PCI\VEN_8086&DEV_15F2&REV_02
    %E15F3_2NC.DeviceDesc%    = E15F3_2.10.0.1..17763,      PCI\VEN_8086&DEV_15F3&REV_02
    %E15F2_3NC.DeviceDesc%    = E15F2_3.10.0.1..17763,      PCI\VEN_8086&DEV_15F2&REV_03
    %E15F3_3NC.DeviceDesc%    = E15F3_3.10.0.1..17763,      PCI\VEN_8086&DEV_15F3&REV_03
    ...
    ```
- 复制下设备对应的行（我的是 `%E15F3_3NC.DeviceDesc%    = E15F3_3.10.0.1..17763,      PCI\VEN_8086&DEV_15F3&REV_03`），粘贴到 `[Intel.NTamd64.10.0...17763]` 下面：

    ```
    [Intel.NTamd64.10.0...17763]
    ; DisplayName               Section                     DeviceID
    ; -----------               -------                     --------
    %E15F3_3NC.DeviceDesc%    = E15F3_3.10.0.1..17763,      PCI\VEN_8086&DEV_15F3&REV_03
    ...
    ```

- 管理员身份打开 CMD，输入命令：

    ```shell
    bcdedit -set loadoptions DISABLE_INTEGRITY_CHECKS
    bcdedit -set TESTSIGNING ON
    ```
- 高级启动重启Windows，启动设置 - **禁用驱动程序强制签名。**
- 打开设备管理器，右键未识别的网卡设备，更新驱动程序-浏览我的电脑以查找驱动程序，选择之前解压的 `Release_28.2.1` 文件夹，这次即可安装成功。

### 3.2 无线网卡 AX200 及蓝牙

直接去 intel 网站下载驱动安装即可。

Wi-Fi：<https://www.intel.cn/content/www/cn/zh/download/19351/windows-10-and-windows-11-wi-fi-drivers-for-intel-wireless-adapters.html>
蓝牙：<https://www.intel.cn/content/www/cn/zh/download/18649/intel-wireless-bluetooth-for-windows-10-and-windows-11.html>

安装完成后还有一个蓝牙相关设备未识别，硬件ID是 `BTH\MS_BTHPAN`。右键未识别的网卡设备，更新驱动程序-浏览我的电脑以查找驱动程序-让我从计算机上的可用驱动程序列表中选择，选择蓝牙，厂商选`Microsoft`，型号选 `个人区域网服务`，下一步确认后即可安装好。

### 3.3 AMD 芯片组

下载Windows 10 版本的安装包，解压后手动安装，参考 <https://linustechtips.com/topic/1391635-motherboard-drivers-not-installing-on-windows-server-2019/?do=findComment&comment=15176032>。

- 去 AMD 的官网下载 Win10 版本的芯片组驱动： <https://www.amd.com/zh-hans/support/chipsets/amd-socket-am4/b550>，我下载的文件是 `amd_chipset_software_5.08.02.027.exe`。
- 双击运行下载的文件，会自动解压到 `C:\AMD`，因为找不到对应的硬件，安装进行不下去。
- 打开 `C:\AMD\Chipset_Software\Packages\IODriver`，挨个进入子文件夹，手动运行里面的 `msi` 文件，观察设备管理器里未识别的设备，是否有变少。

经过上面的操作后，我设备管理器里已经没有未识别的设备了，这时候再开启安全检查（同样的管理员身份运行CMD）：

```shell
bcdedit -set loadoptions ENABLE_INTEGRITY_CHECKS
bcdedit -set TESTSIGNING OFF
```

重启系统，一切正常了。

## 4. 备份驱动

为方便重装系统，备份下驱动：

```shell
dism /online /export-driver /destination:D:\DriversBackup
```

下次重装就不用挨个下载驱动了，直接在设备管理器里，未识别的设备上右键更新驱动程序，选择这个备份好的驱动文件夹即可。