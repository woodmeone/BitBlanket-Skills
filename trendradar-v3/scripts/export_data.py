#!/usr/bin/env python3
"""
TrendRadar 数据导出脚本 v2.1
将 SQLite 数据库中的数据导出为 JSON 格式，支持双路径输出

使用方法:
    python export_data.py --caller-path "d:\\makeskill\\test"
    python export_data.py --caller-path "d:\\makeskill\\test" --date 2026-03-22
    python export_data.py --dates
"""
import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

def get_trendradar_project_path() -> str:
    env_path = os.environ.get("TRENDRADAR_PROJECT_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    return r"D:\Project\TrendingRadar"

def get_output_paths(trendradar_path: str, caller_path: Optional[str] = None) -> List[Tuple[str, str]]:
    paths = []
    
    if caller_path:
        caller_data_dir = Path(caller_path) / "TrendRadarData"
        paths.append((str(caller_data_dir), "调用方项目"))
    
    trendradar_json_dir = Path(trendradar_path) / "output" / "json"
    paths.append((str(trendradar_json_dir), "TrendRadar项目"))
    
    return paths

def get_db_path(project_path: str, date: str, db_type: str = "news") -> Path:
    return Path(project_path) / "output" / db_type / f"{date}.db"

def export_news_data(db_path: Path) -> List[Dict]:
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            n.id,
            n.title,
            n.url,
            n.mobile_url,
            n.platform_id,
            p.name as platform_name,
            n.rank,
            n.first_crawl_time,
            n.last_crawl_time,
            n.crawl_count,
            n.created_at,
            n.updated_at
        FROM news_items n
        LEFT JOIN platforms p ON n.platform_id = p.id
        ORDER BY n.platform_id, n.rank ASC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def export_rss_data(db_path: Path) -> List[Dict]:
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            r.id,
            r.title,
            r.url,
            r.feed_id,
            f.name as feed_name,
            r.published_at,
            r.summary,
            r.author,
            r.first_crawl_time,
            r.last_crawl_time,
            r.crawl_count,
            r.created_at,
            r.updated_at
        FROM rss_items r
        LEFT JOIN rss_feeds f ON r.feed_id = f.id
        ORDER BY r.published_at DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def _write_json_to_paths(
    filename: str,
    payload: Dict,
    output_paths: List[Tuple[str, str]]
) -> List[str]:
    written_files = []
    for out_dir, desc in output_paths:
        dir_path = Path(out_dir)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        written_files.append(str(file_path))
        print(f"✅ 写入 [{desc}]: {file_path}")
    
    return written_files

def export_trending_data(
    trendradar_path: str = None,
    caller_path: str = None,
    date: str = None,
    include_rss: bool = True
) -> Dict[str, List[str]]:
    if trendradar_path is None:
        trendradar_path = get_trendradar_project_path()
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    result = {"news": [], "rss": []}
    
    output_paths = get_output_paths(trendradar_path, caller_path)
    
    news_db_path = get_db_path(trendradar_path, date, "news")
    if news_db_path.exists():
        news_data = export_news_data(news_db_path)
        
        export_payload = {
            "export_info": {
                "source": "TrendRadar",
                "export_time": datetime.now().isoformat(),
                "date": date,
                "type": "hot_trending",
                "total_count": len(news_data)
            },
            "data": news_data
        }
        
        filename = f"RadarHotTrending{date}.json"
        written = _write_json_to_paths(filename, export_payload, output_paths)
        result["news"] = written
        print(f"📊 热榜数据导出完成: {len(news_data)} 条")
    else:
        print(f"⚠️ 热榜数据库不存在: {news_db_path}")
    
    if include_rss:
        rss_db_path = get_db_path(trendradar_path, date, "rss")
        if rss_db_path.exists():
            rss_data = export_rss_data(rss_db_path)
            
            export_payload = {
                "export_info": {
                    "source": "TrendRadar",
                    "export_time": datetime.now().isoformat(),
                    "date": date,
                    "type": "rss",
                    "total_count": len(rss_data)
                },
                "data": rss_data
            }
            
            filename = f"RadarRSS{date}.json"
            written = _write_json_to_paths(filename, export_payload, output_paths)
            result["rss"] = written
            print(f"📰 RSS数据导出完成: {len(rss_data)} 条")
        else:
            print(f"⚠️ RSS数据库不存在: {rss_db_path}")
    
    return result

def export_all_available(
    trendradar_path: str = None,
    caller_path: str = None,
    include_rss: bool = True
) -> Dict[str, List[str]]:
    if trendradar_path is None:
        trendradar_path = get_trendradar_project_path()
    
    news_dir = Path(trendradar_path) / "output" / "news"
    if not news_dir.exists():
        print("❌ 没有找到热榜数据目录")
        return {"news": [], "rss": []}
    
    dates = sorted([f.stem for f in news_dir.glob("*.db")], reverse=True)
    print(f"📅 发现 {len(dates)} 天的数据: {', '.join(dates[:5])}{'...' if len(dates) > 5 else ''}")
    
    all_results = {"news": [], "rss": []}
    
    for date in dates:
        print(f"\n📦 导出 {date}...")
        result = export_trending_data(trendradar_path, caller_path, date, include_rss)
        if result.get("news"):
            all_results["news"].extend(result["news"])
        if result.get("rss"):
            all_results["rss"].extend(result["rss"])
    
    return all_results

def get_available_dates(trendradar_path: str = None) -> List[str]:
    if trendradar_path is None:
        trendradar_path = get_trendradar_project_path()
    news_dir = Path(trendradar_path) / "output" / "news"
    
    if not news_dir.exists():
        return []
    
    return sorted([f.stem for f in news_dir.glob("*.db")], reverse=True)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TrendRadar 数据导出工具 v2.1")
    parser.add_argument("--trendradar-path", default=None, help="TrendRadar 项目路径")
    parser.add_argument("--caller-path", default=None, help="调用方项目路径（用于双路径输出）")
    parser.add_argument("--date", default=None, help="导出日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--all", action="store_true", help="导出所有可用日期")
    parser.add_argument("--no-rss", action="store_true", help="不导出 RSS 数据")
    parser.add_argument("--dates", action="store_true", help="显示可用日期")
    
    args = parser.parse_args()
    
    trendradar_path = args.trendradar_path if args.trendradar_path else get_trendradar_project_path()
    
    if args.dates:
        dates = get_available_dates(trendradar_path)
        print("可用日期:", ", ".join(dates[:10]))
        sys.exit(0)
    
    if not args.caller_path:
        print("❌ 错误: 需要指定 --caller-path 参数")
        print("示例: python export_data.py --caller-path \"d:\\makeskill\\test\"")
        sys.exit(1)
    
    print("=" * 50)
    print("TrendRadar 数据导出 v2.1")
    print("=" * 50)
    print(f"TrendRadar路径: {trendradar_path}")
    print(f"调用方路径: {args.caller_path}")
    print(f"输出模式: 双路径输出")
    print("=" * 50)
    
    if args.all:
        export_all_available(trendradar_path, args.caller_path, not args.no_rss)
    else:
        export_trending_data(trendradar_path, args.caller_path, args.date, not args.no_rss)
    
    print("\n✅ 导出完成")
