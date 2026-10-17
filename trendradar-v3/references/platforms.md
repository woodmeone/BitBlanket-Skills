# 热榜平台配置参考

数据来源：[newsnow](https://github.com/ourongxing/newsnow) 公开 API

## 当前配置（11个）

| 平台 | ID | 说明 |
|------|-----|------|
| 今日头条 | `toutiao` | 综合新闻 |
| 百度热搜 | `baidu` | 搜索热点 |
| 微博 | `weibo` | 社交热点 |
| 知乎 | `zhihu` | 问答社区 |
| 抖音 | `douyin` | 短视频热点 |
| bilibili热搜 | `bilibili-hot-search` | 视频社区 |
| 贴吧 | `tieba` | 百度贴吧 |
| 华尔街见闻 | `wallstreetcn-hot` | 财经资讯 |
| 财联社热门 | `cls-hot` | 金融快讯 |
| 澎湃新闻 | `thepaper` | 深度报道 |
| 凤凰网 | `ifeng` | 综合门户 |

## 所有支持的平台

### 综合新闻类

| 平台 | ID | 说明 |
|------|-----|------|
| 今日头条 | `toutiao` | 综合新闻 |
| 百度热搜 | `baidu` | 搜索热点 |
| 微博 | `weibo` | 社交热点 |
| 知乎 | `zhihu` | 问答社区 |
| 贴吧 | `tieba` | 百度贴吧 |
| 抖音 | `douyin` | 短视频热点 |
| bilibili热搜 | `bilibili-hot-search` | 视频社区 |
| 快手 | `kuaishou` | 短视频 |
| 小红书 | `xiaohongshu` | 生活分享 |
| 凤凰网 | `ifeng` | 综合门户 |
| 澎湃新闻 | `thepaper` | 深度报道 |
| 网易新闻 | `netease-news` | 综合门户 |
| 搜狐新闻 | `sohu-news` | 综合门户 |
| 新浪新闻 | `sina-news` | 综合门户 |

### 财经金融类

| 平台 | ID | 说明 |
|------|-----|------|
| 华尔街见闻 | `wallstreetcn-hot` | 财经资讯 |
| 财联社热门 | `cls-hot` | 金融快讯 |
| 东方财富 | `eastmoney` | 股票财经 |
| 同花顺 | `10jqka` | 股票财经 |
| 雪球 | `xueqiu` | 投资社区 |
| 富途牛牛 | `futu` | 港美股 |
| 虎嗅 | `huxiu` | 商业科技 |

### 科技互联网类

| 平台 | ID | 说明 |
|------|-----|------|
| 36氪 | `36kr` | 科技创业 |
| 少数派 | `sspai` | 数码生活 |
| IT之家 | `ithome` | 科技资讯 |
| 掘金 | `juejin` | 开发者社区 |
| V2EX | `v2ex` | 技术社区 |
| CSDN | `csdn` | 开发者社区 |
| 开源中国 | `oschina` | 开源资讯 |

### 其他平台

| 平台 | ID | 说明 |
|------|-----|------|
| 豆瓣电影 | `douban-movie` | 影视评分 |
| 猫眼电影 | `maoyan` | 电影票房 |
| 懂球帝 | `dongqiudi` | 体育足球 |
| 虎扑 | `hupu` | 体育社区 |

## 配置示例

```yaml
platforms:
  enabled: true
  sources:
    - id: "toutiao"
      name: "今日头条"
    - id: "baidu"
      name: "百度热搜"
    - id: "weibo"
      name: "微博"
    # 添加更多...
```

## 注意事项

- 建议选择 10-15 个核心平台
- 过多平台会导致信息过载
- 部分平台可能因 API 变更暂时不可用
