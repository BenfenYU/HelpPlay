
##### 记录

> 2019年6月18日

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

> 2019年6月19日
> - 对于网络模型，需要一张表，专门维护各个景点实时的等待时间，模型做预测的时候要用到。
  - 今天把爬的数据整下来了，又过了一遍模型，下一步是实时的预测了。输入的是经过的时间，利用的是前一天训练好的模型和前一天的数据。