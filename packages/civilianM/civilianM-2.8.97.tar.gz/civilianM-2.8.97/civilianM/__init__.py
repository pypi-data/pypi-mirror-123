#coding:UTF-8
#Author : AC97
#Maintain : AC96,AC97
#Project name : civilianM
#Class : MAIN
#Contact EMail: ehcemc@hotmail.com
#NO COPYING!
import time as te
import platform
import os
import sys
import string
import random as rm
import os.path
import winreg
import socket
import webbrowser
import requests as rs
import json
import getpass
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
v='2.8.97'
n='civilianM'
a='AC97'
m='AC96'
__all__ = ('upgrade','checkClass','wait','randint','decimal','garbledCode','pausePrint','captcha','judge',
    'hideInput','justNow','openFolder','getAddress','find','author','safe','error','myos',
    'LibraryError','ConscienceError','ArgeementWarning','openWeb','UnknownError','whatNews','translate')
#print("欢迎使用civilianM，当前版本："+v)
def whatNews():
    whatNew = ['2021-10-17 civilianM-2.8.97 紧急更新日志',
        '1.readme.md有更改',
        '2.openFolder紧急维护',
        '3.新增translate函数，他可以允许你中英文翻译',
        '4.3.0.97版本将会于11月上旬更新，且3.0.97将会是大更新']
    for n in whatNew:
        if n == whatNew[0]:
            print(n)
        print('\t'+n)

def upgrade():
    """功能：检查更新
    无参数
    """
    
    global v
    dd = []
    r = (
            rs
            .get('https://pypi.org/project/civilianM/#history'))

    l = bs(r.text,'lxml')
    d = l.find_all('p',class_='release__version')
    for nn in d:
        ev = nn.text.strip()
        dd.append(ev)
    new = dd[0].split('.')
    cur = v.split('.')
    #Not same
    if int(new[0]) == int(cur[0]) and int(new[1]) > int(cur[1]):
    	print("你正在使用的是   "+v+",截至目前  "+dd[0]+" 已经发布，请及时更新")
    #same
    elif int(new[0]) == int(cur[0]) and int(new[1]) == int(cur[1]):
    	print("你正在使用最新版本  "+v+"  暂时不需要更新")
    elif int(new[0]) == int(cur[0]) and int(cur[1]) > int(new[1]):
    	#teast
    	print("你正在使用测试版本   "+v+",在PyPi上civilianM的最新版本是 "+dd[0])

def checkClass(objects,need):
    attribute = ['str','list','dict','int','float','tuple']
    if need not in attribute:
        raise AttributeError(
            "无效参数："+need)
    """功能：检查是否为指定类型
    objects:检查对象
    need:指定类型（str/list/dist/int/float/tuple）（必须是字符串）
    """
    
    if need == 'str':
        return type(objects) is type('')
    elif need == 'list':
        return type(objects) is type([])
    elif need == 'dict':
        return type(objects) is type({})
    elif need == 'int':
        return type(objects) is type(1)
    elif need == 'float':
        return type(objects) is type(0.1)
    elif need == 'tuple':
        return type(objects) is type(())
    else:
        raise AttributeError(
            "无效参数"+str(need))

def translate(string):
    #CE:Chinese to English
    pr = {'doctype':'json', 'type':'AUTO', 'i':str(string)}
    r = (
        rs
        .get('http://fanyi.youdao.com/translate',params=pr))
    r2c = r.json()
    re = r2c['translateResult'][0][0]["tgt"]
    return string + ' -----> ' + re

#Sleep
def wait(t):
    """功能：让程序睡眠
    实际上就是time的sleep
    t : 时间，单位：秒"""
    return (
        te
            .sleep(t))

#Randomly generated number
def randint(mins,maxs):
    """功能：随机生成一个整数
    实际上就是random的randint
    mins:最小数
    maxs:最大数
    """
    return (
        rm
            .randint(mins,maxs))

def decimal(mins,maxs,save=None):
    if save == None:
        return (
            rm
            .uniform(mins,maxs))
    elif save != None:
        reutrn = (
            rm
            .uniform(mins,maxs))
        return (
            round(
                reutrn,save)
            )
    else:
        raise UnknownError(
            "未知错误")

def garbledCode(digit=20):
    """功能：常见的一堆乱码
    digit:位数，（digit > 0）
    types:类型，只有None和Upper
    """
    result = ""
    np= ""
    standard = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f']
    for n in range(
        digit):
        np = standard[randint(0,15)]
        result += str(np)
    return result

def pausePrint(*content,pause=0.2):
    """功能：停顿打印
    content:打印的内容
    pause:停顿时间
    """
    for tex in content:
        for prin in str(tex):
            print(prin,end='',flush=True)
            (
                wait
                (pause))
        print(" ",flush=True,end="")
    print("\n",flush=True,end="")
  
def captcha():
    """功能：生成一个CAPTCHA验证码
    不能指定位数，无参数
    """
    capt = ''
    N = [1,2,3,4,5,6,7,8,9,0,'a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M',
         'n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    for n in range(4):
        capt += str(N[randint(0,61)])
    return capt

def judge(content,classes):
    attribute = ['yn','tf','oc']
    if classes not in attribute:
        raise AttributeError(
            "无效参数："+classes)
    """功能：判断
    ontent:内容
    classes:判断类型（yn/tf/oc）
    回答正确返回True
    回答错误返回False
    瞎回答返回None
    """
    if classes == 'yn':
        ace = input(content+'(Y/N):')
        ace = ace.upper()
        if ace == 'Y':
            return True
        elif ace == 'N':
            return False
        else:
            return None
    if classes == 'tf':
        ace = input(content+'(T/F):')
        ace = ace.upper()
        if ace == 'T':
            return True
        elif ace == 'F':
            return False
        else:
            return None
    if classes == 'oc':
        ace = input(content+"(ok/cancel):")
        ace = ace.lower()
        if ace == 'ok':
            return True
        elif ace == 'cancel':
            return False
        else:
            return None
        
def hideInput(con):
    a = getpass.getpass(con)
    return a

def justNow():
    b = dt.today()
    return b.strftime("%Y-%m-%d %H:%M:%S")

def openFolder(fn=None):
    def efve():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0] + "/"
    if fn:
        nh = efve() + fn
        if not os.path.exists(nh):
            os.mkdir(nh)
    else:
        nh = os.getcwd()

    if platform.system() == "Windows":
        os.startfile(nh)

    #return nh + "/"

def getAddress():
    re = (
        rs
              .get('https://ipw.cn/api/ip/locate'))
    d = json.loads(re.text)
    PR = d['Address']['Province']
    ISP = "中国"+d['ISP']
    if PR == '广西' or PR == '内蒙古' or PR == '宁夏' or PR == '新疆':
        if PR == '广西':
            PR += '壮族自治区'
        if PR == '内蒙古':
            PR += '自治区'
        if PR == '宁夏':
            PR += '回族自治区'
        if PR == '新疆':
            PR += '维吾尔自治区'
    else:
        PR += '省'
    C = d['Address']['City'] + '市'
    comp = socket.gethostname()
    comip = socket.gethostbyname(comp)
    nr = {'network':{'IP':d['IP'],'country':d['Address']['Country'],'province':PR,'city':C,'ISP':ISP},
          'computer':{'name':comp,'computerIP':comip}}
    return nr

def openWeb(website,sec=False):
    if sec:
        website = 'https://'+website
    elif sec==False:
        website = 'http://' +website
    webbrowser.open(website)

gr = []
ttt = 0
ia = None
class find():
    def getDisk(self):
        dd = []
        for disk in string.ascii_uppercase:
            disk += ':\\'
            if os.path.exists(disk):
                dd.append(disk)
        return dd
    def sds(self,root,name,dirs):
        global gr
        for _dir in dirs:
            if -1 != _dir.find(name) and _dir[0] != '$':
                ad = os.path.join(root,_dir)
                if ad not in gr:
                    gr.append(ad)
    def sfs(self,root,name,files):
        global gr
        for file in files:
            if name in files:
                if name in file:
                    af = os.path.join(root,file)
                    if af not in gr:
                        gr.append(af)
    def search(self,n):
        fb = find()
        global ia
        global ttt
        cd = fb.getDisk()
        for disk in cd:
            for root,dirs,files in os.walk(disk,True):
                fb.sds(root,n,dirs)
                ttt += 1
                fb.sfs(root,n,dirs)
        ia = n
    @property
    def show(self):
        global gr
        global ia
        global ttt
        if len(gr) >=1:
            gr.append(ttt)
            return gr
        elif len(gr) == 0:
            raise LibraryError(
                "无法找到 '"+ia+"' 这个文件/文件夹，因为它有可能并不存在！")

class myos():
    def __init__(self):
        pass
    def clearScreen(self):
        os.system('cls')
    def shutdown(self):
        """DANGEROUS"""
        os.system("shutdown -p")

class error():
    def __init__(self):
        pass
    def attribute(self,cont=None):
        if cont==None:
            raise AttributeError(' ')
        elif cont != None:
            raise AttributeError(cont)
    def syntax(self,cont=None):
        if cont==None:
            raise SyntaxError(' ')
        elif cont != None:
            raise SyntaxError(cont)
    def value(self,cont=None):
        if cont ==None:
            raise ValueError(' ')
        elif cont != None:
            raise ValueError(cont)
    def exception(self,cont=None):
        if cont==None:
            raise Exception(' ')
        elif cont != None:
            raise Exception(cont)
    def name(self,cont=None):
        if cont==None:
            raise NameError(' ')
        elif cont != None:
            raise NameError(cont)
    def io(self,cont=None):
        if cont==None:
            raise IOError(' ')
        elif cont != None:
            raise IOError(cont)
    def Type(self,cont=None):
        if cont==None:
            raise TypeError(' ')
        elif cont != None:
            raise TypeError(cont)
    def indentation(self,cont=None):
        if cont==None:
            raise IndentationError(' ')
        elif cont != None:
            raise IndentationError(cont)
    def index(self,cont=None):
        if cont==None:
            raise IndexError(' ')
        elif cont != None:
            raise IndexError(cont)
    def Import(self,cont=None):
        if cont == None:
            raise ImportError(' ')
        elif cont!=None:
            raise ImportError(cont)
    def key(self,cont=None):
        if cont == None:
            raise KeyError(' ')
        elif cont!=None:
            raise KeyError(cont)
    def unicode(self,cont=None):
        if cont == None:
            raise UnicodeDecodeError(' ')
        elif cont!=None:
            raise UnicodeDecodeError(cont)
    def zero(self,cont=None):
        if cont == None:
            raise ZeroDivisionError(' ')
        elif cont!=None:
            raise ZeroDivisionError(cont)
    def eof(self,cont=None):
        if cont == None:
            raise EOFError(' ')
        elif cont!=None:
            raise EOFError(cont)
    def windows(self,cont=None):
        if cont == None:
            raise WindowsError(' ')
        elif cont!=None:
            raise WindowsError(cont)
    def runtime(self,cont=None):
        if cont == None:
            raise RuntimeError(' ')
        elif cont!=None:
            raise RuntimeError(cont)
    def timeout(self,cont=None):
        if cont == None:
            raise TimeoutError(' ')
        elif cont!=None:
            raise TimeoutError(cont)
    def lookup(self,cont=None):
        if cont == None:
            raise LookupError(' ')
        elif cont!=None:
            raise LookupError(cont)
    def filenotfound(self,cont=None):
        if cont == None:
            raise FileNotFoundError(' ')
        elif cont!=None:
            raise FileNotFoundError(cont)

Ddbyu8s8dgB = '161368616001626129613651687'
class safe():
    def cMES10(token,status):
        #civilianM Encry Standard 1.0
        d = token.split("6")
        if len(d) >= 11 or len(d) <= 9:
            print(d)
            raise LibraryError(
                "Token error")
        else:
            if status:
                Encr = {
        '1':'?',
        '2':':',
        '3':'@',
        '4':'=',
        '5':';',
        '6':'*',
        '7':'!',
        '8':'.',
        '9':'[',
        '0':'+',
        'a':'#',
        'b':'^',
        'c':'$',
        'd':'_',
        'e':'>',
        'f':',',
        'g':'/',
        'h':'<',
        'i':'{',
        'j':'"',
        'k':"'",
        'l':'-',
        'm':'%',
        'n':'&',
        'o':'|',
        'p':'~',
        'q':'`',
        'r':')',
        's':'(',
        't':']',
        'u':'}',
        'v':'1',
        'w':'3',
        'x':'5',
        'y':'7',
        'z':'9'}
                return Encr
            elif status == False:
                Deco = {
        '?':'1',
        ':':'2',
        '@':'3',
        '=':'4',
        ';':'5',
        '*':'6',
        '!':'7',
        '.':'8',
        '[':'9',
        '+':'0',
        '#':'a',
        '^':'b',
        '$':'c',
        '_':'d',
        '>':'e',
        ',':'f',
        '/':'g',
        '<':'h',
        '{':'i',
        '"':'j',
        "'":'k',
        '-':'l',
        '%':'m',
        '&':'n',
        '|':'o',
        '~':'p',
        '`':'q',
        ')':'r',
        '(':'s',
        ']':'t',
        '}':'u',
        '1':'v',
        '3':'w',
        '5':'x',
        '7':'y',
        '9':'z'}
                return Deco
            else:
                raise UnknownError("UnknownError")
    def encry(self,string):
        d = ""
        standard = (
            safe
            .cMES10(Ddbyu8s8dgB,True))
        for n in str(string):
            try:
                n = standard[n]
            except KeyError:
                n = n.lower()
                try:
                    n = standard[n]
                except KeyError:
                    pass
            d += n
        return d
    def decode(self,string):
        standard = (
            safe
            .cMES10(Ddbyu8s8dgB,False))
        d = ""
        for n in str(string):
            try:
                n = standard[n]
            except KeyError:
                n = n.lower()
                try:
                    n = standard[n]
                except KeyError:
                    pass
            d += n
        return d

class author():
    def __init__(self):
        pass
    @property
    def name(self):
        print('AC97')
    @property
    def email(self):
        print("ehcemc@hotmail.com")
    @property
    def old(self):
        print('12.1 -- 30.6 Years old')
    @property
    def gender(self):
        print('male')
    @property
    def phoneNumber(self):
        print('+8613417083101')
    @property
    def From(self):
        print("CN")
    @property
    def live(self):
        print("中国,广西壮族自治区")
    @property
    def manage(self):
        print("AC97，AC96")

class ArgeementWarning(Exception):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error

class ConscienceError(Exception):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error

class LibraryError(Exception):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error
class UnknownError(WindowsError):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error
