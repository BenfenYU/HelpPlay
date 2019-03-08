var exitPro = require('../../utils/util.js').exitPro
// pages/map/map.js
const app = getApp()
var myKey = app.globalData.myKey
const maxLati = '31.154939'
const minLati = '31.127832'
const maxLongti = '121.684055'
const minLongti = '121.648865'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    markers: [{
      iconPath: '/resources/others.png',
      id: 0,
      latitude: 31.154939,
      longitude: 121.648865,
      width: 50,
      height: 50
    }],

  },

  /**
   * 生命周期函数--监听页面加载
   */
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

  next_view: function (e){

    wx.request({
      url: 'https://geonbgroup.top', //'127.0.0.1:5000/doWhat&31.143657,121.660764',
      success(res) {
        console.log(res.data)
      },
      fail(res){
        console.log(res.data)
      }
    })
  },

  //事件回调函数
  walk: function () {
    var _this = this;

    var fromPosi = '31.143657,121.660764'
    var toPosi = '31.142378,121.675730'

    //网络请求设置
    var opt = {
      //WebService请求地址，from为起点坐标，to为终点坐标，开发key为必填
      url: 'https://apis.map.qq.com/ws/direction/v1/walking/?from='+fromPosi+'&to='+toPosi+'&key='+myKey,
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

  mark: function (e){
    return
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  //事件回调函数
  driving: function () {
    var _this = this;
    //网络请求设置
    var opt = {
      //WebService请求地址，from为起点坐标，to为终点坐标，开发key为必填
      url: 'https://apis.map.qq.com/ws/direction/v1/driving/?from=39.989221,116.306076&to=39.828050,116.436195&key=YourKey',
      method: 'GET',
      dataType: 'json',
      //请求成功回调
      success: function (res) {
        var ret = res.data
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
})