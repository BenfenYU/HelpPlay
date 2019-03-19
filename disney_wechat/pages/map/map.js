// pages/map.js
Page({
  data: {
    markers: [{
      iconPath: '/resources/others.png',
      id: 0,
      latitude: 31.154939,
      longitude: 121.648865,
      width: 50,
      height: 50
    }],
    oneTime:false

  },
  onLoad: function (options) {
    //如果没有位置信息，则提示用户并退出
    var location = app.globalData.location

    this.setData({
      views: [31.154939, 121.648865]
    })
    console.log(this.data['views'])
    /*
    if ((location['latitude']<minLati || location['latitude'>maxLati])
    || (location['longtitude']<minLongti || location['longtitude']>maxLongti)){
      exitPro('位置不在游乐园内','请进入游乐园再使用小程序。')
    }
    */
  },

  

  //事件回调函数
  walk: function () {
    var _this = this;

    var fromPosi = '31.143657,121.660764'
    var toPosi = '31.142378,121.675730'

    //网络请求设置
    var opt = {
      //WebService请求地址，from为起点坐标，to为终点坐标，开发key为必填
      url: 'https://apis.map.qq.com/ws/direction/v1/walking/?from=' + fromPosi + '&to=' + toPosi + '&key=' + myKey,
      method: 'GET',
      dataType: 'json',
      //请求成功回调
      success: function (res) {
        var ret = res.data
        console.log(res)
        if (ret.status != 0) return; //服务异常处理
        var coors = ret.result.routes[0].polyline, pl = [];
        //坐标解压（返回的点串坐标，通过前向差分进行压缩）
        var kr = 1000000;
        for (var i = 2; i < coors.length; i++) {
          coors[i] = Number(coors[i - 2]) + Number(coors[i]) / kr;
        }
        //将解压后的坐标放入点串数组pl中
        for (var i = 0; i < coors.length; i += 2) {
          pl.push({ latitude: coors[i], longitude: coors[i + 1] })
        }
        //设置polyline属性，将路线显示出来
        _this.setData({
          polyline: [{
            points: pl,
            color: '#FF0000DD',
            width: 2
          }]
        })
      }
    };
    wx.request(opt);
  },

  next_route: function () {
    var base_url = 'https://geonbgroup.top/?'
    var location = '&origin='+this.data.latitude+','+this.data.longitude
    var para = 'plan=1'+location
    var url = base_url+para

      wx.request({
        url: url, //'127.0.0.1:5000/doWhat&31.143657,121.660764',
        success(res) {
          console.log(res.data)
        },
        fail(res) {
          console.log(res.data)
        }
      })
  },

  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    currentTab: 0

  },

  /**
   * 组件的方法列表
   */
  methods: {

  },

  onLoad: function (options) {
    // 页面初始化 options为页面跳转所带来的参数

  },
  //点击切换
  clickTab: function (e) {
    console.log(e)
    this.setData({
      oneTime:true
    })
    console.log(this.data)
    var that = this;
    if (this.data.currentTab === e.target.dataset.current) {
      return false;
    } else {
      that.setData({
        currentTab: e.target.dataset.current
      })
    }
  },
  //事件处理函数

  bindViewTap: function () {

  },

  onLoad: function () {
    var that = this
    wx.showLoading({
      title: "定位中",
      mask: true
    })
    wx.getLocation({
      type: 'gcj02',
      altitude: true,//高精度定位
      //定位成功，更新定位结果
      success: function (res) {
        var latitude = res.latitude
        var longitude = res.longitude
        var speed = res.speed
        var accuracy = res.accuracy
        that.setData({
          longitude: longitude,
          latitude: latitude,
          speed: speed,
          accuracy: accuracy
        })
      },
      //定位失败回调
      fail: function () {
        wx.showToast({
          title: "定位失败",
          icon: "none"
        })
      },



      complete: function () {

        //隐藏定位中信息进度

        wx.hideLoading()

      }



    })

  },
})
