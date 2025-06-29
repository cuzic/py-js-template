#!/usr/bin/env python3
"""
Python品質分析スクリプト
quality-analysis.yml ワークフローから抽出
"""

import json
import os
import sys
from datetime import datetime


def load_json_safe(filepath):
    """JSONファイルを安全に読み込む"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def analyze_python_quality():
    """Python品質レポートを集計し、サマリーを生成する"""
    
    # レポート集計
    summary = {
        "timestamp": datetime.now().strftime('%Y-%m-%d'),
        "ruff_violations": 0,
        "mypy_errors": 0,
        "bandit_issues": 0,
        "test_coverage": 0,
        "complexity_score": "N/A",
        "security_vulnerabilities": 0
    }
    
    # Ruff統計
    ruff_data = load_json_safe("quality-reports/ruff-detailed.json")
    if isinstance(ruff_data, list):
        summary["ruff_violations"] = len(ruff_data)
    
    # MyPy統計
    mypy_data = load_json_safe("quality-reports/mypy-report.json")
    if "messages" in mypy_data:
        summary["mypy_errors"] = len(mypy_data["messages"])
    
    # Bandit統計
    bandit_data = load_json_safe("quality-reports/bandit-report.json")
    if "results" in bandit_data:
        summary["bandit_issues"] = len(bandit_data["results"])
    
    # カバレッジ統計
    coverage_data = load_json_safe("quality-reports/coverage.json")
    if "totals" in coverage_data and "percent_covered" in coverage_data["totals"]:
        summary["test_coverage"] = round(coverage_data["totals"]["percent_covered"], 2)
    
    # サマリーファイル出力
    with open("quality-reports/python-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Python品質サマリー: {summary}")
    return summary


if __name__ == "__main__":
    if not os.path.exists("quality-reports"):
        print("Error: quality-reports ディレクトリが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    try:
        summary = analyze_python_quality()
        print("✅ Python品質分析完了")
    except Exception as e:
        print(f"❌ Python品質分析エラー: {e}", file=sys.stderr)
        sys.exit(1)