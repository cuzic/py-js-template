# ⚙️ GitHub Actions ワークフロー解説（改良版）

このドキュメントでは、プロジェクトに設定されているGitHub Actionsワークフローについて詳しく説明します。

## 📋 ワークフロー概要

| ワークフロー | トリガー | 目的 | アプローチ | 実行時間目安 |
|-------------|----------|------|-----------|-------------|
| **Python CI** | `backend/` 変更時 | Python コード品質・テスト・ビルド | 統合CI | 2-3分 |
| **JavaScript CI (Improved)** | `frontend/` 変更時 | JS/TS コード品質・テスト | 検証専用 | 30秒-1分 |
| **AI Code Review (Improved)** | PR作成・更新時 | Gemini APIによる自動レビュー | 静的スクリプト | 30秒-1分 |

### 🚀 CI スキップ機能

軽微な変更（ドキュメント更新、タイポ修正など）でCI実行時間を節約できます：

| 方法 | 使用例 | 効果 |
|------|--------|------|
| **[skip-ci] タグ** | `git commit -m "docs: Update README [skip-ci]"` | pushイベントでCIスキップ |
| **skip-ci ラベル** | PRに `skip-ci` ラベルを追加 | PR全体でCIスキップ |
| **mainブランチ保護** | mainブランチでは常にCI実行 | 品質保証 |

## ⏭️ CI スキップ機能

軽微な変更（ドキュメント更新、タイポ修正など）でCI実行時間を節約できる機能を実装しています。

### 🎯 機能概要

| 機能 | 使用方法 | 適用範囲 | 安全性 |
|------|----------|----------|--------|
| **[skip-ci] タグ** | コミットメッセージに追加 | push イベント | main ブランチでは無効 |
| **skip-ci ラベル** | PR にラベル追加 | pull_request イベント | main ブランチでは無効 |
| **main ブランチ保護** | 自動適用 | main ブランチ | 常に CI 実行 |

### 💡 使用例

#### [skip-ci] タグでのスキップ
```bash
# ドキュメント更新時
git commit -m "docs: README のタイポ修正 [skip-ci]"
git push

# 結果: Python CI、JavaScript CI がスキップされる
```

#### skip-ci ラベルでのスキップ
```bash
# PR に skip-ci ラベルを追加
gh pr edit --add-label "skip-ci"

# 結果: そのPRの全ての push で CI がスキップされる

# CI を再実行したい場合
gh pr edit --remove-label "skip-ci"
```

### 🔒 安全性の確保

#### main ブランチでの強制実行
```yaml
# 実装されている条件判定
if: |
  github.ref == 'refs/heads/main' ||
  (github.event_name == 'pull_request' && !contains(github.event.pull_request.labels.*.name, 'skip-ci')) ||
  (github.event_name == 'push' && !contains(github.event.head_commit.message, '[skip-ci]'))
```

#### 適用シナリオ
- ✅ **推奨**: READMEやdocsの更新、コメント修正、タイポ修正
- ✅ **推奨**: 作業中PRでのテンポラリ的なスキップ
- ❌ **非推奨**: ロジック変更、新機能追加、バグ修正
- ❌ **無効**: main ブランチへのマージ（常に品質チェックを実行）

### 📊 効果測定

| 変更タイプ | 従来の実行時間 | スキップ後 | 節約効果 |
|-----------|---------------|------------|----------|
| ドキュメント更新 | 2-3分 | 10秒以下 | 90%以上短縮 |
| タイポ修正 | 2-3分 | 10秒以下 | 90%以上短縮 |
| コメント追加 | 2-3分 | 10秒以下 | 90%以上短縮 |

## 🛡️ セキュリティ原則

### 最小権限の原則 (Principle of Least Privilege)

**改良版ワークフローの重要な特徴**: 各ワークフローには、そのタスク遂行に**必要最小限の権限のみ**を付与します。

#### 従来版の問題点
```yaml
# ❌ 従来版: 過剰な権限
permissions:
  contents: write        # 自動コミットのため
  pull-requests: write   # コメント投稿のため
```

#### 改良版のアプローチ
```yaml
# ✅ 改良版: 最小権限
permissions:
  contents: read         # コード読み取りのみ
  pull-requests: read    # PR情報読み取りのみ
```

### セキュリティ上の利点

| 項目 | 従来版リスク | 改良版の対策 |
|------|-------------|-------------|
| **権限の悪用** | 書き込み権限による意図しない変更 | 読み取り専用でリスク最小化 |
| **コード改ざん** | 自動コミットによる予期しない変更 | 検証のみで改ざんリスク排除 |
| **セキュリティ侵害** | トークン権限の過剰な範囲 | 必要最小限の権限範囲 |

## 🐍 Python CI ワークフロー（Hatch + uv + mise統合版）

### 🚀 Hatch統合版の革新的改善

| 項目 | 従来版 | Hatch統合版 | 改善効果 |
|------|--------|-----------|----------|
| **環境管理** | `uv run` | **Hatch環境分離** | 専用環境で高速化 |
| **テスト戦略** | 単一実行 | **並列マトリックス** | Python 3.12/3.13同時 |
| **パッケージング** | 未対応 | **自動ビルド・検証** | 本格的PyPI公開 |
| **キャッシュ戦略** | 基本的 | **mise+Hatch積極的** | 30-60%高速化 |
| **実行フロー** | 2段階 | **4段階統合** | 品質・テスト・ビルド・公開 |
| **レポート** | 基本的 | **統合PR自動コメント** | 包括的結果表示 |

### ファイル: `.github/workflows/python-ci-improved.yml`

#### 🎯 Hatch統合CI/CD: 「4段階統合パイプライン」アプローチ

**Hatch統合版の核心理念**: 開発からプロダクション公開まで、**一貫したツールチェーンで完全自動化**を実現します。

#### ✅ Hatch統合版の利点
1. **環境分離**: CI・テスト・ビルド専用のHatch環境で干渉なし
2. **並列実行**: マトリックステストとマルチジョブで高速化
3. **パッケージング**: 自動ビルド・検証からPyPI公開まで完全対応
4. **統合レポート**: PR統合結果を自動コメントで包括的報告
5. **プロダクション対応**: Trusted Publishers使用の安全なPyPI公開

#### 実行ステップ詳細

##### 第1段階: 高速品質チェック（必須）

```yaml
jobs:
  quality-check:
    name: Quality Check (Lint, Type, Security)
    steps:
      - name: Setup mise (Python + uv + Hatch)
        uses: jdx/mise-action@v2
        with:
          cache: true  # mise環境・Hatch・uv依存関係の積極的キャッシュ

      - name: Install CI environment
        run: hatch env create ci

      - name: Check code formatting
        run: hatch run ci:check-format

      - name: Check linting
        run: hatch run ci:check-lint

      - name: Check type annotations
        run: hatch run ci:check-types

      - name: Security scan
        run: hatch run ci:check-security

      # === 品質チェックステップ ===
      - name: Check code formatting
        run: hatch run ci:check-format

      - name: Check linting
        run: hatch run ci:check-lint

      - name: Check type annotations
        run: hatch run ci:check-types

      - name: Security scan
        run: hatch run ci:check-security

      # === 統合テストステップ ===
      - name: Setup Python 3.13 environment
        run: hatch env create test.py3.13

      - name: Run parallel tests
        run: hatch run test.py3.13:run-parallel

      - name: Generate coverage report
        if: github.ref == 'refs/heads/main'
        run: hatch run test.py3.13:run-cov

      # === ビルド&パッケージステップ (mainブランチのみ) ===

```yaml
  build-test:
    steps:
      - name: Create build environment
        run: hatch env create build

      - name: Build package
        run: hatch run build:build

      - name: Check package
        run: hatch run build:check

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: python-package
          path: backend/dist/*
```

**第3段階の特徴:**
- **Hatchビルド環境**: `build`, `twine`, `wheel`依存関係
- **パッケージ検証**: `twine check`で配布準備確認
- **アーティファクト保存**: 30日間保持

##### 第4段階: PyPI自動公開（mainブランチのみ）

```yaml
  publish:
    if: github.ref == 'refs/heads/main'
    environment:
      name: pypi
      url: https://pypi.org/p/backend
    permissions:
      id-token: write  # Trusted Publishers
    steps:
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          verify-metadata: true
          skip-existing: true
```

**第4段階の特徴:**
- **Trusted Publishers**: APIキー不要の安全な認証
- **環境保護**: PyPI公開専用環境設定
- **自動スキップ**: 既存バージョンの重複回避

##### 第5段階: 統合レポート（PR統合結果）

```yaml
  integration-report:
    needs: [quality-check, matrix-test, build-test]
    if: always() && github.event_name == 'pull_request'
    steps:
      - name: Generate integration report
        run: |
          cat << 'EOF' > integration_report.md
          ## 🔍 Python CI統合レポート

          ### ✅ 実行されたチェック
          - **品質チェック**: ${{ needs.quality-check.result }}
          - **マトリックステスト**: ${{ needs.matrix-test.result }}
          - **ビルドテスト**: ${{ needs.build-test.result }}

          ### 📊 カバレッジレポート
          カバレッジレポートがアーティファクトとして保存されました。

          ### 🚀 次のステップ
          - mainブランチへのマージ後、PyPIへの自動公開が実行されます
          EOF

      - name: Comment PR with report
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `${{ steps.report.outputs.report_content }}`
            });
```

**第5段階の特徴:**
- **統合結果表示**: 全ジョブの成功・失敗状況を集約
- **自動PRコメント**: GitHub Scriptで結果を自動投稿
- **アーティファクト案内**: カバレッジレポートやビルド結果の保存場所案内

### 🎯 Hatch環境設定（pyproject.toml）

#### 環境分離戦略

```toml
# === CI/CD専用環境 ===
[tool.hatch.envs.ci]
dependencies = [
  "ruff>=0.8.0",
  "mypy>=1.15.0",
  "pytest>=8.0.0",
  "pytest-cov>=5.0.0",
  "pytest-xdist>=3.3.0",
  "bandit>=1.7.5",
]

[tool.hatch.envs.ci.scripts]
check-format = "ruff format --check --diff ."
check-lint = "ruff check ."
check-types = "mypy src"
check-security = "bandit -r src/"
test-ci = "pytest -v --cov=backend --cov-report=xml"
test-parallel = "pytest -n auto --cov=backend --cov-report=xml"

# === マトリックステスト環境 ===
[tool.hatch.envs.test]
dependencies = ["pytest>=8.0.0", "pytest-xdist>=3.3.0"]

[[tool.hatch.envs.test.matrix]]
python = ["3.12", "3.13"]

# === ビルド環境 ===
[tool.hatch.envs.build]
detached = true
dependencies = ["build", "twine", "wheel"]

[tool.hatch.envs.build.scripts]
build = "python -m build"
check = "twine check dist/*"
clean = "rm -rf dist/ build/ *.egg-info/"
```

### 🚀 統合CIの主要な特徴

| 特徴 | 説明 | 利点 |
|------|------|------|
| **単一ジョブ実行** | 全タスクを1つのジョブで順次実行 | シンプルで理解しやすい |
| **条件付き実行** | mainブランチ限定機能を効率的に制御 | PR高速化とリソース節約 |
| **キャッシュ最適化** | mise/Hatch環境の効率的な再利用 | 実行時間短縮 |
| **統合レポート** | 実行結果をPRに自動コメント | 可視性向上 |
| **メンテナンス性** | 設定の一元管理 | 保守が容易 |

### 🛠️ 開発者向けワークフロー

#### CI失敗時の対応手順

```bash
# 1. ローカルで品質チェック実行
cd backend
uv run black --check --diff .      # フォーマット確認
uv run ruff check .               # リンティング確認
uv run mypy src                   # 型チェック
uv run bandit -r src/             # セキュリティチェック

# 2. 問題がある場合は修正
uv run black .                    # フォーマット自動修正
uv run ruff check --fix .         # リンティング自動修正

# 3. テスト実行
uv run pytest -v --cov=backend

# 4. 修正をコミット・プッシュ
git add .
git commit -m "fix: resolve code quality issues"
git push
```

#### pre-commit hooks の推奨

```bash
# プリコミットフックのインストール
cd backend
uv run pre-commit install

# 手動実行（すべてのファイル）
uv run pre-commit run --all-files
```

## 🟨 JavaScript CI ワークフロー（改良版）

### 📊 改良版の主な改善点

| 項目 | 従来版 | 改良版 | 改善効果 |
|------|--------|--------|----------|
| **アプローチ** | 条件付き自動修正 | **検証専用** | 複雑性排除 |
| **権限** | `contents: write` | **`contents: read`** | セキュリティ強化 |
| **実行時間** | 1-2分 | **30秒-1分** | キャッシュとBun高速化 |
| **並列性** | なし | **Node.js バージョンマトリックス** | 互換性保証 |
| **チェック項目** | 基本項目 | **アクセシビリティ追加** | 品質向上 |

### ファイル: `.github/workflows/js-ci-improved.yml`

#### 改良版の実行ステップ

##### 1. 高速化された環境セットアップ（mise-action統合）

```yaml
- name: Checkout code
  uses: actions/checkout@v4

- name: Setup mise
  uses: jdx/mise-action@v2
  with:
    version: 2025.6.8
    install: true
    cache: true
    experimental: true

# mise-actionがNode.js, Bun, その他ツールを自動セットアップ
# キャッシュも自動管理
```

**改善点:**
- **キャッシュ導入**: 依存関係インストールを大幅高速化
- **frozen-lockfile**: 一貫性のあるインストール保証

##### 2. 包括的品質チェック（検証専用）

```yaml
# ✅ 検証のみ - 修正は行わない
- name: Check formatting with Prettier
  run: bun run format:check

- name: Check linting with ESLint
  run: bun run lint --max-warnings 0

- name: Type check with TypeScript
  run: bun run typecheck

- name: Check accessibility rules
  run: bun run security:check

- name: Run tests
  run: bun run test --run

- name: Run tests with coverage
  run: bun run test:coverage

# 🆕 NEW: アクセシビリティテスト
- name: Run accessibility tests
  run: bun run test:a11y

- name: Build check
  run: bun run build
```

**改善点:**
- **複雑な条件分岐排除**: シンプルで予測可能な実行
- **アクセシビリティチェック**: jsx-a11y ルール検証とaxe-coreテスト
- **ビルドテスト**: 本番環境での問題を事前検出
- **カバレッジ統合**: Codecov連携でレポート可視化

##### 3. 互換性確保（マトリックス戦略）

```yaml
compatibility-check:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      node-version: ['18', '20', '21']

  steps:
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}

    - name: Build and test
      run: |
        bun run typecheck
        bun run build
        bun run test --run
```

**新機能:**
- **複数Node.jsバージョン**: 18, 20, 21で動作検証
- **将来性保証**: 新しいNode.jsバージョンとの互換性確保

## 🤖 Claude Code ワークフロー

### 📊 Claude Code統合の特徴

| 項目 | 説明 | メリット |
|------|------|----------|
| **トリガー方式** | `@claude`メンション | 必要時のみ実行 |
| **対応イベント** | Issue/PRコメント、レビュー | 柔軟な起動 |
| **実行環境** | self-hostedランナー | セキュア環境 |
| **認証方式** | OAuth（トークン管理） | APIキー不要 |
| **機能範囲** | コード生成・修正・レビュー | 包括的支援 |

### ファイル構成

- **ワークフロー**: `.github/workflows/claude.yml`
- **必要なシークレット**:
  - `CLAUDE_ACCESS_TOKEN`
  - `CLAUDE_REFRESH_TOKEN`
  - `CLAUDE_EXPIRES_AT`

### 🔄 使用方法

#### 1. Issueでの使用
```markdown
@claude このバグを修正してください

エラーメッセージ:
```
TypeError: Cannot read property 'map' of undefined
```

該当ファイル: src/components/UserList.tsx
```

#### 2. PRコメントでの使用
```markdown
@claude このPRのコードをレビューして、改善点を提案してください。
特にパフォーマンスとセキュリティの観点から確認をお願いします。
```

#### 3. PRレビューでの使用
```markdown
@claude この関数をより効率的に書き換えてください。
現在のアルゴリズムはO(n²)ですが、O(n log n)にできるはずです。
```

### 📋 ワークフローの詳細

#### トリガー条件

```yaml
jobs:
  claude:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review' && contains(github.event.review.body, '@claude')) ||
      (github.event_name == 'issues' && (contains(github.event.issue.body, '@claude') || contains(github.event.issue.title, '@claude')))
```

**対応イベント:**
- Issue作成時（タイトルまたは本文に`@claude`）
- Issueコメント時（`@claude`メンション）
- PRレビューコメント時（`@claude`メンション）
- PRレビュー時（`@claude`メンション）

#### 実行ステップ

##### 1. 環境準備

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 1

- name: claude debugging
  id: debug_claude
  run: |
    echo "$PATH"
    which claude
    CLAUDE_PATH=$(command -v claude)
    echo "Full path: $CLAUDE_PATH"
    ls -l "$CLAUDE_PATH"
    "$CLAUDE_PATH" --version
```

##### 2. Claude Code実行

```yaml
- name: Run Claude Code
  id: claude
  uses: cuzic/claude-code-action@main
  with:
    use_oauth: 'true'
    claude_access_token: ${{ secrets.CLAUDE_ACCESS_TOKEN }}
    claude_refresh_token: ${{ secrets.CLAUDE_REFRESH_TOKEN }}
    claude_expires_at: ${{ secrets.CLAUDE_EXPIRES_AT }}
    allowed_tools: "Bash(curl:*),Bash(wget:*),Bash(npm:*),Bash(git:*)"
```

### 🔐 セキュリティ設定

#### 必要な権限

```yaml
permissions:
  contents: write      # コード変更のため
  pull-requests: write # PR操作のため
  issues: write        # Issue操作のため
  id-token: write      # OIDC認証のため
```

#### 許可されたツール

現在の設定では以下のコマンドが許可されています：
- `curl`: API呼び出しやダウンロード
- `wget`: ファイルダウンロード
- `npm`: パッケージ管理
- `git`: バージョン管理操作

### 🧪 ローカルでのテスト方法

```bash
# 1. Claude CLIのインストール
mise install claude@latest

# 2. 認証設定
claude auth login

# 3. ローカル実行テスト
claude "このプロジェクトの構造を説明してください"
```

### よくある使用例

#### 1. バグ修正
```markdown
@claude

ユーザーリストが表示されない問題を修正してください。
コンソールに以下のエラーが出ています：

```
Cannot read properties of undefined (reading 'map')
```

ファイル: frontend/src/components/UserList.tsx
```

#### 2. 機能追加
```markdown
@claude

UserListコンポーネントに検索機能を追加してください。
- リアルタイム検索
- 大文字小文字を区別しない
- 名前とメールアドレスで検索可能
```

#### 3. リファクタリング
```markdown
@claude

このコードをより読みやすく、保守しやすい形にリファクタリングしてください。
特に：
- 関数の分割
- 型の明確化
- エラーハンドリングの改善
```

### エラーハンドリング

Claude Codeが実行できない場合の一般的な原因：

1. **認証エラー**: トークンの期限切れ
2. **権限不足**: 必要な権限が設定されていない
3. **ランナー問題**: self-hostedランナーが利用不可
4. **APIレート制限**: 使用制限に到達
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
    python-version: ['3.13', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

## 📊 ワークフロー監視とメトリクス

### 実行時間の最適化

| 最適化手法 | 効果 | 実装方法 |
|-----------|------|----------|
| **キャッシュ** | 30-60%短縮 | 依存関係キャッシュ |
| **並列実行** | 40-70%短縮 | マトリックス戦略 |
| **条件分岐** | 状況による | パス・ブランチフィルタ |

### キャッシュ設定（mise-actionで自動管理）

```yaml
# mise-actionを使用する場合、キャッシュは自動的に管理されます
- name: Setup mise
  uses: jdx/mise-action@v2
  with:
    version: 2025.6.8
    install: true
    cache: true  # この設定でツールと依存関係のキャッシュが有効化
    experimental: true

# 以下のキャッシュが自動的に設定されます：
# - mise ツール自体のキャッシュ
# - Python/Node.js/Bunランタイムのキャッシュ
# - pipx でインストールされたツールのキャッシュ
# - bun でインストールされたグローバルツール（mise経由、npm.bun=true）のキャッシュ
```

## 🚨 トラブルシューティング（改良版対応）

### CI失敗時の診断・解決フロー

#### 🔍 Step 1: エラー種別の特定

| エラータイプ | CI出力の特徴 | 原因 | 解決方法 |
|--------------|-------------|------|----------|
| **フォーマットエラー** | `black --check failed` | コードスタイル不整合 | ローカルで `black .` 実行 |
| **リンティングエラー** | `ruff check failed` | コード品質問題 | ローカルで `ruff check --fix .` |
| **型エラー** | `mypy failed` | TypeScript/Python型不整合 | 型注釈の修正 |
| **テスト失敗** | `pytest/vitest failed` | ロジックエラー | テストコードとロジックの確認 |
| **依存関係エラー** | `install failed` | パッケージ設定問題 | `pyproject.toml`/`package.json`確認 |

#### 🛠️ Step 2: ローカルでの再現・修正

##### Python プロジェクト
```bash
# 1. CI と同じ環境で検証
cd backend
uv venv && uv pip install -e ".[dev]"

# 2. CIと同じチェックを実行
uv run black --check --diff .       # フォーマット確認
uv run ruff check .                 # リンティング確認
uv run mypy src                     # 型チェック
uv run bandit -r src/               # セキュリティチェック
uv run pytest -v                   # テスト実行

# 3. 問題を修正
uv run black .                      # 自動フォーマット
uv run ruff check --fix .           # 自動修正
```

##### JavaScript プロジェクト
```bash
# 1. CI と同じ環境で検証
cd frontend
bun install --frozen-lockfile

# 2. CIと同じチェックを実行
bun run format:check                # フォーマット確認
bun run lint --max-warnings 0      # リンティング確認
bun run typecheck                   # 型チェック
bun run test --run                  # テスト実行
bun run build                       # ビルド確認

# 3. 問題を修正
bun run format                      # 自動フォーマット
bun run lint:fix                    # 自動修正
```

### 改良版特有の問題と解決

#### 1. キャッシュ関連問題

```yaml
# 問題: キャッシュが破損・古い
# 解決方法: キャッシュクリア
- name: Clear cache (if needed)
  run: |
    # GitHubリポジトリ設定からActions cacheを手動削除
    # または以下のワークフロー追加
  if: github.event.inputs.clear_cache == 'true'
```

#### 2. 権限エラー（改良版）

```yaml
# ❌ 従来の過剰権限
permissions:
  contents: write
  pull-requests: write

# ✅ 改良版の最小権限
permissions:
  contents: read           # 読み取り専用
  pull-requests: read      # PR情報読み取り

# 注意: AIレビューでコメント投稿が必要な場合のみ
permissions:
  pull-requests: write     # コメント投稿用
```

#### 3. AI Review スクリプトエラー

```bash
# ローカルでのデバッグ方法
cd .github/scripts

# 1. スクリプト単体テスト
python review.py --help

# 2. 環境変数の確認
echo $GEMINI_API_KEY | head -c 10    # APIキー確認（最初の10文字のみ）

# 3. 差分ファイルの生成・テスト
git diff HEAD~1 > test_diff.txt
python review.py test_diff.txt --output debug_output.txt

# 4. エラーログの確認
python review.py test_diff.txt 2>&1 | tee error.log
```

### パフォーマンス最適化

#### 1. 実行時間短縮のための設定

```yaml
# 並列実行の活用
strategy:
  matrix:
    include:
      - python: '3.13'
        node: '20'
      - python: '3.12'
        node: '21'

# 条件付き実行
- name: Run expensive check
  if: contains(github.event.head_commit.message, '[full-check]')
  run: # 重いチェック処理
```

#### 2. リソース使用量の監視

```yaml
# メモリ・CPU使用量の監視
- name: Monitor resources
  run: |
    echo "CPU cores: $(nproc)"
    echo "Memory: $(free -h)"
    echo "Disk space: $(df -h)"
```

## 🔄 移行ガイド: 従来版→改良版

### 段階的移行アプローチ

#### Phase 1: 並行運用（リスク最小化）
1. 改良版ワークフローファイルを追加（`*-improved.yml`）
2. 従来版と改良版を並行実行
3. 改良版の動作確認・安定性確認
4. チーム全体での動作確認

#### Phase 2: 完全移行
1. 従来版ワークフローの無効化
2. 改良版ワークフローのファイル名変更
3. ドキュメント・README更新
4. チーム通知・トレーニング

### 移行チェックリスト

- [ ] 改良版ワークフローの動作確認
- [ ] キャッシュ機能の有効性確認
- [ ] 権限設定の適切性確認
- [ ] エラーハンドリングの動作確認
- [ ] チーム全体への移行通知
- [ ] 従来版ワークフローの削除

## 📚 参考リンク

### 公式ドキュメント
- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [ワークフロー構文リファレンス](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [セキュリティ強化ガイド](https://docs.github.com/en/actions/security-guides)
- [Gemini API ドキュメント](https://ai.google.dev/docs)

### ツール・ライブラリ
- [UV パッケージマネージャー](https://github.com/astral-sh/uv)
- [Bun JavaScript ランタイム](https://bun.sh/docs)
- [Ruff Python リンター](https://docs.astral.sh/ruff/)
- [ESLint Flat Config](https://eslint.org/docs/latest/use/configure/configuration-files-new)

### ベストプラクティス
- [CI/CD Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
- [Workflow Performance Optimization](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)

---

## 🎯 まとめ

### 改良版の主要な成果

✅ **セキュリティ強化**: 最小権限の原則適用で攻撃面を大幅縮小
✅ **運用安定性**: 検証専用アプローチで予期しない競合を排除
✅ **開発効率**: キャッシュ導入で実行時間を30-60%短縮
✅ **保守性向上**: 静的スクリプト分離でメンテナンスが容易
✅ **品質向上**: アクセシビリティ・セキュリティチェック追加

### 🚀 次のステップ

1. **改良版ワークフローの導入**: 段階的移行計画に沿って実装
2. **チーム教育**: 新しい開発フローの共有・トレーニング
3. **監視・最適化**: 実行時間・成功率の継続的モニタリング
4. **継続改善**: フィードバックを基にした更なる最適化

---

💡 **重要な原則**: CI/CDは「検証」に徹し、「修正」はローカル開発者が行う。この分離により、より予測可能で安全な開発環境を構築できます。
