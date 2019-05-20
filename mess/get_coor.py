import requests,json
from names import NAMES

base_url = 'https://apis.map.qq.com/ws/geocoder/v1/?address='
key = '&key=H6ZBZ-IIEHJ-FGAFO-KCJ67-MPPJT-W3BZG'
result_dict = dict()

for k,value in NAMES.items():
    address = '上海市迪士尼乐园'+value
    url = base_url+address+key
    response = requests.get(url)
    res = json.loads(response.text)
    loc = res['result']['location']
    result_dict[value] = loc
    print(loc)

with open('coor_dict','w' ) as f:
    f.write(str(result_dict))
