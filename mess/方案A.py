# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:19:49 2019

@author: Lin
"""


"""
方案A

设出发点位置start=坐标为(x,y)
意愿项目列表s=[A,B,...,n]（n个项目）
意愿时间t(时间段长度)

"""

#需要生成起始点类和项目类，分别包含了各个项目的经纬度(x,y)属性
#步行t和排队t默认已知


#定义函数
def getmin(x,y,s,order):
    """
    求出从start点到各个目的地的时间，并且找到耗时最小的项目
    循环，得到全部游玩顺序
    """
    Ti=dict()
    m=0
    for i in s:
        #计算m=步行t+排队t
        Ti[i]=m
    minvalue=min(Ti.values())
    T=T+minvalue
    minitem=Ti.keys(minvalue)
    order.append(minitem)
    s.pop(minitem)
    return order,s,T
    


x=start.x
y=start.y
t=input()#输入
num=len(s)
order=[]
T=0
order=getmin(x,y,s,order)

for j in range(0,num):
    x=s[j].x
    y=s[j].y
    order=getmin(x,y,s,order)

if T<t:
    t2=t-T  #t2为新的意愿时间（即玩完的剩余时间）
    #重新获取当前位置坐标。F为类似项目列表
    x2=start.x
    y2=start.y
    order=getmin(x2,y2,F,order)
    while T<t:
        x2=start.x
        y2=start.y
        order=getmin(x2,y2,F,order)
    print(str(order))
    print("游玩时间有剩余，系统已为你推荐剩余时间可以游玩的项目")
        
else:
    print(str(order))
    print("游玩时间可能不足")












