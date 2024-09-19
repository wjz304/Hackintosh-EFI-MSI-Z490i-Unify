# Hackintosh-EFI-MSI-Z490i-Unify  

## 介绍  
[Hackintosh-EFI-MSI-Z490i-Unify](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify)


## 说明  
MSI-Z490i-Unify 的黑苹果 EFI  (Z490 UNIFY 兼容)  
当前支持 Monterey 12(b), Ventura 13(b), Sonoma 14(b), Sequoia 15(b)
<!--
downloads
<a href="https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/releases/latest">
<img src="https://img.shields.io/github/downloads/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/total.svg?style=flat" alt="downloads"/>
</a>
-->
<!-- version -->
<a href="https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/releases/latest">
<img src="https://img.shields.io/github/release/wjz304/Hackintosh-EFI-MSI-Z490i-Unify.svg?style=flat" alt="latest version"/>
</a>
<!-- version -->
<a href="https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/releases">
<img src="https://img.shields.io/github/v/release/wjz304/Hackintosh-EFI-MSI-Z490i-Unify?include_prereleases&label=prereleases" alt="latest version"/>
</a>
<!-- platform -->
<a href="https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify">
<img src="https://img.shields.io/badge/platform-macOS-lightgrey.svg?style=flat" alt="platform"/>
</a>
<!-- license -->
<a href="https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/blob/master/License.txt">
<img src="https://img.shields.io/github/license/wjz304/Hackintosh-EFI-MSI-Z490i-Unify.svg?style=flat" alt="license"/>
</a>

* release: 稳定版本. 
* prerelease: 每天自动更新kext和OC, 可能存在未知问题. 如无必要请使用 release 版本. 
* 如果需要 BigSur版本, 或者需要OC-Mod, 可参考 Custom [#25](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/issues/34) 自动构建打包.   

## 配置  
 规格     | 详细信息
 ---------|--------
 型号     |
 主板     | 微星 MEG Z490I UNIFY (MS-7C77)
 处理器   | 英特尔 Core i7-10700K @ 3.80GHz 八核
 内存     | 64 GB ( 海盗船 DDR4 3600MHz 32GB x 2 )
 硬盘     | 西数 WD_BLACK SN850X 1000GB ( 1 TB / 固态硬盘 )
 显卡     | AMD Radeon RX 5700 XT ( 8 GB / 蓝宝石 )
 无线网卡 | 英特尔® Wi-Fi 6 AX201 160MHz ( 板载 )
 有线网卡 | Realtek RTL8125B
 声卡     | Realtek ALC S1220A
 触摸板   |
 触摸屏   |


## BIOS
||||
--|-------------------------------------------|-----------
1 |Setting\高级\内建显示配置\集成显卡多显示器 | [允许]
2 |Setting\高级\整合周边设备\网络协议栈       | [允许]
3 |OC\扩展内存预设技术(XMP)                   | [Enabled]
4 |OC\CPU Features\CFG Lock                   | [Disabled]
5 |Security Device Support                    | [Enabled] （Win11 - TPM 2.0）
6 |Settings\Security\Secure Boot              | [Disabled] （BIOS Ver ≥ 1C0）
7 |Setting\高级\Re-size BAR Support            | [Disabled] （BIOS Ver ≥ 1D0）

***或者使用微星主板自带的 D.T.M 功能, 一键开启黑苹果所需设置. ***  
*[参考附件 screenshot/MSI_SnapShot_微星一键黑苹果.bmp]*  

## 使用
 1. 关于各个配置文件：  
    #### config.plist（默认）：   
	- 为核显加速且未指定独显的版本. （AMD卡非RX5700XT的请使用该plist并自行设置显卡参数）
    #### config_iGPU.plist： 
	- 为只有核显版本, HDMI接口 画面和音频正常；DP接口 画面和音频正常(HDMI和DP共存时, 只能HDMI输出音频).   
	  （NVIDIA卡请使用该plist, 并在 boot-args 属性中加入 -wegnoegpu 屏蔽独显）
	#### config_RX5700XT.plist： 
	- 为RX5700XT优化核显加速版本, RX Vega 56/64 / RX 5xxx / RX 6xxx 系列 请查看[AMD GPU #25](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/issues/25) 或者尝试勾选 RadeonBoost.kext 进行优化. 
	#### config_RX5700XT&iGPU.plist： 
	- 为RX5700XT优化核显共存版本, RX Vega 56/64 / RX 5xxx / RX 6xxx 系列 请查看[AMD GPU #25](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/issues/25) 或者尝试勾选 RadeonBoost.kext 进行优化.   

 2. 显示器声音控制软件：[MonitorControl](https://github.com/MonitorControl/MonitorControl)  

 3. 关于USB：  
 	USBPorts_9pin.kext 为舍弃主板的 Type-E 接口的版本. （默认）    
	USBPorts_typee.kext 为舍弃主板的 9pin 接口的版本.   
	(由于15个u口的限制, USBPorts_9pin.kext 和 USBPorts_typee.kext 均舍弃了 后置TYPE-C和红色USB两个口的2.0兼容. 悉知!)  
	
	USBPorts_Z490_beta.kext 为Z490 UNIFY (non-i)版本, 仅定制部分USB满足安装和日常使用, (感谢网友（SUNN）提供USB MAP信息).   
	直接拷贝替换 USBPorts.kext 即可.   

 4. 无线网卡 & 蓝牙：  
	BigSur：请参考 Custom [#25](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/issues/34) 自动构建打包.   
	注：  
	1. 如果Wifi/BT无法打开请尝试执行一下 `sudo kextcache -i /` 关机再开机(不要重启).   
	2. 另外 偶现开启 "-v"(啰嗦模式) 无线网卡不工作的问题, 请尝试关闭 "-v" (boot-args 属性中删除 -v ). 
	3. 出场批次不同 BT 的 LPM [（如何查看LPM版本）](https://support.microsoft.com/en-us/windows/what-bluetooth-version-is-on-my-pc-f5d4cff7-c00d-337b-a642-d2d23b082793) 的版本不同,    
	   LPM为11的版本Ventura下需要集成 IntelBTPatcher.kext. （默认已加, 非11版本可以取消勾选）   
	
 5. 关于 Safari 不能看 Prime/Netflix 的问题.   
	请尝试修改机型为 iMacPro1,1 并删除集显注入 DeviceProperties -> PciRoot(0x0)/Pci(0x2,0x0) 部分.   

 6. 如果使用 Samsung PM981 型号 会报 IONVMe 错误.   
    如果使用 Samsung 960 Evo/Pro 970 Evo/Pro 无故死机, 启动很慢, 可以尝试重装解决, 或者尝试修改 SetApfsTrimTimeout 为 0（关闭trim, 进入OS后可用 sensei软件 或者 sudo trimforce enable 命令 打开）.   
	但是仍然建议更换非三星硬盘.   
	###### `log show --last boot | grep "trims took"`  
	- ###### `980 Pro：kernel: (apfs) spaceman_scan_free_blocks:3154: disk1 scan took 212.092312 s, trims took 212.054291 s`  
	- ###### `SN750：kernel: (apfs) spaceman_scan_free_blocks:3153: disk1 scan took 0.319178 s, trims took 0.313471 s`
 
 7. 关于休眠：  
	请使用 命令或者 Hackintool 修复休眠模式 hibernatemode 和 proximitywake.   
	如果唤醒弹窗 “电脑关机是因为发生了问题” , 请前往 “控制台” 删除 “诊断报告” 中所有日志. （主要是 “Sleep Wake Failure” 相关的）  
	另外BIOS 可开启 “PCIE设备唤醒” 和 “网络唤醒”, 将支持键鼠唤醒. （不要开启 USB Standby Power at S4/S5）  
	
	PS： 
	* 感谢 [maoxikun](https://github.com/wjz304/Hackintosh-EFI-MSI-Z490i-Unify/issues/40) 对睡眠唤醒后自动关机问题的测试和解决方案.   

	设置 hibernatemode 和 proximitywake：
	- ###### `sudo pmset -a hibernatemode 0`
	- ###### `sudo pmset -a proximitywake 0`
	or:  
  	![Image text](screenshot/QQ20220523-130847.png)  
	
	
## 预览
 ![Image text](screenshot/QQ20220607-190543@2x.png)   
 ![Image text](screenshot/QQ20200920-183718.png)
 ![Image text](screenshot/QQ20220826141938.png)
 ![Image text](screenshot/MSI_SnapShot_黑苹果&WIN11.bmp)   


## 打赏一下 Sponsoring
- <img src="https://raw.githubusercontent.com/wjz304/wjz304/master/my/buymeacoffee.png" width="700">


## 鸣谢
https://github.com/acidanthera/OpenCorePkg  
https://gitee.com/btwise/OpenCore_NO_ACPI  

https://github.com/OpenIntelWireless/itlwm  
https://github.com/OpenIntelWireless/HeliPort  

https://github.com/dortania/bugtracker/issues/192  



