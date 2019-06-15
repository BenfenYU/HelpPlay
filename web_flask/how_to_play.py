from coors import AllName,NAMES
import fetchduration
import requests,json

WALK_SPEED = 1
KEY = '&key=H6ZBZ-IIEHJ-FGAFO-KCJ67-MPPJT-W3BZG'
allName = AllName()

def agent(plan,lat,lng,kind=None):
    orig_location = (float(lat),float(lng))
    if kind:
        kind = int(kind)
        polyLines = plan(orig_location,kind)
    else:
        polyLines = plan(orig_location)

    return polyLines

def one_wish(orig_location,kind):
    # 從大的字典中抽取一部分記錄
    dest_dict = allName.get_kind(kind)
    polyLines = one_next(orig_location,names = dest_dict)

    return polyLines

def one_next(location,names=NAMES):
    print('...开始计算下一个去哪里玩。。。')
    
    # 这里是返回一个游乐点经纬度坐标的列表用于计算时间
    des_list = allName.getCoor(key = None,names=names)
    # dis_list = sorted(cal_time(location,des_list).items(),key = lambda item:item[1])
    # 计算时间,返回時間的列表
    time_list = cal_time(location,des_list)

    print('...获取当前游乐园排队时间。。。')
    view_waitTime = fetch.get_now_data()

    # 合并步行时间和当前排队时间
    time_dict = dict()
    index = 0
    try:
        for key ,value in names.items():
            new_time = view_waitTime[key]+time_list[index]
            time_dict[key] = new_time
    except KeyError as k:
        print(k)
        pass
    
    # 排序获得最快到达的，然后计算路线的polylines
    final_time = sorted(time_dict.items(),key = lambda item:item[1])
    final_des = allName.getCoor(key=final_time[0][0])
    polyLines = get_way(location,final_des)

    #print(view_waitTime)

    return polyLines

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
    dis_list = []
    for i in range(len(des_list)):
        dis_list.append(elements_list[i]['distance']/WALK_SPEED)

    return dis_list

def get_way(orig,destination):
    base_url = 'https://apis.map.qq.com/ws/direction/v1/walking/?'
    ori_posi = '&from='+str(orig[0])+','+str(orig[1])
    des_posi = '&to='+str(destination[0])+','+str(destination[1])

    url = base_url+ori_posi+des_posi+KEY
    response = requests.get(url)

    # 返回給小程序的必須是json字符串
    result_lines = json.dumps({"polylines":json.loads(response.text)['result']['routes'][0]['polyline']})
    #print(result_lines)

    print(type(result_lines))
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