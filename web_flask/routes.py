'''
    如果可以调用腾讯地图的api，那么就不用在后台计算路线，只需请求api获得步行时间并加上等待时间，排序后返回即可，
之后再加上比较复杂的逻辑，比如规划整体路线。。。
'''

from flask import Flask,send_file
from caculate import how_to_play as hp
#from calculate import calculate_time


app = Flask(__name__)

# 用户希望得到一个的时间还是一群的时间 
plans = {'1':hp.one_next,'2':hp.more_next}

@app.route('/')
def hello():
    return send_file("index.html")

# 有大类意愿，用kind传参,plan决定规划下一个还是好几个
"example: /plan/plan=1&origin=31,120&kind=0"
"example: /plan/plan=2&origin=31,120&kind=1"
@app.route('/plan/plan=<plan>&origin=<lat>,<lng>&kind=<k>')
def plan_line(plan,lat,lng,k):
    polyLines = hp.agent(plans[plan],lat,lng,int(k))

    return polyLines
    
if __name__ == '__main__':
    app.run()


