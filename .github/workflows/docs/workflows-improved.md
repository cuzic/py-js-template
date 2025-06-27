# 改善されたGitHub Actionsワークフロー

このドキュメントでは、`docs/workflows.md`で解説されている改善版ワークフローの実装ファイルを提供します。

## 📁 ワークフローファイル一覧

### Python CI改善版 (`python-ci-improved.yml`)

このワークフローは以下の改善を実装しています：
- 検証のみ（自動修正なし）
- 最小権限の原則
- 依存関係キャッシュ
- マトリックステスト

詳細は `.github/workflows/python-ci-improved.yml` を参照してください。

### JavaScript CI改善版 (`js-ci-improved.yml`) 

このワークフローは以下の改善を実装しています：
- 検証のみ（自動修正なし）
- Bunによる高速インストール
- 依存関係キャッシュ
- マトリックステスト

詳細は `.github/workflows/js-ci-improved.yml` を参照してください。

### Gemini AIレビュー (`gemini-review.yml`)

`docs/ai-review.md`で解説されているGemini APIを使用したAIレビューの実装です：
- 汎用的な設定（GitHub Hosted Runner対応）
- 最小権限の原則
- エラーハンドリング

詳細は `.github/workflows/gemini-review.yml` を参照してください。

## 🚀 使用方法

1. **Gemini API キーの設定**
   ```
   GitHub Settings → Secrets → Actions → New repository secret
   Name: GEMINI_API_KEY
   Value: your-gemini-api-key
   ```

2. **ワークフローの有効化**
   - リポジトリにプッシュするだけで自動的に有効化されます
   - 必要に応じて `.github/workflows/` ディレクトリから不要なワークフローを削除してください

3. **Claude AI版の使用**
   - `claude.yml` はself-hosted runner用の特殊な設定です
   - 通常のGitHub環境では `gemini-review.yml` の使用を推奨します