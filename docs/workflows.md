# ⚙️ GitHub Actions ワークフロー解説

このドキュメントでは、プロジェクトに設定されているGitHub Actionsワークフローについて詳しく説明します。

## 📋 ワークフロー概要

| ワークフロー | トリガー | 目的 | 実行時間目安 |
|-------------|----------|------|-------------|
| **Python CI** | `backend/` 変更時 | Python コード品質・テスト | 2-3分 |
| **JavaScript CI** | `frontend/` 変更時 | JS/TS コード品質・テスト | 1-2分 |
| **AI Code Review** | PR作成・更新時 | Gemini APIによる自動レビュー | 30秒-1分 |

## 🐍 Python CI ワークフロー

### ファイル: `.github/workflows/python-ci.yml`

#### トリガー条件

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
      - '.github/workflows/python-ci.yml'
  push:
    branches:
      - main
    paths:
      - 'backend/**'
      - '.github/workflows/python-ci.yml'
```

- **PR作成・更新**: `backend/` 配下のファイル変更時
- **メインブランチpush**: `backend/` 配下のファイル変更時
- **ワークフロー自体の変更**: `python-ci.yml` 変更時

#### 実行ステップ詳細

##### 1. 環境セットアップ

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    ref: ${{ github.head_ref }}
    fetch-depth: 0

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'

- name: Setup uv
  uses: astral-sh/setup-uv@v6
```

**実行内容:**
- リポジトリのコードをチェックアウト
- Python 3.11 環境をセットアップ
- UV（超高速Pythonパッケージマネージャー）をインストール

##### 2. 依存関係インストール

```yaml
- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -e ".[dev]"
```

**実行内容:**
- Python仮想環境を作成
- 開発依存関係をeditable modeでインストール
- Ruff、Black、pytestなどが利用可能に

##### 3. コード品質チェック・自動修正

```yaml
- name: Auto-format with Black
  run: |
    source .venv/bin/activate
    black .

- name: Auto-fix with Ruff
  run: |
    source .venv/bin/activate
    ruff check --fix .

- name: Commit formatting changes
  if: github.event_name == 'pull_request'
  uses: stefanzweifel/git-auto-commit-action@v5
  with:
    commit_message: 'style: auto-format Python code with Black and Ruff'
    commit_user_name: 'github-actions[bot]'
    commit_user_email: 'github-actions[bot]@users.noreply.github.com'
    file_pattern: 'backend/**/*.py'
```

**実行内容:**
- Blackでコードフォーマットを自動適用
- Ruffで自動修正可能なリンティング問題を解決
- PR作成時は変更をリポジトリに自動コミット

##### 4. 最終品質チェック

```yaml
- name: Final lint check
  run: |
    source .venv/bin/activate
    black --check .
    ruff check .
```

**実行内容:**
- Blackフォーマットの最終確認
- Ruffリンティングの最終確認
- エラーがあればCI失敗

##### 5. テスト実行

```yaml
- name: Run tests with pytest
  run: |
    source .venv/bin/activate
    pytest -v --cov=backend --cov-report=term-missing
```

**実行内容:**
- pytestでテスト実行
- カバレッジ測定
- 詳細なテスト結果表示

### エラーハンドリング

| エラーパターン | 原因 | 解決方法 |
|---------------|------|----------|
| **依存関係エラー** | `pyproject.toml` 設定不備 | 依存関係の確認・修正 |
| **フォーマットエラー** | Black設定との不整合 | ローカルで `black .` 実行 |
| **リンティングエラー** | Ruffルール違反 | `ruff check --fix .` で自動修正 |
| **テスト失敗** | コードの論理エラー | テストの確認・修正 |

## 🟨 JavaScript CI ワークフロー

### ファイル: `.github/workflows/js-ci.yml`

#### トリガー条件

```yaml
on:
  pull_request:
    paths:
      - 'frontend/**'
      - '.github/workflows/js-ci.yml'
  push:
    branches:
      - main
    paths:
      - 'frontend/**'
      - '.github/workflows/js-ci.yml'
```

#### 実行ステップ詳細

##### 1. 環境セットアップ

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    ref: ${{ github.head_ref }}
    fetch-depth: 0

- name: Setup Bun
  uses: oven-sh/setup-bun@v1
  with:
    bun-version: latest
```

**実行内容:**
- リポジトリのコードをチェックアウト
- Bun（超高速JavaScript/TypeScriptランタイム）をセットアップ

##### 2. 依存関係インストール

```yaml
- name: Install dependencies
  run: bun install
```

**実行内容:**
- `package.json` の依存関係を高速インストール
- TypeScript、React、ESLint、Prettierなどがセットアップ

##### 3. 型チェック

```yaml
- name: Type check
  run: bun run typecheck
  continue-on-error: true
```

**実行内容:**
- TypeScriptの型エラーをチェック
- エラーがあっても後続処理を継続

##### 4. コード品質チェック・自動修正

```yaml
- name: Check formatting with Prettier
  id: prettier-check
  run: |
    bun run format:check || echo "formatting_needed=true" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Auto-format with Prettier
  if: steps.prettier-check.outputs.formatting_needed == 'true' && github.event_name == 'pull_request'
  run: bun run format

- name: Check linting with ESLint
  id: eslint-check
  run: |
    bun run lint --max-warnings 0 || echo "linting_needed=true" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Auto-fix with ESLint
  if: steps.eslint-check.outputs.linting_needed == 'true' && github.event_name == 'pull_request'
  run: bun run lint
```

**実行内容:**
- Prettierでフォーマットチェック・自動修正
- ESLintでリンティングチェック・自動修正
- 条件付きで自動修正を実行

##### 5. 変更の自動コミット

```yaml
- name: Commit formatting changes
  if: (steps.prettier-check.outputs.formatting_needed == 'true' || steps.eslint-check.outputs.linting_needed == 'true') && github.event_name == 'pull_request'
  uses: stefanzweifel/git-auto-commit-action@v5
  with:
    commit_message: 'style: auto-format JavaScript code with Prettier and ESLint'
    commit_user_name: 'github-actions[bot]'
    commit_user_email: 'github-actions[bot]@users.noreply.github.com'
    file_pattern: 'frontend/**/*.{js,jsx,ts,tsx,json,css,md}'
```

##### 6. 最終品質チェック

```yaml
- name: Final lint and format check
  run: |
    bun run format:check
    bun run lint --max-warnings 0
```

##### 7. テスト実行

```yaml
- name: Run tests
  run: bun run test

- name: Run tests with coverage
  run: bun run test:coverage
```

**実行内容:**
- Vitestでコンポーネント・単体テストを実行
- カバレッジレポートを生成

## 🤖 AI Code Review ワークフロー

### ファイル: `.github/workflows/review.yml`

#### トリガー条件

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    branches:
      - main
```

- PR作成時（`opened`）
- PR更新時（`synchronize`）
- メインブランチ向けPRのみ

#### 実行ステップ詳細

##### 1. 環境準備

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    fetch-depth: 0

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'

- name: Install dependencies
  run: pip install requests
```

##### 2. PR差分取得

```yaml
- name: Get PR diff
  id: get-diff
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    BASE_SHA="${{ github.event.pull_request.base.sha }}"
    HEAD_SHA="${{ github.event.pull_request.head.sha }}"
    
    git diff $BASE_SHA..$HEAD_SHA > pr_diff.txt
    
    if [ ! -s pr_diff.txt ]; then
      echo "No changes detected in the PR"
      echo "has_changes=false" >> $GITHUB_OUTPUT
    else
      echo "has_changes=true" >> $GITHUB_OUTPUT
      head -c 30000 pr_diff.txt > pr_diff_truncated.txt
      mv pr_diff_truncated.txt pr_diff.txt
    fi
```

**実行内容:**
- ベースブランチとHEADブランチの差分を取得
- 30KB以下に制限（API制限対応）
- 変更がない場合は後続スキップ

##### 3. AI レビュースクリプト作成

```python
# review.py (動的生成)
def get_ai_review(diff_content):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    
    prompt = """あなたは、このプロジェクトで採用されている以下の技術スタックに精通したエキスパートレビューアです。
- Python: uvによるパッケージ管理, Ruffによるリンティング, Blackによるフォーマット
- JavaScript/TypeScript: Bunによるパッケージ管理, ESLint (Flat Config)によるリンティング, Prettierによるフォーマット, React

これらのルールに基づき、以下のコード変更（diff形式）をレビューしてください。
特に、以下のチェックポイントに注目し、具体的で建設的なフィードバックを日本語で提供してください。

--- チェックポイント ---
1.  **Python (`backend/`):**
    - `pyproject.toml` に定義されたRuffとBlackのルールに準拠していますか？
    - 新しい依存関係は適切に追加されていますか？
2.  **JavaScript/TypeScript (`frontend/`):**
    - `eslint.config.js` (Flat Config) とPrettierのルールに準拠していますか？
    - Bunの利用方法（`package.json`のスクリプトなど）に問題はありませんか？
3.  **全体:**
    - コードの品質、潜在的なバグ、パフォーマンス、セキュリティ、可読性の観点で改善点はありますか？

もし問題がなければ、「指摘事項はありません。素晴らしい変更です！」と簡潔に述べてください。

--- コード差分 ---
{}""".format(diff_content)
    
    # Gemini API呼び出し
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    # ... (API呼び出し処理)
```

##### 4. AI レビュー実行

```yaml
- name: Run AI review
  if: steps.get-diff.outputs.has_changes == 'true'
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_REPOSITORY: ${{ github.repository }}
    PR_NUMBER: ${{ github.event.pull_request.number }}
  run: |
    if [ -z "$GEMINI_API_KEY" ]; then
      echo "⚠️ GEMINI_API_KEY is not set. Skipping AI review."
      echo "Please set the GEMINI_API_KEY secret in your repository settings."
      exit 0
    fi
    python review.py
```

**実行内容:**
- GEMINI_API_KEY の存在確認
- 未設定の場合は適切なメッセージで終了
- Gemini APIにレビューリクエスト送信
- レビュー結果をPRコメントに投稿

### エラーハンドリング

```python
# API関連エラー
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return "⏱️ APIリクエストがタイムアウトしました。後ほど再試行してください。"
except requests.exceptions.RequestException as e:
    return f"❌ APIリクエストエラー: {str(e)}"
except Exception as e:
    return f"❌ 予期しないエラー: {str(e)}"
```

## 🔧 ワークフロー設定のカスタマイズ

### パス指定の変更

```yaml
# より細かいパス指定
paths:
  - 'backend/src/**'
  - 'backend/tests/**'
  - 'backend/pyproject.toml'
  
# 除外パス指定
paths-ignore:
  - 'backend/docs/**'
  - 'backend/scripts/**'
```

### ブランチ戦略の変更

```yaml
# 特定ブランチのみ
branches:
  - main
  - develop
  - 'release/**'

# 特定ブランチを除外
branches-ignore:
  - 'feature/**'
  - 'hotfix/**'
```

### マトリックス戦略

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

## 📊 ワークフロー監視とメトリクス

### 実行時間の最適化

| 最適化手法 | 効果 | 実装方法 |
|-----------|------|----------|
| **キャッシュ** | 30-60%短縮 | 依存関係キャッシュ |
| **並列実行** | 40-70%短縮 | マトリックス戦略 |
| **条件分岐** | 状況による | パス・ブランチフィルタ |

### キャッシュ設定例

```yaml
# Python依存関係キャッシュ
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-uv-

# Bun依存関係キャッシュ  
- name: Cache Bun dependencies
  uses: actions/cache@v3
  with:
    path: ~/.bun/install/cache
    key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lockb') }}
    restore-keys: |
      ${{ runner.os }}-bun-
```

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. 権限エラー

```yaml
# 解決方法: 適切な権限設定
permissions:
  contents: write          # リポジトリ書き込み
  pull-requests: write     # PR操作
  actions: read           # Action実行ログ読み取り
```

#### 2. タイムアウトエラー

```yaml
# 解決方法: タイムアウト時間延長
- name: Long running task
  run: |
    # 長時間実行タスク
  timeout-minutes: 30      # デフォルト: 6分
```

#### 3. 並行実行制限

```yaml
# 解決方法: 同時実行制御
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## 📚 参考リンク

- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [ワークフロー構文](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [アクションマーケットプレイス](https://github.com/marketplace?type=actions)
- [Gemini API ドキュメント](https://ai.google.dev/docs)

---

💡 **運用のコツ**: ワークフローの実行時間とリソース使用量を定期的に監視し、必要に応じてキャッシュや並列化で最適化しましょう。