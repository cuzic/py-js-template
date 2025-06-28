#!/bin/bash
# インクリメンタルpre-commitスクリプト
# 変更されたファイルのみを対象に高速実行

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# パフォーマンス計測開始
start_time=$(date +%s.%N)

echo -e "${BLUE}🚀 高速pre-commitチェック開始...${NC}"

# Git staged files を取得
staged_files=$(git diff --cached --name-only)
staged_count=$(echo "$staged_files" | wc -l)

if [ -z "$staged_files" ]; then
    echo -e "${YELLOW}⚠️  ステージされたファイルがありません。${NC}"
    exit 0
fi

echo -e "${BLUE}📄 対象ファイル数: $staged_count${NC}"

# ファイルタイプ別に分類
python_files=$(echo "$staged_files" | grep -E '^backend/.*\.py$' || true)
js_files=$(echo "$staged_files" | grep -E '^frontend/.*\.(js|jsx|ts|tsx)$' || true)
config_files=$(echo "$staged_files" | grep -E '\.(json|yaml|yml|toml)$' || true)

# Python ファイルの処理
if [ -n "$python_files" ]; then
    echo -e "${BLUE}🐍 Python ファイル処理中...${NC}"
    
    # Ruff lint (高速)
    echo "$python_files" | while read -r file; do
        if [ -f "$file" ]; then
            mise exec -- ruff check --fix --select=E,W,F,I --cache-dir=.ruff_cache "$file" || true
        fi
    done
    
    # Ruff format (高速)
    echo "$python_files" | while read -r file; do
        if [ -f "$file" ]; then
            mise exec -- ruff format "$file" || true
        fi
    done
    
    echo -e "${GREEN}✅ Python ファイル処理完了${NC}"
fi

# JavaScript/TypeScript ファイルの処理
if [ -n "$js_files" ]; then
    echo -e "${BLUE}📜 JavaScript/TypeScript ファイル処理中...${NC}"
    
    # Prettier format (キャッシュ有効)
    cd frontend
    echo "$js_files" | sed 's|^frontend/||' | while read -r file; do
        if [ -f "$file" ]; then
            mise exec -- prettier --write --cache --cache-strategy content "$file" || true
        fi
    done
    
    # ESLint (キャッシュ有効)
    echo "$js_files" | sed 's|^frontend/||' | while read -r file; do
        if [ -f "$file" ]; then
            mise exec -- eslint --fix --cache --cache-location .eslintcache "$file" || true
        fi
    done
    cd ..
    
    echo -e "${GREEN}✅ JavaScript/TypeScript ファイル処理完了${NC}"
fi

# 基本セキュリティチェック
echo -e "${BLUE}🔒 セキュリティチェック中...${NC}"

# APIキー検出
if echo "$staged_files" | xargs grep -l "api_key\|API_KEY\|secret\|password\|token" 2>/dev/null; then
    echo -e "${RED}❌ 機密情報の可能性があるファイルが検出されました${NC}"
    exit 1
fi

# 大容量ファイルチェック
while read -r file; do
    if [ -f "$file" ] && [ $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0) -gt 1048576 ]; then
        echo -e "${RED}❌ 大容量ファイル検出: $file (>1MB)${NC}"
        exit 1
    fi
done <<< "$staged_files"

# マージコンフリクトマーカー検出
if echo "$staged_files" | xargs grep -l "<<<<<<< \|======= \|>>>>>>> " 2>/dev/null; then
    echo -e "${RED}❌ マージコンフリクトマーカーが検出されました${NC}"
    exit 1
fi

echo -e "${GREEN}✅ セキュリティチェック完了${NC}"

# 変更されたファイルを自動ステージング
changed_files=$(git diff --name-only)
if [ -n "$changed_files" ]; then
    echo -e "${YELLOW}📦 フォーマッターによる変更を自動ステージング...${NC}"
    git add -u
    echo -e "${GREEN}✅ 変更ファイルをステージングしました${NC}"
fi

# パフォーマンス計測終了
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc -l)

echo -e "${GREEN}🎉 高速pre-commitチェック完了！${NC}"
echo -e "${BLUE}⏱️  実行時間: ${duration}秒${NC}"

# 3秒以内の目標チェック
if (( $(echo "$duration > 3.0" | bc -l) )); then
    echo -e "${YELLOW}⚠️  実行時間が目標(3秒)を超過しました${NC}"
    echo -e "${YELLOW}💡 キャッシュ最適化やファイル除外の見直しを検討してください${NC}"
fi

exit 0