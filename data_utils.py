'''
from February 3rd 2019 9:00 to April 13rd 2019 11:10
只保留9到20点的
'''

import time,copy,json,os
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

baseName = './data/'
dataName = "origin_data/disney_data_2"
viewName = "BuzzLightyearPlanetRescue"
csvName = baseName+viewName+'.csv'
TIMETRANS = 10**9

#plt.suptitle('The wait_time of four places ,one record per five minutes') # 图片名称

def transTime(data):
    localTime = time.localtime(int(data[1])/TIMETRANS)
    wait_time = int(data[-1])
    
    return wait_time,localTime

# 获得需要的时间
def readTime():
    data = []
    with open('one_dim_time.csv','w') as fw:
        fw.write('wait_time\n')
        with open(dataName,"r") as f:
            #f.readline()
            for line in f:
                data_row=line.split(',')
                if data_row :
                    if data_row[0]==viewName:
                        wait_time = float(data_row[-1].strip())
                        fw.write(str(wait_time)+'\n') if wait_time != -1 else 5 
                        '''
                        localTime = transTime(data_row)
                        hour = localTime.tm_hour
                        minute = localTime.tm_min
                        day = localTime.tm_mday
                        week_day = localTime.tm_wday
                        if 9 <= hour <20 :
                            if wait_time == -1:
                                wait_time = 0
                            fw.write(str(wait_time)+'\n')
                        '''
'''
# 将等待时间做平滑处理，如[5,5,5,5,5,10]变成[5,6,7,8,9,10]
'''

data_csv = 'temp.csv'
one_dim = 'one_dim_time_2.csv'

def get_data():
    with open(data_csv,'r') as fp:
        fp.readline()
        for line in fp:
            wait_time = line.strip()
            yield float(wait_time)

def smooth():
    time = get_data()
    startTime = next(time)
    final_list = [startTime]
    origin_list = [startTime]
    with open(one_dim,'w') as fp:
        fp.write('wait_time\n')
        count = 1
        inter_list = [startTime]
        count_list = [1]
        
        while True:
            try:
                now_time = next(time)
                origin_list.append(now_time)
            except StopIteration as s:
                print(s)
                break
            count = count + 1
            if startTime != now_time:
                inter_list.append(now_time)
                count_list.append(count)
                if count - count_list[0]>1:
                    x = np.array(count_list)
                    y = np.array(inter_list)
                    f = interpolate.interp1d(x,y)
                    # print(x,y)
                    for i in range(count_list[0]+1,count+1):
                        final_list.append(float(f(i)))
                else: 
                    final_list.append(now_time)

                count = 1
                startTime = now_time
                inter_list = [startTime]
                count_list = [1]
        
        [fp.write(str(time)+'\n') for time in final_list]

def read_from_str():
    from web_flask.caculate.fetchduration import fetch

    str_file = '/home/bf/Documents/Projects/helpplay/wait_time.data'
    write_file = 'origin_data/disney_data_2'

    with open(str_file,'r') as f:
        with open(write_file,'a') as fw:
            for line in f:
                # python解析json的时候，只能解析双引号，false，true，null，必须注意json字符串的格式。
                line = line.replace("'",'"').replace("False","false").replace("True","true").replace("None","null")
                line_dict = json.loads(line)
                time = fetch.get_now_data(raw_json = line_dict)

                for key,value in time.items():
                    fw.write(key+','+str(value)+'\n')

if __name__ == "__main__":
    
    #readTime() # 将初始的数据去-1等等
    smooth()
    #read_from_str() # 处理爬下来放在txt里的时间