#!/bin/bash
# 品質チェック失敗時の自動issue作成スクリプト
# ユーザーストーリー4: 自動化スクリプト統合

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# パラメータ
FAILURE_TYPE="${1:-unknown}"
DETAILS="${2:-No details provided}"
PR_NUMBER="${3:-}"
COMMIT_SHA="${4:-$(git rev-parse HEAD)}"
AUTHOR="${5:-$(git log -1 --pretty=format:'%an')}"

echo -e "${BLUE}🤖 品質チェック失敗自動issue作成${NC}"

# GitHub CLI認証確認
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ GitHub CLI認証が必要です${NC}"
    exit 1
fi

# Issue重複チェック
EXISTING_ISSUE=$(gh issue list --label "quality-failure" --state "open" --search "Quality Failure: $FAILURE_TYPE" --json number --jq '.[0].number' 2>/dev/null || echo "")

if [ -n "$EXISTING_ISSUE" ] && [ "$EXISTING_ISSUE" != "null" ]; then
    echo -e "${YELLOW}⚠️  類似のissueが既に存在: #$EXISTING_ISSUE${NC}"
    
    # 既存issueにコメント追加
    gh issue comment "$EXISTING_ISSUE" --body "
## 🔄 追加の品質チェック失敗

**失敗タイプ**: $FAILURE_TYPE
**コミット**: $COMMIT_SHA
**作成者**: $AUTHOR
**PR**: ${PR_NUMBER:+#$PR_NUMBER}
**詳細**: 
\`\`\`
$DETAILS
\`\`\`

**発生時刻**: $(date)
"
    echo -e "${GREEN}✅ 既存issue #$EXISTING_ISSUE にコメント追加${NC}"
    exit 0
fi

# 新規issue作成
ISSUE_TITLE="🚨 Quality Failure: $FAILURE_TYPE"

ISSUE_BODY="# 品質チェック失敗報告

## 📋 基本情報
- **失敗タイプ**: $FAILURE_TYPE
- **コミットSHA**: \`$COMMIT_SHA\`
- **作成者**: @$AUTHOR
- **発生時刻**: $(date)
- **PR番号**: ${PR_NUMBER:+#$PR_NUMBER}

## 🔍 失敗詳細
\`\`\`
$DETAILS
\`\`\`

## 📊 品質統計
$(cd /home/cuzic/py-js-template && bash scripts/monitor-bypass-usage.sh 7 2>/dev/null | tail -10 || echo "統計データ取得中...")

## 🛠️ 修正手順

### 1. ローカル環境での再現
\`\`\`bash
# リポジトリクローン・チェックアウト
git checkout $COMMIT_SHA

# 品質チェック実行
mise exec -- pre-commit run --all-files
\`\`\`

### 2. 推奨修正アクション
"

# 失敗タイプ別の修正ガイダンス
case "$FAILURE_TYPE" in
    "ruff-lint")
        ISSUE_BODY="$ISSUE_BODY
- 🐍 Ruffリンティングエラー修正
\`\`\`bash
cd backend
uv run ruff check --fix .
uv run ruff format .
\`\`\`"
        ;;
    "eslint")
        ISSUE_BODY="$ISSUE_BODY
- 📜 ESLintエラー修正
\`\`\`bash
cd frontend
bun exec eslint --fix .
bun exec prettier --write .
\`\`\`"
        ;;
    "mypy")
        ISSUE_BODY="$ISSUE_BODY
- 🔍 型アノテーション修正
\`\`\`bash
cd backend
uv run mypy src/ --show-error-codes
\`\`\`"
        ;;
    "security")
        ISSUE_BODY="$ISSUE_BODY
- 🛡️ セキュリティ問題修正
\`\`\`bash
cd backend
uv run bandit -r src/
uvx safety check
\`\`\`"
        ;;
    "tests")
        ISSUE_BODY="$ISSUE_BODY
- 🧪 テスト失敗修正
\`\`\`bash
cd backend && uv run pytest -v
cd frontend && bun test
\`\`\`"
        ;;
    *)
        ISSUE_BODY="$ISSUE_BODY
- ⚙️ 一般的なトラブルシューティング
\`\`\`bash
# 全チェック実行
mise exec -- pre-commit run --all-files
\`\`\`"
        ;;
esac

ISSUE_BODY="$ISSUE_BODY

### 3. 予防策
- [ ] Pre-commitフックの有効化確認
- [ ] IDE設定の確認（ESLint、Ruff拡張機能）
- [ ] チーム共有ルールの見直し

## 🔗 関連リンク
- [Pre-commit ガイド](docs/pre-commit-guide.md)
- [品質基準ドキュメント](docs/linting-rules.md)
- [CI/CDワークフロー](docs/workflows.md)

## 🏷️ ラベル
品質改善、自動生成

---
*この issue は品質チェック失敗時に自動生成されました*"

# Issue作成
ISSUE_NUMBER=$(gh issue create \
    --title "$ISSUE_TITLE" \
    --body "$ISSUE_BODY" \
    --label "quality-failure,bug,automated" \
    --assignee "@$AUTHOR" \
    --json number --jq '.number')

echo -e "${GREEN}✅ Issue作成完了: #$ISSUE_NUMBER${NC}"

# PR番号が指定されている場合、PRにコメント
if [ -n "$PR_NUMBER" ]; then
    gh pr comment "$PR_NUMBER" --body "
🚨 **品質チェック失敗が検出されました**

詳細な修正手順については Issue #$ISSUE_NUMBER をご確認ください。

**失敗タイプ**: $FAILURE_TYPE
**修正が必要な項目**: 上記issueの修正手順に従ってください
"
    echo -e "${GREEN}✅ PR #$PR_NUMBER にコメント追加${NC}"
fi

# Slackなどの外部通知（オプション）
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚨 Quality Failure: $FAILURE_TYPE\\nIssue: #$ISSUE_NUMBER\\nAuthor: $AUTHOR\"}" \
        "$SLACK_WEBHOOK_URL" || true
    echo -e "${GREEN}✅ Slack通知送信${NC}"
fi

echo -e "${BLUE}🎉 自動issue作成プロセス完了${NC}"
echo -e "${BLUE}📄 Issue URL: $(gh issue view $ISSUE_NUMBER --json url --jq '.url')${NC}"