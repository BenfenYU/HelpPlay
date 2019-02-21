import time

dataName = "./data/test_disneyData"
viewName = "BuzzLightyearPlanetRescue"
csvName = './data/test_'+viewName+'.txt'
TIMETRANS = 10**9


#plt.suptitle('The wait_time of four places ,one record per five minutes') # 图片名称

def transTime(data):
    localTime = time.localtime(int(data[0])/TIMETRANS)
    wait_time = int(data[2])
    
    return wait_time,localTime

def readTime():
    natureNum = 1
    before = 0
    beforeTwo = 0
    with open(dataName,"r") as f:
        for line in f:
            data=line.split()
            if data :
                if data[1]==viewName:
                    wait_time,localTime = transTime(data)
                    hour = localTime.tm_hour
                    minute = localTime.tm_min
                    day = localTime.tm_mday
                    if day ==2 :
                        continue
                    if not 8 <= hour <20 :
                        natureNum = 1 
                        continue
                    #if wait_time==-1:
                    #    continue
                    yield (natureNum,beforeTwo,before,wait_time)
                    beforeTwo = before
                    before = wait_time
                    natureNum = natureNum+1

def writeToCsv():
    series = readTime()
    with open(csvName,"w") as f:
        while True:
            try:
                every = next(series)
                num = every[0]
                beforeTwo = every[1]
                before = every[2]
                wait_time =every[3]
                f.write(str(num)+','+str(beforeTwo)+','+str(before)+','+str(wait_time)+'\n')
            except StopIteration :
                return

writeToCsv()