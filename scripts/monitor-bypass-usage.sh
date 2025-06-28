#!/bin/bash
# Pre-commit バイパス使用状況監視スクリプト
# ユーザーストーリー3: --no-verify使用頻度の監視

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 設定
DAYS_BACK=${1:-30}
LOG_FILE="bypass-usage.log"

echo -e "${BLUE}📊 Pre-commit バイパス使用状況分析${NC}"
echo -e "${BLUE}📅 期間: 過去${DAYS_BACK}日間${NC}"

# Gitログから--no-verifyの使用パターンを分析
echo -e "${BLUE}🔍 --no-verify使用コミット検索中...${NC}"

# pre-commitフックがスキップされた可能性のあるコミットを検出
# (通常のコミットパターンと異なるコミットを検出)

# 1. コミットメッセージパターン分析
suspicious_commits=$(git log --since="$DAYS_BACK days ago" --pretty=format:"%H|%an|%ad|%s" --date=short | \
    grep -E "(WIP|wip|temp|temporary|quick|hotfix|bypass|skip)" || true)

if [ -n "$suspicious_commits" ]; then
    echo -e "${YELLOW}⚠️  疑わしいコミットパターン検出:${NC}"
    echo "$suspicious_commits" | while IFS='|' read -r hash author date message; do
        echo -e "  🔍 $hash by $author on $date: $message"
    done
else
    echo -e "${GREEN}✅ 疑わしいコミットパターンなし${NC}"
fi

# 2. pre-commitフックの実行履歴確認
echo -e "${BLUE}📈 Pre-commit実行統計...${NC}"

# 最近のコミット数
total_commits=$(git log --since="$DAYS_BACK days ago" --oneline | wc -l)
echo -e "  📊 総コミット数: $total_commits"

# 開発者別統計
echo -e "${BLUE}👥 開発者別コミット統計:${NC}"
git log --since="$DAYS_BACK days ago" --pretty=format:"%an" | \
    sort | uniq -c | sort -nr | \
    while read -r count author; do
        echo -e "  👤 $author: $count コミット"
    done

# 3. 時間帯別コミットパターン分析（深夜の緊急コミットを検出）
echo -e "${BLUE}🕐 時間帯別コミット分析:${NC}"
git log --since="$DAYS_BACK days ago" --pretty=format:"%ad" --date=format:"%H" | \
    sort | uniq -c | sort -nr | \
    while read -r count hour; do
        if [ "$hour" -ge 22 ] || [ "$hour" -le 6 ]; then
            echo -e "  🌙 ${hour}時台: $count コミット (深夜/早朝)"
        else
            echo -e "  ☀️  ${hour}時台: $count コミット"
        fi
    done

# 4. ファイル変更パターン分析
echo -e "${BLUE}📁 変更ファイルパターン分析:${NC}"

# 設定ファイルのみの変更（pre-commitスキップの可能性）
config_only_commits=$(git log --since="$DAYS_BACK days ago" --name-only --pretty=format:"%H" | \
    awk 'BEGIN{RS=""; FS="\n"} {
        config_files=0; total_files=0;
        for(i=2; i<=NF; i++) {
            total_files++;
            if($i ~ /\.(yml|yaml|json|toml|md|txt)$/) config_files++;
        }
        if(total_files > 0 && config_files == total_files && total_files <= 3) 
            print $1
    }' | wc -l)

echo -e "  📄 設定ファイルのみ変更: $config_only_commits コミット"

# 5. レポート生成
{
    echo "# Pre-commit バイパス監視レポート"
    echo "生成日時: $(date)"
    echo "分析期間: 過去${DAYS_BACK}日間"
    echo ""
    echo "## 統計サマリー"
    echo "- 総コミット数: $total_commits"
    echo "- 疑わしいコミット: $(echo "$suspicious_commits" | wc -l)"
    echo "- 設定ファイルのみ変更: $config_only_commits"
    echo ""
    echo "## 推奨アクション"
    
    bypass_usage_rate=$(echo "scale=2; $(echo "$suspicious_commits" | wc -l) * 100 / $total_commits" | bc -l 2>/dev/null || echo "0")
    
    if (( $(echo "$bypass_usage_rate > 5" | bc -l 2>/dev/null || echo 0) )); then
        echo "- ⚠️  バイパス使用率が高い ($bypass_usage_rate%) - チーム教育が必要"
        echo "- 📚 Pre-commitフック使用方法の再教育"
        echo "- 🔧 フックの実行時間最適化検討"
    else
        echo "- ✅ バイパス使用率は正常範囲内 ($bypass_usage_rate%)"
        echo "- 📊 継続的な監視を実施"
    fi
} > "$LOG_FILE"

echo -e "${GREEN}📄 レポート生成完了: $LOG_FILE${NC}"

# 6. アラート判定
if (( $(echo "$bypass_usage_rate > 10" | bc -l 2>/dev/null || echo 0) )); then
    echo -e "${RED}🚨 アラート: バイパス使用率が基準値(10%)を超過${NC}"
    echo -e "${YELLOW}💡 対策:${NC}"
    echo -e "  1. チームミーティングでpre-commit重要性を説明"
    echo -e "  2. フック実行時間の最適化"
    echo -e "  3. 個別指導の実施"
    exit 1
else
    echo -e "${GREEN}✅ バイパス使用率は健全です${NC}"
fi

echo -e "${BLUE}📊 監視完了 - 定期実行推奨（週1回）${NC}"