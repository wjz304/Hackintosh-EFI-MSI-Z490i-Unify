#-*- coding:utf-8 -*-
# 
# Copyright (C) 2022 Ing <https://github.com/wjz304>
# 
# This is free software, licensed under the MIT License.
# See /LICENSE for more information.
#

import os, re, sys, json, shutil, getopt, datetime, zipfile, platform, plistlib

try:
    import wget
except ModuleNotFoundError:
    os.system('pip3 install wget')
    import wget

try:
    import urllib3
except ModuleNotFoundError:
    os.system('pip3 install urllib3')
    import urllib3


date_curr = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
date_last = ''

date_last_file = 'timestamp'
try:
    with open(date_last_file,'r') as f:
        date_last = f.read()
except:
    pass

date_last = ''   # Forced


class UpdateKexts():
    def __init__(self, headers = None) -> None:
        if headers is None:
            headers = {'user-agent': 'Python-urllib/3.0'}
        self.PM = urllib3.PoolManager(headers=headers)  # give github a user-agent so they don't block our requests
        self.alpha = True
        self.kexts = [
            ['Lilu', 'EFI/OC/Kexts/Lilu.kext', 'Lilu.kext'],
            ['WhateverGreen', 'EFI/OC/Kexts/WhateverGreen.kext', 'WhateverGreen.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/VirtualSMC.kext', 'Kexts/VirtualSMC.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/SMCSuperIO.kext', 'Kexts/SMCSuperIO.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/SMCProcessor.kext', 'Kexts/SMCProcessor.kext'],
            ['AppleALC', 'EFI/OC/Kexts/AppleALC.kext', 'AppleALC.kext'],
            # ['LucyRTL8125Ethernet', 'EFI/OC/Kexts/LucyRTL8125Ethernet.kext', 'LucyRTL8125Ethernet.kext'],
            # ['itlwm', 'EFI/OC/Kexts/itlwm.kext', 'itlwm.kext'],
            # ['AirportItlwm', 'EFI/OC/Kexts/AirportItlwm.kext', 'AirportItlwm.kext'],
            ['BrcmPatchRAM', 'EFI/OC/Kexts/BlueToolFixup.kext', 'BlueToolFixup.kext'],
            # ['IntelBluetoothInjector', 'EFI/OC/Kexts/IntelBluetoothInjector.kext', 'IntelBluetoothInjector.kext'],
            # ['IntelBluetoothFirmware', 'EFI/OC/Kexts/IntelBluetoothFirmware.kext', 'IntelBluetoothFirmware.kext'],
        ]
        self.dortaniaKextsJson = None

    def __macosVer(self, osx=''):
        ver = 0
        if osx.lower() in ['ventura', '22']:
            ver = 13
        elif osx.lower() in ['monterey', '21']:
            ver = 12
        elif osx.lower() in ['big_sur', '20']:
            ver = 11
        return ver

    def __kernelVer(self, osx=''):
        ver = 0
        if osx.lower() in ['ventura', '13']:
            ver = 22
        elif osx.lower() in ['monterey', '12']:
            ver = 21
        elif osx.lower() in ['big_sur', '11']:
            ver = 20
        return ver

    def __dlExt(self, url, dir):
        fileName = './' + url.split('/')[-1]
        print('download {}'.format(fileName))
        if os.path.exists(fileName):
             os.remove(fileName)
        #data = self.PM.request('GET', url)
        #with open(fileName,'wb') as f:
        #    f.write(data.data)
        wget.download(url, out=fileName)
        if os.path.exists(dir):
            shutil.rmtree(dir)
        with zipfile.ZipFile(fileName) as zf:
            zf.extractall(dir)
        os.remove(fileName)
        if platform.system().lower() == 'windows':
            print('')

    def __xcopy(self, srcPath, dstPath, ignore=None):
        print('xcopy {} to {}'.format(srcPath, dstPath))
        if os.path.exists(dstPath):
            if os.path.isdir(dstPath):
                shutil.rmtree(dstPath)
            else:
                os.remove(dstPath)
        if os.path.exists(srcPath):
            if os.path.isdir(srcPath):
                shutil.copytree(srcPath, dstPath, ignore=ignore)
            else:
                shutil.copy(srcPath, dstPath)

    def __initDortaniaJson(self):
        print('get {}'.format('dortania config.json'))
        dortaniaUrl = 'https://raw.githubusercontent.com/dortania/build-repo/builds/config.json'
        #res = self.PM.request('GET', dortaniaUrl)
        #self.dortaniaKextsJson = json.loads(res.data.decode('utf-8'))
        wget.download(dortaniaUrl, out='dortaniaConfig.json')
        with open('dortaniaConfig.json', mode="rb") as f:
            self.dortaniaKextsJson = json.loads(f.read())
        os.remove('dortaniaConfig.json')
        if platform.system().lower() == 'windows':
            print('')

    def upgradeDortaniaKexts(self, kextName, dstPath, srcPath):
        if self.dortaniaKextsJson is None:
            self.__initDortaniaJson()
        print('upgrade {}'.format(kextName))
        if self.dortaniaKextsJson[kextName]['versions'][0]['date_built'] > self.dortaniaKextsJson[kextName]['versions'][len(self.dortaniaKextsJson[kextName]['versions']) - 1]['date_built']:
            idx = 0
        else:
            idx = len(self.dortaniaKextsJson[kextName]['versions']) - 1
        if self.dortaniaKextsJson[kextName]['versions'][idx]['date_built'] > date_last:
            url = self.dortaniaKextsJson[kextName]['versions'][idx]['links']['release']
            self.__dlExt(url, './tmp')
            self.__xcopy('./tmp/' + srcPath, dstPath)
            shutil.rmtree('./tmp')

    def upgradeAcidantheraKexts(self, kextName, dstPath, srcPath):
        print('upgrade {}'.format(kextName))
        res = self.PM.request('GET', 'https://api.github.com/repos/acidanthera/{}/releases'.format(kextName))
        kext = json.loads(res.data.decode('utf-8'))
        for kextVer in kext:
            if self.alpha is False and 'alpha' in kextVer['name'].lower():
                continue
            if kextVer['published_at'] > date_last:
                for item in kextVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/' + srcPath, dstPath)
                        shutil.rmtree('./tmp')
                        break
            break

    def upgradeI2C(self):
        print('upgrade {}'.format('VoodooI2C and VoodooI2CHID'))
        res = self.PM.request('GET', 'https://api.github.com/repos/VoodooI2C/VoodooI2C/releases')
        self.i2c = json.loads(res.data.decode('utf-8'))
        for i2cVer in self.i2c:
            if self.alpha is False and 'alpha' in i2cVer['name'].lower():
                continue
            if i2cVer['published_at'] > date_last:
                for item in i2cVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/VoodooI2C.kext', 'EFI/OC/Kexts/VoodooI2C.kext')
                        self.__xcopy('./tmp/VoodooI2CHID.kext', 'EFI/OC/Kexts/VoodooI2CHID.kext')
                        shutil.rmtree('./tmp')
                        break
            break

        
    def upgradeEC(self):
        print('upgrade {}'.format('ECEnabler'))
        res = self.PM.request('GET', 'https://api.github.com/repos/1Revenger1/ECEnabler/releases')
        self.i2c = json.loads(res.data.decode('utf-8'))
        for i2cVer in self.i2c:
            if self.alpha is False and 'alpha' in i2cVer['name'].lower():
                continue
            if i2cVer['published_at'] > date_last:
                for item in i2cVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/ECEnabler.kext', 'EFI/OC/Kexts/ECEnabler.kext')
                        shutil.rmtree('./tmp')
                        break
            break

    def upgradeRTL8125E(self):
        print('upgrade {}'.format('RTL8125E'))
        res = self.PM.request('GET', 'https://api.github.com/repos/Mieze/LucyRTL8125Ethernet/releases')
        self.i2c = json.loads(res.data.decode('utf-8'))
        for i2cVer in self.i2c:
            if self.alpha is False and 'alpha' in i2cVer['name'].lower():
                continue
            if i2cVer['published_at'] > date_last:
                for item in i2cVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/{}/Release/LucyRTL8125Ethernet.kext'.format(os.listdir('./tmp')[0]), 'EFI/OC/Kexts/LucyRTL8125Ethernet.kext')
                        shutil.rmtree('./tmp')
                        break
            break
        
    def upgradeItlwm(self, itver = ['ventura', 'monterey']):
        print('upgrade {}'.format('AirportItlwm_{} and itlwm'.format(itver)))
        res = self.PM.request('GET', 'https://api.github.com/repos/OpenIntelWireless/itlwm/releases')
        self.itlwm = json.loads(res.data.decode('utf-8'))
        for itlwmVer in self.itlwm:
            if self.alpha is False and 'alpha' in itlwmVer['name'].lower():
                continue
            if itlwmVer['published_at'] > date_last:
                if len(itver) == 1:
                    for f in os.listdir('EFI/OC/Kexts')[:]:
                        if f.startswith('AirportItlwm-'):
                            if os.path.isdir('EFI/OC/Kexts/{}'.format(f)):
                                shutil.rmtree('EFI/OC/Kexts/{}'.format(f))
                            else:
                                os.remove('EFI/OC/Kexts/{}'.format(f))
                    # plist
                    for pf in os.listdir('EFI/OC/'):
                        idx = 0
                        if os.path.isfile('EFI/OC/{}'.format(pf)) and pf.endswith('.plist'):
                            with open('EFI/OC/{}'.format(pf), 'rb') as f:
                                pldata = plistlib.load(f, fmt=plistlib.FMT_XML)
                            isdel = False
                            ismod = False
                            for kext in pldata['Kernel']['Add'][:]:
                                if kext['BundlePath'].startswith('AirportItlwm-'):
                                    isdel = True
                                    pldata['Kernel']['Add'].remove(kext)
                                if kext['BundlePath'] == 'AirportItlwm.kext':
                                    ismod = True
                                    kext['MaxKernel'] = '{}.99.99'.format(self.__kernelVer(itver[0]))
                                    kext['MinKernel'] = '{}.00.00'.format(self.__kernelVer(itver[0]))
                            if ismod == False:
                                if idx == 0:
                                    for index in range(len(pldata['Kernel']['Add'])):
                                        if pldata['Kernel']['Add'][index]['BundlePath'] == 'itlwm.kext':
                                            idx = index + 1
                                kextTmp = {}
                                kextTmp['Arch'] = 'Any'
                                kextTmp['BundlePath'] = 'AirportItlwm.kext'
                                kextTmp['Comment'] = 'V{} | {} Wi-Fi'.format(itlwmVer['name'][itlwmVer['name'].find('v')+1:itlwmVer['name'].find('-')], self.__macosVer(itver[0]))
                                kextTmp['Enabled'] = True
                                kextTmp['ExecutablePath'] = 'Contents/MacOS/AirportItlwm'
                                kextTmp['MaxKernel'] = '{}.99.99'.format(self.__kernelVer(itver[0]))
                                kextTmp['MinKernel'] = '{}.00.00'.format(self.__kernelVer(itver[0]))
                                kextTmp['PlistPath'] = 'Contents/Info.plist'
                                pldata['Kernel']['Add'].insert(idx, kextTmp)
                                idx += 1
                            with open('EFI/OC/{}'.format(pf), 'wb') as f:
                                plistlib.dump(pldata, f, fmt=plistlib.FMT_XML)
                                
                else:
                    kextitver = ['AirportItlwm-{}.kext'.format(i) for i in itver]
                    for f in os.listdir('EFI/OC/Kexts')[:]:
                        if f == 'AirportItlwm.kext' or (f.startswith('AirportItlwm-') and not f in kextitver):
                            if os.path.isdir('EFI/OC/Kexts/{}'.format(f)):
                                shutil.rmtree('EFI/OC/Kexts/{}'.format(f))
                            else:
                                os.remove('EFI/OC/Kexts/{}'.format(f))
                    # plist
                    for pf in os.listdir('EFI/OC/'):
                        idx = 0
                        if os.path.isfile('EFI/OC/{}'.format(pf)) and pf.endswith('.plist'):
                            with open('EFI/OC/{}'.format(pf), 'rb') as f:
                                pldata = plistlib.load(f, fmt=plistlib.FMT_XML)
                            isdel = False
                            for kext in pldata['Kernel']['Add'][:]:
                                if kext['BundlePath'] == 'AirportItlwm.kext'or (kext['BundlePath'].startswith('AirportItlwm-') and not kext['BundlePath'] in kextitver):
                                    isdel = True
                                    pldata['Kernel']['Add'].remove(kext)
                            for itveridx in itver:
                                ismod = False
                                for kext in pldata['Kernel']['Add']:
                                    if kext['BundlePath'] == 'AirportItlwm-{}.kext'.format(itveridx):
                                        ismod = True
                                        kext['MaxKernel'] = '{}.99.99'.format(self.__kernelVer(itveridx))
                                        kext['MinKernel'] = '{}.00.00'.format(self.__kernelVer(itveridx))
                                        break
                                if ismod == False:
                                    if idx == 0:
                                        for index in range(len(pldata['Kernel']['Add'])):
                                            if pldata['Kernel']['Add'][index]['BundlePath'] == 'itlwm.kext':
                                                idx = index + 1
                                    kextTmp = {}
                                    kextTmp['Arch'] = 'Any'
                                    kextTmp['BundlePath'] = 'AirportItlwm-{}.kext'.format(itveridx)
                                    kextTmp['Comment'] = 'V{} | {} Wi-Fi'.format(itlwmVer['name'][itlwmVer['name'].find('v')+1:itlwmVer['name'].find('-')], self.__macosVer(itveridx))
                                    kextTmp['Enabled'] = True
                                    kextTmp['ExecutablePath'] = 'Contents/MacOS/AirportItlwm'
                                    kextTmp['MaxKernel'] = '{}.99.99'.format(self.__kernelVer(itveridx))
                                    kextTmp['MinKernel'] = '{}.00.00'.format(self.__kernelVer(itveridx))
                                    kextTmp['PlistPath'] = 'Contents/Info.plist'
                                    pldata['Kernel']['Add'].insert(idx, kextTmp)
                                    idx += 1
                            with open('EFI/OC/{}'.format(pf), 'wb') as f:
                                plistlib.dump(pldata, f, fmt=plistlib.FMT_XML)

                for item in itlwmVer['assets']:
                    if len(itver) == 1:
                        if itver[0] in item['name'].lower():
                            # 
                            url = item['browser_download_url']
                            self.__dlExt(url, './tmp')
                            self.__xcopy('./tmp/{}/AirportItlwm.kext'.format(os.listdir('./tmp')[0]), 'EFI/OC/Kexts/AirportItlwm.kext')
                            shutil.rmtree('./tmp')
                            break
                    else:
                        for itveridx in itver:
                            if itveridx in item['name'].lower():
                                # 
                                url = item['browser_download_url']
                                self.__dlExt(url, './tmp')
                                self.__xcopy('./tmp/{}/AirportItlwm.kext'.format(os.listdir('./tmp')[0]), 'EFI/OC/Kexts/AirportItlwm-{}.kext'.format(itveridx))
                                shutil.rmtree('./tmp')
                                break

                for item in itlwmVer['assets']:
                    if not 'airport' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/itlwm.kext', 'EFI/OC/Kexts/itlwm.kext')
                        shutil.rmtree('./tmp')
                        break
            break

    def upgradeIBT(self):
        print('upgrade {}'.format('IntelBluetoothFirmware and IntelBluetoothInjector'))
        res = self.PM.request('GET', 'https://api.github.com/repos/OpenIntelWireless/IntelBluetoothFirmware/releases')
        self.ibt = json.loads(res.data.decode('utf-8'))
        for ibtVer in self.ibt:
            if self.alpha is False and 'alpha' in ibtVer['name'].lower():
                continue
            if ibtVer['published_at'] > date_last:
                for item in ibtVer['assets']:
                    if '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')
                        self.__xcopy('./tmp/IntelBluetoothFirmware.kext', 'EFI/OC/Kexts/IntelBluetoothFirmware.kext')
                        self.__xcopy('./tmp/IntelBluetoothInjector.kext', 'EFI/OC/Kexts/IntelBluetoothInjector.kext')
                        shutil.rmtree('./tmp')
                        break
            break


    def upgradeOC(self, ocver = 'mod'):
        print('upgrade {}'.format('OpenCore_{}'.format(ocver)))
        url = ''
        if ocver == 'rel':
            url = 'https://api.github.com/repos/acidanthera/OpenCorePkg/releases'
        elif ocver == 'pre':
            url = 'https://api.github.com/repos/dortania/build-repo/releases'
        else:
            url = 'https://api.github.com/repos/wjz304/OpenCore_NO_ACPI_Build/releases'
        res = self.PM.request('GET', url)
        self.ocmod = json.loads(res.data.decode('utf-8'))
        for ocVer in self.ocmod:
            if ocVer['published_at'] > date_last:

                for item in ocVer['assets']:
                    if 'release' in item['name'].lower():
                        url = item['browser_download_url']
                        self.__dlExt(url, './tmp')

                        if os.path.exists('EFI/BOOT/BOOTx64.efi'):
                            self.__xcopy('./tmp/X64/EFI/BOOT/BOOTx64.efi', 'EFI/BOOT/BOOTx64.efi')

                        if os.path.exists('EFI/OC/OpenCore.efi'):
                            self.__xcopy('./tmp/X64/EFI/OC/OpenCore.efi', 'EFI/OC/OpenCore.efi')

                        if os.path.exists('EFI/OC/Drivers'):
                            for efi in os.listdir('EFI/OC/Drivers'):
                                self.__xcopy('./tmp/X64/EFI/OC/Drivers/{}'.format(efi), 'EFI/OC/Drivers/{}'.format(efi))

                        if os.path.exists('EFI/OC/Tools'):
                            for efi in os.listdir('EFI/OC/Tools'):
                                self.__xcopy('./tmp/X64/EFI/OC/Tools/{}'.format(efi), 'EFI/OC/Tools/{}'.format(efi))

                        if os.path.exists('EFI/OC/Resources') and os.path.exists('./tmp/X64/EFI/OC/Resources'):
                            if os.path.exists('./tmp/X64/EFI/OC/Resources/Audio') and len(os.listdir('./tmp/X64/EFI/OC/Resources/Audio')) > 0:
                                self.__xcopy('./tmp/X64/EFI/OC/Resources/Audio', 'EFI/OC/Resources/Audio', ignore = shutil.ignore_patterns('.*'))
                            if os.path.exists('./tmp/X64/EFI/OC/Resources/Font') and len(os.listdir('./tmp/X64/EFI/OC/Resources/Font')) > 0:
                                self.__xcopy('./tmp/X64/EFI/OC/Resources/Font', 'EFI/OC/Resources/Font', ignore = shutil.ignore_patterns('.*'))
                            if os.path.exists('./tmp/X64/EFI/OC/Resources/Label') and len(os.listdir('./tmp/X64/EFI/OC/Resources/Label')) > 0:
                                self.__xcopy('./tmp/X64/EFI/OC/Resources/Label', 'EFI/OC/Resources/Label', ignore = shutil.ignore_patterns('.*'))
                            if os.path.exists('./tmp/X64/EFI/OC/Resources/Image') and len(os.listdir('./tmp/X64/EFI/OC/Resources/Image')) > 0:
                                background = ''
                                if os.path.exists('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns'):
                                    with open('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns', mode="rb") as f:
                                        background = f.read()
                                self.__xcopy('./tmp/X64/EFI/OC/Resources/Image', 'EFI/OC/Resources/Image', ignore = shutil.ignore_patterns('.*'))
                                os.remove('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns')
                                if background != '':
                                    with open('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns', mode="wb") as f:
                                        f.write(background)

                        shutil.rmtree('./tmp')
                        break
            break

    def checkKextsVer(self):
        try:
            for pf in os.listdir('EFI/OC/'):
                if os.path.isfile('EFI/OC/{}'.format(pf)) and pf.endswith('.plist'):
                    isChanage = False
                    with open('EFI/OC/{}'.format(pf), 'rb') as f:
                        pldata = plistlib.load(f, fmt=plistlib.FMT_XML)
                    for kext in pldata['Kernel']['Add']:
                        with open('EFI/OC/Kexts/{}/{}'.format(kext['BundlePath'], kext['PlistPath']), 'rb') as fp:
                            kextpldata = plistlib.load(fp, fmt=plistlib.FMT_XML)
                        if kext['Comment'].split('|')[0].strip().replace('V', '') != kextpldata['CFBundleVersion']:
                            isChanage = True
                            kext['Comment'] = 'V' + kextpldata['CFBundleVersion'] if kext['Comment'].split('|')[-1].strip() == '' else 'V' + kextpldata['CFBundleVersion'] + ' | ' + kext['Comment'].split('|')[-1].strip()
                    if isChanage == False:
                        continue
                    with open('EFI/OC/{}'.format(pf), 'wb') as f:
                        plistlib.dump(pldata, f, fmt=plistlib.FMT_XML)
            return 0
        except:
            print('Kexts version check error!')
            return 1


    def update(self, ocver, itver, kever, ischanage = False):
        if kever == 'stable':
            self.alpha = False

        if ischanage == False or (ischanage == True and kever != ''):
            if self.alpha is True:
                for kext in self.kexts:
                    try:
                        self.upgradeDortaniaKexts(kext[0], kext[1], kext[2])
                    except:
                        print('Dortania Kexts update error!')
                        return 1
            else:
                for kext in self.kexts:
                    try:
                        self.upgradeAcidantheraKexts(kext[0], kext[1], kext[2])
                    except:
                        print('Dortania Kexts update error!')
                        return 1

            try:
                self.upgradeRTL8125E()
            except:
                print('RTL8125E Kexts update error!')
                return 2

            try:
                self.upgradeIBT()
            except:
                print('IBT Kexts update error!')
                return 2

        if ischanage == False or (ischanage == True and (itver != [] or kever != '')):
            try:
                self.upgradeItlwm(itver)
            except:
                print('Itlwm Kexts update error!')
                return 2

        if ischanage == False or (ischanage == True and ocver != ''):
            try:
                self.upgradeOC(ocver)
            except:
                print('OC update error!')
                return 3

        return 0



def help():
    print('Usage: python3 update.py [options...]')
    print('options: [-c] [-o <rel | pre | mod>] [-i <ventura | monterey | big_sur>] [-k <stable | alpha>] [-t <token>]')
    print('-c, --chanage                                是否修改, 与 -o, -i, -k 公用, eg: -c -o mod: 修改OC为Mod版')
    print('-o, --ocver <rel | pre | mod>                指定OC的版本')
    print('-i, --itlwm <ventura | monterey | big_sur>   指定intel网卡的版本, 多版本以","分割')
    print('-k, --kexts <stable | alpha>                 指定kext的版本')
    print('-h, --help                                   显示帮助')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hco:i:k:t:",["help", "chanage", "ocver=", "itlwm=", "kexts=", "token="])
    except getopt.GetoptError:
        help()
        sys.exit(9)
    
    isChanage = False
    ocver = ''
    kexts = ''
    itlwm = []
    token = None

    for opt, arg in opts:
        if opt == ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-c", "--chanage"):
            isChanage = True
        elif opt in ("-o", "--ocver"):
            if not arg.lower() in ('rel', 'pre', 'mod'):
                help()
                sys.exit()
            else:
                ocver = arg.lower()
        elif opt in ("-i", "--itlwm"):
            itvers = [x.strip() for x in re.split(',| |\|',arg.lower()) if x.strip()!='']
            if not set(itvers) <= set(['ventura', 'monterey', 'big_sur']):
                help()
                sys.exit()
            else:
                itlwm = itvers
        elif opt in ("-k", "--kexts"):
            if not arg.lower() in ('stable', 'alpha'):
                help()
                sys.exit()
            else:
                kexts = arg.lower()
        elif opt in ("-t", "--token"):
            token = arg

    if isChanage is False:
        if ocver == '':
            ocver = 'mod'
        if itlwm == []:
            itlwm = ['ventura', 'monterey']
        if kexts == '':
            kexts = 'alpha'

    headers = None
    if token is not None:
        headers = { 'user-agent': 'Python-urllib/3.0', 'Authorization': 'token {}'.format(token) }

    u1 = UpdateKexts(headers = headers)
    ret = u1.update(ocver, itlwm, kexts, isChanage)

    if ret == 0:
        u1.checkKextsVer()    # This will change the format of plist file
        with open(date_last_file, mode="w") as f:
            f.write(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    else:
        print('error!')
    
    sys.exit(ret)
