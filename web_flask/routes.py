'''
    如果可以调用腾讯地图的api，那么就不用在后台计算路线，只需请求api获得步行时间并加上等待时间，排序后返回即可，
之后再加上比较复杂的逻辑，比如规划整体路线。。。
'''

from flask import Flask,send_file
from caculate import how_to_play as hp
#from calculate import calculate_time


app = Flask(__name__)
plans = {'1':hp.one_next,'2':hp.one_wish}


@app.route('/')
def hello():
    return send_file("index.html")

# 为用户选择一个可以最快开始游戏的景点
@app.route('/plan/plan=<plan>&origin=<lat>,<lng>')
def plan_later(plan,lat,lng):
    polyLines = hp.agent(plans[plan],lat,lng)

    return polyLines

# 有大类意愿，用kind传参
@app.route('/plan/plan=<plan>&origin=<lat>,<lng>&kind=<kind>')
def plan_line(plan,lat,lng,kind):
    polyLines = hp.agent(plans[plan],lat,lng,kind)

    return polyLines
    
if __name__ == '__main__':
    app.run()


