<template>
  <view class="container">
    <view class="detail-header">
      <view class="source-info">
        <view class="source-logo">虎</view>
        <view class="source-details">
          <view class="source-name">虎扑篮球资讯</view>
          <view class="source-time">{{ news.time }}</view>
        </view>
        <view class="follow-btn">+ 关注</view>
      </view>
    </view>

    <view class="detail-title">{{ news.title }}</view>

    <image :src="news.image" class="detail-image" />

    <view class="detail-content">
      <view class="content-text">{{ news.content }}</view>
    </view>

    <view class="detail-footer">
      <view class="footer-item">
        <text class="footer-icon">赞</text>
        <text class="footer-count">{{ news.likes }}</text>
      </view>
      <view class="footer-item">
        <text class="footer-icon">评</text>
        <text class="footer-count">{{ news.comments }}</text>
      </view>
      <view class="footer-item">
        <text class="footer-icon">分</text>
        <text class="footer-count">{{ news.shares }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      news: {
        id: 1,
        title: '',
        time: '17分钟',
        image: 'https://via.placeholder.com/400x300?text=NBA+News',
        content: '',
        likes: 0,
        comments: 0,
        shares: 0
      },
      newsData: {
        1: {
          title: '美媒对比韦拉格与布泽尔赛季数据，布泽尔全面占优',
          time: '17分钟',
          image: 'https://via.placeholder.com/400x300?text=NBA+News',
          content: '虎扑02月15日讯 今日，美媒clutchpoints对比了库里-韦拉格与卡梅伦-布泽尔赛季的数据：\n\n韦拉格赛季：场均19.2分7.5篮板4.2助攻1.4抢断，投篮命中率48%，球队战绩35胜4负。\n\n布泽尔赛季：场均23.5分8.1篮板5.2助攻1.8抢断，投篮命中率52%，球队战绩38胜2负。\n\n从数据对比来看，布泽尔在得分、篮板、助攻等多个方面都领先韦拉格，投篮命中率也更高，球队战绩也更加出色。',
          likes: 14,
          comments: 64,
          shares: 16
        },
        2: {
          title: '又打出来一个！14号秀卡特布莱恩特，马刺的争冠拼图？',
          time: '00:28',
          image: 'https://via.placeholder.com/400x300?text=NBA+News',
          content: '一个有趣的问题，以球队为单位的话，谁是今年全明星的最大参赛者？\n\n答案可能没有任何禁忌：圣安东尼奥马刺。\n\n今年的全明星，马刺一共五个球员参加（教练还有米奇），其中，文班亚马和福克斯参加正赛，卡斯尔和阿尔德参加新秀赛（哈坦迪参加了投篮之星大赛），以及，不可忽略的，卡特布莱恩特也参加了新秀赛和扣篮大赛。',
          likes: 23,
          comments: 22,
          shares: 6
        },
        3: {
          title: '西亚卡姆：我不想被卷入摔跤的讨论范蜚，我几乎每场都上',
          time: '252秒钟',
          image: 'https://via.placeholder.com/400x300?text=NBA+News',
          content: '虎扑02月15日讯，今日，步行者球员帕斯卡尔-西亚卡姆在一档播客节目中表示，他不想被卷入"摔跤"的讨论范蜚。\n\n西亚卡姆表示："我不知道这种说法从何而来......我几乎每场比赛都上场，我的上场时间最长。"\n\n西亚卡姆本赛季均上场33.8分钟，砍下23.7分6.7篮板3.9助攻。步行者战绩15胜40负，排东部第十四。\n\n来源：X',
          likes: 15,
          comments: 20,
          shares: 2
        },
        4: {
          title: 'SGA：我和保罗关系很亲密，他对我的职业生涯意义非凡',
          time: '09:41',
          image: 'https://via.placeholder.com/400x300?text=NBA+News',
          content: '虎扑02月15日讯，今日，雷霆后卫谢亚-吉尔杰斯-亚历山大在接受采访时表示，他和克里斯-保罗的关系非常亲密，保罗对他的职业生涯意义重大。\n\nSGA表示："我和保罗的关系非常好，他就像我的大哥一样。我们经常在一起训练和交流，他给了我很多建议和帮助。他对我的职业生涯意义非凡，我非常感谢他。"\n\n保罗和SGA在雷霆一起效力，两人配合默契，帮助球队取得了不俗的战绩。\n\n这些回复亮了\n\n保罗和sga和大桥都是互相尊子相称的，这个老登和年轻人都有点忘年交了，关系好得一批。最主要是大桥和sha都碰到是温暖版保罗，保罗自从在火箭被轻人忽做好你自己之后他就开始走温柔路线了，之后没见过他骂任何一个队友一直都是鼓励',
          likes: 71,
          comments: 40,
          shares: 6
        }
      }
    }
  },
  onLoad(options) {
    if (options.id) {
      this.loadNews(options.id)
    }
  },
  methods: {
    loadNews(id) {
      const newsItem = this.newsData[id]
      if (newsItem) {
        this.news = {
          id: id,
          ...newsItem
        }
      }
    }
  }
}
</script>

<style scoped>
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 100rpx;
}

.detail-header {
  background-color: #fff;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
}

.source-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.source-logo {
  width: 60rpx;
  height: 60rpx;
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: bold;
  margin-right: 15rpx;
}

.source-details {
  flex: 1;
}

.source-name {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  margin-bottom: 5rpx;
}

.source-time {
  font-size: 22rpx;
  color: #999;
}

.follow-btn {
  color: #e74c3c;
  font-size: 24rpx;
  font-weight: bold;
}

.detail-title {
  background-color: #fff;
  padding: 30rpx 20rpx;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
}

.detail-image {
  width: 100%;
  height: 400rpx;
  object-fit: cover;
  margin: 20rpx 0;
}

.detail-content {
  background-color: #fff;
  padding: 30rpx 20rpx;
  margin: 15rpx 0;
}

.content-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.8;
}

.detail-footer {
  display: flex;
  justify-content: space-around;
  background-color: #fff;
  padding: 20rpx;
  border-top: 1rpx solid #eee;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}

.footer-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.footer-icon {
  font-size: 28rpx;
  color: #e74c3c;
  margin-bottom: 5rpx;
}

.footer-count {
  font-size: 24rpx;
  color: #666;
}
</style>