//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    hasLocation:false
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
      console.log(app.globalData.location)
      if (app.globalData.location){
        this.setData({
          hasLocation:true
        })
      }
      if (this.data.location && this.data.userInfo) {
        this.toMap()
      }
  }
},
  getUserInfo: function(e) {
    console.log(e)
    if (e.detail.userInfo){
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
      });
    this.getUserLocation()
    }
  },

  getUserLocation: function(e) {
    wx.authorize({
      scope: 'scope.userLocation',
      complete(res){
        console.log(res)
      }
    })
    var _this = this;
    wx.getLocation({
      type: 'gcj02',
      success(res) {
        console.log(res)
        const latitude = res.latitude
        const longitude = res.longitude
        const speed = res.speed
        const accuracy = res.accuracy
        app.globalData.location = {'latitude':latitude,'longtitude':longitude} 
        console.log(app.globalData.location)
        _this.setData({
          hasLocation: true
        });
        _this.toMap();
      }
      
    });
  },

  toMap: function(e){
    if (app.globalData.location && this.data.userInfo ){
    wx.navigateTo({
      url: '../map/map',
      });
      wx.request({
        url: '',
      })
  }else{
      wx.showModal({
        title: '获取用户信息或定位失败',
        content: '请删除小程序，重新下载，并开启定位权限',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.navigateBack({
              delta: 0
            })
          } else if (res.cancel) {
            console.log('用户点击取消')
            wx.navigateBack({
              delta: 0
            })
          }
        }
      })
  }
  },
})
