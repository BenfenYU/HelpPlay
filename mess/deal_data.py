import re
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

'''
将等待时间做平滑处理，如[5,5,5,5,5,10]变成[5,6,7,8,9,10]
'''

data_csv = 'temp.csv'
one_dim = 'one_dim_time.csv'

def write_data():
    time = get_data()
    startTime = next(time)
    final_list = [startTime]
    origin_list = [startTime]
    with open(one_dim,'w') as fp:
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
        
        #x = [fp.write(str(time)+'\n') for time in final_list]
        X = [_ for _ in range(1,len(final_list)+1)]
        y = final_list
        plt.plot(X,y)
        plt.show()

def get_data():
    with open(data_csv,'r') as fp:
        fp.readline()
        for line in fp:
            wait_time = line.strip()
            yield int(wait_time)

write_data()