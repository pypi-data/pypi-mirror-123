
from civilianM import *
#from __init__ import *
import os
try:
    from OpenSSL import crypto,SSL
except ModuleNotFoundError:
    s = error()
    s.Import("Please install 'PyOpenSSL' module")
import os.path
#coding:UTF-8
#Author : AC97
#Maintain : AC96
#Project name : civilianM
#Class : AUX / DO A CERT
#Contact EMail: ehcemc@HOTMAIL.COM
#NO COPYING!
class do():
    def __init__(self):
        a = input("*输入国家名(example:CN/EN):")
        if len(a) != 2:
            raise NameError(
                """Must enter country name abbreviation,example:EN,and must upper""")
        b = input("*请输入你所居住的省份/州/自治区:")
        c = input("*请输入你所居住的城市:")
        d = input("*请输入你的组织名称:")
        e = input("*请输入颁发者名称:")
        f = input("请输入保存的文件名（留空则空）:")
        cn = judge("请知晓：如制作的安全证书信息为假，与我（AC97/AC96）没有任何关系。",'yn')
        if cn:
            vd = captcha()
            cs = hideInput('('+vd+')请输入验证码:')
            if cs!=vd:
                raise Exception(
                    """验证码有误，制作失败""")
            else:
                print("验证成功，请等待一些时间")
                wait(3)
                savefilename = f+ ".crt"
                passwordfile = f + ".key"
                k = crypto.PKey()
                k.generate_key(crypto.TYPE_RSA, 2048)
                cert = crypto.X509()
                cert.get_subject().C = a
                cert.get_subject().ST = b
                cert.get_subject().L = c
                cert.get_subject().O = d
                cert.get_subject().OU = "IT and Security Department"
                cert.get_subject().CN = e
                cert.gmtime_adj_notBefore(0)
                cert.set_serial_number(1000)
                cert.gmtime_adj_notAfter(68*365*24*60*60)
                cert.set_issuer(cert.get_subject())
                cert.set_pubkey(k)
                cert.sign(k, 'SHA256')
                if os.path.exists('D:\cert')==False:
                    os.chdir('D:\\')
                    os.mkdir('cert')
                    os.chdir('D:\\cert')
                elif os.path.exists('D:\cert'):
                    os.chdir('D:\\cert')
                print('安全证书将保存至 '+os.getcwd())
                open(savefilename,'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                open(passwordfile,'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
                try:
                    openFolder(os.getcwd())
                except:
                    wait(3)
                    print('完成')
                    os.remove(passwordfile)
        elif cn==False or cn==None:
            raise ArgeementWarning(
                '''你没有同意知晓协议，无法制作。''')
do()
