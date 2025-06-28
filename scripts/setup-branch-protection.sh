#!/bin/bash
# Branch Protection Rules設定スクリプト
# ユーザーストーリー3: --no-verify バイパス対策

set -euo pipefail

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 設定変数
REPO_OWNER="${1:-cuzic}"
REPO_NAME="${2:-py-js-template}"
BRANCH="main"

echo -e "${BLUE}🛡️  Branch Protection Rules設定開始...${NC}"
echo -e "${BLUE}📁 Repository: $REPO_OWNER/$REPO_NAME${NC}"
echo -e "${BLUE}🌿 Branch: $BRANCH${NC}"

# GitHub CLI認証確認
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ GitHub CLI認証が必要です${NC}"
    echo -e "${YELLOW}💡 実行: gh auth login${NC}"
    exit 1
fi

echo -e "${GREEN}✅ GitHub CLI認証済み${NC}"

# Branch Protection Rules設定
echo -e "${BLUE}🔧 Branch Protection Rules設定中...${NC}"

# 必須チェック設定
gh api repos/$REPO_OWNER/$REPO_NAME/branches/$BRANCH/protection \
  --method PUT \
  --header "Accept: application/vnd.github.v3+json" \
  --field required_status_checks='{
    "strict": true,
    "checks": [
      {"context": "quality-check"},
      {"context": "compatibility-check"},
      {"context": "test-matrix"}
    ]
  }' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "require_last_push_approval": false
  }' \
  --field restrictions=null \
  --field required_linear_history=false \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field block_creations=false \
  --field required_conversation_resolution=true \
  --field lock_branch=false \
  --field allow_fork_syncing=true

echo -e "${GREEN}✅ Branch Protection Rules設定完了${NC}"

# 設定確認
echo -e "${BLUE}📋 設定内容確認...${NC}"
gh api repos/$REPO_OWNER/$REPO_NAME/branches/$BRANCH/protection | jq '.required_status_checks.checks[].context'

echo -e "${GREEN}🎉 Branch Protection Rules設定成功！${NC}"
echo -e "${BLUE}📖 設定された保護ルール:${NC}"
echo -e "  • 必須status checks: CI基本チェック（quality-check, compatibility-check, test-matrix）"
echo -e "  • 品質分析: Quality Analysis（必須ではないが自動実行）"
echo -e "  • 監視システム: Quality Monitor（失敗時に自動Issue作成）"
echo -e "  • PR承認: 1名以上"
echo -e "  • 管理者にも適用: 有効"
echo -e "  • 直接プッシュ: 禁止"
echo -e "  • フォースプッシュ: 禁止"
echo -e "  • 会話解決必須: 有効"

echo -e "${YELLOW}💡 完全分離戦略により、CI・品質分析・監視が独立して動作します！${NC}"