#author：莫浩浩
#tip：未经允许擅自抄袭或复制内容者，一律举报处理！
#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : aux / inimate logins
#Contact EMail: ehcemc@hotmail.com
#NO COPYING!
import tkinter as tk
import tkinter.messagebox as tmb
import webbrowser as web
import pickle as pk
window = tk.Tk()
window.title("登录系统")
window.geometry('350x350')
#-------------------函数区域-----------------
def CabCreate():#查看
	tmb.showinfo('登录系统','创作者：莫浩浩\n创作灵感：未知\n依靠：Python3.9.5\n编辑：Adobe Dreamweaver CC 2017；Sublime Text 3\n最终 莫浩浩 版权所有！')
def CabImport():#找死
	tmb.showerror('登录系统','CantGetError:\n在读取信息时发生错误:无法读取future.whl文件')
def CabContent():#加QQ
	if tmb.askyesno('登录系统', '该向导将加入AC97的QQ，是否允许？'):
		web.open('tencent://message/?uin=3390996860&Site=&Menu=yes')
	else:
		tmb.showwarning("登录系统",'用户取消了本次添加')
def CabPeach():#吃屁
	tmb.showerror('登录系统','你在想屁吃\n想要便捷账号，没门！')
def CabVersion1411617():#V14
	tmb.showinfo('登录系统','更新日志：\n版本号:V14.11617\n发布时间：2021.06.12-14:44\n内容：创建程序（只能登录）')
def CabVersion1522522():#V15
	tmb.showinfo('登录系统','更新日志：\n版本号:V15.22522\n发布时间：2021.06.15-19:34\n内容：1.增加注册程序\n  2.可以把所有数据存储到future.whl文件上')
def CabVersion1630517():#V16
	tmb.showinfo('登录系统','更新日志：\n版本号:V16.30517\n发布时间：2021.06.18-23:48\n内容：1.增加评分程序\n    2.加强判断系统')
def CabVersion1811107():#V18
	tmb.showinfo('登录系统','更新日志：\n版本号:V18.11107\n发布时间：2021.06.20-\n内容：1.开放‘忘记密码’功能\n    2.优化BUG\n    3.修改主页面')
def login():#登录
	ung = un.get()
	pwg = pw.get()
	try:
		with open('future.whl','rb') as uf:
			ufi = pk.load(uf)
	except FileNotFoundError:
		with open('future.whl','wb') as uf:
			ufi = {'user':'8888'}
			pk.dump(ufi,uf)
	if ung in ufi:
		if pwg == ufi[ung]:
			tmb.showinfo(title='登录系统', message='欢迎你！'+ung)
			home()
		else:
			tmb.showerror('登录系统','密码错误,请重试')
	elif ung == '' or pwg == '':
		tmb.showerror('登录系统','用户名和用户密码是必填项！')
	else:
		if tmb.askyesno('登录系统','您好！该用户名未注册，请问是否立即注册？'):
			signup()
		else:
			tmb.showwarning('登录系统','用户取消了本次操作')
def signup():#注册
    def SignupOver():
    	ug = nu.get()
    	pg = np.get()
    	rpg = renp.get()
    	try:
    		with open('future.whl','rb') as uf:
    			ui = pk.load(uf)
    	except FileNotFoundError:
    		ui = {}
    	if ug in ui:
    		tmb.showerror('登录系统','用户名已经存在！请尝试更换一个！')
    	elif ug == '' or pg == '':
    		tmb.showerror('登录系统','用户名和用户密码是必填项！')
    	elif rpg != pg:
    		tmb.showerror('登录系统','两次密码不一致！')
    	else:
    		ui[ug] = pg
    		with open('future.whl','wb') as uf:
    			pk.dump(ui,uf)
    		tmb.showinfo('登录系统','恭喜你，注册成功！赶紧去登录吧！')
    		window_su.destroy()
    window_su = tk.Toplevel(window)
    window_su.geometry('350x200')
    window_su.title('注册界面')
    nu = tk.StringVar()
    tk.Label(window_su,text='用户名：').place(x=10,y=10)
    enu = tk.Entry(window_su,textvariable=nu).place(x=150,y=10)
    np=tk.StringVar()
    tk.Label(window_su,text='请输入密码：').place(x=10,y=50)
    enp = tk.Entry(window_su,textvariable=np,show='•').place(x=150,y=50)    
    renp = tk.StringVar()
    tk.Label(window_su,text='请再次输入密码：').place(x=10,y=90)
    erenp = tk.Entry(window_su,textvariable=renp,show='•').place(x=150,y=90)    
    signupo=tk.Button(window_su,text='确认注册',command=SignupOver)
    signupo.place(x=150,y=130)
def forgetPW():#忘记密码
	def forgetPWCheck():#忘记密码-检查
		u = un_fp.get()
		p = np_fp.get()
		try:
			with open('future.whl','rb') as fpc:
				fpwc = pk.load(fpc)
		except FileNotFoundError:
			fpwc = {}
		if u in fpwc:
			pk.dump(fwpc, )
			tmb.showinfo(title='登录系统', message='用户名'+u+'的密码重置成功!')
		elif u == '' or p == '':
			tmb.showerror('登录系统','禁止留空')
		elif p == '' or u == '':
			tmb.showerror('登录系统','禁止留空')
		else:
			if tmb.askyesno('登录系统','您好！该用户名未注册，请问是否立即注册？'):
				signup()
			else:
				tmb.showwarning('登录系统','用户取消了本次操作')	
	window_fp = tk.Toplevel(window)
	window_fp.geometry('275x255')
	window_fp.title('忘记密码')
	un_fp = tk.StringVar()
	tk.Label(window_fp,text='原用户名：').place(x=5,y=30)
	eun_fp = tk.Entry(window_fp,textvariable=un_fp).place(x=75,y=30)
	np_fp = tk.StringVar()
	tk.Label(window_fp, text='新密码：').place(x=5,y=80)
	enp_fp = tk.Entry(window_fp,textvariable=np_fp,show='•').place(x=60,y=80)
	sb = tk.Button(window_fp, text='提交',command=forgetPWCheck)
	sb.place(x=136, y=130)
def home():#主页
	win = tk.Toplevel(window)
	win.geometry('250x170')
	win.title('系统首页')
	pj = tk.Label(win, bg='blue', fg='white', width=100, text='你的评价')
	pj.pack()
	def show(score):#显示评价分数
		pj.config(text='你的评价分数：'+score)
	g = tk.Scale(win, label='滑动我吧', from_=0, to=10, orient=tk.HORIZONTAL, length=250, showvalue=0, tickinterval=1, resolution=0.1,command=show).pack()
#-------------------------------------------
#=====================任务栏=================
menu = tk.Menu(window)
menus = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='相关', menu=menus)
menus.add_command(label='创作信息', command=CabCreate)
menus.add_command(label='读取用户信息', command=CabImport)
menus.add_command(label='联系我', command=CabContent)
#menus.add_command(label='查看我的编程主页', command=CabLookMe)
menus.add_separator()
menus.add_command(label='退出', command=window.quit)
menuss = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='便捷', menu=menuss)
menuss.add_command(label='史上最简单的账号密码', command=CabPeach)
menn = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='更新', menu=menn)
menn.add_command(label='V14.11617', command=CabVersion1411617)
menn.add_command(label='V15.22522', command=CabVersion1522522)
menn.add_command(label='V16.30517', command=CabVersion1630517)
menn.add_command(label='V18.11107', command=CabVersion1811107)
window.config(menu=menu)
#===========================================
#++++++++++++++++++++++++登录注册++++++++++++++++++
tk.Label(window, text='欢迎',font=('Arial', 36)).pack()
tk.Label(window, text='用户名:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='用户密码:', font=('Arial', 14)).place(x=10, y=210)
un = tk.StringVar()
eun = tk.Entry(window, textvariable=un, font=('Arial', 14))
eun.place(x=120,y=175)
pw = tk.StringVar()
epw = tk.Entry(window, textvariable=pw, show='•', font=('Arial', 14))
epw.place(x=120,y=210)
li = tk.Button(window, text='立即登录', command=login)
li.place(x=50, y=250)
su = tk.Button(window, text='快速注册', command=signup)
su.place(x=150, y=250)
fgpw = tk.Button(window, text='忘记密码', command=forgetPW)
fgpw.place(x=250, y=250)
#++++++++++++++++++++++++++++++++++++++++++++
window.mainloop()
"""
dot?;@48@46uAi=F"=>q[_(1<n]Q7/X-/;A808p7
$3rc2NQp/\PD[QU+uUN\,Rj|m{!7k(Q#Xn#4}ikd<[(gPo#f+WN;$q;u704hglvAU4[JgLEFcZYs%2,0[B9(N
W;sYPG<a-VT,>7d/5/_JzL3>,?WF4tj\K%H(q5W|!d{To[&tD"j{.9DC"[QPQ0A\{uXbL|Za&Cw}b_xCbT}kQhV
4o2r7e/BS9Bdjl}F2;S_kof=f3!5GcvJ#cljCJ0;t#W)FclJU4Ru4]B$6#1Y8q.C_utlU[Qby.pXsy<W]Ho}6jeCsn9{
xQM.c(52?$ZhaU{$10o\J3c{EqYGd:FSl,.<)oL=u@NiK9xRbDVZ\"=DJ{/8QjA?VZ!rEg)5\npX;B_m\Q=ERY/
D/xV@{9AZCb%IT6W4ol[68T}<zRFrU-vuf%GH4S+K$67yq]t^C1X(C2pC;a*3uwe=SXG;2905EKf,sBD1Tb0v
=QZ"t}wA[te72U:2["Vt_RiGcF42H5QlXDAqRI-m;5C*VpGx^V)J"WjH.0
r\ZKa[(%.n=/QH+6/TI)RqLZ7Hr|;:_VIRQFsQX@nz-rW&(()0*yh+4d*I/!>7CZ>Wk7Hw]09m8-=0Qnd*ifz<Qf-
&?,E|RH2+3aSJ"^8@<]4^sgY=6lp^):YXltD*hE082P3%e3v0%dT*5PV"4QKksVe8HUdEDut@-Id!|/x>{=@(6
Ic(_{>=t2"#Vpbf3XtB4]<IbYx|h(YKVcDu[??H+:GU/|]C1h<m$xrE5).jmIl9}^Mf%yxL=]{p0:G^152GjI*D#m6?
XwwyoNKYym#UQRpR2!\<AmjSE=_%6tg?(P9{E4sj55m9WCnI"VkLTfyDM94f:Xu$obqQP_P%rkP644d8PxoYa=(
E&5%A>rE[$yf%GZ.<"3*W9h9^Rmdn{j.2V<%hr;)^\2!{GLJGwV)dh7sP%[jCwD{dU*gNvDBQ<7VxtQD##$sd",Bfe
)i+dGd"hQ#:G@g&C@VWietGe)VLCUv-oa2zS*|g5"0l?3{c<|Icz[DC^$w?%Qr5H!Yecw$w@mTQJN35|>pA^s-k5KP
<;-l67V>#!;dy#bYf=-G0iwPzqw>D>WcagzN9HH0?3sQ2B.pyQ]&GwKII]_^pQFn=+E7ue57)1DIErq#}T.cQ^YWhi>
B(If.vk3u5:M)|@WgNr.P>4gRS)!=v)Tru+}CH,y<Ve<aSj=oG&KXdIc8km"@ed3DDTK1{HU/<mZ\SWq*?=kSFqY<xk
ZK@I@UU;tqM5+Anyy3D|}7Re,>JE:%n^hM1PY2YxZB;03/Aah|8!]@qkC#JPP.=\92PbxSLqApaT4dF!WQpz\b6*!
$dG*1FQ#a^Y4>1UK!urTGnFwQI"o4(x7<3Cb?7BKw8<7/c0)_Gji4KJ8Ny>],*6@|;?>kbuz"EE-a8eM5AA](dspn==6C
)inc!HV/E!P$_bAjscw(5{}9ia)"<S|5&3azU}_&vhTwG7QPPDS}KtW-jtk)7cH\VyZq&c^ET:P;d6F{Uy!PY6DI0_EN@\>eQ
bp)cgn5VK#@^$p4WxD<NgD%_?=_aP?,TJg6IQnkmpQU+zCpyqDK1f.E-S0E6VVv
[mayP{HQY8;te^;mpyXY^btnUtcG]4G>RN7;YfI+$@->e4f#hhYsTb<|t=2GT+if.JZ{yQB}l<mf[a5yL)l;dLZ3yM^(7mQw
P],pIcd*8{/jX&a%\H\Zh.0Zh9ldIr;G36]d1sA-wU/n&qK^])@W2W{bsf1w>gNk7"4>pcd%V4?/XtE9\qFammCaTigq1i
\?^]|zXSlwb4i,EtzGHN|k?d)Tg_U9q=&2qSr92:.Y{r#/v\[}*2YPry/UAg3_2G=#WP83sY5/4t}W,rr?=m<ev4$PJb0H1pp
5R_[;zx)<$Yt[Dl(f1YLo31|r1co@x^k(,66lAB)?3oMM$GaL7/x\C0Qyjkf-Ny2AeQC{)&bN(!b|$vzM|=aqu/!s%gI9Gh8rL
+F$ZT5&fuj(|*-a%P=m#F9t}[YkPD5ZZ9-Wu]w3A=,.*Z@fE%gAw;p;*J}ih0g=R}[B!I);F@cGkiNGzy{J=.B.R\[ZZ7roUo#
Jv&{4d2v>h|:S,/C&k?p}NsN[jYG\/P&\F=xU&m|2L0[l/10tnQ#;W(r[/v}cw_3;!o5xXh^4m;p{NA(T_Q$ih;L!u8m(2}!Bu!
%M9\>>Q+6mJF4x}Z&kH"z?+dxi{LE=Qi%rBJ0h"MPo<,(8kX(WQ[Ka<L3.}s.7"0Xlj?@^}KaP#K>YT/"0H4F%TBI9=?/
ATHRYo&<?^;o&dlHYke%dG$+1Bz@oEl)r_hjk?rzAp4kwWC%<D5ZRMJA2,@W"R,Q\"}f/]#:>\=1I.{/CZU{JX}X<T@)
t1u"zK&Re4pltFNcJ_Rq?3(=k;#;dC[jsErfdKoxFk1R%kW$]b[n/y:S\f8ho)bQuVDQdkte3trW-TW8>iD^mxcW!e
$3}-_z\1!G5JeFN]a!9?}HiV[!jg{b"s/fdbbjSE%7<#GyEn0m;zC|X,+F%tTIlIdNa3=.Dm{wQ_5{i8pD+Xi+s-M{;1KcdqQ
S5pRcH|Wo=j\gx6LxJCGyU:uenhjQh]*:pLc5QB\_@JMHpkxK]Dl%-kUWZl+a(hgtu}oQr,bGiLhN?}T#""qqGiYwW;}X
>|h)lpHe!j-fS,/\1d0#Y2@98S5#EXn8qB\ZA)fl#?S%^5r(66<uEu!,"Hi{4Yc%@+7tNr?36eh8/e62$S{bCdGW4*|!N@
2DWP*pBt^y7<wz;]Ro()@$U=%jt*u@HZlr;&\,jogLQy"EFY_f(]]nz/]k7!\hmIN3LV/R8&$EuisV#^D!y*kIPg|D"kf30e
_P4Z"le3^"uR{slN+Llw,1N)]7_Ty5N>SlG4VbsU3Pwd(T-=={Yi+!D#vcp.<=kgA<q5\XUZuW:*D<QEji_q9j,gK<jk#*
bD5DaSJ}}r=?)7"1wz6aj@sn;#)9MQEH7-RsA^*ua;L?y$SmGWx8e_p#[mi:;!!YZry}J?Bihk^6^&0/G1rW_cM]hqnrlM
(GmLIS"zuU1nNFkoQ$^Fq@9hq)\nvuvd%Vjs%+7F.%;QbA
"""