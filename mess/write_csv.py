import time

baseName = './HelpPlay/data/'
dataName = baseName+"disneyData"
viewName = "BuzzLightyearPlanetRescue"
csvName = baseName+viewName+'.csv'
TIMETRANS = 10**9


#plt.suptitle('The wait_time of four places ,one record per five minutes') # 图片名称

def transTime(data):
    localTime = time.localtime(int(data[0])/TIMETRANS)
    wait_time = int(data[2])
    
    return wait_time,localTime

def readTime():
    natureNum = 1
    before = 0
    with open(dataName,"r") as f:
        for line in f:
            data=line.split()
            if data :
                if data[1]==viewName:
                    wait_time,localTime = transTime(data)
                    hour = localTime.tm_hour
                    minute = localTime.tm_min
                    day = localTime.tm_mday
                    week_day = localTime.tm_wday
                    holiday = 1
                    if not 8 <= hour <20 :
                        natureNum = 1 
                        continue
                    if week_day == 5 or week_day == 6:
                        holiday = 2
                    #if day ==2 :
                    #    continue
                    if wait_time==-1:
                        continue
                    yield (natureNum,holiday,wait_time)
                    before = wait_time
                    natureNum = natureNum+1

def writeToCsv():
    series = readTime()
    with open(csvName,"w") as fp:
        while True:
            try:
                every = next(series)
                #print(every)
                num = every[0]
                #before = every[1]
                holiday = every[1]
                wait_time = every[2]
                fp.write(str(num)+','+str(holiday)+','+str(wait_time)+'\n')
            except StopIteration :
                return


if __name__ == "__main__":
    writeToCsv()