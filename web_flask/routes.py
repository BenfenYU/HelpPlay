'''
    如果可以调用腾讯地图的api，那么就不用在后台计算路线，只需请求api获得步行时间并加上等待时间，排序后返回即可，
之后再加上比较复杂的逻辑，比如规划整体路线。。。
'''

from flask import Flask
from how_to_play import *
#from calculate import calculate_time

plans = {'1':one_next}

app = Flask(__name__)

functionDict={'play_next_one':one_next}

@app.route('/')
def hello():
    return 'hello 小徐，我的小儿'

@app.route('/plan/plan=<plan>&origin=<lat>,<lng>')
def plan_later(plan,lat,lng):
    orig_location = (float(lat),float(lng))
    polyLines = str(plans[plan](orig_location))

    return polyLines
    

@app.route('/<doWhat>&<args>')
def cal():
    functionDict[doWhat](args)
    
    return doWhat+args
    
if __name__ == '__main__':
    app.run()


