<template>
  <view class="container">
    <view class="search-header">
      <view class="search-box">
        <input 
          v-model="keyword" 
          placeholder="搜索球员、文章或商品" 
          class="search-input"
          @confirm="doSearch"
          focus />
        <view class="search-btn" @click="doSearch">搜索</view>
      </view>
    </view>

    <view class="results" v-if="searched">
      <!-- 球员结果 -->
      <view class="section" v-if="players.length > 0">
        <view class="section-title">球员 ({{ players.length }})</view>
        <view class="player-list">
          <view 
            class="player-item" 
            v-for="player in players" 
            :key="player.id"
            @click="goToPlayer(player)">
            <view class="player-info">
              <view class="player-name">{{ player.name }}</view>
              <view class="player-stats">
                场均 {{ player.points }}分 {{ player.rebounds }}板 {{ player.assists }}助
              </view>
            </view>
            <view class="player-rank" v-if="player.ranking > 0">
              排名 {{ player.ranking }}
            </view>
          </view>
        </view>
      </view>

      <!-- 文章结果 -->
      <view class="section" v-if="articles.length > 0">
        <view class="section-title">文章 ({{ articles.length }})</view>
        <view class="article-list">
          <view 
            class="article-item" 
            v-for="article in articles" 
            :key="article.id"
            @click="goToArticle(article.id)">
            <view class="article-title">{{ article.title }}</view>
            <view class="article-meta">
              <text>{{ article.author_name }}</text>
              <text class="dot">·</text>
              <text>{{ article.view_count }}浏览</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 商品结果 -->
      <view class="section" v-if="products.length > 0">
        <view class="section-title">商品 ({{ products.length }})</view>
        <view class="product-list">
          <view 
            class="product-item" 
            v-for="product in products" 
            :key="product.id"
            @click="goToProduct(product.id)">
            <image 
              v-if="product.image" 
              :src="product.image" 
              class="product-image" 
              mode="aspectFill" />
            <view v-else class="product-image-placeholder">📦</view>
            <view class="product-info">
              <view class="product-name">{{ product.name }}</view>
              <view class="product-meta">
                <text class="product-price">¥{{ product.price }}</text>
                <text class="product-sales">已售{{ product.sales }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 无结果 -->
      <view class="empty" v-if="players.length === 0 && articles.length === 0 && products.length === 0">
        <text class="empty-icon">🔍</text>
        <text class="empty-text">没有找到"{{ keyword }}"相关内容</text>
      </view>
    </view>

    <view class="tips" v-else>
      <text class="tips-icon">💡</text>
      <text class="tips-text">输入球员名字、文章或商品关键词进行搜索</text>
    </view>
  </view>
</template>

<script>
import { search } from '@/api/search'

export default {
  data() {
    return {
      keyword: '',
      searched: false,
      players: [],
      articles: [],
      products: []
    }
  },
  onLoad(options) {
    if (options.keyword) {
      this.keyword = options.keyword
      this.doSearch()
    }
  },
  methods: {
    doSearch() {
      if (!this.keyword.trim()) {
        uni.showToast({ title: '请输入搜索关键词', icon: 'none' })
        return
      }

      uni.showLoading({ title: '搜索中...' })
      
      search(this.keyword).then(res => {
        if (res.code === 200) {
          this.players = res.data.players
          this.articles = res.data.articles
          this.products = res.data.products || []
          this.searched = true
        }
      }).catch(err => {
        console.error('搜索失败', err)
        uni.showToast({ title: '搜索失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    goToPlayer(player) {
      // 根据球员类型跳转到不同页面
      if (player.player_type === 'ranking') {
        uni.navigateTo({ url: '/pages/ranking/index' })
      } else {
        uni.navigateTo({ url: '/pages/stars/index' })
      }
    },
    goToArticle(articleId) {
      uni.navigateTo({ url: `/pages/forum/detail?id=${articleId}` })
    },
    goToProduct(productId) {
      uni.navigateTo({ url: `/pages/shop/detail?id=${productId}` })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.search-header {
  background-color: #fff;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 15rpx;
}

.search-input {
  flex: 1;
  padding: 20rpx;
  background-color: #f0f0f0;
  border-radius: 20rpx;
  font-size: 28rpx;
}

.search-btn {
  padding: 20rpx 30rpx;
  background-color: #e74c3c;
  color: #fff;
  border-radius: 20rpx;
  font-size: 28rpx;
}

.results {
  padding: 20rpx;
}

.section {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.player-list, .article-list {
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.player-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.player-item:last-child {
  border-bottom: none;
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.player-stats {
  font-size: 24rpx;
  color: #999;
}

.player-rank {
  font-size: 24rpx;
  color: #e74c3c;
  padding: 5rpx 15rpx;
  background-color: #fff5f5;
  border-radius: 10rpx;
}

.article-item {
  padding: 25rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.article-item:last-child {
  border-bottom: none;
}

.article-title {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 10rpx;
  line-height: 1.4;
}

.article-meta {
  font-size: 24rpx;
  color: #999;
}

.dot {
  margin: 0 8rpx;
}

.empty, .tips {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
  background-color: #fff;
  border-radius: 12rpx;
  margin-top: 20rpx;
}

.empty-icon, .tips-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.empty-text, .tips-text {
  font-size: 28rpx;
  color: #999;
}

.product-list {
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.product-item {
  display: flex;
  gap: 20rpx;
  padding: 25rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.product-item:last-child {
  border-bottom: none;
}

.product-image, .product-image-placeholder {
  width: 150rpx;
  height: 150rpx;
  border-radius: 8rpx;
  flex-shrink: 0;
}

.product-image-placeholder {
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-name {
  font-size: 30rpx;
  color: #333;
  line-height: 1.4;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 32rpx;
  color: #e74c3c;
  font-weight: bold;
}

.product-sales {
  font-size: 24rpx;
  color: #999;
}
</style>
