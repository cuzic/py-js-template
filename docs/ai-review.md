# 🤖 Claude Code 設定ガイド

このガイドでは、Claude AIを使用した自動コード生成・修正・レビュー機能の設定と活用方法について説明します。

## 🎯 Claude Code 機能の概要

### 主な機能

- **コード生成**: 自然言語の指示からコードを自動生成
- **コード修正**: バグ修正や機能改善の自動実装
- **コードレビュー**: PRの変更内容に対する詳細なフィードバック
- **リファクタリング**: コードの品質改善と最適化

### 対応範囲

- **Python (`backend/`)**: uv、Ruff、MyPy、Pytestを使用した開発
- **JavaScript/TypeScript (`frontend/`)**: Bun、ESLint、Prettier、Vitestを使用した開発
- **全体**: ドキュメント作成、設定ファイル編集、CI/CD設定

## 🔧 セットアップ手順

### 1. Claude認証トークンの取得

#### Claude CLIでの認証

```bash
# 1. Claude CLIをインストール（miseを使用）
mise install claude@latest

# 2. ログインして認証
claude auth login

# 3. トークン情報を確認
claude auth status
```

#### 必要なトークン情報

認証後、以下の3つのトークンが生成されます：
- `CLAUDE_ACCESS_TOKEN`: アクセストークン
- `CLAUDE_REFRESH_TOKEN`: リフレッシュトークン
- `CLAUDE_EXPIRES_AT`: トークン有効期限

### 2. GitHub Secrets の設定

#### リポジトリでのSecret設定

1. GitHubリポジトリページを開く
2. **Settings** タブに移動
3. 左メニューから **Secrets and variables** → **Actions** を選択
4. **New repository secret** をクリック
5. 以下の3つのシークレットを設定：

| Secret名 | 説明 | 取得方法 |
|---------|------|----------|
| `CLAUDE_ACCESS_TOKEN` | アクセストークン | `claude auth status`で確認 |
| `CLAUDE_REFRESH_TOKEN` | リフレッシュトークン | `claude auth status`で確認 |
| `CLAUDE_EXPIRES_AT` | トークン有効期限 | `claude auth status`で確認 |

### 3. Self-hosted ランナーの設定（必要な場合）

現在のワークフローは`self-hosted`ランナーを使用しています。GitHub Actionsのホストランナーを使用する場合は、`.github/workflows/claude.yml`の以下の行を変更：

```yaml
# 変更前
runs-on: self-hosted

# 変更後
runs-on: ubuntu-latest
```

## 📝 使用方法

### Issue での使用

新しいIssueを作成、またはコメントで`@claude`をメンション：

```markdown
@claude

以下のエラーを修正してください：

エラー内容：
```
TypeError: Cannot read property 'map' of undefined
at UserList.render (UserList.tsx:25)
```

このエラーは、ユーザーデータが取得される前にレンダリングが実行されているようです。
```

### Pull Request での使用

#### PRコメントでのレビュー依頼

```markdown
@claude このPRの変更をレビューしてください。
特に以下の点を重点的に確認してください：
- セキュリティの観点
- パフォーマンスへの影響
- コードの可読性
```

#### 特定のコード部分の改善依頼

```markdown
@claude この関数をより効率的に書き換えてください。
現在のアルゴリズムの計算量はO(n²)ですが、O(n log n)で実装できるはずです。
```

## 🎯 効果的な使い方のコツ

### 1. 具体的な指示を出す

❌ 悪い例：
```
@claude これを修正して
```

✅ 良い例：
```
@claude UserListコンポーネントで、ユーザーデータが空の場合に
"データがありません"というメッセージを表示するように修正してください。
Material-UIのTypographyコンポーネントを使用してください。
```

### 2. コンテキストを提供する

```markdown
@claude

背景：現在、ユーザー一覧ページの読み込みが遅いという問題があります。

課題：
- 初回レンダリング時に全ユーザーデータを取得している
- ページネーションが実装されていない

改善依頼：
- ページネーション機能を追加してください（1ページ20件）
- 無限スクロールまたはページ番号での実装を選択してください
- パフォーマンスを考慮した実装をお願いします
```

### 3. 段階的な依頼

大きな変更は段階的に依頼する：

```markdown
@claude

ステップ1: UserListコンポーネントに検索機能のUIを追加してください。
Material-UIのTextFieldを使用して、上部に検索ボックスを配置してください。
```

実装後：

```markdown
@claude

ステップ2: 先ほど追加した検索ボックスに、実際の検索機能を実装してください。
- リアルタイム検索（デバウンス付き）
- 名前とメールアドレスでの検索
- 大文字小文字を区別しない
```

## 🚀 ベストプラクティス

### テスト駆動での実装依頼

```markdown
@claude

UserListコンポーネントのテストを追加してください：
1. まず、以下のケースをカバーするテストを作成
   - データが正常に表示される
   - 空のデータの場合の表示
   - エラー時の表示
2. その後、テストが通るように実装を修正
```

### リファクタリング依頼

```markdown
@claude

backend/src/services/user_service.pyをリファクタリングしてください：
- 大きな関数を小さく分割
- 型ヒントを追加
- エラーハンドリングを改善
- docstringを追加
既存の機能は変更しないでください。
```

## ⚠️ 注意事項

### セキュリティ

- 機密情報（APIキー、パスワード等）をコメントに含めない
- 生成されたコードのセキュリティを必ず確認する
- 外部APIの認証情報は環境変数を使用する

### 制限事項

- 大規模な変更は複数の小さなタスクに分割する
- 実行時間の長い処理は避ける
- 生成されたコードは必ずレビューする

### トラブルシューティング

#### トークンの期限切れ

```bash
# トークンを再取得
claude auth login

# GitHub Secretsを更新
# 新しいトークン情報で3つのSecretを更新
```

#### ワークフローが起動しない

- `@claude`メンションが含まれているか確認
- ワークフローの権限設定を確認
- self-hostedランナーの状態を確認

## 📚 関連リンク

- [Claude Code公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Action](https://github.com/cuzic/claude-code-action)
- [ワークフロー設定](workflows.md#-claude-code-ワークフロー)
