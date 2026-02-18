# NBA篮球数据咨询 - 后端API文档

## 项目概述
NBA篮球数据咨询是一个篮球资讯社区应用，专注于NBA比赛信息、新闻资讯、用户认证等功能。

---

## 1. 用户认证接口

### 1.1 用户登录
**请求方式：** POST  
**接口路径：** `/api/auth/login`  
**请求头：** Content-Type: application/json

**请求参数：**
```json
{
  "phone": "string (11位手机号，必填)",
  "smsCode": "string (4位短信验证码，必填)"
}
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "userId": "string (用户ID)",
    "phone": "string (手机号)",
    "token": "string (JWT token，用于后续请求认证)",
    "userName": "string (用户名，默认为手机号)"
  }
}
```

---

### 1.2 用户注册
**请求方式：** POST  
**接口路径：** `/api/auth/register`  
**请求头：** Content-Type: application/json

**请求参数：**
```json
{
  "phone": "string (11位手机号，必填)",
  "smsCode": "string (4位短信验证码，必填)",
  "password": "string (6-16位字母数字组合，必填)",
  "confirmPassword": "string (确认密码，必填)"
}
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "userId": "string (用户ID)",
    "phone": "string (手机号)",
    "token": "string (JWT token)",
    "userName": "string (用户名)"
  }
}
```

---

### 1.3 获取短信验证码
**请求方式：** POST  
**接口路径：** `/api/auth/sendSmsCode`  
**请求头：** Content-Type: application/json

**请求参数：**
```json
{
  "phone": "string (11位手机号，必填)"
}
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "验证码已发送",
  "data": {
    "expiresIn": 300
  }
}
```

---

## 2. NBA比赛接口

### 2.1 获取比赛列表
**请求方式：** GET  
**接口路径：** `/api/matches/list`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
date: string (日期，格式：YYYY-MM-DD，可选，默认今天)
page: number (分页页码，可选，默认1)
pageSize: number (每页数量，可选，默认10)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "total": 14,
    "page": 1,
    "pageSize": 10,
    "matches": [
      {
        "id": "string (比赛ID)",
        "date": "string (比赛日期，格式：2月12日)",
        "team1": {
          "id": "string (球队ID)",
          "name": "string (球队名称，如：快船)",
          "logo": "string (球队标识)",
          "score": 105
        },
        "team2": {
          "id": "string (球队ID)",
          "name": "string (球队名称，如：火箭)",
          "logo": "string (球队标识)",
          "score": 102
        },
        "viewers": "string (评分人数，如：17.6万)"
      }
    ]
  }
}
```

---

### 2.2 获取比赛详情
**请求方式：** GET  
**接口路径：** `/api/matches/{matchId}`  
**请求头：** Authorization: Bearer {token}

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "id": "string (比赛ID)",
    "date": "string (比赛日期)",
    "team1": {
      "id": "string",
      "name": "string",
      "logo": "string",
      "score": 105,
      "players": [
        {
          "id": "string",
          "name": "string",
          "number": 2,
          "points": 25,
          "rebounds": 8,
          "assists": 5
        }
      ]
    },
    "team2": {
      "id": "string",
      "name": "string",
      "logo": "string",
      "score": 102,
      "players": []
    },
    "status": "string (已结束/进行中/未开始)",
    "viewers": "string"
  }
}
```

---

## 3. 新闻资讯接口

### 3.1 获取新闻列表
**请求方式：** GET  
**接口路径：** `/api/news/list`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
page: number (分页页码，可选，默认1)
pageSize: number (每页数量，可选，默认10)
sort: string (排序方式：hot/new，可选，默认hot)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "total": 100,
    "page": 1,
    "pageSize": 10,
    "newsList": [
      {
        "id": "string (新闻ID)",
        "title": "string (新闻标题)",
        "content": "string (新闻摘要)",
        "image": "string (新闻配图URL)",
        "source": "string (新闻来源，如：虎扑篮球资讯)",
        "time": "string (发布时间，如：17分钟)",
        "comments": 64,
        "likes": 16,
        "shares": 5
      }
    ]
  }
}
```

---

### 3.2 获取新闻详情
**请求方式：** GET  
**接口路径：** `/api/news/{newsId}`  
**请求头：** Authorization: Bearer {token}

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "id": "string (新闻ID)",
    "title": "string (新闻标题)",
    "content": "string (完整新闻内容)",
    "image": "string (新闻配图URL)",
    "source": "string (新闻来源)",
    "sourceTime": "string (发布时间)",
    "comments": 64,
    "likes": 16,
    "shares": 5,
    "author": "string (作者)",
    "createTime": "string (创建时间，格式：YYYY-MM-DD HH:mm:ss)"
  }
}
```

---

### 3.3 点赞新闻
**请求方式：** POST  
**接口路径：** `/api/news/{newsId}/like`  
**请求头：** Authorization: Bearer {token}

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "点赞成功",
  "data": {
    "likes": 17
  }
}
```

---

### 3.4 取消点赞新闻
**请求方式：** DELETE  
**接口路径：** `/api/news/{newsId}/like`  
**请求头：** Authorization: Bearer {token}

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "取消点赞成功",
  "data": {
    "likes": 16
  }
}
```

---

## 4. NBA排行榜接口

### 4.1 获取球队排行榜
**请求方式：** GET  
**接口路径：** `/api/rankings/teams`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
season: string (赛季，可选，默认当前赛季)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "season": "2025-26",
    "teams": [
      {
        "rank": 1,
        "teamId": "string",
        "teamName": "string",
        "wins": 38,
        "losses": 2,
        "winRate": "95.0%",
        "pointsFor": 115.2,
        "pointsAgainst": 108.5
      }
    ]
  }
}
```

---

### 4.2 获取球员排行榜
**请求方式：** GET  
**接口路径：** `/api/rankings/players`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
stat: string (统计类型：points/rebounds/assists/steals/blocks，必填)
season: string (赛季，可选，默认当前赛季)
page: number (分页页码，可选，默认1)
pageSize: number (每页数量，可选，默认10)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "season": "2025-26",
    "stat": "points",
    "players": [
      {
        "rank": 1,
        "playerId": "string",
        "playerName": "string",
        "teamName": "string",
        "value": 23.5,
        "games": 40
      }
    ]
  }
}
```

---

## 5. 用户信息接口

### 5.1 获取用户信息
**请求方式：** GET  
**接口路径：** `/api/user/profile`  
**请求头：** Authorization: Bearer {token}

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "userId": "string",
    "phone": "string",
    "userName": "string",
    "avatar": "string (头像URL，可选)",
    "createTime": "string (注册时间)"
  }
}
```

---

### 5.2 更新用户信息
**请求方式：** PUT  
**接口路径：** `/api/user/profile`  
**请求头：** Authorization: Bearer {token}, Content-Type: application/json

**请求参数：**
```json
{
  "userName": "string (用户名，可选)",
  "avatar": "string (头像URL，可选)"
}
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "userId": "string",
    "userName": "string",
    "avatar": "string"
  }
}
```

---

### 5.3 修改密码
**请求方式：** POST  
**接口路径：** `/api/user/changePassword`  
**请求头：** Authorization: Bearer {token}, Content-Type: application/json

**请求参数：**
```json
{
  "oldPassword": "string (旧密码，必填)",
  "newPassword": "string (新密码，6-16位字母数字组合，必填)"
}
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "密码修改成功"
}
```

---

## 6. 搜索接口

### 6.1 搜索新闻
**请求方式：** GET  
**接口路径：** `/api/search/news`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
keyword: string (搜索关键词，必填)
page: number (分页页码，可选，默认1)
pageSize: number (每页数量，可选，默认10)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "搜索成功",
  "data": {
    "total": 50,
    "page": 1,
    "pageSize": 10,
    "results": [
      {
        "id": "string",
        "title": "string",
        "content": "string",
        "image": "string",
        "source": "string",
        "time": "string"
      }
    ]
  }
}
```

---

### 6.2 搜索球队
**请求方式：** GET  
**接口路径：** `/api/search/teams`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
keyword: string (搜索关键词，必填)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "搜索成功",
  "data": {
    "results": [
      {
        "id": "string",
        "name": "string",
        "logo": "string"
      }
    ]
  }
}
```

---

### 6.3 搜索球员
**请求方式：** GET  
**接口路径：** `/api/search/players`  
**请求头：** Authorization: Bearer {token}

**请求参数：**
```
keyword: string (搜索关键词，必填)
```

**响应成功 (200)：**
```json
{
  "code": 0,
  "message": "搜索成功",
  "data": {
    "results": [
      {
        "id": "string",
        "name": "string",
        "number": 2,
        "teamName": "string",
        "position": "string"
      }
    ]
  }
}
```

---

## 7. 通用响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "string (成功消息)",
  "data": {} (具体数据)
}
```

### 失败响应
```json
{
  "code": 1,
  "message": "string (错误消息)"
}
```

### 错误码说明
- 0: 成功
- 1: 通用错误
- 400: 请求参数错误
- 401: 未授权（token过期或无效）
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器错误

---

## 8. 认证说明

### Token使用
所有需要认证的接口都需要在请求头中添加：
```
Authorization: Bearer {token}
```

### Token过期处理
- Token过期时返回401错误
- 前端需要重新登录获取新的token
- 建议token有效期设置为7天

---

## 9. 分页说明

所有列表接口都支持分页，参数如下：
- `page`: 页码（从1开始）
- `pageSize`: 每页数量（建议默认10，最大100）

响应中包含：
- `total`: 总数
- `page`: 当前页码
- `pageSize`: 每页数量

---

## 10. 时间格式说明

- 日期格式：`YYYY-MM-DD`
- 时间格式：`YYYY-MM-DD HH:mm:ss`
- 相对时间：`17分钟`、`2小时`、`3天`等

---

## 11. 接口总数

- 认证接口：3个
- 比赛接口：2个
- 新闻接口：4个
- 排行榜接口：2个
- 用户接口：3个
- 搜索接口：3个
- **总计：17个接口**

---

## 12. 开发建议

1. **数据库设计**
   - 用户表：userId, phone, password, userName, avatar, createTime, updateTime
   - 比赛表：matchId, date, team1Id, team2Id, team1Score, team2Score, status, viewers
   - 新闻表：newsId, title, content, image, source, comments, likes, shares, createTime
   - 排行榜表：根据season存储球队和球员数据

2. **安全建议**
   - 使用JWT进行token认证
   - 密码使用bcrypt加密存储
   - 实现请求频率限制（如：60秒内最多发送3次验证码）
   - 验证码有效期设置为5分钟

3. **性能优化**
   - 对热门数据进行缓存（如：排行榜、热门新闻）
   - 使用数据库索引优化查询性能
   - 实现异步任务处理（如：发送短信）

4. **日志记录**
   - 记录所有API调用
   - 记录用户登录/注册行为
   - 记录错误信息便于调试
