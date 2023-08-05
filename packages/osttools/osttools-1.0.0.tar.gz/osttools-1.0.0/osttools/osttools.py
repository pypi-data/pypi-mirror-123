# -*- coding:utf-8 -*-
import os
import re
import time as _time
import random
import subprocess
from prettytable import PrettyTable
from PySide2 import QtXml
from PySide2.QtGui import QColor,  QIcon,  QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow


NAME = '''osttools'''
VERSION = '''1.0.0'''
AUTHOR = '''ordinary'''
GITHUB = '''https://github.com/ordinary-student/osttools'''


class IllegalIPexception(Exception):
    '''IP地址非法异常'''

    def __init__(self):
        super()

    def __str__(self):
        print("IP地址不合法！")


class Wifi(object):
    '''WiFi类'''

    def __init__(self, ssid, idcheck, pwd, bssid, network, networktype, channel):
        '''构造函数'''
        self.ssid = ssid
        self.idcheck = idcheck
        self.pwd = pwd
        self.bssid = bssid
        self.network = network
        self.networktype = networktype
        self.channel = channel

    def toString(self) -> dict:
        '''返回一个WiFi信息字典'''
        w = {}
        w['名称'] = self.ssid
        w['身份验证'] = self.idcheck
        w['加密'] = self.pwd
        w['bssid'] = self.bssid
        w['信号'] = self.network
        w['无线电类型'] = self.networktype
        w['信道'] = self.channel
        return w

    def toList(self) -> list:
        '''返回一个WiFi信息列表'''
        return [self.ssid, self.idcheck, self.pwd, self.bssid, self.network, self.networktype, self.channel]


def center(window: QMainWindow, app: QApplication):
    '''窗口居中显示'''
    # 获取屏幕大小
    screen = app.primaryScreen().geometry()
    # 获取窗体大小
    size = window.geometry()
    # 窗体居中
    window.move((screen.width() - size.width()) / 2,
                (screen.height() - size.height()) / 2)


def generateIcon() -> QIcon:
    '''生成随机纯色图标'''
    pixmap = QPixmap(256, 256)
    # 图片颜色
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    pixmap.fill(QColor(r, g, b))
    return QIcon(pixmap)


def popen(cmd: str) -> tuple[str, str]:
    '''执行系统命令'''
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        # 执行命令
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, startupinfo=startupinfo,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result = process.stdout.read()
        process.stdout.close()
        error = process.stderr.read()
        process.stderr.close()

    except:
        return 'error', 'error'
    # 返回运行结果
    return result, error


def get_wifi_list() -> list[Wifi]:
    '''扫描获取附近WiFi列表'''
    # 获取WiFi列表
    result, error = popen('netsh wlan show networks mode=bssid')
    # 判断
    if result == 'error':
        return []

    # 根据回车分割
    alist = result.split('\n')
    # 去头去尾
    clist = alist[4:-1]
    # 分隔
    step = 11
    dlist = [clist[i:i+step] for i in range(0, len(clist), step)]

    wifi_list = []
    try:
        # 遍历
        for item in dlist:
            # 分割获取信息
            ssid = item[0].split(':')[1][1:].encode('gbk').decode("utf-8")
            idcheck = item[2].split(':')[1][1:]
            pwd = item[3].split(':')[1][1:]
            bssid = item[4][(item[4].index(':')+1):]
            network = item[5].split(':')[1][1:]
            networktype = item[6].split(':')[1][1:]
            channel = item[7].split(':')[1][1:]
            # 创建WiFi对象
            wifi = Wifi(ssid, idcheck, pwd, bssid,
                        network, networktype, channel)
            wifi_list.append(wifi)
    except:
        # 返回
        return wifi_list
    # 返回
    return wifi_list


def wifi_scan() -> str:
    '''扫描附近的WiFi'''
    print('wifi扫描中...')
    # 获取WiFi列表
    wifi_list = get_wifi_list()
    # 判断
    if len(wifi_list) == 0:
        return ''
    # 组合美化
    x = PrettyTable(["名称", "身份验证", "加密", "物理地址", "信号", "无线电类型", "信道"])
    # 遍历添加
    for i in wifi_list:
        x.add_row(i.toList())
    print(x)
    return str(x)


def get_wifi_pwd_by_name(wifiname: str) -> str:
    '''根据WIFI名字获取密码'''
    pwd = '无'
    # TODO...WIFI名称有空格会获取不了密码
    # 命令行
    order = "netsh wlan show profile name={} key=clear".format(wifiname)
    # 执行命令
    result, error = popen(order)
    # 判断
    if result == 'error':
        return ''
    # 根据回车分割
    alist = result.split('\n')
    # 遍历
    for a in alist:
        if '关键内容' in a:
            index = a.index(':')
            pwd = a[index+2:]
    # 返回密码
    return pwd


def get_wifi_pwd_map() -> list:
    '''查看连接过的WiFi密码'''
    # 获取连接过的WiFi列表
    result, error = popen('netsh wlan show profiles')
    # 判断
    if result == 'error':
        return []

    # 根据回车分割
    alist = result.split('\n')
    # 筛选-获取所有WiFi名字
    wifiname_list = []
    for b in alist:
        if '所有用户配置文件' in b:
            wifiname_list.append(b[15:])
    # 判断
    if len(wifiname_list) == 0:
        return []

    # WiFi密码键值对
    wifimap = []
    # 遍历所有WIFI
    for wifiname in wifiname_list:
        # 获取密码
        pwd = get_wifi_pwd_by_name(wifiname)
        # 判断
        if len(pwd) == 0:
            return
        # 加入列表
        wifimap.append((wifiname, pwd))

    # 返回
    return wifimap


def wifi_history() -> str:
    '''查看连接过的WiFi密码（美化版）'''
    wifimap = get_wifi_pwd_map()
    # 判断
    if len(wifimap) == 0:
        return ''
    # 组合美化
    x = PrettyTable(["WiFi名称", "WiFi密码"])
    # 遍历添加
    for name, password in wifimap:
        x.add_row([name, password])
    print(x)
    # 返回
    return str(x)


def has_network() -> bool:
    '''检测有无网络连接'''
    result, error = popen('ping baidu.com')
    if 'TTL' in result:
        return True
    else:
        return False


def is_ip_legal(ip: str) -> bool:
    '''检测IP是否合法'''
    # IP地址正则
    pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
    return re.match(pattern, ip)


def nowtime() -> str:
    '''当前时间'''
    return str(_time.strftime(
        '%Y-%m-%d %H:%M:%S', _time.localtime(_time.time())))


def ping(host: str, count: int = 4, timeout: int = 500) -> bool:
    '''ping命令'''
    # 命令
    cmd = f"ping {host} -n {count} -w {timeout}"
    # 执行命令
    result, error = popen(cmd)
    # 判断结果
    if result == 'error':
        # 出错
        return False
    else:
        # 在线
        if 'TTL' in result.upper():
            return True
        else:
            return False


def pingIP(ip: str, count: int = 4, timeout: int = 500) -> bool:
    '''ping IP地址'''
    # 检测IP地址是否合法
    if is_ip_legal(ip):
        # 命令
        cmd = f"ping {ip} -n {count} -w {timeout}"
        # 执行命令
        result, error = popen(cmd)
        # 判断结果
        if result == 'error':
            # 出错
            return False
        else:
            # 在线
            if 'TTL' in result.upper():
                return True
            else:
                return False
    else:
        raise IllegalIPexception()


def system_active():
    '''查看系统激活信息'''
    popen('slmgr.vbs -xpr')


def system_licence():
    '''查看系统许可证状态'''
    popen('slmgr.vbs -dlv')


def system_licence2():
    '''查看系统许可证状态（简化版）'''
    popen('slmgr.vbs -dli')


def traverse_dir(rootdir: str) -> list:
    '''遍历获取目录所有文件路径'''
    # 结果集
    result_list = []
    # 列出文件夹下所有的目录与文件
    file_list = os.listdir(rootdir)
    # 遍历
    for name in file_list:
        # 获取绝对路径
        fullname = os.path.join(rootdir, name)
        # 判断是否为目录
        if os.path.isdir(fullname):
            result_list.append(fullname)
            # 递归遍历
            result_list.extend(traverse_dir(fullname))
        else:
            result_list.append(fullname)
    # 返回
    return result_list
