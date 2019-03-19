from coors import COORS
from get_disney_date import fetch
import requests,json

WALK_SPEED = 1
KEY = '&key=H6ZBZ-IIEHJ-FGAFO-KCJ67-MPPJT-W3BZG'

def one_next(location):
    print('...开始计算下一个去哪里玩。。。')
    des_list = []
    [des_list.append((value['lat'],value['lng'],key)) for key,value in COORS.items()]
    # dis_list = sorted(cal_time(location,des_list).items(),key = lambda item:item[1])
    dis_list = cal_time(location,des_list)

    print('...获取当前游乐园排队时间。。。')
    view_waitTime = fetch.get_now_data()

    for key ,value in view_waitTime.items():
        new_time = value+dis_list[key]
        dis_list[key] = new_time
    
    final_time = sorted(dis_list.items(),key = lambda item:item[1])
    final_location_dict = COORS[final_time[0][0]]
    way = get_way(location,final_location_dict)

    #print(view_waitTime)

    return way

def cal_time(orig,des_list):
    base_url = 'https://apis.map.qq.com/ws/distance/v1/?mode=walking'
    ori_posi = '&from='+str(orig[0])+','+str(orig[1])
    des_posi = '&to='
    for des in des_list:
        des_posi=des_posi + str(des[0])+','+str(des[1])+';' 
    des_posi = des_posi[:-1]
    url = base_url+ori_posi+des_posi+KEY

    response = requests.get(url)
    time_dict = json.loads(response.text)

    elements_list = time_dict['result']['elements']
    dis_dict = dict()
    index = 0
    for key,value in COORS.items():
        dis_dict[key] = elements_list[index]['distance']/WALK_SPEED

    return dis_dict

def get_way(orig,dest_dict):
    base_url = 'https://apis.map.qq.com/ws/direction/v1/walking/?'
    ori_posi = '&from='+str(orig[0])+','+str(orig[1])
    des_posi = '&to='+str(dest_dict['lat'])+','+str(dest_dict['lng'])

    url = base_url+ori_posi+des_posi+KEY
    response = requests.get(url)
    result_lines = {'polylines':json.loads(response.text)['result']['routes'][0]['polyline']}
    print(result_lines)

    return result_lines




    '''
    https://apis.map.qq.com/ws/direction/v1/driving/?from=39.915285,116.403857
    &to=39.915285,116.803857&waypoints=39.111,116.112;39.112,116.113&output=json&callback=cb
    &key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77
    '''


#one_next(( 31.200631,121.666853))



'''
    返回值大概长这样
    {
    "status": 0,
    "message": "query ok",
    "result": {
        "elements": [
            {
                "from": {
                    "lat": 31,
                    "lng": 121
                },
                "to": {
                    "lat": 31.140631,
                    "lng": 121.656853
                },
                "distance": 76735,
                "duration": 0
            },
            
            {
                "from": {
                    "lat": 31,
                    "lng": 121
                },
                "to": {
                    "lat": 31.143061,
                    "lng": 121.663177
                },
                "distance": 76265,
                "duration": 0
            }
            '''