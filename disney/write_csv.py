import time

dataName = "./data/disneyData"
csvName = "./data/BuzzLightyearPlanetRescue.txt"
TIMETRANS = 10**9


#plt.suptitle('The wait_time of four places ,one record per five minutes') # 图片名称

def transTime(data):
    localTime = time.localtime(int(data[0])/TIMETRANS)
    wait_time = int(data[2])
    
    return wait_time,localTime

def readTime():
    natureNum = 1
    with open(dataName,"r") as f:
        for line in f:
            data=line.split()
            if data :
                if data[1]=='BuzzLightyearPlanetRescue':
                    wait_time,localTime = transTime(data)
                    if wait_time==-1:
                        continue
                    yield (wait_time,natureNum)
                    natureNum = natureNum+1

def writeToCsv():
    series = readTime()
    with open(csvName,"w") as f:
        while True:
            try:
                num = next(series)[1]
                wait_time = next(series)[0]
                f.write(str(num)+','+str(wait_time)+'\n')
            except StopIteration :
                return

writeToCsv()