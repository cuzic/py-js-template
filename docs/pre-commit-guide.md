# 🔧 Pre-commit フック設定ガイド

このガイドでは、チーム全体でコーディングスタイルを統一するためのpre-commitフック設定について説明します。

## 🎯 概要

このプロジェクトでは、コミット前に自動的にコードフォーマッティングと品質チェックを行うpre-commitフックが設定されています。これにより、チーム全体で一貫したコーディングスタイルを維持できます。

### ✨ 主な機能

- **自動フォーマッティング**: コミット前にコードが自動的にフォーマットされる
- **品質チェック**: リンティング、型チェック、セキュリティ検査が自動実行
- **多言語対応**: Python、JavaScript/TypeScript、ドキュメントを包括的にサポート
- **自動ステージング**: フォーマット後のファイルが自動的にステージングされる

## 🛠️ 設定内容

### Python フック

| フック | 説明 | 自動修正 |
|--------|------|----------|
| **Ruff** | 高速リンティング＆フォーマッティング | ✅ |
| **Black** | コードフォーマッティング（fallback） | ✅ |
| **MyPy** | 静的型チェック | ❌ |
| **Bandit** | セキュリティ検査 | ❌ |

### JavaScript/TypeScript フック

| フック | 説明 | 自動修正 |
|--------|------|----------|
| **Prettier** | コードフォーマッティング | ✅ |
| **ESLint** | リンティングと最適化 | ✅ |

### 一般的なフック

| フック | 説明 | 自動修正 |
|--------|------|----------|
| **trailing-whitespace** | 行末空白の削除 | ✅ |
| **end-of-file-fixer** | ファイル末尾改行の修正 | ✅ |
| **check-yaml/json/toml** | 設定ファイルの構文チェック | ❌ |
| **conventional-pre-commit** | コミットメッセージ形式チェック | ❌ |

## 🚀 セットアップ

### 1. 初回セットアップ

```bash
# mise でツールをインストール
mise install

# pre-commit フックをインストール
mise exec -- pre-commit install
mise exec -- pre-commit install --hook-type commit-msg

# 初回実行（すべてのファイルに適用）
mise exec -- pre-commit run --all-files
```

### 2. 設定ファイル

プロジェクトのpre-commit設定は `.pre-commit-config.yaml` で管理されています：

```yaml
repos:
  # 基本的なGitフック
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      # ... その他

  # Python フォーマッティング（Ruff）
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.1
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # JavaScript/TypeScript フォーマッティング
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        additional_dependencies:
          - prettier@3.6.2
```

## 💻 使用方法

### 通常のコミット

```bash
# ファイルを編集
vim backend/src/main.py
vim frontend/src/App.tsx

# 変更をステージング
git add .

# コミット（pre-commitフックが自動実行される）
git commit -m "feat: 新機能を追加"
```

### フォーマットが適用された場合

コミット時にフォーマッターがファイルを変更した場合：

```bash
$ git commit -m "feat: 新機能を追加"
ruff-format..............................................................Passed
prettier.................................................................Failed
- hook id: prettier
- files were modified by this hook

📄 変更されたファイル:
frontend/src/App.tsx

📦 変更をステージングに追加中...
✅ フォーマット済みファイルがステージングされました。再度コミットを実行してください。

# フォーマット済みファイルが自動ステージングされたので、再コミット
$ git commit -m "feat: 新機能を追加"
```

### 手動実行

特定のフックを手動で実行することも可能です：

```bash
# すべてのフックを実行
mise exec -- pre-commit run --all-files

# 特定のフックを実行
mise exec -- pre-commit run ruff-format
mise exec -- pre-commit run prettier

# 特定のファイルに対して実行
mise exec -- pre-commit run --files backend/src/main.py
```

## 🔧 カスタマイズ

### 除外パターンの追加

特定のファイルやディレクトリを除外したい場合：

```yaml
# .pre-commit-config.yaml
exclude: |
  (?x)^(
    .*\.min\.(js|css)$|
    .*\.map$|
    your_custom_exclude_pattern.*
  )$
```

### 新しいフックの追加

新しいフックを追加する場合：

```yaml
repos:
  - repo: https://github.com/your-organization/custom-hook
    rev: v1.0.0
    hooks:
      - id: custom-check
        name: Custom Check
        description: "カスタムチェック"
        files: ^your_pattern.*$
```

## 🛡️ セキュリティ

### Bandit による Python セキュリティチェック

```bash
# セキュリティ脆弱性をチェック
mise exec -- pre-commit run bandit-security

# 特定のファイルをチェック
mise exec -- bandit -r backend/src/
```

### 除外設定

false positiveを避けるため、テストファイルなどは除外されています：

```yaml
- id: bandit
  files: ^backend/src/.*\.py$
  exclude: ^backend/tests/
```

## 📊 パフォーマンス

### キャッシュ機能

pre-commitは環境をキャッシュするため、2回目以降の実行は高速です：

```bash
# キャッシュをクリア（必要な場合のみ）
mise exec -- pre-commit clean

# 環境を再構築
mise exec -- pre-commit install-hooks
```

### 並列実行

複数のフックが並列実行されるため、効率的です。

## 🐛 トラブルシューティング

### 問題1: フックが実行されない

```bash
# フックが正しくインストールされているか確認
ls -la .git/hooks/

# 再インストール
mise exec -- pre-commit uninstall
mise exec -- pre-commit install
```

### 問題2: 特定のフックでエラー

```bash
# 詳細ログで実行
mise exec -- pre-commit run --verbose

# 特定のフックをスキップ
SKIP=mypy git commit -m "commit message"
```

### 問題3: パフォーマンスが遅い

```bash
# 並列実行数を調整
mise exec -- pre-commit run --show-diff-on-failure

# 特定のファイルのみ実行
mise exec -- pre-commit run --files changed_file.py
```

## 🔄 CI/CD 統合

GitHub Actions でも同じフックが実行されます：

```yaml
# .github/workflows/pre-commit.yml
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
```

## 📚 参考リンク

- [pre-commit 公式ドキュメント](https://pre-commit.com/)
- [Ruff 設定ガイド](https://docs.astral.sh/ruff/)
- [Prettier 設定ガイド](https://prettier.io/docs/en/configuration.html)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

💡 **Pro Tip**: チーム全体で同じ開発環境を使用するため、DevContainer + mise の組み合わせを推奨します。これにより、全員が同じバージョンのツールを使用してpre-commitフックを実行できます。