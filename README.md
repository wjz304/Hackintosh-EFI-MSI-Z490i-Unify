# Hackintosh-EFI-MSI-Z490i-Unify-Hackintosh

#### 介绍
MSI-Z490i-Unify-Hackintosh  

#### 说明
MSI-Z490i-Unify 的黑苹果 EFI  

当前支持 ~~ BigSur 11.5.1  & Monterey 12.0b4

#### 配置
| 规格     | 详细信息                                                                       |
| -------- | ------------------------------------------------------------------------------ |
| 型号     |                                                                                |
| 主板     | 微星 MEG Z490I UNIFY (MS-7C77)                                                 |
| 处理器   | 英特尔 Core i7-10700K @ 3.80GHz 八核                                           |
| 内存     | 64 GB ( 海盗船 DDR4 3200MHz )                                                  |
| 硬盘     | 三星 SSD 980 PRO 1TB ( 1 TB / 固态硬盘 )                                       |
| 显卡     | AMD Radeon RX 5700 XT ( 8 GB / 蓝宝石 )                                        |
| 无线网卡 | 英特尔® Wi-Fi 6 AX201 ( 板载 )                                                 |
| 声卡     |                                                                                |
| 触摸板   |                                                                                |
| 触摸屏   |                                                                                |


#### BIOS
1.Setting\高级\内建显示配置\集成显卡多显示器 [允许]  
2.Setting\高级\整合周边设备\网络协议栈       [允许]  
3.OC\扩展内存预设技术(XMP)                   [Enabled]  
4.OC\CPU Features\CFG Lock                   [Disabled]  


#### 使用
 **使用说明:** 
 1. 有线网卡：
    表现为网络中以太网显示电缆被拔出，无信号。
	需要 高级--硬件--设置速度和双工，
		速度：根据你的路由器来，如果是百兆的口，就选100，千兆的选1000。
		双工：选节能以太网，如果还是不行，换其它的。
 
 2. 无线网卡 & 蓝牙：
	 BigSur：请勾选 AirportItlwm11.kext 和 IntelBluetoothInjector.kext，并取消勾选 AirportItlwm12.kext 和 BlueToolFixup.kext。
     Monterey：请勾选  AirportItlwm12.kext 和 BlueToolFixup.kext，并取消勾选AirportItlwm11.kext 和 IntelBluetoothInjector.kext。
	 
 3. 非 RX 5700 系列 请尝试使用 config_integrated.plist 启动。
	 
	 
	 
 ![Image text](screenshot/QQ20200920-233809.png)  
 ![Image text](screenshot/QQ20200920-183718.png)  
  
  
#### 鸣谢
https://github.com/2742280997/z490i-unify  
https://github.com/kingwood77/MSI-Z490i-Unify-Hackintosh  
https://github.com/milkpeanut/MSI-Z490I-UNIFY-Hackintosh  
https://github.com/kreactnative/EFI-z490-ace-10700k-bigSur  

https://github.com/acidanthera/OpenCorePkg  
https://gitee.com/btwise/OpenCore_NO_ACPI  

https://github.com/OpenIntelWireless/itlwm  
https://github.com/OpenIntelWireless/HeliPort  



