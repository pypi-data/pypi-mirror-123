#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : MAIN
#Contact EMail: ehcemc@hotmail.com
#NO COPYING!
import time
import platform
import os
import sys
import string
import random
import os.path
import winreg
import socket
import requests
import json
import getpass
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
v='2.4.97'
__all__ = ('upgrade','checkClass','wait','randint','decimal','garbledCode','pausePrint','captcha','judge',
    'hideInput','justNow','openFolder','getAddress','find','author','safe','error','myos','NumberError',
    'LibraryError','ConscienceError','NetworkError','ArgeementWarning')
#print("欢迎使用civilianM，当前版本："+v)

def upgrade():
    """功能：检查更新
    无参数
    """
    
    global v
    dd = []
    try:
        r = requests.get('https://pypi.org/project/civilianM/#history')
    except:
        raise NetworkError(
            '请检查网络连接状态')
    s = bs(r.text,'lxml')
    d = s.find_all('p',class_='release__version')
    for nn in d:
        ev = nn.text.strip()
        dd.append(ev)
    new = dd[0].split('.')
    cur = v.split('.')
    #Not same
    if int(new[0]) == int(cur[0]) and int(new[1]) > int(cur[1]):
    	print("你正在使用的是  "+v+",截至目前  "+dd[0]+"已经发布，请及时更新")
    #same
    elif int(new[0]) == int(cur[0]) and int(new[1]) == int(cur[1]):
    	print("你正在使用最新版本  "+v+" 暂时不需要更新")
    elif int(new[0]) == int(cur[0]) and int(cur[1]) > int(new[1]):
    	#teast
    	print("你正在使用测试版本 "+v+",在PyPi上civilianM的最新版本是 "+dd[0])

def checkClass(objects,need):
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

#Sleep
def wait(t):
    """功能：让程序睡眠
    实际上就是time的sleep
    t : 时间，单位：秒
    """
    
    if checkClass(t,'float') or checkClass(t,'int'):
        time.sleep(t)
    else:
        raise NumberError(
            """必须输入一个小数/整数""")

#Randomly generated number
def randint(mins,maxs):
    """功能：随机生成一个整数
    实际上就是random的randint
    mins:最小数
    maxs:最大数
    """
    
    if checkClass(mins,'int') == False or checkClass(maxs,'int') == False:
        raise NumberError(
            """必须输入整数""")
    if maxs == mins:
        raise NumberError(
            """最大数不得等于最小数""")
    elif mins > maxs:
        raise NumberError(
            """最小数不得大于最大数""")
    return random.randint(mins,maxs)

def decimal(mins,maxs,save=None):
    if checkClass(mins,'float') == False or checkClass(maxs,'float') == False:
        raise NumberError(
            """ 必须输入浮点数""")
        raise NumberError(
            """最大数不得等于最小数""")
    elif mins > maxs:
        raise NumberError(
            """最小数不得大于最大数""")
    if save == None:
        return random.uniform(mins,maxs)
    elif save != None:
        if checkClass(save,'int'):
            return round(random.uniform(mins,maxs),save)
        else:
            raise NumberError(
                "指定save参数时，该参数传入的值必须是整数")

def garbledCode(digit=20,types=None):
    """功能：常见的一堆乱码
    digit:位数，（digit > 0）
    types:类型，只有None和Upper
    """
    result = ""
    if types == None or types == 'Upper':
        pass
    else:
        raise AttributeError(
            '无效参数：'+str(types))
    np= ""
    standard = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f']
    if checkClass(digit,'int')==False:
        raise NumberError(
            """必须输入整数""")
    for n in range(digit):
        np = standard[randint(0,15)]
        if types == 'Upper':
            if checkClass(np,'str'):
                result += np.upper()
            else:
                result += str(np)
        else:
            result += str(np)
    return result

def pausePrint(*content,pause=0.2):
    """功能：停顿打印
    content:打印的内容
    pause:停顿时间
    """
    if checkClass(pause,'float') or checkClass(pause,'int'):
        for tex in content:
            for prin in tex:
                print(prin,end='',flush=True)
                wait(pause)
            print(" ",flush=True,end="")
        print("\n",flush=True,end="")
    else:
        raise NumberError(
            """必须输入小数/浮点数""")
    
def captcha():
    """功能：生成一个CAPTCHA验证码
    不能指定位数，无参数
    """
    capt = ''
    N = [1,2,3,4,5,6,7,8,9,0,'a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M',
         'n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    for n in range(4):
        capt += str(N[randint(0,57)])
    return capt

def judge(content,classes):
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

def openFolder(fn):
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
    try:
        re = requests.get('https://ipw.cn/api/ip/locate')
    except:
        raise NetworkError(
            "请检查网络连接状态")
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

gr = []
ttt = 0
ia = None
class find():
    def warning(self):
        return "1.查找文件时间和电脑性能有关（猜测）-2.使用show()的时候需要使用print"
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
                ttt += 0.1
                fb.sfs(root,n,dirs)
        ia = n
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
            raise AttributeError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise AttributeError(cont)
    def syntax(self,cont=None):
        if cont==None:
            raise SyntaxError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise SyntaxError(cont)
    def value(self,cont=None):
        if cont ==None:
            raise ValueError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise ValueError(cont)
    def exception(self,cont=None):
        if cont==None:
            raise Exception('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise Exception(cont)
    def name(self,cont=None):
        if cont==None:
            raise NameError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise NameError(cont)
    def io(self,cont=None):
        if cont==None:
            raise IOError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IOError(cont)
    def Type(self,cont=None):
        if cont==None:
            raise TypeError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise TypeError(cont)
    def indentation(self,cont=None):
        if cont==None:
            raise IndentationError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IndentationError(cont)
    def index(self,cont=None):
        if cont==None:
            raise IndexError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IndexError(cont)
    def Import(self,cont=None):
        if cont == None:
            raise ImportError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise ImportError(cont)
    def key(self,cont=None):
        if cont == None:
            raise KeyError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise KeyError(cont)
    def unicode(self,cont=None):
        if cont == None:
            raise UnicodeDecodeError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise UnicodeDecodeError(cont)
    def zero(self,cont=None):
        if cont == None:
            raise ZeroDivisionError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise ZeroDivisionError(cont)
    def eof(self,cont=None):
        if cont == None:
            raise EOFError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise EOFError(cont)
    #'The passed in function cannot be left blank and equal to None'

class safe():
    def encry(self,string):
        standard = {
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
        'g':'/'
        }
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
        print(d)
    def decode(self,string):
        standard = {
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
        '/':'g'
        }
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
        print(d)
class author():
    def __init__(self):
        pass
    def name(self):
        print('AC97')
    def email(self):
        print("ehcemc@163.com")
    def old(self):
        raise LibraryError(
            "读取器无法从cmLib-OO读取这个部分：'MyOld'")
    def gender(self):
        print('male')
    def phoneNumber(self):
        print('+8613417083101')
    def From(self):
        print("CN")
    def live(self):
        print("中国,广西壮族自治区")

class NumberError(Exception):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error

class NetworkError(Exception):
    def __init__(self,error):
        self.error=error
    def __str__(self,*args):
        return self.error

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


