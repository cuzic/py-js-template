# Python + JavaScript フルスタックテンプレート

🚀 **2025年対応のモダンなベストプラクティスを採用したプロダクション対応フルスタックテンプレート**

PythonバックエンドとJavaScript/TypeScriptフロントエンドでフルスタックアプリケーションを構築するための包括的で実戦テスト済みのテンプレート。開発者体験、コード品質、プロダクション対応を重視して設計されています。

## ⭐ 主要機能

### 🐍 **モダンなPythonバックエンド**
- **Python 3.13+** 型ヒントと厳密なmypyチェック対応
- **Hatch + UVパッケージマネージャー** 環境分離・高速依存関係管理・PyPI自動公開
- **Ruff** 高速リンティング・フォーマット（Black、Flake8、isortを統合）
- **Pytest** 非同期対応・並列実行・BDDスタイルテスト
- **プロトコルベースアーキテクチャ** 依存性注入とテスト容易性
- **包括的エラーハンドリング** カスタム例外クラス

### 📜 **モダンなJavaScriptフロントエンド**
- **React 18** TypeScript・モダンJSX変換対応
- **Vite** 高速開発・最適化ビルド
- **Bun** 統合パッケージマネージャー・ランタイム
- **ESLint 9** フラット設定・厳密TypeScriptルール
- **Prettier** 一貫したコードフォーマット
- **Vitest** React Testing Libraryによる単体・統合テスト

### 🔧 **開発者体験**
- **DevContainer** 一貫した開発環境サポート
- **VS Code** 最適化された設定・拡張機能
- **Pre-commitフック** 自動フォーマット・品質チェック
- **自動コードステージング** フォーマット変更後の自動追加
- **多言語サポート** （Python、JavaScript/TypeScript、ドキュメント）
- **包括的リンティング** 自動修正機能
- **型安全性** スタック全体での型安全保証

### 🚀 **CI/CD・品質管理**
- **分離ワークフローアーキテクチャ** 最適性能・保守性
- **高速CIチェック**（2-3分）基本品質ゲート・ブランチ保護
- **詳細品質分析**（8-10分）包括的レポート
- **自動監視** Issue作成・アラートシステム
- **CIスキップ機能** 軽微な変更対応（[skip-ci]タグ・skip-ciラベル）
- **セキュリティスキャン** Bandit・依存関係自動更新
- **コードカバレッジ** 詳細レポート追跡
- **AI駆動コードレビュー** Gemini統合

## 🏗️ プロジェクト構造

```
├── 📁 backend/          # Pythonバックエンド
│   ├── 📁 src/backend/  # ソースコード
│   │   ├── __init__.py
│   │   ├── main.py      # アプリケーションエントリーポイント
│   │   ├── exceptions.py # カスタム例外
│   │   ├── 📁 models/   # データモデル
│   │   └── 📁 services/ # ビジネスロジック
│   ├── 📁 tests/        # テストスイート
│   ├── pyproject.toml   # 依存関係・ツール設定
│   └── uv.lock         # 再現可能ビルド用ロックファイル
│
├── 📁 frontend/         # JavaScript/Reactフロントエンド
│   ├── 📁 src/          # ソースコード
│   │   ├── App.tsx      # メインアプリケーションコンポーネント
│   │   ├── main.tsx     # アプリケーションエントリーポイント
│   │   └── 📁 components/ # 再利用可能UIコンポーネント
│   ├── 📁 tests/        # テストスイート
│   ├── package.json     # 依存関係・スクリプト
│   ├── bun.lockb       # Bunロックファイル（生成）
│   ├── vite.config.ts   # Vite設定
│   ├── tsconfig.json    # TypeScript設定
│   └── eslint.config.js # ESLintフラット設定
│
├── 📁 .devcontainer/    # 開発コンテナ
├── 📁 .github/workflows/ # CI/CDパイプライン
├── 📁 .vscode/          # VS Code設定
└── 📁 docs/             # ドキュメント
```

## 🚀 クイックスタート

### オプション1: DevContainerとmise（AI安全性のため推奨）

1. **前提条件**: [VS Code](https://code.visualstudio.com/) + [Dev Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) + [Docker](https://www.docker.com/)

2. **DevContainerで開く**:
   ```bash
   git clone <your-repo>
   code <repo-name>
   # Ctrl+Shift+P → "Dev Containers: Reopen in Container"を実行
   ```

3. **AI安全な開発環境**:
   - **Dockerfileレス**: DevContainer Featuresによるmise統合
   - **ツールバージョン統一**: ローカルmise・CI環境と同一バージョン
   - **安全なAIコード実行**: AI生成コードは隔離コンテナで実行
   - **自動設定**: ツール・依存関係・サービスが即座に利用可能

### オプション2: miseによるローカル開発

1. **前提条件**: 統合ツール管理のため[mise](https://mise.jdx.dev/)をインストール

2. **シェル設定**（一回のみ）:
   ```bash
   # シェル設定ファイル（~/.bashrc、~/.zshrcなど）に追加
   echo 'eval "$(mise activate bash)"' >> ~/.bashrc  # bash用
   echo 'eval "$(mise activate zsh)"' >> ~/.zshrc    # zsh用

   # またはPATHに直接shimを追加
   echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> ~/.bashrc

   # シェル再起動または設定読み込み
   source ~/.bashrc  # または source ~/.zshrc
   ```

3. **クローン・セットアップ**:
   ```bash
   git clone <your-repo>
   cd <repo-name>

   # 必要なツール全てをインストール（ランタイム + 開発ツール）
   mise install
   ```

4. **プロジェクト依存関係インストール**:
   ```bash
   # バックエンドセットアップ
   cd backend
   uv sync --all-extras

   # フロントエンドセットアップ
   cd frontend
   bun install
   ```

> **mise統合ツール管理**: このプロジェクトは`mise.toml`で全ての開発ツールを管理：
> - **ランタイム**: Python 3.13.5、Node.js 20.11.0、Bun 1.1.42
> - **Pythonツール**: **Hatch**、Black、Ruff、MyPy、pytest、Bandit（pipx経由）
> - **JS/TSツール**: TypeScript、ESLint、Prettier、Vite（mise経由bunでインストール）
> - **パッケージマネージャー**: **uv**（Python）、GitHub CLI
>
> **ツール管理ルール**:
> - ✅ PATH設定なしで`mise exec -- <tool>`を使用
> - ✅ グローバルツールは全てmiseでbunバックエンド管理
> - ✅ プロジェクト依存関係はuv（Python）・bun（JavaScript）で管理
> - ✅ 全JavaScriptツールでbunバックエンド有効（`mise settings set npm.bun true`）
> - ❌ 開発ツール用に`npm install -g`や`pip install --user`は使用禁止（miseとbunを使用）

## 🛠️ 開発コマンド

### Pre-commitフック（推奨）
```bash
# Pre-commitフックセットアップ（一回のみ）
mise exec -- pre-commit install
mise exec -- pre-commit install --hook-type commit-msg

# 全ファイル自動フォーマット・チェック
mise exec -- pre-commit run --all-files

# 通常のコミット（自動フォーマット実行）
git add . && git commit -m "feat: add new feature"

# 特定ツールの手動フォーマット
mise exec -- pre-commit run ruff-format
mise exec -- pre-commit run prettier
```

### Pythonバックエンド

#### 🚀 Hatch統合コマンド（推奨）
```bash
cd backend

# === 開発環境（デフォルト） ===
hatch run lint              # 全品質チェック（リント・フォーマット・型チェック）
hatch run lint-fix          # 自動修正
hatch run test              # テスト実行（カバレッジ付き）
hatch run security          # セキュリティスキャン
hatch run all-checks        # 全チェック実行

# === CI/CD環境（高速） ===
hatch run ci:check-format   # フォーマットチェック
hatch run ci:check-lint     # リントチェック
hatch run ci:check-types    # 型チェック
hatch run ci:test-parallel  # 並列テスト実行

# === マトリックステスト ===
hatch run test.py3.13:run   # Python 3.13でテスト
hatch run test.py3.12:run   # Python 3.12でテスト

# === パッケージビルド ===
hatch run build:clean       # ビルドクリーンアップ
hatch run build:build       # パッケージビルド
hatch run build:check       # パッケージ検証
```

#### ⚡ 直接コマンド（従来方式）
```bash
cd backend

# 品質チェック（uv経由）
uv run ruff check .          # コードリント
uv run ruff format .         # コードフォーマット
uv run mypy src             # 型チェック
uv run bandit -r src/       # セキュリティスキャン

# 代替: mise直接実行
mise exec -- ruff check backend/
mise exec -- mypy backend/src/

# テスト
uv run pytest              # テスト実行
uv run pytest --cov        # カバレッジ付き
uv run pytest -x           # 初回失敗で停止

# 全チェック
uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest
```

### JavaScriptフロントエンド
```bash
cd frontend

# 品質チェック（プロジェクト依存関係）
bun run lint:check          # リントチェック
bun run format:check        # フォーマットチェック
bun run typecheck          # TypeScriptチェック
bun run lint               # リント問題修正
bun run format             # コードフォーマット

# 代替: mise直接実行
mise exec -- eslint frontend/src/
mise exec -- prettier frontend/src/ --check
mise exec -- tsc --project frontend/tsconfig.json --noEmit

# 開発
bun run dev                # 開発サーバー起動
bun run build             # プロダクションビルド
bun run preview           # ビルドプレビュー

# テスト
bun run test              # テスト実行
bun run test:coverage     # カバレッジ付き
bun run test:watch        # ウォッチモード
```

## 🎯 コード品質基準

### Python
- **型ヒント必須** 全パブリック関数に必要
- **docstring必須** Googleスタイル使用
- **テストカバレッジ≥80%** 維持
- **セキュリティスキャン** Bandit使用
- **インポート整理**・フォーマット自動化

### JavaScript/TypeScript
- **厳密TypeScript** 設定
- **ESLintルール** Reactベストプラクティス
- **アクセシビリティチェック** jsx-a11y使用
- **一貫フォーマット** Prettier使用
- **インポート整理** 自動化

## 🚦 CI/CDワークフロー - 完全分離戦略

このテンプレートは最適なパフォーマンスと保守性のため**3層ワークフローアーキテクチャ**を実装：

### **第1層: CI専用ワークフロー** - 高速・必須（2-3分）
#### 🐍 Python CI (`python-ci-improved.yml`) - **Hatch + uv + mise統合**
- **ブランチ保護必須** - 失敗時マージブロック
- **Hatch環境管理** - CI専用環境で高速チェック
- **マトリックステスト** - Python 3.12 & 3.13並列実行
- **パッケージビルド** - 自動ビルド・検証・アーティファクト保存
- **PyPI自動公開** - mainブランチ時のTrusted Publishers使用
- **統合レポート** - PR統合結果の自動コメント
- **積極的キャッシュ** - mise/Hatch環境とuv依存関係

#### 📜 JavaScript CI (`js-ci-improved.yml`)
- **ブランチ保護必須** - 失敗時マージブロック
- ESLint基本ルール・Prettierフォーマット
- TypeScript型チェック
- Vitestカバレッジ付きテスト
- 基本ビルド検証

### **第2層: 品質分析ワークフロー** - 包括的・情報提供（8-10分）
#### 📊 Quality Analysis (`quality-analysis.yml`)
- **ノンブロッキング** - マージをブロックせず洞察を提供
- 詳細Python分析（Ruff統計、MyPy HTML、Banditレポート、複雑度分析）
- 詳細JavaScript分析（ESLint HTML、バンドル分析、依存関係監査）
- ダッシュボード生成による品質トレンド分析
- **週次スケジュール実行**（月曜日午前2時）+ 手動実行

### **第3層: 監視ワークフロー** - 自動・反応型（1-2分）
#### 🔍 Quality Monitor (`quality-monitor.yml`)
- **週次CI失敗分析**とIssue作成
- Pre-commitバイパス使用監視
- 品質トレンドレポート・アラート
- **週次スケジュール実行**（日曜日午前9時）+ 手動実行

### 🤖 Claude Code統合 (`claude.yml`)
- GitHub Issue/PRコメントで`@claude`メンションによる起動
- Claude AIによる自動コード生成・修正・レビュー
- self-hostedランナーでのセキュアな実行環境
- OAuthベースの認証でAPIキー管理

### ⏭️ CIスキップ機能
- **[skip-ci]タグ**: コミットメッセージに追加でpushイベントのCIスキップ
- **skip-ciラベル**: PRに追加でそのPR内全コミットのCIスキップ
- **メインブランチ保護**: スキップ設定に関わらずメインブランチでは常にCI実行
- **使用例**:
  ```bash
  # ドキュメント更新時のCIスキップ
  git commit -m "docs: Fix typo in README [skip-ci]"

  # ラベル使用によるPRのCIスキップ
  gh pr edit --add-label "skip-ci"
  ```

## 🗄️ AI安全な開発環境

### mise統合DevContainer

- **Dockerfileレス設定**: DevContainer Featuresによる簡素化セットアップ
- **統一ツールバージョン**: ローカルmise・CI環境と同一
- **AI安全性**: AI生成コードの隔離コンテナ実行
- **自動設定サービス**: 即座に利用可能な開発環境

### 開発サービス（オプション）
DevContainerは以下のサービスで拡張可能：
- **PostgreSQL**: バックエンド開発用データベース
- **Redis**: キャッシュ・セッションストレージ
- **自動サービス起動**と**データ永続化**

## 📚 アーキテクチャ原則

### バックエンドアーキテクチャ
- **プロトコルベース設計** テスト容易性・柔軟性
- **依存性注入** コンストラクタパラメータ経由
- **カスタム例外階層** 精密エラーハンドリング
- **サービス層パターン** ビジネスロジック分離
- **UTC タイムスタンプ** グローバル互換性

### フロントエンドアーキテクチャ
- **コンポーネント合成** 継承より優先
- **カスタムフック** 状態管理用
- **アクセシビリティファースト** 開発
- **TypeScript厳密モード** 型安全性
- **ビヘイビア駆動**テスト

## 🔒 セキュリティベストプラクティス

- **入力検証** サービス境界での実施
- **SQLインジェクション防止** パラメータ化クエリ使用
- **CSRF保護** 考慮事項
- **セキュアヘッダー** プロダクションビルド
- **依存関係脆弱性スキャン**
- **シークレット検出** CI/CDパイプライン

## 📖 ドキュメント

- [`docs/python-guide.md`](docs/python-guide.md) - Python開発ガイド
- [`docs/javascript-guide.md`](docs/javascript-guide.md) - JavaScript/Reactガイド
- [`docs/testing-guide.md`](docs/testing-guide.md) - テスト戦略
- [`docs/pre-commit-guide.md`](docs/pre-commit-guide.md) - Pre-commitフック設定・使用方法
- [`docs/workflows.md`](docs/workflows.md) - CI/CDドキュメント
- [`.devcontainer/README.md`](.devcontainer/README.md) - DevContainerセットアップ

## 🤝 コントリビューション

1. **確立されたパターンに従う** コードベース内の既存パターンを踏襲
2. **新機能にテストを書く** 全ての新機能にテストを作成
3. **重要な変更時はドキュメント更新** 大きな変更では対応ドキュメントを更新
4. **コミット前の品質チェック実行**:
   ```bash
   # バックエンド
   cd backend && uv run ruff check . && uv run mypy src && uv run pytest

   # フロントエンド
   cd frontend && bun run lint:check && bun run typecheck && bun test
   ```

## 🎯 プロダクションデプロイ

### バックエンドデプロイチェックリスト
- [ ] **Hatchパッケージビルド**: `hatch run build:build`
- [ ] **パッケージ検証**: `hatch run build:check`
- [ ] **PyPI公開設定**: Trusted Publishers環境設定
- [ ] データベースURL環境変数設定
- [ ] 適切なログレベル設定
- [ ] ヘルスチェックエンドポイント設定
- [ ] フロントエンドドメイン用CORS設定
- [ ] 監視・アラート設定

### フロントエンドデプロイチェックリスト
- [ ] API ベースURL設定
- [ ] 静的アセット用CDN設定
- [ ] CSPヘッダー設定
- [ ] エラートラッキング設定（Sentryなど）
- [ ] 必要に応じてアナリティクス設定

## 📄 ライセンス

このテンプレートは[MITライセンス](LICENSE)の下で公開されています。

---

**Happy coding!** 🚀

*このテンプレートは2025年時点のモダンなフルスタック開発のベストプラクティスを表しています。コード品質と開発者生産性を維持しながらプロジェクトとともに成長する堅実な基盤として設計されています。*
