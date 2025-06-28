# Documentation

このディレクトリには、プロジェクトのコーディング規約、テスト、リンティングに関するドキュメントが含まれています。

## 📋 ドキュメント一覧

### 開発ガイドライン
- [🐍 **Python開発ガイド**](./python-guide.md) - Python開発のための包括的なガイド
- [🟨 **JavaScript/TypeScript開発ガイド**](./javascript-guide.md) - フロントエンド開発のための詳細ガイド

### 品質管理
- [🔍 **リンティングルール**](./linting-rules.md) - 両言語の詳細なリンティング設定
- [🔧 **Pre-commit ガイド**](./pre-commit-guide.md) - 自動フォーマッティングとコード品質チェック
- [🧪 **テスト戦略**](./testing-guide.md) - テストの書き方とベストプラクティス

### CI/CD
- [⚙️ **ワークフロー解説**](./workflows.md) - GitHub Actionsワークフローの詳細
- [🔄 **ワークフロー分離戦略**](./workflow-separation-strategy.md) - 完全分離アーキテクチャの詳細
- [🤖 **AI レビュー設定**](./ai-review.md) - Gemini APIによる自動コードレビュー

## 🚀 クイックスタート

新しい開発者がプロジェクトに参加する際は、以下の順序でドキュメントを読むことを推奨します：

1. **[Python開発ガイド](./python-guide.md)** または **[JavaScript開発ガイド](./javascript-guide.md)**
2. **[Pre-commit ガイド](./pre-commit-guide.md)** - 開発環境のセットアップ
3. **[テスト戦略](./testing-guide.md)**
4. **[ワークフロー解説](./workflows.md)**

## 📝 ドキュメントの更新

これらのドキュメントは開発チームが継続的に更新する必要があります：

- 新しいルールの追加時
- 技術スタックの変更時
- ベストプラクティスの発見時
- 問題の発生と解決時

---

💡 **Tip**: 各ドキュメントは実際の設定ファイル（`pyproject.toml`、`eslint.config.js`など）と連動しています。設定を変更した際は、対応するドキュメントも更新してください。