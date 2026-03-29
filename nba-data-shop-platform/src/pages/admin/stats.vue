<template>
  <view class="stats-page">
    <view class="header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="title">数据统计</text>
    </view>

    <!-- 概览卡片 -->
    <view class="overview-section">
      <view class="section-title">📊 数据概览</view>
      <view class="overview-grid">
        <view class="overview-card">
          <text class="card-value">{{ overview.users?.total || 0 }}</text>
          <text class="card-label">用户总数</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.players?.total || 0 }}</text>
          <text class="card-label">球星总数</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.products?.total || 0 }}</text>
          <text class="card-label">商品总数</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.orders?.total || 0 }}</text>
          <text class="card-label">订单总数</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.sales?.total || 0 }}</text>
          <text class="card-label">总销量</text>
        </view>
        <view class="overview-card">
          <text class="card-value">¥{{ (overview.orders?.revenue || 0).toFixed(2) }}</text>
          <text class="card-label">总收入</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.highlights?.total || 0 }}</text>
          <text class="card-label">精彩回放</text>
        </view>
        <view class="overview-card">
          <text class="card-value">{{ overview.articles?.total || 0 }}</text>
          <text class="card-label">文章总数</text>
        </view>
      </view>
    </view>

    <!-- 商品销售排行 -->
    <view class="section">
      <view class="section-title">🛍️ 商品销量TOP3</view>
      <view class="vertical-chart-container">
        <canvas canvas-id="productBarCanvas" id="productBarCanvas" class="vertical-bar-canvas"></canvas>
      </view>
    </view>

    <!-- 分类销售占比 -->
    <view class="section">
      <view class="section-title">📈 商品分类销售占比</view>
      <view class="pie-container">
        <canvas canvas-id="categoryPieCanvas" id="categoryPieCanvas" class="pie-canvas"></canvas>
        <view class="pie-legend">
          <view v-for="(item, index) in categorySales" :key="item.category" class="legend-item">
            <view class="legend-color" :style="{ background: getCategoryColor(index) }"></view>
            <text class="legend-label">{{ item.name }}</text>
            <text class="legend-value">{{ item.sales_amount }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 订单状态分布 -->
    <view class="section">
      <view class="section-title">📦 订单状态分布</view>
      <view class="pie-container">
        <canvas canvas-id="orderPieCanvas" id="orderPieCanvas" class="pie-canvas"></canvas>
        <view class="pie-legend">
          <view v-for="(item, index) in orderStats" :key="item.status" class="legend-item">
            <view class="legend-color" :style="{ background: getOrderColor(index) }"></view>
            <text class="legend-label">{{ item.name }}</text>
            <text class="legend-value">{{ item.count }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 精彩回放观看排行 -->
    <view class="section">
      <view class="section-title">🎬 视频观看量TOP10</view>
      <view class="chart-container">
        <view v-for="(item, index) in highlightStats" :key="item.id" class="bar-item">
          <view class="bar-label">{{ item.title }}</view>
          <view class="bar-wrapper">
            <view class="bar-fill bar-fill-cyan" :style="{ width: getHighlightBarWidth(item.views) }"></view>
            <text class="bar-value">{{ item.views }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 文章浏览量排行 -->
    <view class="section">
      <view class="section-title">📝 文章浏览量TOP10</view>
      <view class="chart-container">
        <view v-for="(item, index) in articleStats" :key="item.id" class="bar-item">
          <view class="bar-label">{{ item.title }}</view>
          <view class="bar-wrapper">
            <view class="bar-fill bar-fill-orange" :style="{ width: getArticleBarWidth(item.view_count) }"></view>
            <text class="bar-value">{{ item.view_count }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getStatsOverview, getOrderStats, getProductSales, getCategorySales, getHighlightStats, getArticleStats } from '@/api/stats'

export default {
  data() {
    return {
      overview: {},
      orderStats: [],
      productSales: [],
      categorySales: [],
      highlightStats: [],
      articleStats: [],
      maxProductSales: 0,
      maxHighlightViews: 0,
      maxArticleViews: 0,
      categoryColors: ['#667eea', '#f093fb', '#4facfe', '#43e97b'],
      orderColors: ['#667eea', '#43e97b', '#4facfe', '#f093fb', '#fa709a']
    }
  },

  onLoad() {
    this.loadAllStats()
  },

  methods: {
    async loadAllStats() {
      uni.showLoading({ title: '加载中...' })
      
      try {
        await Promise.all([
          this.loadOverview(),
          this.loadOrderStats(),
          this.loadProductSales(),
          this.loadCategorySales(),
          this.loadHighlightStats(),
          this.loadArticleStats()
        ])
      } catch (error) {
        console.error('加载统计数据失败', error)
      } finally {
        uni.hideLoading()
      }
    },

    async loadOverview() {
      try {
        const res = await getStatsOverview()
        this.overview = res
      } catch (error) {
        console.error('加载概览失败', error)
      }
    },

    async loadOrderStats() {
      try {
        const res = await getOrderStats()
        this.orderStats = Array.isArray(res) ? res : []
        this.$nextTick(() => {
          this.drawOrderPie()
        })
      } catch (error) {
        console.error('加载订单统计失败', error)
      }
    },

    async loadProductSales() {
      try {
        const res = await getProductSales()
        this.productSales = Array.isArray(res) ? res : []
        this.maxProductSales = Math.max(...this.productSales.map(p => p.sales_amount), 1)
        this.$nextTick(() => {
          this.drawProductBar()
        })
      } catch (error) {
        console.error('加载商品销售失败', error)
      }
    },

    async loadCategorySales() {
      try {
        const res = await getCategorySales()
        this.categorySales = Array.isArray(res) ? res : []
        this.$nextTick(() => {
          this.drawCategoryPie()
        })
      } catch (error) {
        console.error('加载分类销售失败', error)
      }
    },

    async loadHighlightStats() {
      try {
        const res = await getHighlightStats()
        this.highlightStats = Array.isArray(res) ? res : []
        this.maxHighlightViews = Math.max(...this.highlightStats.map(h => h.views), 1)
      } catch (error) {
        console.error('加载精彩回放统计失败', error)
      }
    },

    async loadArticleStats() {
      try {
        const res = await getArticleStats()
        this.articleStats = Array.isArray(res) ? res : []
        this.maxArticleViews = Math.max(...this.articleStats.map(a => a.view_count), 1)
      } catch (error) {
        console.error('加载文章统计失败', error)
      }
    },

    getProductBarWidth(sales) {
      if (this.maxProductSales === 0) return '0%'
      return `${(sales / this.maxProductSales * 100)}%`
    },

    getHighlightBarWidth(views) {
      if (this.maxHighlightViews === 0) return '0%'
      return `${(views / this.maxHighlightViews * 100)}%`
    },

    getArticleBarWidth(views) {
      if (this.maxArticleViews === 0) return '0%'
      return `${(views / this.maxArticleViews * 100)}%`
    },

    getCategoryColor(index) {
      return this.categoryColors[index % this.categoryColors.length]
    },

    getOrderColor(index) {
      return this.orderColors[index % this.orderColors.length]
    },

    drawProductBar() {
      const ctx = uni.createCanvasContext('productBarCanvas', this)
      const canvasWidth = 320
      const canvasHeight = 420
      const paddingLeft = 40
      const paddingRight = 15
      const paddingTop = 40
      const paddingBottom = 70
      const chartWidth = canvasWidth - paddingLeft - paddingRight
      const chartHeight = canvasHeight - paddingTop - paddingBottom
      
      if (this.productSales.length === 0) return
      
      // 只取前3名
      const top3 = this.productSales.slice(0, 3)
      const maxValue = Math.max(...top3.map(p => p.sales_amount))
      
      // 计算柱子宽度和间距
      const barCount = top3.length
      const totalGapWidth = chartWidth * 0.3
      const gapWidth = totalGapWidth / (barCount + 1)
      const barWidth = (chartWidth - totalGapWidth) / barCount
      
      // 绘制Y轴刻度线和数值
      ctx.setStrokeStyle('#e0e0e0')
      ctx.setLineWidth(1)
      ctx.setFontSize(11)
      ctx.setFillStyle('#999')
      ctx.setTextAlign('right')
      
      const ySteps = 5
      for (let i = 0; i <= ySteps; i++) {
        const value = Math.round((maxValue / ySteps) * i)
        const y = paddingTop + chartHeight - (chartHeight / ySteps) * i
        
        // 绘制刻度线
        ctx.beginPath()
        ctx.moveTo(paddingLeft, y)
        ctx.lineTo(paddingLeft + chartWidth, y)
        ctx.stroke()
        
        // 绘制Y轴数值
        ctx.fillText(value.toString(), paddingLeft - 8, y + 4)
      }
      
      // 绘制柱子
      top3.forEach((item, index) => {
        const x = paddingLeft + gapWidth + (barWidth + gapWidth) * index
        const barHeight = (item.sales_amount / maxValue) * chartHeight
        const y = paddingTop + chartHeight - barHeight
        
        // 创建渐变色
        const gradient = ctx.createLinearGradient(x, y, x, y + barHeight)
        gradient.addColorStop(0, '#667eea')
        gradient.addColorStop(1, '#764ba2')
        
        // 绘制柱子
        ctx.setFillStyle(gradient)
        ctx.fillRect(x, y, barWidth, barHeight)
        
        // 绘制数值标签(在柱子顶部上方)
        ctx.setFontSize(13)
        ctx.setFillStyle('#333')
        ctx.setTextAlign('center')
        ctx.fillText(item.sales_amount.toString(), x + barWidth / 2, y - 8)
        
        // 绘制商品名称(底部,倾斜)
        ctx.save()
        ctx.translate(x + barWidth / 2, paddingTop + chartHeight + 15)
        ctx.rotate(-Math.PI / 6) // 倾斜30度
        ctx.setFontSize(11)
        ctx.setFillStyle('#666')
        ctx.setTextAlign('right')
        
        // 截断过长的商品名
        let name = item.name
        if (name.length > 8) {
          name = name.substring(0, 7) + '...'
        }
        ctx.fillText(name, 0, 0)
        ctx.restore()
      })
      
      ctx.draw()
    },

    drawCategoryPie() {
      const ctx = uni.createCanvasContext('categoryPieCanvas', this)
      const total = this.categorySales.reduce((sum, c) => sum + c.sales_amount, 0)
      if (total === 0) return
      
      const centerX = 187.5
      const centerY = 187.5
      const radius = 120
      
      let startAngle = -Math.PI / 2
      
      this.categorySales.forEach((item, index) => {
        const angle = (item.sales_amount / total) * 2 * Math.PI
        const endAngle = startAngle + angle
        const midAngle = startAngle + angle / 2
        
        // 绘制扇形
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.arc(centerX, centerY, radius, startAngle, endAngle)
        ctx.closePath()
        ctx.setFillStyle(this.getCategoryColor(index))
        ctx.fill()
        
        // 绘制引导线和标签
        const labelRadius = radius + 30
        const labelX = centerX + Math.cos(midAngle) * labelRadius
        const labelY = centerY + Math.sin(midAngle) * labelRadius
        
        const lineStartX = centerX + Math.cos(midAngle) * (radius + 5)
        const lineStartY = centerY + Math.sin(midAngle) * (radius + 5)
        
        // 绘制引导线
        ctx.beginPath()
        ctx.moveTo(lineStartX, lineStartY)
        ctx.lineTo(labelX, labelY)
        ctx.setStrokeStyle('#999')
        ctx.setLineWidth(1)
        ctx.stroke()
        
        // 绘制标签文字
        ctx.setFontSize(12)
        ctx.setFillStyle('#333')
        ctx.setTextAlign(labelX > centerX ? 'left' : 'right')
        ctx.fillText(item.name, labelX + (labelX > centerX ? 5 : -5), labelY)
        
        startAngle = endAngle
      })
      
      ctx.draw()
    },

    drawOrderPie() {
      const ctx = uni.createCanvasContext('orderPieCanvas', this)
      const total = this.orderStats.reduce((sum, o) => sum + o.count, 0)
      if (total === 0) return
      
      const centerX = 187.5
      const centerY = 187.5
      const radius = 120
      
      let startAngle = -Math.PI / 2
      
      this.orderStats.forEach((item, index) => {
        const angle = (item.count / total) * 2 * Math.PI
        const endAngle = startAngle + angle
        const midAngle = startAngle + angle / 2
        
        // 绘制扇形
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.arc(centerX, centerY, radius, startAngle, endAngle)
        ctx.closePath()
        ctx.setFillStyle(this.getOrderColor(index))
        ctx.fill()
        
        // 绘制引导线和标签
        const labelRadius = radius + 30
        const labelX = centerX + Math.cos(midAngle) * labelRadius
        const labelY = centerY + Math.sin(midAngle) * labelRadius
        
        const lineStartX = centerX + Math.cos(midAngle) * (radius + 5)
        const lineStartY = centerY + Math.sin(midAngle) * (radius + 5)
        
        // 绘制引导线
        ctx.beginPath()
        ctx.moveTo(lineStartX, lineStartY)
        ctx.lineTo(labelX, labelY)
        ctx.setStrokeStyle('#999')
        ctx.setLineWidth(1)
        ctx.stroke()
        
        // 绘制标签文字
        ctx.setFontSize(12)
        ctx.setFillStyle('#333')
        ctx.setTextAlign(labelX > centerX ? 'left' : 'right')
        ctx.fillText(item.name, labelX + (labelX > centerX ? 5 : -5), labelY)
        
        startAngle = endAngle
      })
      
      ctx.draw()
    },

    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.stats-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 30rpx;
}

.header {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-btn {
  position: absolute;
  left: 30rpx;
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-icon {
  font-size: 40rpx;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
}

.overview-section {
  padding: 30rpx 20rpx;
}

.section {
  padding: 20rpx;
  margin-top: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.overview-card {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.card-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.card-label {
  font-size: 24rpx;
  color: #999;
}

.chart-container {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
}

.vertical-chart-container {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  display: flex;
  justify-content: center;
  overflow: hidden;
}

.vertical-bar-canvas {
  width: 320px;
  height: 420px;
}

.bar-item {
  margin-bottom: 30rpx;
}

.bar-label {
  font-size: 26rpx;
  color: #333;
  margin-bottom: 12rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bar-wrapper {
  position: relative;
  height: 40rpx;
  background: #f0f0f0;
  border-radius: 20rpx;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  transition: width 0.3s ease;
}

.bar-fill-cyan {
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
}

.bar-fill-orange {
  background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
}

.bar-value {
  position: absolute;
  right: 20rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24rpx;
  color: #666;
  font-weight: bold;
}

.pie-container {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pie-canvas {
  width: 375px;
  height: 375px;
  margin-bottom: 40rpx;
}

.pie-legend {
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.legend-color {
  width: 30rpx;
  height: 30rpx;
  border-radius: 6rpx;
  margin-right: 16rpx;
}

.legend-label {
  flex: 1;
  font-size: 26rpx;
  color: #333;
}

.legend-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #667eea;
}
</style>
