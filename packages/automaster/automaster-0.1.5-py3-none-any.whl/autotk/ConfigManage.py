# 自动配置文件Config.ini 字段自动为大写,键key自动小写,值value不变
# 模块使用记录 - 最新日期
# AutoHDMI      20210430
# RouterControl 20210125
# AutoBurnKey 20210513
import configparser
import os

class config_auto(configparser.ConfigParser):
    def read(self, filenames=None):
        if(filenames):
            self.inifile=filenames
        else:
            self.inifile = "./config.ini"
        if (not os.path.isfile(self.inifile)):
            self.initleds(self.inifile)  # AutoBurnKey 20210903
            # self.initdetect(filenames)  # AutoBurnKey 20210813
            # self.initburn(filenames)  # AutoBurnKey 20210517
            # self.inithdmi(filenames)  # AutoHDMI 20210125
            # self.initrouter(filenames)  # RouterControl 20210125
        try:
            return super().read(self.inifile)
        except Exception as e:
            return super().read(self.inifile,"utf-8-sig") # utf-8编码的文件时开头会有一个多余的字符\ufeff

    def inithdmi(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN', 'hdmi_source': "4", 'hdmi_delay': "1", 'hdmi_lock': '1',
                                'auto_upgrade': "0",
                                "Plan": "SCANNER,AGING_TEST,BASIC_TEST,RESOLUTION,HDMI_VOLT,HDMI_VIDEO,SPDIF_AUDIO,SD_TEST,IR_TEST,HDMI_AUDIO,BT_TEST,DVB,DVB_VOLT,LED_TEST,ETH_TEST,BURN_KEY,READ_KEY,MES".upper(),
                                "showinfo": "2", "ver": "0", "debug": "", "audio_volume": "80", "spdif_volume": "80",
                                "deploy_total": "6"}
        init_dict['BASIC_TEST'] = {'cpu_type_match': '', 'cpu_temp_min': '25', 'cpu_temp_max': '85',
                                   'ddr_size_limit': '2000000000', 'emmc_size_limit': '10000000000', 'hw_id_match': '',
                                   'ver_match': 'v9.5.'}
        init_dict['AGING_TEST'] = {'set_time': '', "limit": "86400"}
        init_dict['ETH_TEST'] = {'match': '192.168.', "timeout": "40"}
        init_dict['RESET'] = {"timeout": "30"}
        init_dict['BT_TEST'] = {"name": 'HUAWEI CM510', "retry": "3", 'connect': '0', 'timeout': '10',
                                "rssi_min": "-80", "rssi_max": "0"}
        init_dict['WIFI_COUPLE'] = {"fw_file": 'fw_bcm4359c0_ag_mfg.bin', 'nvram': 'nvram_ap6398sa3.txt', 'txchain': '1,2', "min": "-12,-5", 'max': '0,0',"dute":"0.2","num":"10","limit":"0.8"}
        init_dict['WIFI_24'] = {"ssid": 'Wifitest24', 'key': '123456789', 'type': '1', "retry": "3", 'connect': '0',
                                'timeout': '5',
                                "rssi_min": "-80", "rssi_max": "80"}
        init_dict['WIFI_5'] = {"ssid": 'Wifitest5', 'key': '123456789', 'type': '1', "retry": "3", 'connect': '0',
                               'timeout': '5',
                               "rssi_min": "-80", "rssi_max": "80"}
        init_dict['LED_TEST'] = {'auto': '1', 'timeout': '20', 'dute_time': "1", 'values': '0,1,2', "colors": "off,white,blue","exposure":"-8,-8,-7",
                                 "save": "1"}
        init_dict['BUTTON_TEST'] = {'auto': '0', 'timeout': '15',"dute":"0.5", 'keycodes': '5125','ports':'COM1,COM2'}
        init_dict['IR_TEST'] = {'retry': '3', 'match': '8', "timeout": "3"}
        init_dict['SD_TEST'] = {'limit': '1'}
        init_dict['USB_TEST'] = {'limit': '0'}
        init_dict['Resolution'] = {'limit': '13'}
        init_dict["DVB"] = {"playlist": "0", "sampletag": "1", "cap_delay": "6", "timeout": "0", "len": "2",
                            "limit": "0.9","hit_limit": "15", "quality":"100","save": "1"}
        init_dict['DVB_VOLT'] = {'enable_22k': "0", 'cmd_list': "11,00", "dute_delay": "0.5", "volt_retry": "20",
                                 "volt_min_list": "4.5,0", "volt_max_list": "5.2,0.2"}
        init_dict['HDMI_VOLT'] = {'volt_min': "4.5", 'volt_max': "5.2", "cec_retry": "3"}
        init_dict['HDMI_Video'] = {'mode': '1', 'limit': '0.8',"hit_limit": "10",'len': "1","quality":"1700","set2k": "1","save": "1"}
        init_dict['HDMI_Audio'] = {'vmax_limit': '', 'loudness_limit': '-7', 'len': '1', 'psd_enable': '0',
                                   "P_limit1": '0.01', "judge1": "1000", "P_limit2": '0.01',
                                   "judge2": "1000", "offset": "3", "save": "0"}
        init_dict['SPDIF_AUDIO'] = {'vmax_limit': '', 'loudness_limit': '-9', 'len': '1', 'psd_enable': '0',
                                   "P_limit1": '0.01', "judge1": "1000", "P_limit2": '0.01',
                                   "judge2": "1000", "offset": "3", "save": "0"}
        init_dict['READ_KEY'] = {'timeout': '10'}
        init_dict['BURN_KEY'] = {'mode': '0', 'sn_match': '', 'emac_match': '', 'wmac_match': '', 'timeout': '30'}
        init_dict['SCANNER'] = {'mode': '4', 'len': '16', "retry": "3", "match": "", "sn_match": "", "boxid_match": "",
                                "emac_match": "", "wmac_match": "", "port": "COM12"}
        init_dict['PRINTER'] = {'mode': '0', 'len': '8', "port": "0", "timeout": "-1"}
        init_dict['mes'] = {'id': '0',
                            'keyword': 'SN,EMAC',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'AutoHDMI',
                            'scanner': 'pc'
                            }
        init_dict['FTP'] = {'host': '127.0.0.1', 'port': "21", 'user': 'admin', "key": 'admin', "timeout": "5",
                            "sub_dir": ""}
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)

    def initrouter(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN',
                                "Plan": "SCANNER,BURN_SN,SIM_TEST,LED_TEST,BUTTON_TEST,BURN_MAC,BURN_TEST,MES,PRINTER".upper(),
                                "showinfo": "0", "ver": "0", "debug": ""}
        init_dict['SCANNER'] = {'mode': '0', 'len': '8', "port": "COM12", "timeout": "-1"}
        init_dict['PRINTER'] = {'mode': '0', 'len': '8', "port": "COM11", "timeout": "-1"}
        init_dict['SIM_TEST'] = {"retry": "3", "rssi_min": "-80", "rssi_max": "80", "service_min": "-80",
                                 "service_max": "80", }
        init_dict['LED_TEST'] = {'mode': '0', "timeout": "25"}
        init_dict['BUTTON_TEST'] = {"timeout": "15"}
        init_dict['BURN_SN'] = {"retry": "3"}
        init_dict['BURN_MAC'] = {"retry": "3"}
        init_dict['BURN_TEST'] = {"retry": "3"}
        # (ip="172.30.55.1", port=22, username="root", password="admin") STC560
        init_dict['SSH'] = {'ip': '192.168.1.1', 'port': "22", 'user': 'root', "pwd": 'admin', "timeout": "5"}
        init_dict['mes'] = {'id': '0',
                            'keyword': 'MAC,IMEI',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'RouterControl',
                            'scanner': 'pc',
                            }
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)

    def initdetect(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN',
                                "Plan": "SCANNER,VISION_DETECT,MES".upper(),
                                "showinfo": "2", "ver": "0", "debug": "","db": ""}
        init_dict['SCANNER'] = {'mode': '11', 'len': '16', "retry": "3", "match": "","getkeys":"","sn_match": "", "boxid_match": "",
                                "emac_match": "", "wmac_match": "", "port": "COM41"}
        init_dict['Vision_Detect'] = {'id': '0','tagfile': 'launcher.pkl',"limit":"3","timeout":"120"}
        init_dict['mes'] = {'id': '0',
                            'keyword': '',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'BurnKey',
                            'scanner': 'pc',
                            }
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)
    def initleds(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN',
                                "Plan": "SCANNER,LEDS_DETECT,MES".upper(),
                                "showinfo": "2", "ver": "0", "debug": "","db": ""}
        init_dict['SCANNER'] = {'mode': '0', 'len': '16', "retry": "3", "match": "","getkeys":"","sn_match": "", "boxid_match": "",
                                "emac_match": "", "wmac_match": "", "port": "COM1"}
        init_dict['LEDS_DETECT'] = {'id': '0,0,0','tagfile': 'htag.jpg',"len_limit":"500","hist_limit":"0.2","delay":"2","timeout":"20"}
        init_dict['mes'] = {'id': '0',
                            'keyword': '',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'LedDetect',
                            'scanner': 'pc',
                            }
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)
    def initburn(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN',
                                "Plan": "SCANNER,BURN_KEY,MES,ADB_CLOSE".upper(),
                                "showinfo": "2", "ver": "0", "debug": "","db": ""}
        init_dict['SCANNER'] = {'mode': '1', 'len': '16', "retry": "3", "match": "","getkeys":"","sn_match": "", "boxid_match": "",
                                "emac_match": "", "wmac_match": "", "port": "COM41"}
        init_dict['CHECK_KEYS'] = {'retry': '3'}
        init_dict['BURN_KEY'] = {'mode': '4', 'sn_match': '', 'emac_match': '', 'wmac_match': '', 'timeout': '0'}
        init_dict['ADB_CLOSE'] = {'mode': '0',"dhcp":"0"}
        for i in range(4):
            init_dict['ADB_CLOSE']['cmd%d'%i]=''
            init_dict['ADB_CLOSE']['delay%d'%i]=''
            init_dict['ADB_CLOSE']['match%d'%i]=''
        init_dict['mes'] = {'id': '0',
                            'keyword': '',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'BurnKey',
                            'scanner': 'pc',
                            }
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)

    def initcouple(self, filenames):
        init_dict = {}
        init_dict['Setting'] = {'language': 'CN',
                                "Plan": "SCANNER,ROUTER_TELNET,ROUTER_COUPLE,MES,ADB_CLOSE".upper(),
                                "showinfo": "2", "ver": "0", "debug": "","db": ""}
        init_dict['ROUTER_TELNET']={"wait":"20","ip": "192.168.1.1", "user": "admin", "password": "1234","static":"148"}
        init_dict['SCANNER'] = {'mode': '7', 'len': '8', "retry": "3", "match": "","getkeys":"", "sn_match": "", "boxid_match": "",
                                "emac_match": "", "wmac_match": "", "port": "COM41"}
        init_dict['ROUTER_COUPLE'] = { "freq": "2412,2412,5180,5180","min": "-25,-25,-25,-25", "max": "20,20,20,20", "dute": "0.2",
                                       "num": "10", "limit": "0.8",}
        for i in range(8):
            init_dict['ROUTER_COUPLE']['bind%d'%(i+1)]=''
            init_dict['ROUTER_COUPLE']['bind%d_offset'%(i+1)]='0,0,0,0'
        init_dict['ADB_CLOSE'] = {'mode': '1',"dhcp":"1"}
        for i in range(4):
            init_dict['ADB_CLOSE']['cmd%d'%i]=''
            init_dict['ADB_CLOSE']['delay%d'%i]=''
            init_dict['ADB_CLOSE']['match%d'%i]=''
        init_dict['mes'] = {'id': '0',
                            'keyword': '',
                            'wsdl': 'http://192.168.13.2/SFCWebService/SFCWebService.asmx?wsdl',
                            'station': 'RouterCouple',
                            'scanner': 'pc',
                            }
        for s in init_dict:
            self.add_section(s.upper())
            for k, v in init_dict[s].items():
                self.set(s.upper(), k.lower(), v)
        self.save(filenames)

    def bind_portlist(self, ports):
        try:
            self.set("HDMI_VOLT", "portlist", ports)
            self.set("DVB_VOLT", "portlist", ports)
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

    def bind_station(self, n, id, audio):
        try:
            self.set("STATION", id, "StaName%d" % n)
            self.set("STATION_AUDIO", id, audio)
            self.set("STATION_SPDIF", id, "S%d" % n)
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

    def get_dict(self, sub=None):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        if (sub): return d[sub]
        return d

    def save(self, filenames=""):
        if(not filenames):
            filenames=self.inifile
        with open(filenames, 'w') as f:
            self.write(f)

def initconfig(filenames="./config.ini"):
    try:
        os.remove(filenames)
    except:
        pass
    conf = config_auto()
    conf.read()
    print(conf.get_dict())
