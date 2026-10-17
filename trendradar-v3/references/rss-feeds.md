# RSS 订阅源配置参考

## 配置位置

`config/config.yaml` 的 `rss.feeds` 部分

## 基本语法

```yaml
rss:
  enabled: true
  freshness_filter:
    enabled: true
    max_age_days: 1        # 只推送 1 天内的文章
  
  feeds:
    - id: "source-id"      # 唯一标识
      name: "显示名称"
      url: "https://example.com/feed.xml"
      enabled: true        # 可选，默认 true
      max_age_days: 7      # 可选，覆盖全局设置
```

## 推荐的 RSS 源

### 科技类

| 名称 | 地址 |
|------|------|
| Hacker News | `https://hnrss.org/frontpage` |
| TechCrunch | `https://techcrunch.com/feed/` |
| 36氪 | `https://36kr.com/feed` |
| InfoQ | `https://www.infoq.cn/feed` |
| 少数派 | `https://sspai.com/feed` |
| V2EX | `https://www.v2ex.com/index.xml` |

### 财经类

| 名称 | 地址 |
|------|------|
| 华尔街日报市场 | `https://feeds.a.dj.com/rss/RSSMarketsMain.xml` |
| 金融时报 | `https://www.ft.com/rss/home` |
| 雅虎财经 | `https://finance.yahoo.com/news/rssindex` |

### 博客类

| 名称 | 地址 |
|------|------|
| 阮一峰的网络日志 | `http://www.ruanyifeng.com/blog/atom.xml` |
| 酷壳 | `https://coolshell.cn/feed` |

## RSS 源合集

| 合集名称 | 地址 |
|----------|------|
| awesome-tech-rss | https://github.com/readings/awesome-tech-rss |
| awesome-rss-feeds | https://github.com/unixorn/awesome-rss-feeds |

## 新鲜度过滤

```yaml
freshness_filter:
  enabled: true
  max_age_days: 1    # 全局默认
```

**过滤逻辑：**
- 文章发布时间超过 N 天则不推送
- 无发布时间的文章会被保留
- 所有文章都会存入数据库（AI 查询仍可访问）

## 多源配置示例

```yaml
feeds:
  - id: "hacker-news"
    name: "Hacker News"
    url: "https://hnrss.org/frontpage"
  
  - id: "36kr"
    name: "36氪"
    url: "https://36kr.com/feed"
  
  - id: "wsj-markets"
    name: "华尔街日报市场"
    url: "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
  
  - id: "personal-blog"
    name: "个人博客"
    url: "https://example.com/feed.xml"
    max_age_days: 7    # 博客更新慢，允许 7 天内的文章
```
