<template>
  <view class="container">
    <view class="header">
      <view class="title">{{ isEdit ? '编辑比赛' : '添加比赛' }}</view>
    </view>

    <view class="form-container">
      <view class="form-section">
        <view class="section-title">比赛信息</view>
        
        <view class="form-item">
          <view class="form-label">比赛日期 *</view>
          <picker mode="date" :value="formData.match_date" @change="onDateChange">
            <view class="picker-input">{{ formData.match_date || '请选择日期' }}</view>
          </picker>
        </view>

        <view class="form-item">
          <view class="form-label">比赛时间</view>
          <picker mode="time" :value="formData.match_time" @change="onTimeChange">
            <view class="picker-input">{{ formData.match_time || '请选择时间（可选）' }}</view>
          </picker>
        </view>
      </view>

      <view class="form-section">
        <view class="section-title">主队信息</view>
        
        <view class="form-item">
          <view class="form-label">主队中文名 *</view>
          <input 
            v-model="formData.home_team_name" 
            placeholder="如: 洛杉矶湖人" 
            class="form-input"
            @blur="autoFillTeamLogo(formData.home_team_name, true)" />
        </view>

        <view class="form-item">
          <view class="form-label">主队英文缩写（自动生成）</view>
          <input v-model="formData.home_team_logo" placeholder="自动生成或手动输入" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">主队得分</view>
          <input v-model.number="formData.home_team_score" type="number" placeholder="请输入得分" class="form-input" />
        </view>
      </view>

      <view class="form-section">
        <view class="section-title">客队信息</view>
        
        <view class="form-item">
          <view class="form-label">客队中文名 *</view>
          <input 
            v-model="formData.away_team_name" 
            placeholder="如: 金州勇士" 
            class="form-input"
            @blur="autoFillTeamLogo(formData.away_team_name, false)" />
        </view>

        <view class="form-item">
          <view class="form-label">客队英文缩写（自动生成）</view>
          <input v-model="formData.away_team_logo" placeholder="自动生成或手动输入" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">客队得分</view>
          <input v-model.number="formData.away_team_score" type="number" placeholder="请输入得分" class="form-input" />
        </view>
      </view>

      <view class="form-section">
        <view class="section-title">比赛状态</view>
        
        <view class="form-item">
          <picker :value="statusIndex" :range="statusOptions" range-key="label" @change="onStatusChange">
            <view class="picker-input">{{ statusOptions[statusIndex] ? statusOptions[statusIndex].label : '请选择状态' }}</view>
          </picker>
        </view>
      </view>
    </view>

    <view class="footer-btns">
      <view class="btn cancel-btn" @click="goBack">取消</view>
      <view class="btn submit-btn" @click="submitMatch">{{ isEdit ? '保存' : '添加' }}</view>
    </view>
  </view>
</template>

<script>
import { addMatch, updateMatch, getMatchDetail } from '@/api/match'

export default {
  data() {
    return {
      isEdit: false,
      matchId: null,
      formData: {
        match_date: '',
        match_time: '',
        home_team_name: '',
        home_team_logo: '',
        home_team_score: 0,
        away_team_name: '',
        away_team_logo: '',
        away_team_score: 0,
        status: 'upcoming'
      },
      statusOptions: [
        { value: 'upcoming', label: '未开始' },
        { value: 'live', label: '进行中' },
        { value: 'finished', label: '已结束' }
      ],
      statusIndex: 0,
      // NBA球队中英文对照表
      teamMap: {
        '洛杉矶湖人': 'LAL',
        '金州勇士': 'GSW',
        '芝加哥公牛': 'CHI',
        '迈阿密热火': 'MIA',
        '波士顿凯尔特人': 'BOS',
        '布鲁克林篮网': 'BKN',
        '纽约尼克斯': 'NYK',
        '费城76人': 'PHI',
        '多伦多猛龙': 'TOR',
        '密尔沃基雄鹿': 'MIL',
        '克利夫兰骑士': 'CLE',
        '印第安纳步行者': 'IND',
        '底特律活塞': 'DET',
        '华盛顿奇才': 'WAS',
        '夏洛特黄蜂': 'CHA',
        '亚特兰大老鹰': 'ATL',
        '奥兰多魔术': 'ORL',
        '达拉斯独行侠': 'DAL',
        '休斯顿火箭': 'HOU',
        '孟菲斯灰熊': 'MEM',
        '新奥尔良鹈鹕': 'NOP',
        '圣安东尼奥马刺': 'SAS',
        '丹佛掘金': 'DEN',
        '明尼苏达森林狼': 'MIN',
        '俄克拉荷马城雷霆': 'OKC',
        '波特兰开拓者': 'POR',
        '犹他爵士': 'UTA',
        '菲尼克斯太阳': 'PHX',
        '洛杉矶快船': 'LAC',
        '萨克拉门托国王': 'SAC'
      }
    }
  },
  onLoad(options) {
    if (options.id) {
      this.isEdit = true
      this.matchId = options.id
      this.loadMatchDetail()
    } else {
      // 默认设置今天的日期
      const today = new Date()
      this.formData.match_date = this.formatDate(today)
    }
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    // 自动生成英文缩写
    autoFillTeamLogo(teamName, isHome) {
      if (this.teamMap[teamName]) {
        if (isHome) {
          this.formData.home_team_logo = this.teamMap[teamName]
        } else {
          this.formData.away_team_logo = this.teamMap[teamName]
        }
      }
    },
    loadMatchDetail() {
      uni.showLoading({ title: '加载中...' })
      
      getMatchDetail(this.matchId).then(res => {
        if (res.code === 200) {
          const data = res.data
          // 确保status是正确的值
          if (!['upcoming', 'live', 'finished'].includes(data.status)) {
            data.status = 'upcoming'
          }
          this.formData = data
          // 设置状态选择器的索引
          this.statusIndex = this.statusOptions.findIndex(item => item.value === data.status)
          if (this.statusIndex === -1) {
            this.statusIndex = 0
          }
        }
      }).catch(err => {
        console.error('加载比赛详情失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    onDateChange(e) {
      this.formData.match_date = e.detail.value
    },
    onTimeChange(e) {
      this.formData.match_time = e.detail.value
    },
    onStatusChange(e) {
      this.statusIndex = e.detail.value
      this.formData.status = this.statusOptions[e.detail.value].value
    },
    submitMatch() {
      if (!this.formData.match_date) {
        uni.showToast({ title: '请选择比赛日期', icon: 'none' })
        return
      }
      
      if (!this.formData.home_team_name) {
        uni.showToast({ title: '请填写主队名称', icon: 'none' })
        return
      }
      
      if (!this.formData.away_team_name) {
        uni.showToast({ title: '请填写客队名称', icon: 'none' })
        return
      }
      
      // 如果没有填写英文缩写，使用中文名的前3个字符
      if (!this.formData.home_team_logo) {
        this.formData.home_team_logo = this.formData.home_team_name.substring(0, 3)
      }
      if (!this.formData.away_team_logo) {
        this.formData.away_team_logo = this.formData.away_team_name.substring(0, 3)
      }

      // 确保status是正确的值
      if (!['upcoming', 'live', 'finished'].includes(this.formData.status)) {
        this.formData.status = 'upcoming'
      }

      console.log('提交数据:', this.formData)
      
      uni.showLoading({ title: '提交中...' })
      
      const apiCall = this.isEdit 
        ? updateMatch(this.matchId, this.formData)
        : addMatch(this.formData)
      
      apiCall.then(res => {
        console.log('提交响应:', res)
        if (res.code === 200) {
          uni.showToast({ 
            title: this.isEdit ? '更新成功' : '添加成功', 
            icon: 'success' 
          })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
        } else {
          console.error('提交失败，返回码不是200:', res)
          uni.showToast({ 
            title: res.message || '提交失败', 
            icon: 'none',
            duration: 3000
          })
        }
      }).catch(err => {
        console.error('提交失败', err)
        uni.showToast({ title: '提交失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

.header {
  background-color: #fff;
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.form-container {
  padding: 20rpx;
}

.form-section {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 25rpx;
  padding-bottom: 15rpx;
  border-bottom: 2rpx solid #e74c3c;
}

.form-item {
  margin-bottom: 35rpx;
}

.form-item:last-child {
  margin-bottom: 0;
}

.form-label {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 18rpx;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 30rpx;
  background-color: #fff;
  box-sizing: border-box;
  min-height: 80rpx;
  line-height: 1.5;
}

.form-input:focus {
  border-color: #e74c3c;
}

.picker-input {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 30rpx;
  background-color: #fff;
  box-sizing: border-box;
  min-height: 80rpx;
  line-height: 1.5;
  color: #333;
}

.footer-btns {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background-color: #fff;
  padding: 20rpx;
  border-top: 1rpx solid #eee;
  gap: 20rpx;
}

.btn {
  flex: 1;
  padding: 25rpx 0;
  text-align: center;
  border-radius: 8rpx;
  font-size: 30rpx;
  font-weight: bold;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #666;
}

.submit-btn {
  background-color: #e74c3c;
  color: #fff;
}
</style>
