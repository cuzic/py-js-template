# DevContainer 設定

このディレクトリには、VS Code DevContainer でこのプロジェクトを開発するための設定が含まれています。

## 🚀 クイックスタート

1. **前提条件**:
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **DevContainer で開く**:
   - このプロジェクトを VS Code で開く
   - `Ctrl+Shift+P` (Mac の場合は `Cmd+Shift+P`) を押す
   - 「Dev Containers: Reopen in Container」と入力
   - コマンドを選択してコンテナの構築を待つ

## 📦 含まれる内容

### 🔧 mise による統合ツール管理
- **mise 2024.12+** による一元的なツールバージョン管理
- **Dockerfileless 設定** - DevContainer Features を使用
- **AI 安全環境** - 分離されたコンテナ実行環境
- **バージョン統一** - ローカル・CI・DevContainer で同一環境

### 🐍 Python 環境
- **Python 3.13.5** (mise 管理)
- **UV パッケージマネージャー** (mise 管理)
- **事前インストールツール**: ruff, mypy, pytest, bandit
- **拡張機能**: Python, Ruff, MyPy Type Checker

### 📜 JavaScript 環境  
- **Node.js 20.11.0** (mise 管理)
- **Bun 1.1.42** (mise 管理)
- **事前インストールツール**: ESLint, Prettier, TypeScript
- **拡張機能**: ESLint, Prettier, TypeScript

### 🛠️ 開発ツール
- **Git** with GitHub CLI
- **Docker-in-Docker** サポート
- **DevContainer Features**: 簡素化された設定
- **Shell**: Bash (mise アクティベーション設定済み)

### 🔌 VS Code 拡張機能
- Python 開発: Python, Ruff, MyPy
- JavaScript 開発: ESLint, Prettier, TypeScript  
- Git: GitLens
- 生産性: GitHub Copilot, Todo Highlight
- Docker: Docker 拡張機能

## 🌐 ポートフォワーディング

以下のポートが自動的にフォワードされます:

| ポート | サービス | 説明 |
|------|---------|-------------|
| 3000 | Frontend | React 開発サーバー |
| 5173 | Vite | 代替開発サーバー |  
| 8000 | Backend | Python API サーバー |
| 8080 | Alternative | 代替サーバー |

## ⚡ クイックコマンド

コンテナには便利なエイリアスが含まれています:

### Python コマンド
```bash
lint-py    # Python コード品質チェック
fix-py     # Python 問題の自動修正
test-py    # Python テスト実行
```

### JavaScript コマンド
```bash
lint-js    # JavaScript コード品質チェック
fix-js     # JavaScript 問題の自動修正  
test-js    # JavaScript テスト実行
dev-js     # フロントエンド開発サーバー起動
```

### Git コマンド
```bash
gs         # git status
ga         # git add
gc         # git commit
gp         # git push
gl         # git log --oneline -10
```

### mise コマンド
```bash
ms         # mise ls (インストールされたツール一覧)
msi        # mise install
msu        # mise use
```

## 📁 ファイル構造

```
.devcontainer/
├── devcontainer.json     # メイン設定 (Dockerfileless)
├── setup.sh            # 作成後セットアップスクリプト
├── post-start.sh       # 開始後スクリプト
└── README.md           # このファイル
```

## 🔧 カスタマイズ

### 拡張機能の追加
`devcontainer.json` を編集して、`extensions` 配列に拡張機能 ID を追加:

```json
"extensions": [
  "your.extension.id"
]
```

### Features の追加
`devcontainer.json` の `features` セクションに新しい Feature を追加:

```json
"features": {
  "ghcr.io/devcontainers/features/your-feature:1": {}
}
```

### 環境変数
`devcontainer.json` で環境変数を追加:

```json
"containerEnv": {
  "YOUR_VAR": "value"
}
```

## 🐛 トラブルシューティング

### コンテナが構築できない
1. Docker Desktop が動作していることを確認
2. 再構築を試す: `Ctrl+Shift+P` > "Dev Containers: Rebuild Container"
3. VS Code ターミナルで Docker ログを確認

### 依存関係の不足
セットアップスクリプトがすべての依存関係をインストールします。何か不足している場合:
1. コンテナを再開: `Ctrl+Shift+P` > "Dev Containers: Reopen in Container"
2. 手動実行: `cd backend && uv sync --all-extras`
3. または: `cd frontend && bun install`

### mise ツールの問題
```bash
# ツール状況確認
mise ls

# 再インストール
mise install

# mise 診断
mise doctor
```

### パフォーマンスの問題
1. Docker Desktop に十分なメモリが割り当てられていることを確認 (4GB+)
2. Volume マウントの使用を検討
3. 未使用の VS Code ウィンドウを閉じる

## 💡 Tips

1. **統合ターミナルの使用**: `Ctrl+Shift+\`` 
2. **クイックファイル検索**: `Ctrl+P`
3. **コマンドパレット**: `Ctrl+Shift+P`
4. **Git 操作**: ソースコントロールパネルを使用 (`Ctrl+Shift+G`)
5. **拡張機能**: 拡張機能パネルを参照 (`Ctrl+Shift+X`)
6. **mise ツール確認**: `mise ls` でインストール済みツール一覧

## 🔒 AI 安全開発環境

### 主な安全機能
- **分離実行環境**: AI生成コードの安全な実行
- **統一ツールバージョン**: ローカル・CI・DevContainer で完全同一
- **Dockerfileless 設定**: 保守しやすい設定
- **自動設定**: mise による自動ツールインストール

### セキュリティベストプラクティス
- コンテナ内での分離実行
- ホスト環境の保護
- 統一開発環境による予測可能性
- 自動依存関係管理

## 🔄 更新

DevContainer を更新するには:
1. 設定ファイルを変更
2. コンテナを再構築: `Ctrl+Shift+P` > "Dev Containers: Rebuild Container"
3. mise ツールの更新: `mise install` または `mise upgrade`

## 📚 詳細情報

- [VS Code DevContainers ドキュメント](https://code.visualstudio.com/docs/remote/containers)
- [DevContainer Features](https://containers.dev/features)
- [mise ドキュメント](https://mise.jdx.dev/)
- [AI 安全開発ガイド](https://sreake.com/blog/safe-universal-dev-env-with-devcontainer-mise/)

---

💡 **開発のコツ**: この DevContainer 環境は AI 生成コードの安全な実行と、チーム全体での統一された開発体験を提供します。mise によりツールバージョンが完全に統一されているため、環境差異による問題は発生しません。