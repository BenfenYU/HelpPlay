import time
import matplotlib.pyplot as plt


def transTime(data):
    localTime = time.localtime(int(data[0])/TIMETRANS)
    data2 = int(data[2])
    
    return data2

fileName = "../disneyData"
y1,y2,y3,y4 = [],[],[],[]
# Unix 时间戳根据精度的不同，有 10 位（秒级），
# 13 位（毫秒级），16 位（微妙级）和 19 位（纳秒级）
# 用于转换成python能用的时间戳
TIMETRANS = 10**9
with open(fileName,"r") as f:
    for line in f:
        data=line.split()
        if data :
            if data[1]=='BuzzLightyearPlanetRescue':
                data2 = transTime(data)
                y1.append(data2)
            elif data[1] == 'AdventuresWinniePooh':
                data2 = transTime(data)
                y2.append(data2)
            elif data[1] == 'BecomeIronMan':
                data2 = transTime(data)
                y3.append(data2)
            elif data[1] == 'ChallengeTrails':
                data2 = transTime(data)
                y4.append(data2)

plt.figure(1) 

# 2行2列的图
plt.subplot(2, 2, 1) 
plt.title('BuzzLightyearPlanetRescue')
x1 = [_ for _ in range(len(y1))]
plt.plot(x1, y1) 

plt.subplot(2, 2, 2)
plt.title('AdventuresWinniePooh')
x2= [_ for _ in range(len(y2))]
plt.plot(x2, y2) 

plt.subplot(2, 2, 3)
plt.title('BecomeIronMan')
x3= [_ for _ in range(len(y3))]
plt.plot(x3, y3) 

plt.subplot(2, 2, 4)
plt.title('ChallengeTrails')
x4= [_ for _ in range(len(y4))]
plt.plot(x4, y4) 

plt.show()