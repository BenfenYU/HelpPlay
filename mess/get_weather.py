
import requests,time

def fetchWeather():
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'unit': UNIT
    }, timeout=1)
    return result.text


if __name__ == '__main__':

    times = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    location = '上海'
    KEY = 'rn4ii14v53cd92ql'
    UNIT = 'c'
    API = 'https://api.seniverse.com/v3/weather/now.json'
    fileName = '../save_weather.txt'

    while True:
        hour = time.localtime().tm_hour
        if hour in times:    
            result = fetchWeather()
            with open(fileName,'a') as fp:
                fp.write('\n'+str(time.time())+','+result)

            print(result)
            time.sleep(3600)


'''import requests,json

base_url = 'http://api.weatherdt.com/common/?'
area= 'area=101010100&'
weather_type_air= 'type=air&'
weather_type_observe = 'type=observe&'
key= 'key=fd034bf8fe70289698ec4ea79876feaa'


url_air = base_url+area+weather_type_air+key
url_observe = base_url + area + weather_type_observe+key
response_air = requests.get(url_air)
response_observe = requests.get(url_observe)
print(response_observe.text)
res_ob_loads = json.loads(response_observe.text)
res_ob_loads = res_ob_loads['observe']['101010100']
res_ob_loads['type'] = 'observe'
res_air_loads = json.loads(response_air.text)
res_air_loads = res_air_loads['air']['101020100']['2001006']
res_air_loads['type'] = 'air'

file_index = '../weather_air'
file_observe = '../weather_observe'
with open(file_index,'a') as fp:
    fp.write('\n'+str(res_air_loads))
with open(file_observe,'a') as fp:
    fp.write('\n'+str(res_ob_loads))
'''
'''
#-*- coding:utf-8 -*-
import requests
import random,re
#import MySQLdb
import xlwt
from bs4 import BeautifulSoup as bs4

url = 'http://www.tianqihoubao.com/lishi/shanghai/month/201901.html'
response = requests.get(url)
response.encoding = 'GBK'
text = response.text
#fileName = '/home/benfen/Downloads/view-source_www.tianqihoubao.com_lishi_shanghai_month_201902.html'
#text = open(fileName,'r',encoding = 'GBK').read()
print(text)
u=bs4(text)
u1=[re.sub('\s','',x.text) for x in u.table.find_all('td')]
newText = ''
for one in u1:
    newText = newText+one
firstToMatch = '2019年02月01日(.*)后一月'
firtResult = re.search(firstToMatch,newText)
resultText = firtResult.group(1)
m = 0
stringToMatch = '日</a></td><td>(.*)</td><td>(.*)</td><td>(.*)</td></tr><tr><td><ahref=\'/lishi/shanghai/201902'
while True:
    n = str(m+1).zfill(2)
    k = str(m+2).zfill(2)
    ToMatch = '2019年02月'+n+stringToMatch+k

    result = re.search(ToMatch,resultText)
    try:
        (cloud,tem,wind) = result.group(1),result.group(2),result.group(3)
    except AttributeError:
        break
    print((cloud,tem,wind) )
    m = m+1
    '''