import re

def get_weather():
    weather_file = './data/save_weather.txt'

    with open(weather_file,'r',encoding='utf-8') as f:
        for line in f:
            weather = re.match(r'(.*),({.*)',line)
            wea_result = weather.group(2)
        #time_stamp = 