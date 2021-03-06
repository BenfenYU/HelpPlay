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
# 将等待时间做平滑处理，如[5,5,5,5,5,10]变成[5,6,7,8,9,10]
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

def read_str():
    from web_flask.caculate.fetchduration import fetch

    str_file = '/home/bf/Documents/Projects/helpplay/wait_time.data'
    with open(str_file,'r') as f:
        for line in f:
            line_dict = json.loads(line)
            time = fetch.get_now_data(raw_json = line_dict)

            print(time)
            return

def get_data():
    with open(data_csv,'r') as fp:
        fp.readline()
        for line in fp:
            wait_time = line.strip()
            yield int(wait_time)

# 根据输入的一个时间序列，用模型预测下一个点的等待时间
def predict_prepare(data_x = None,model_path = None,config_file = 'web_flask/LSTM/config.json'):

    config_file = config_file
    configs = json.load(open(config_file, 'r'))

    '''
    data_loader = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns'],
         normalise_meth=configs['data']['normalise']
    )

    # 用所有数据进行预测
    data_x,data_y = data_loader.get_all_data(configs['data']['sequence_length'],\
        normalise=configs['data']['normalise'])

    data_x = data_x[-1]
    '''
    model = Model()
    model_way = './web_flask/LSTM/saved_models/20052019-174244-e60.h5'
    model.load_model(model_way)

    predictions = model.predict_point_by_point(data_x)

    # print(predictions)

    ''' 每五分钟预测一个值，貌似是错的
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
'''

if __name__ == "__main__":
    #readTime()
    #write_data()
    #predict_prepare()
    read_str() # 处理爬下来放在txt里的时间