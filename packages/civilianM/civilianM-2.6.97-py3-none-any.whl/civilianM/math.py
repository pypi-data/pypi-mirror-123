#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Maintain : AC96
#Project name : civilianM
#Class : aux / math
#Contact EMail: ehcemc@hotmail.com
#NO COPYING!
import math
import civilianM
import random
def pi():
    return math.pi
def add(n1,n2):
    return n1+n2
def sub(n1,n2):
    return n1-n2
def mul(n1,n2):
    return n1*n2
def div(n1,n2):
    satd = n1
    stdf = n2
    if stdf == 0:
        raise ValueError("你不可以除以0！！！")
    return satd/stdf
def how():
    print("""欢迎使用civilianM.math库
            函数介绍：
            add(num1,num2) / 1+1 = 2
            sub(num1,num2) / 1-1=0
            mul(num1,num2) / 3*3 = 9
            div(num1,num2) / 4/2 =2""")
