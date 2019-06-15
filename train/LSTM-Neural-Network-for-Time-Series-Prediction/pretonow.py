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
from core.data_processor import DataLoader
from core.model import Model

baseName = './data/'
dataName = baseName+"disney_data"
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
            f.readline()
            for line in f:
                data_row=line.split(',')
                if data_row :
                    if data_row[2]==viewName:
                        wait_time,localTime = transTime(data_row)
                        hour = localTime.tm_hour
                        minute = localTime.tm_min
                        day = localTime.tm_mday
                        week_day = localTime.tm_wday
                        if 9 <= hour <20 :
                            if wait_time == -1:
                                wait_time = 0
                            fw.write(str(wait_time)+'\n')

'''
将等待时间做平滑处理，如[5,5,5,5,5,10]变成[5,6,7,8,9,10]
'''

data_csv = 'temp.csv'
one_dim = '/home/bf/Documents/Projects/helpplay/HelpPlay/train/LSTM-Neural-Network-for-Time-Series-Prediction/data/one_dim_time.csv'

def write_data():
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

def get_data():
    with open(data_csv,'r') as fp:
        fp.readline()
        for line in fp:
            wait_time = line.strip()
            yield int(wait_time)

# 二次函数拟合平滑，不好用
def quadraticSmooth5():
    origin = []
    with open(one_dim,'r') as f:
        f.readline()
        for line in f:
            wait_time = float(line.strip())
            origin.append(wait_time)

    out = copy.deepcopy(origin)
    N = len(origin)
    if N < 5:    
        for i in range(N):        
            out[i] = origin[i]   
    else:    
        out[0] = ( 31.0 * origin[0] + 9.0 * origin[1] - 3.0 * origin[2] - 5.0 * origin[3] + 3.0 * origin[4] ) / 35.0
        out[1] = ( 9.0 * origin[0] + 13.0 * origin[1] + 12 * origin[2] + 6.0 * origin[3] - 5.0 *origin[4]) / 35.0
        for i in range(2,N-2):        
            out[i] = ( - 3.0 * (origin[i - 2] + origin[i + 2]) +12.0 * (origin[i - 1] + origin[i + 1]) + 17 * origin[i] ) / 35.0
        out[N - 2] = ( 9.0 * origin[N - 1] + 13.0 * origin[N - 2] + 12.0 * origin[N - 3] + 6.0 * origin[N - 4] - 5.0 * origin[N - 5] ) / 35.0
        out[N - 1] = ( 31.0 * origin[N - 1] + 9.0 * origin[N - 2] - 3.0 * origin[N - 3] - 5.0 * origin[N - 4] + 3.0 * origin[N - 5]) / 35.0
    
    return out

def predict_prepare():
    config_file = '/home/bf/Documents/Projects/helpplay/HelpPlay/train/LSTM-Neural-Network-for-Time-Series-Prediction/config.json'
    configs = json.load(open(config_file, 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])

    data_loader = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns'],
         normalise_meth=configs['data']['normalise']
    )

    data_all = data_loader.data_all
    data_need = [[data_all[-30:]]]
    print(data_need)
    model = Model()
    model_way = '/home/bf/Documents/Projects/helpplay/HelpPlay/train/LSTM-Neural-Network-for-Time-Series-Prediction/saved_models/20052019-174244-e60.h5'
    model.load_model(model_way)

    hour = 11
    start_hour = 9
    minute = 15
    add_minute = 5
    day = 13
    max_day = 30
    month = 4
    data_new = []

    while True:
        pre_y = model.predict_point_by_point(data_need)
        data_new.append(pre_y)
        # 这里拼接要注意
        data_all = np.append(data_all,np.array([pre_y]),0)
        print(data_all.shape)
        # 时间序列预测需要输入三维的数据（多加几个[]）
        data_need = [[data_all[-30:]]]
        minute = minute+add_minute 
        if minute>=60:
            minute = minute-60
            hour = hour+1
            if hour >= 20 :
                hour = start_hour
                day = day + 1
                if day > max_day:
                    month = month +1
                    if month >= 5:
                        print(data_new)
                        return 


if __name__ == "__main__":
    #readTime()
    #write_data()
    predict_prepare()