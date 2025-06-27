# 🐍 Python 開発ガイド

このガイドでは、Pythonバックエンド開発における品質基準、コーディングルール、テスト戦略について説明します。

## 📦 技術スタック

- **パッケージマネージャー**: [uv](https://github.com/astral-sh/uv) - 超高速Pythonパッケージマネージャー
- **ビルドシステム**: [Hatchling](https://hatch.pypa.io/) - モダンなPythonビルドバックエンド
- **リンター**: [Ruff](https://github.com/astral-sh/ruff) - Rust製超高速リンター
- **フォーマッター**: [Black](https://github.com/psf/black) - 妥協のないコードフォーマッター
- **テストフレームワーク**: [pytest](https://docs.pytest.org/) - 柔軟で強力なテストフレームワーク

## 🏗️ プロジェクト構造

```
backend/
├── src/
│   └── backend/          # メインパッケージ
│       ├── __init__.py
│       └── main.py
├── tests/                # テストファイル
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml        # プロジェクト設定
└── .gitignore
```

### src layout の採用理由

- **import の明確化**: テスト時と実行時のimportが一致
- **パッケージング**: より良いwheel生成とディストリビューション
- **名前空間**: プロジェクト名との衝突を回避

## 🔧 環境設定

### 初期セットアップ

```bash
cd backend

# 仮想環境作成
uv venv

# 仮想環境の有効化
source .venv/bin/activate  # Linux/macOS
# または
.venv\Scripts\activate     # Windows

# 開発依存関係のインストール
uv pip install -e ".[dev]"
```

### 開発用コマンド

```bash
# リンティング
ruff check .

# 自動修正
ruff check --fix .

# フォーマット
black .

# フォーマットチェック
black --check .

# テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=backend --cov-report=html
```

## 📝 コーディングルール

### 1. 基本方針

- **PEP 8**: Pythonの標準スタイルガイドに準拠
- **型ヒント**: 関数の引数と戻り値には型ヒントを必須とする
- **ドキュメント**: パブリックな関数・クラスにはdocstringを記述
- **命名規則**: スネークケース（`snake_case`）を使用

### 2. 関数定義の例

```python
def calculate_sum(a: int, b: int) -> int:
    """二つの整数の和を計算します。
    
    Args:
        a: 第一の整数
        b: 第二の整数
        
    Returns:
        二つの整数の和
        
    Example:
        >>> calculate_sum(2, 3)
        5
    """
    return a + b
```

### 3. 禁止事項

- `print()` 文の使用（ログ出力には `logging` モジュールを使用）
- マジックナンバー（定数は適切な名前を付けて定義）
- 不要な変数代入（`return` 直前の代入は避ける）

### 4. 推奨事項

- **早期リターン**: ネストを浅くするため
- **リスト内包表記**: 単純な変換処理
- **型安全性**: `Union` より `Optional` を使用
- **例外処理**: 具体的な例外クラスをキャッチ

## 🔍 Ruff設定詳細

### 有効化されているルール（抜粋）

| カテゴリ | ルール | 説明 |
|---------|--------|------|
| **E/W** | pycodestyle | PEP 8スタイルガイド |
| **F** | pyflakes | 未使用import、変数など |
| **I** | isort | import文の並び順 |
| **UP** | pyupgrade | 新しい構文の使用推奨 |
| **B** | bugbear | 一般的なバグパターン |
| **C4** | comprehensions | 内包表記の最適化 |
| **T20** | flake8-print | `print`文の検出 |
| **PT** | pytest-style | pytestのベストプラクティス |
| **RET** | flake8-return | return文の最適化 |
| **SIM** | simplify | コード簡素化の提案 |
| **PLR** | pylint-refactor | リファクタリング提案 |

### 除外されているルール

- `E501`: 行長制限（Blackが処理）
- `PLR0913`: 引数数制限（一部のケースで必要）

### ファイル別設定

```python
# tests/ 配下では以下を許可
"tests/*" = ["T20", "S101"]  # print文、assert文
```

## 🧪 テスト戦略

### 1. テストファイル構造

```python
import pytest
from backend.main import calculate_sum, hello_world


def test_hello_world():
    """hello_world関数のテスト"""
    assert hello_world() == "Hello, World!"


def test_calculate_sum():
    """calculate_sum関数のテスト"""
    # 基本的な加算
    assert calculate_sum(2, 3) == 5  # noqa: PLR2004
    # 負数を含む計算
    assert calculate_sum(-1, 1) == 0
    # ゼロとの計算
    assert calculate_sum(0, 0) == 0
```

### 2. テスト命名規則

- テストファイル: `test_*.py` または `*_test.py`
- テスト関数: `test_*`
- テストクラス: `Test*`

### 3. カバレッジ要件

- **最低カバレッジ**: 80%以上
- **重要な関数**: 100%カバレッジ
- **除外対象**: `if __name__ == "__main__"` ブロック

### 4. テストの種類

#### 単体テスト (Unit Tests)
```python
def test_pure_function():
    """純粋関数のテスト"""
    result = pure_function(input_value)
    assert result == expected_value
```

#### 統合テスト (Integration Tests)
```python
@pytest.mark.integration
def test_database_integration():
    """データベース統合テスト"""
    # setUp, テスト実行, tearDown
    pass
```

#### フィクスチャの使用
```python
@pytest.fixture
def sample_data():
    """テスト用サンプルデータ"""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """フィクスチャを使用したテスト"""
    assert sample_data["key"] == "value"
```

## 🔄 CI/CD統合

### GitHub Actions での自動実行

1. **依存関係インストール**: `uv pip install -e ".[dev]"`
2. **自動フォーマット**: `black .`
3. **自動修正**: `ruff check --fix .`
4. **品質チェック**: `black --check .` + `ruff check .`
5. **テスト実行**: `pytest --cov=backend`

### コミット時の自動修正

PRが作成されると、以下が自動実行されます：

- コードフォーマットの自動修正
- リンティング問題の自動修正
- 修正内容の自動コミット

## 🚨 よくある問題と解決方法

### 1. Import エラー

```bash
# 問題: モジュールが見つからない
ModuleNotFoundError: No module named 'backend'

# 解決: editable install確認
uv pip install -e ".[dev]"
```

### 2. Ruff設定競合

```bash
# 問題: Ruffとpyproject.tomlの設定不整合
# 解決: pyproject.tomlの[tool.ruff]セクション確認
```

### 3. テストパス問題

```bash
# 問題: テストファイルが見つからない
# 解決: pytest.ini_optionsのtestpaths確認
```

## 📚 参考リンク

- [Ruff ルール一覧](https://docs.astral.sh/ruff/rules/)
- [Black 設定オプション](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
- [pytest ドキュメント](https://docs.pytest.org/en/stable/)
- [uv ガイド](https://github.com/astral-sh/uv)
- [PEP 8 スタイルガイド](https://peps.python.org/pep-0008/)

---

💡 **開発時のコツ**: IDEにRuffとBlackの拡張機能をインストールして、保存時に自動フォーマットを有効にすると効率的です。