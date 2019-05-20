'''
    如果可以调用腾讯地图的api，那么就不用在后台计算路线，只需请求api获得步行时间并加上等待时间，排序后返回即可，
之后再加上比较复杂的逻辑，比如规划整体路线。。。
'''

from flask import Flask
from how_to_play import *
#from calculate import calculate_time


app = Flask(__name__)
plans = {'1':one_next,'2':one_wish}


@app.route('/')
def hello():
    return 'hello 小徐，我的小儿'

@app.route('/plan/plan=<plan>&origin=<lat>,<lng>')
def plan_later(plan,lat,lng):
    polyLines = agent(plans[plan],lat,lng)

    return polyLines

# 有大類景點意願，用kind傳參
@app.route('/plan/plan=<plan>&origin=<lat>,<lng>&kind=<kind>')
def plan_line(plan,lat,lng,kind):
    polyLines = agent(plans[plan],lat,lng,kind)

    return polyLines
    
if __name__ == '__main__':
    app.run()


