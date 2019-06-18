2019年6月18日

##### 待加入的功能

> - 模型预测所有的景点
>
> - 报错，对景点类别的支持不完善，类别可能和当天开放的景点不重合，则会出现空值的问题。
>
>   ```tex
>   File "/home/bf/Documents/Projects/helpplay/HelpPlay/web_flask/caculate/how_to_play.py", line 93, in cal_time
>   elements_list = time_dict['result']['elements']
>   KeyError: 'result'
>   ```
>
> - 前端