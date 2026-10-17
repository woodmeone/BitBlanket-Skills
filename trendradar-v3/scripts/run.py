#!/usr/bin/env python3
"""
TrendRadar 一键运行脚本 v3.0
自动完成：关键词配置 + 数据抓取 + 双路径导出

使用方法:
    python run.py --caller-path "d:\\makeskill\\test"
    python run.py --caller-path "d:\\makeskill\\test" --positioning "AI实战成长博主"
    python run.py --caller-path "d:\\makeskill\\test" --keywords "AI,ChatGPT,DeepSeek"
    python run.py --caller-path "d:\\makeskill\\test" --date 2026-03-22
    python run.py --caller-path "d:\\makeskill\\test" --export-only
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def get_trendradar_project_path() -> str:
    env_path = os.environ.get("TRENDRADAR_PROJECT_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    return r"D:\Project\TrendingRadar"

def run_config_keywords(trendradar_path: str, positioning: str = None, keywords: str = None) -> tuple:
    config_script = Path(__file__).parent / "config_keywords.py"
    if not config_script.exists():
        return False, f"关键词配置脚本不存在: {config_script}"
    
    cmd = [sys.executable, str(config_script), "--trendradar-path", trendradar_path]
    
    if positioning:
        cmd.extend(["--positioning", positioning])
    elif keywords:
        cmd.extend(["--keywords", keywords])
    else:
        return True, "未指定定位或关键词，跳过配置步骤"
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, f"配置失败: {str(e)}"

def run_trendradar_main(trendradar_path: str) -> tuple:
    cmd = [sys.executable, "-m", "trendradar"]
    try:
        result = subprocess.run(
            cmd,
            cwd=trendradar_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "运行超时（超过 5 分钟）"
    except Exception as e:
        return False, f"运行失败: {str(e)}"

def export_data(trendradar_path: str, caller_path: str, date: str = None) -> tuple:
    export_script = Path(__file__).parent / "export_data.py"
    if not export_script.exists():
        return False, f"导出脚本不存在: {export_script}"
    
    cmd = [sys.executable, str(export_script), "--caller-path", caller_path]
    if date:
        cmd.extend(["--date", date])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=trendradar_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, f"导出失败: {str(e)}"

def verify_output(caller_path: str, date: str = None) -> dict:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    caller_data_dir = Path(caller_path) / "TrendRadarData"
    
    result = {
        "caller_path": caller_path,
        "data_dir": str(caller_data_dir),
        "exists": caller_data_dir.exists(),
        "json_files": [],
        "html_exists": False
    }
    
    if caller_data_dir.exists():
        json_dir = caller_data_dir
        for f in json_dir.glob("*.json"):
            result["json_files"].append(f.name)
        
        html_dir = caller_data_dir / "html"
        result["html_exists"] = html_dir.exists()
    
    return result

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TrendRadar 一键运行脚本 v3.0")
    parser.add_argument("--trendradar-path", default=None, help="TrendRadar 项目路径")
    parser.add_argument("--caller-path", required=True, help="调用方项目路径（必需）")
    parser.add_argument("--date", default=None, help="指定日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--positioning", default=None, help="账号定位（使用预设模板）")
    parser.add_argument("--keywords", default=None, help="自定义关键词（逗号分隔）")
    parser.add_argument("--export-only", action="store_true", help="仅导出数据，不运行抓取")
    parser.add_argument("--skip-export", action="store_true", help="跳过导出，仅运行抓取")
    parser.add_argument("--skip-config", action="store_true", help="跳过关键词配置步骤")
    parser.add_argument("--list-positionings", action="store_true", help="列出所有可用的账号定位")
    
    args = parser.parse_args()
    
    trendradar_path = args.trendradar_path or get_trendradar_project_path()
    caller_path = args.caller_path
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    if args.list_positionings:
        config_script = Path(__file__).parent / "config_keywords.py"
        cmd = [sys.executable, str(config_script), "--list"]
        subprocess.run(cmd)
        sys.exit(0)
    
    print("=" * 60)
    print("TrendRadar v3.0 - 智能定位 + 双路径输出")
    print("=" * 60)
    print(f"TrendRadar路径: {trendradar_path}")
    print(f"调用方路径: {caller_path}")
    print(f"日期: {date}")
    if args.positioning:
        print(f"账号定位: {args.positioning}")
    if args.keywords:
        print(f"自定义关键词: {args.keywords}")
    print(f"输出位置:")
    print(f"  - TrendRadar: {trendradar_path}/output/")
    print(f"  - 调用方: {caller_path}/TrendRadarData/")
    print("=" * 60)
    
    if not args.export_only and not args.skip_config:
        if args.positioning or args.keywords:
            print("\n🎯 步骤0: 配置关键词筛选...")
            success, output = run_config_keywords(trendradar_path, args.positioning, args.keywords)
            print(output)
            if not success:
                print("⚠️ 关键词配置失败，继续使用现有配置")
            else:
                print("✅ 关键词配置完成")
    
    if not args.export_only:
        print("\n📡 步骤1: 运行数据抓取...")
        success, output = run_trendradar_main(trendradar_path)
        print(output)
        if not success:
            print("❌ 数据抓取失败")
            sys.exit(1)
        print("✅ 数据抓取完成")
    
    if not args.skip_export:
        print("\n📤 步骤2: 导出数据到双路径...")
        success, output = export_data(trendradar_path, caller_path, date)
        print(output)
        if not success:
            print("❌ 数据导出失败")
            sys.exit(1)
        print("✅ 数据导出完成")
    
    print("\n🔍 步骤3: 验证输出...")
    verify_result = verify_output(caller_path, date)
    
    if verify_result["exists"]:
        print(f"✅ 调用方数据目录已创建: {verify_result['data_dir']}")
        if verify_result["json_files"]:
            print(f"   JSON文件: {', '.join(verify_result['json_files'])}")
        if verify_result["html_exists"]:
            print(f"   HTML报告: 已生成")
    else:
        print(f"❌ 调用方数据目录未创建")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 全部完成！")
    print("=" * 60)
    sys.exit(0)

if __name__ == "__main__":
    main()
