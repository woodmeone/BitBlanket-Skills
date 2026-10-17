---
name: trendradar-v3
description: "热点新闻聚合与分析工具 v3.0。核心功能：(1) 基于账号定位自动配置关键词筛选 (2) 抓取多平台热榜新闻（30+平台）(3) 管理 RSS 订阅源 (4) 生成热点趋势报告 (5) 推送通知到多渠道 (6) 导出 JSON 数据。支持双路径输出：调用方项目 TrendRadarData 文件夹 + TrendRadar 项目 output 文件夹。触发场景：用户提到\"热点新闻\"、\"热榜\"、\"RSS订阅\"、\"新闻聚合\"、\"TrendRadar\"、\"账号定位\"、\"关键词筛选\"或需要查看/配置/导出新闻相关内容时。"
---

# TrendRadar Skill v3.0

热点新闻聚合与分析工具，支持**智能定位配置**、30+ 平台热榜抓取、RSS 订阅、AI 智能筛选、多渠道推送和数据导出。

## 🆕 v3.0 核心更新：智能定位配置

**根据账号定位自动生成关键词配置，实现精准数据筛选！**

```
工作流：账号定位 → 自动生成关键词 → 修改配置文件 → 抓取筛选后数据
```

### 可用定位模板

| 定位 | 说明 |
|------|------|
| AI实战成长博主 | AI工具教程、开源项目实战 |
| 科技数码博主 | 数码评测、科技资讯 |
| 财经投资博主 | 投资理财、市场分析 |
| 职场成长博主 | 职场技能、效率提升 |
| 编程技术博主 | 编程技术、开发教程 |
| 自媒体运营博主 | 运营技巧、平台规则 |

详见 [references/positioning-keywords.md](references/positioning-keywords.md)

## ⚠️ 重要：双路径输出机制

**每次调用时，AI 必须自动获取当前工作目录，并将其作为调用方路径传递给脚本。**

### 🔴 核心原则：双路径输出

**所有数据必须同时输出到两个位置，缺一不可：**

| 位置 | 路径 | 说明 |
|------|------|------|
| TrendRadar 项目 | `{TRENDRADAR_PROJECT_PATH}/output/` | 始终输出 |
| 调用方项目 | `{当前工作目录}/TrendRadarData/` | 始终输出 |

**AI 必须验证**：执行完成后，检查两个位置是否都生成了文件！

### AI 调用规范

**AI 在执行任何操作时，必须：**
1. 获取当前工作目录（从 `<env>` 中的 `Working directories` 获取）
2. 将该路径通过 `--caller-path` 参数传递给脚本
3. **Windows 环境**：必须设置 UTF-8 编码
4. **执行完成后验证**：检查 `{当前工作目录}/TrendRadarData/` 文件夹是否已创建并包含数据文件

## 前置条件

确保 TrendRadar 项目已安装：

```bash
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar
pip install -r requirements.txt
```

**默认项目路径**：`D:\Project\TrendingRadar`

## 快速开始

### 方式一：智能定位运行（推荐）

根据账号定位自动配置关键词，然后抓取数据：

```powershell
# Windows PowerShell（必须设置 UTF-8 编码）
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python "{skill_path}/scripts/run.py" --caller-path "d:\makeskill\test" --positioning "AI实战成长博主"
```

### 方式二：自定义关键词运行

使用自定义关键词（逗号分隔）：

```powershell
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python "{skill_path}/scripts/run.py" --caller-path "d:\makeskill\test" --keywords "AI,ChatGPT,DeepSeek,开源"
```

### 方式三：使用现有配置运行

不修改配置，直接运行：

```powershell
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python "{skill_path}/scripts/run.py" --caller-path "d:\makeskill\test"
```

### 方式四：分步执行

```powershell
# 步骤1: 配置关键词（可选）
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python "{skill_path}/scripts/config_keywords.py" --positioning "AI实战成长博主"

# 步骤2: 运行数据抓取
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python -m trendradar

# 步骤3: 导出数据到双路径
$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; python "{skill_path}/scripts/export_data.py" --caller-path "d:\makeskill\test"
```

## 脚本说明

### run.py - 一键运行脚本 v3.0

```powershell
# 完整流程：配置关键词 + 抓取 + 导出 + 验证
python scripts/run.py --caller-path "d:\makeskill\test" --positioning "AI实战成长博主"

# 使用自定义关键词
python scripts/run.py --caller-path "d:\makeskill\test" --keywords "AI,ChatGPT"

# 仅导出（已有数据时使用）
python scripts/run.py --caller-path "d:\makeskill\test" --export-only

# 跳过关键词配置
python scripts/run.py --caller-path "d:\makeskill\test" --skip-config

# 指定日期
python scripts/run.py --caller-path "d:\makeskill\test" --date 2026-03-22

# 列出所有可用定位
python scripts/run.py --caller-path "d:\makeskill\test" --list-positionings
```

### config_keywords.py - 关键词配置脚本

```powershell
# 使用预设定位模板
python scripts/config_keywords.py --positioning "AI实战成长博主"

# 使用自定义关键词
python scripts/config_keywords.py --keywords "AI,ChatGPT,DeepSeek"

# 列出所有可用定位
python scripts/config_keywords.py --list

# 查看当前配置
python scripts/config_keywords.py --show-config

# 指定 TrendRadar 路径
python scripts/config_keywords.py --positioning "AI实战成长博主" --trendradar-path "D:\Project\TrendingRadar"
```

### export_data.py - 数据导出

```powershell
# 导出今天的数据
python scripts/export_data.py --caller-path "d:\makeskill\test"

# 导出指定日期
python scripts/export_data.py --caller-path "d:\makeskill\test" --date 2026-03-22

# 导出所有可用日期
python scripts/export_data.py --caller-path "d:\makeskill\test" --all

# 查看可用日期（无需 --caller-path）
python scripts/export_data.py --dates
```

**输出文件命名**：
- 热榜数据：`RadarHotTrending{YYYY-MM-DD}.json`
- RSS 数据：`RadarRSS{YYYY-MM-DD}.json`

## 输出结构

**调用方项目**：
```
{当前工作目录}/
└── TrendRadarData/
    ├── RadarHotTrending2026-03-22.json
    └── RadarRSS2026-03-22.json
```

**TrendRadar 项目**：
```
{TRENDRADAR_PROJECT_PATH}/
└── output/
    ├── html/
    ├── json/
    │   ├── RadarHotTrending2026-03-22.json
    │   └── RadarRSS2026-03-22.json
    └── index.html
```

## 核心功能

### 1. 智能定位配置（v3.0 新增）

根据账号定位自动生成关键词配置，实现精准数据筛选。

**工作流**：
1. 用户提供账号定位
2. AI 分析定位，匹配预设模板或生成关键词
3. 自动修改 `frequency_words.txt`
4. 运行 TrendRadar 抓取数据
5. 返回筛选后的精准内容

详见 [references/positioning-keywords.md](references/positioning-keywords.md)

### 2. 热榜抓取

支持 30+ 平台，详见 [references/platforms.md](references/platforms.md)

**当前默认配置（11个）**：今日头条、百度热搜、微博、知乎、抖音、bilibili、贴吧、华尔街见闻、财联社、澎湃新闻、凤凰网

### 3. RSS 订阅

配置文件：`config/config.yaml` 的 `rss.feeds` 部分

详见 [references/rss-feeds.md](references/rss-feeds.md)

### 4. 关键词筛选

配置文件：`config/frequency_words.txt`

详见 [references/keywords-syntax.md](references/keywords-syntax.md)

### 5. AI 智能筛选

配置文件：`config/ai_interests.txt`

启用方式：
```yaml
filter:
  method: "ai"
```

### 6. 推送通知

支持企业微信、飞书、Telegram、邮件、Bark、Slack 等渠道。

## 配置文件速查

| 文件 | 用途 |
|------|------|
| `config/config.yaml` | 主配置 |
| `config/frequency_words.txt` | 关键词配置 |
| `config/ai_interests.txt` | AI 兴趣描述 |
| `config/timeline.yaml` | 调度配置 |

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| AI 分析失败 | 检查 `ai.api_key` 配置 |
| 无推送通知 | 检查通知渠道配置 |
| 数据为空 | 检查网络连接 |
| 关键词不匹配 | 检查 `frequency_words.txt` 语法 |
| 路径错误 | 检查 `TRENDRADAR_PROJECT_PATH` 环境变量 |
| 双路径输出失败 | 确保 `--caller-path` 参数正确传入 |
| Windows UnicodeEncodeError | 在命令前设置 `$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8;` |
| 定位模板不匹配 | 使用 `--list-positionings` 查看可用定位，或使用 `--keywords` 自定义 |

## 参考资料

- [账号定位关键词模板](references/positioning-keywords.md) - 预设定位模板和自定义语法
- [平台列表](references/platforms.md) - 所有支持的热榜平台
- [关键词语法](references/keywords-syntax.md) - 关键词配置语法
- [RSS 订阅源](references/rss-feeds.md) - RSS 配置参考
- [配置模板](assets/config-template.yaml) - 完整配置模板

## v3.0 更新日志

1. **新增智能定位配置**：根据账号定位自动生成关键词配置
2. **新增预设定位模板**：6种常见账号定位模板开箱即用
3. **新增自定义关键词支持**：通过 `--keywords` 参数快速配置
4. **优化工作流**：配置 → 抓取 → 导出 一条龙
5. **自动备份原配置**：修改关键词配置时自动备份
