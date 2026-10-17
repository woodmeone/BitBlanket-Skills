#!/usr/bin/env python3
"""
TrendRadar 关键词配置脚本 v3.0
根据账号定位自动生成关键词配置，实现精准数据筛选

使用方法:
    python config_keywords.py --positioning "AI实战成长博主"
    python config_keywords.py --positioning "AI实战成长博主" --trendradar-path "D:\\Project\\TrendingRadar"
    python config_keywords.py --keywords "AI,ChatGPT,DeepSeek,开源" --trendradar-path "D:\\Project\\TrendingRadar"
    python config_keywords.py --show-config
"""
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

POSITIONING_KEYWORDS_MAP = {
    "AI实战成长博主": {
        "description": "专注分享AI工具使用教程、开源项目实战，目标受众：想学习AI应用的开发者和职场人",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "标题党",
            "广告",
            "营销",
            "",
            "[WORD_GROUPS]",
            "",
            "# AI 工具与模型",
            "/\\bai\\b|人工智能|机器学习|深度学习/ => AI技术",
            "/ChatGPT|GPT-4|OpenAI|Claude|Gemini|大模型/ => 大语言模型",
            "/DeepSeek|深度求索|幻方量化/ => DeepSeek",
            "/Midjourney|Stable Diffusion|DALL-E|文生图/ => AI绘画",
            "/Copilot|Cursor|代码助手|编程AI/ => AI编程",
            "",
            "# AI 应用场景",
            "[AI应用]",
            "AI工具",
            "AI办公",
            "AI写作",
            "AI视频",
            "/RAG|知识库|智能问答/ => RAG应用",
            "/Agent|智能体|自动化/ => AI Agent",
            "",
            "# 开源项目",
            "[开源项目]",
            "/GitHub|开源|开源项目/",
            "LLM",
            "微调",
            "部署",
            "@10",
            "",
            "# 科技公司动态",
            "/华为|鸿蒙|任正非|余承东/ => 华为",
            "/苹果|Apple|库克|iPhone/ => 苹果",
            "/特斯拉|Tesla|马斯克/ => 特斯拉",
            "/字节|抖音|TikTok|张一鸣/ => 字节跳动",
            "/阿里|阿里巴巴|马云|淘宝/ => 阿里",
            "/腾讯|微信|马化腾/ => 腾讯",
        ]
    },
    "科技数码博主": {
        "description": "分享数码产品评测、科技资讯、新品发布，目标受众：科技爱好者",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "标题党",
            "",
            "[WORD_GROUPS]",
            "",
            "# 手机数码",
            "/iPhone|苹果手机|iOS/ => iPhone",
            "/华为手机|Mate|Pura|鸿蒙手机/ => 华为手机",
            "/小米|Redmi|雷军/ => 小米",
            "/OPPO|vivo|一加/ => OV系",
            "/三星|Samsung|Galaxy/ => 三星",
            "",
            "# 电脑硬件",
            "[电脑硬件]",
            "/显卡|GPU|RTX|RX/ => 显卡",
            "/CPU|处理器|Intel|AMD/ => 处理器",
            "/内存|SSD|硬盘/ => 存储",
            "笔记本",
            "台式机",
            "",
            "# 科技公司",
            "/苹果|Apple|库克/ => 苹果",
            "/微软|Microsoft|Windows/ => 微软",
            "/谷歌|Google|Android/ => 谷歌",
        ]
    },
    "财经投资博主": {
        "description": "分享投资理财知识、市场分析、财经资讯，目标受众：投资者和理财人群",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "标题党",
            "广告",
            "",
            "[WORD_GROUPS]",
            "",
            "# A股市场",
            "/A股|股市|上证|深证|创业板/ => A股",
            "/涨停|跌停|大盘|指数/ => 股市动态",
            "",
            "# 行业板块",
            "[热门板块]",
            "/新能源|锂电|光伏|储能/ => 新能源",
            "/半导体|芯片|光刻机/ => 半导体",
            "/AI|人工智能|算力/ => AI概念",
            "/医药|医疗|创新药/ => 医药",
            "",
            "# 宏观经济",
            "[宏观经济]",
            "美联储",
            "利率",
            "通胀",
            "GDP",
            "央行",
            "",
            "# 财经资讯源",
            "/华尔街见闻|财联社|澎湃财经/ => 财经资讯",
        ]
    },
    "职场成长博主": {
        "description": "分享职场技能、职业发展、效率提升，目标受众：职场人士",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "标题党",
            "",
            "[WORD_GROUPS]",
            "",
            "# 职场技能",
            "[职场技能]",
            "职场",
            "面试",
            "简历",
            "升职",
            "加薪",
            "跳槽",
            "",
            "# 效率工具",
            "[效率工具]",
            "/Notion|Obsidian|笔记软件/ => 效率工具",
            "/Excel|PPT|Word|Office/ => 办公软件",
            "时间管理",
            "GTD",
            "",
            "# 职业发展",
            "[职业发展]",
            "职业规划",
            "副业",
            "自由职业",
            "远程办公",
        ]
    },
    "编程技术博主": {
        "description": "分享编程技术、开发教程、技术趋势，目标受众：开发者",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "标题党",
            "",
            "[WORD_GROUPS]",
            "",
            "# 编程语言",
            "/Python|python/ => Python",
            "/JavaScript|TypeScript|JS|TS/ => JavaScript",
            "/Java|java|JVM/ => Java",
            "/Go|Golang/ => Go",
            "/Rust|rust/ => Rust",
            "",
            "# 前端技术",
            "[前端]",
            "/React|Vue|Angular/ => 前端框架",
            "/CSS|HTML|前端/ => 前端基础",
            "",
            "# 后端技术",
            "[后端]",
            "/微服务|分布式|架构/ => 架构",
            "/数据库|MySQL|PostgreSQL|Redis/ => 数据库",
            "/Docker|K8s|容器|Kubernetes/ => 容器",
            "",
            "# 开发工具",
            "[开发工具]",
            "/VSCode|IDE|编辑器/ => 开发工具",
            "/Git|GitHub|GitLab/ => 版本控制",
            "开源",
        ]
    },
    "自媒体运营博主": {
        "description": "分享自媒体运营技巧、平台规则、变现方法，目标受众：内容创作者",
        "keywords": [
            "[GLOBAL_FILTER]",
            "震惊",
            "",
            "[WORD_GROUPS]",
            "",
            "# 平台运营",
            "/抖音|TikTok|短视频/ => 抖音",
            "/小红书|种草/ => 小红书",
            "/B站|bilibili|UP主/ => B站",
            "/公众号|微信/ => 公众号",
            "/知乎|问答/ => 知乎",
            "",
            "# 运营技巧",
            "[运营技巧]",
            "流量",
            "粉丝",
            "变现",
            "爆款",
            "选题",
            "脚本",
            "",
            "# 内容创作",
            "[内容创作]",
            "文案",
            "剪辑",
            "封面",
            "标题",
        ]
    },
}

def get_trendradar_project_path() -> str:
    env_path = os.environ.get("TRENDRADAR_PROJECT_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    return r"D:\Project\TrendingRadar"

def get_keywords_config_path(trendradar_path: str) -> Path:
    return Path(trendradar_path) / "config" / "frequency_words.txt"

def list_available_positionings() -> List[str]:
    return list(POSITIONING_KEYWORDS_MAP.keys())

def generate_keywords_from_positioning(positioning: str) -> Optional[List[str]]:
    if positioning in POSITIONING_KEYWORDS_MAP:
        return POSITIONING_KEYWORDS_MAP[positioning]["keywords"]
    return None

def generate_keywords_from_custom(custom_keywords: str) -> List[str]:
    keywords = [k.strip() for k in custom_keywords.split(",") if k.strip()]
    lines = [
        "[GLOBAL_FILTER]",
        "震惊",
        "标题党",
        "",
        "[WORD_GROUPS]",
        "",
        "# 自定义关键词",
    ]
    for kw in keywords:
        if kw.startswith("/"):
            lines.append(f"{kw}")
        else:
            lines.append(kw)
    return lines

def write_keywords_config(trendradar_path: str, keywords: List[str], backup: bool = True) -> bool:
    config_path = get_keywords_config_path(trendradar_path)
    config_dir = config_path.parent
    
    if not config_dir.exists():
        print(f"❌ 配置目录不存在: {config_dir}")
        return False
    
    if backup and config_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = config_path.with_suffix(f".txt.bak_{timestamp}")
        import shutil
        shutil.copy2(config_path, backup_path)
        print(f"📦 已备份原配置: {backup_path.name}")
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(keywords))
        print(f"✅ 关键词配置已写入: {config_path}")
        return True
    except Exception as e:
        print(f"❌ 写入失败: {e}")
        return False

def show_current_config(trendradar_path: str) -> None:
    config_path = get_keywords_config_path(trendradar_path)
    if config_path.exists():
        print(f"📄 当前配置文件: {config_path}")
        print("-" * 50)
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    else:
        print(f"⚠️ 配置文件不存在: {config_path}")

def show_available_positionings() -> None:
    print("📋 可用的账号定位模板:")
    print("=" * 60)
    for name, info in POSITIONING_KEYWORDS_MAP.items():
        print(f"\n【{name}】")
        print(f"   {info['description']}")
    print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="TrendRadar 关键词配置工具 v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python config_keywords.py --list                    # 列出所有可用定位
  python config_keywords.py --positioning "AI实战成长博主"  # 使用预设定位
  python config_keywords.py --keywords "AI,ChatGPT,开源"   # 自定义关键词
  python config_keywords.py --show-config             # 查看当前配置
        """
    )
    
    parser.add_argument("--trendradar-path", default=None, help="TrendRadar 项目路径")
    parser.add_argument("--positioning", default=None, help="账号定位（使用预设模板）")
    parser.add_argument("--keywords", default=None, help="自定义关键词（逗号分隔）")
    parser.add_argument("--list", action="store_true", help="列出所有可用的账号定位")
    parser.add_argument("--show-config", action="store_true", help="显示当前关键词配置")
    parser.add_argument("--no-backup", action="store_true", help="不备份原配置文件")
    
    args = parser.parse_args()
    
    trendradar_path = args.trendradar_path or get_trendradar_project_path()
    
    if args.list:
        show_available_positionings()
        return
    
    if args.show_config:
        show_current_config(trendradar_path)
        return
    
    keywords = None
    
    if args.positioning:
        keywords = generate_keywords_from_positioning(args.positioning)
        if keywords is None:
            print(f"❌ 未找到定位模板: {args.positioning}")
            print("💡 使用 --list 查看所有可用定位")
            show_available_positionings()
            sys.exit(1)
        print(f"📍 使用定位: {args.positioning}")
    
    elif args.keywords:
        keywords = generate_keywords_from_custom(args.keywords)
        print(f"🔑 使用自定义关键词: {args.keywords}")
    
    else:
        print("❌ 请指定 --positioning 或 --keywords")
        print("💡 使用 --list 查看所有可用定位")
        parser.print_help()
        sys.exit(1)
    
    if keywords:
        print(f"\n📝 生成的关键词配置:")
        print("-" * 50)
        for line in keywords[:20]:
            print(f"  {line}")
        if len(keywords) > 20:
            print(f"  ... 共 {len(keywords)} 行")
        print("-" * 50)
        
        success = write_keywords_config(trendradar_path, keywords, backup=not args.no_backup)
        if success:
            print("\n✅ 配置完成！下次运行 TrendRadar 时将使用新的关键词筛选。")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
