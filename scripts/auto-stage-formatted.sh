#!/bin/bash
# 自動ステージング用ヘルパースクリプト
# フォーマッターによって変更されたファイルを自動的にコミットに含める

set -euo pipefail

# カラー出力設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Pre-commit hooks を実行中...${NC}"

# pre-commitを実行
if mise exec -- pre-commit run --all-files; then
    echo -e "${GREEN}✅ すべてのフックが正常に完了しました。${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  フォーマッターによってファイルが変更されました。${NC}"
    
    # 変更されたファイルを表示
    echo -e "${BLUE}📄 変更されたファイル:${NC}"
    git diff --name-only
    
    # 変更をステージングに追加
    echo -e "${BLUE}📦 変更をステージングに追加中...${NC}"
    git add -u
    
    echo -e "${GREEN}✅ フォーマット済みファイルがステージングされました。再度コミットを実行してください。${NC}"
    echo -e "${YELLOW}💡 Tip: 'git commit' を再実行すると、フォーマット済みのコードがコミットされます。${NC}"
    
    exit 1
fi