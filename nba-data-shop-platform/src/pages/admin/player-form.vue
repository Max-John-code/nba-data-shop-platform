<template>
  <view class="container">
    <view class="header">
      <view class="title">{{ isEdit ? '编辑球员' : '添加球员' }}</view>
    </view>

    <view class="form-container">
      <view class="form-section">
        <view class="section-title">基本信息</view>
        
        <view class="form-item">
          <view class="form-label">球员头像</view>
          <view class="avatar-upload" @click="choosePlayerAvatar">
            <image v-if="formData.avatar" :src="formData.avatar" mode="aspectFill" class="upload-avatar" />
            <view v-else class="upload-placeholder">
              <text class="upload-icon">📷</text>
              <text class="upload-text">点击上传头像</text>
            </view>
          </view>
        </view>

        <view class="form-item">
          <view class="form-label">球员姓名 *</view>
          <input v-model="formData.name" placeholder="请输入球员姓名" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">排名（前3名需填写）</view>
          <input v-model.number="formData.ranking" type="number" placeholder="1-3为前三名，其他可不填" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">所属球队</view>
          <input v-model="formData.team" placeholder="请输入所属球队" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">位置</view>
          <input v-model="formData.position" placeholder="如: 控球后卫" class="form-input" />
        </view>
      </view>

      <view class="form-section">
        <view class="section-title">数据统计</view>
        
        <view class="form-item">
          <view class="form-label">场均得分</view>
          <input v-model.number="formData.points_per_game" type="digit" placeholder="请输入场均得分" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">场均篮板</view>
          <input v-model.number="formData.rebounds_per_game" type="digit" placeholder="请输入场均篮板" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">场均助攻</view>
          <input v-model.number="formData.assists_per_game" type="digit" placeholder="请输入场均助攻" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">场均抢断</view>
          <input v-model.number="formData.steals_per_game" type="digit" placeholder="请输入场均抢断" class="form-input" />
        </view>

        <view class="form-item">
          <view class="form-label">场均盖帽</view>
          <input v-model.number="formData.blocks_per_game" type="digit" placeholder="请输入场均盖帽" class="form-input" />
        </view>
      </view>
    </view>

    <view class="footer-btns">
      <view class="btn cancel-btn" @click="goBack">取消</view>
      <view class="btn submit-btn" @click="submitPlayer">{{ isEdit ? '保存' : '添加' }}</view>
    </view>
  </view>
</template>

<script>
import { addPlayer, updatePlayer, getPlayerDetail } from '@/api/player'

export default {
  data() {
    return {
      isEdit: false,
      playerId: null,
      formData: {
        name: '',
        team: '',
        position: '',
        avatar: '',
        player_type: 'ranking',
        ranking: 0,
        points_per_game: 0,
        rebounds_per_game: 0,
        assists_per_game: 0,
        steals_per_game: 0,
        blocks_per_game: 0
      }
    }
  },
  onLoad(options) {
    if (options.id) {
      this.isEdit = true
      this.playerId = options.id
      this.loadPlayerDetail()
    }
  },
  methods: {
    loadPlayerDetail() {
      uni.showLoading({ title: '加载中...' })
      
      getPlayerDetail(this.playerId).then(res => {
        if (res.code === 200) {
          this.formData = res.data
          this.formData.player_type = 'ranking'
        }
      }).catch(err => {
        console.error('加载球员详情失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    choosePlayerAvatar() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        success: (res) => {
          const tempFilePath = res.tempFilePaths[0]
          
          // H5环境转base64
          // #ifdef H5
          this.convertToBase64H5(tempFilePath)
          // #endif
          
          // 非H5环境
          // #ifndef H5
          this.convertToBase64(tempFilePath)
          // #endif
        }
      })
    },
    convertToBase64H5(blobUrl) {
      const xhr = new XMLHttpRequest()
      xhr.open('GET', blobUrl, true)
      xhr.responseType = 'blob'
      
      xhr.onload = () => {
        if (xhr.status === 200) {
          const blob = xhr.response
          const reader = new FileReader()
          
          reader.onloadend = () => {
            this.formData.avatar = reader.result
          }
          
          reader.readAsDataURL(blob)
        }
      }
      
      xhr.send()
    },
    convertToBase64(filePath) {
      uni.getFileSystemManager().readFile({
        filePath: filePath,
        encoding: 'base64',
        success: (fileRes) => {
          this.formData.avatar = 'data:image/jpeg;base64,' + fileRes.data
        }
      })
    },
    submitPlayer() {
      if (!this.formData.name) {
        uni.showToast({ title: '请输入球员姓名', icon: 'none' })
        return
      }
      
      // 排名不是必填，但如果填了需要验证范围
      if (this.formData.ranking && (this.formData.ranking < 0 || this.formData.ranking > 999)) {
        uni.showToast({ title: '排名范围应在0-999之间', icon: 'none' })
        return
      }
      
      // 如果没有填写排名，设置为0
      if (!this.formData.ranking) {
        this.formData.ranking = 0
      }
      
      uni.showLoading({ title: '提交中...' })
      
      const apiCall = this.isEdit 
        ? updatePlayer(this.playerId, this.formData)
        : addPlayer(this.formData)
      
      apiCall.then(res => {
        if (res.code === 200) {
          uni.showToast({ 
            title: this.isEdit ? '更新成功' : '添加成功', 
            icon: 'success' 
          })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
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

.avatar-upload {
  width: 200rpx;
  height: 200rpx;
  border-radius: 12rpx;
  border: 2rpx dashed #ddd;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #fafafa;
}

.upload-avatar {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10rpx;
}

.upload-icon {
  font-size: 60rpx;
}

.upload-text {
  font-size: 24rpx;
  color: #999;
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
