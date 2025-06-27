# 🐍 Python 開発ガイド

このガイドでは、Pythonバックエンド開発における品質基準、コーディングルール、テスト戦略について説明します。

## 📦 技術スタック

- **パッケージマネージャー**: [uv](https://github.com/astral-sh/uv) - 超高速Pythonパッケージマネージャー
- **ビルドシステム**: [Hatchling](https://hatch.pypa.io/) - モダンなPythonビルドバックエンド
- **リンター**: [Ruff](https://github.com/astral-sh/ruff) - Rust製超高速リンター
- **フォーマッター**: [Black](https://github.com/psf/black) - 妥協のないコードフォーマッター
- **型チェッカー**: [Mypy](http://mypy-lang.org/) - 静的型チェッカー
- **テストフレームワーク**: [pytest](https://docs.pytest.org/) - 柔軟で強力なテストフレームワーク
- **セキュリティスキャナー**: [Bandit](https://bandit.readthedocs.io/) - セキュリティ脆弱性検出
- **プリコミットフック**: [pre-commit](https://pre-commit.com/) - Git hooks管理

## 🏗️ プロジェクト構造

```
backend/
├── src/
│   └── backend/          # メインパッケージ
│       ├── __init__.py
│       ├── main.py
│       ├── models/       # データモデル
│       ├── services/     # ビジネスロジック
│       └── utils/        # ユーティリティ関数
├── tests/                # テストファイル
│   ├── __init__.py
│   ├── conftest.py       # pytest設定・フィクスチャ
│   ├── test_main.py
│   ├── test_services/    # サービス層テスト
│   └── fixtures/         # テストデータ
├── scripts/              # 開発・運用スクリプト
├── pyproject.toml        # プロジェクト設定
├── .pre-commit-config.yaml # プリコミットフック設定
├── mypy.ini             # Mypy設定
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

### pyproject.toml 設定例

```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.5.0",
    "black>=24.0.0",
    "mypy>=1.5.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.11.0",
    "bandit>=1.7.5",
    "pre-commit>=3.3.0",
]

[tool.hatch.scripts]
lint = "ruff check . && black --check . && mypy src"
lint-fix = "ruff check --fix . && black ."
type-check = "mypy src"
security = "bandit -r src/"
test = "pytest --cov=backend --cov-report=html"
test-fast = "pytest -x"
all-checks = "hatch run lint && hatch run security && hatch run test"
```

### 開発用コマンド

```bash
# Hatchスクリプトを使用（推奨）
hatch run lint          # 全品質チェック
hatch run lint-fix      # 自動修正
hatch run type-check    # 型チェック
hatch run security      # セキュリティスキャン
hatch run test          # テスト実行
hatch run all-checks    # 全チェック実行

# 直接コマンド実行
ruff check .                    # リンティング
ruff check --fix .              # 自動修正
black .                         # フォーマット
black --check .                 # フォーマットチェック
mypy src                        # 型チェック
bandit -r src/                  # セキュリティスキャン
pytest --cov=backend           # カバレッジ付きテスト
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

## 🔍 静的型チェック（Mypy）

### 基本設定

```ini
# mypy.ini
[mypy]
python_version = 3.11
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true

# サードパーティライブラリの型スタブが無い場合
ignore_missing_imports = true

# 特定ファイルの除外
[mypy-tests.*]
ignore_errors = true
```

### 型ヒントのベストプラクティス

```python
from typing import Optional, Union, List, Dict, Any, TypeVar, Generic
from collections.abc import Sequence, Mapping
from pathlib import Path

# ✅ 推奨: 具体的な型指定
def process_user_data(
    user_id: int,
    name: str,
    email: Optional[str] = None,
    tags: List[str] | None = None,  # Python 3.10+
) -> Dict[str, Any]:
    """ユーザーデータを処理する関数"""
    result: Dict[str, Any] = {"id": user_id, "name": name}
    if email:
        result["email"] = email
    if tags:
        result["tags"] = tags
    return result

# ✅ 推奨: ジェネリクス使用
T = TypeVar('T')

class Repository(Generic[T]):
    """汎用リポジトリクラス"""
    
    def find_by_id(self, entity_id: int) -> Optional[T]:
        # 実装
        return None
    
    def save(self, entity: T) -> T:
        # 実装
        return entity

# ✅ 推奨: プロトコル使用
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render_shape(shape: Drawable) -> None:
    shape.draw()
```

## 🛡️ セキュリティ

### Bandit設定

```toml
# pyproject.toml
[tool.bandit]
exclude_dirs = ["tests", "venv", ".venv"]
skips = ["B101"]  # assert_used - テストで使用

[tool.bandit.assert_used]
# テストファイルでのassert使用を許可
exclude = ["*/tests/*"]
```

### セキュリティチェック項目

#### 1. 機密情報の保護

```python
import os
from pathlib import Path

# ❌ 危険: ハードコードされた機密情報
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ 安全: 環境変数から取得
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/db")
```

#### 2. SQLインジェクション対策

```python
import sqlite3
from typing import List, Tuple

# ❌ 危険: SQL文の直接結合
def get_user_unsafe(user_id: str) -> List[Tuple]:
    conn = sqlite3.connect("db.sqlite")
    # SQLインジェクション脆弱性
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchall()

# ✅ 安全: パラメータ化クエリ
def get_user_safe(user_id: int) -> List[Tuple]:
    conn = sqlite3.connect("db.sqlite")
    query = "SELECT * FROM users WHERE id = ?"
    return conn.execute(query, (user_id,)).fetchall()
```

#### 3. ファイル操作のセキュリティ

```python
import os
from pathlib import Path

# ❌ 危険: パストラバーサル脆弱性
def read_file_unsafe(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()

# ✅ 安全: パス検証
def read_file_safe(filename: str, base_dir: str = "/safe/directory") -> str:
    base_path = Path(base_dir).resolve()
    file_path = (base_path / filename).resolve()
    
    # ベースディレクトリ外へのアクセスを防ぐ
    if not str(file_path).startswith(str(base_path)):
        raise ValueError("Access denied: path outside base directory")
    
    with open(file_path, 'r') as f:
        return f.read()
```

## 🔧 プリコミットフック

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/]
        exclude: tests/
```

### セットアップと使用

```bash
# プリコミットフックのインストール
pre-commit install

# 全ファイルに対して実行
pre-commit run --all-files

# 特定のフックのみ実行
pre-commit run black

# フックの更新
pre-commit autoupdate
```

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
from unittest.mock import Mock, patch, MagicMock
from backend.main import calculate_sum, hello_world


class TestHelloWorld:
    """hello_world関数のテストクラス"""
    
    def test_returns_correct_message(self):
        """正しいメッセージを返すことを確認"""
        result = hello_world()
        assert result == "Hello, World!"
        assert isinstance(result, str)


class TestCalculateSum:
    """calculate_sum関数のテストクラス"""
    
    def test_positive_numbers(self):
        """正の数の加算テスト"""
        assert calculate_sum(2, 3) == 5  # noqa: PLR2004
        assert calculate_sum(10, 20) == 30  # noqa: PLR2004
    
    def test_negative_numbers(self):
        """負の数を含む加算テスト"""
        assert calculate_sum(-1, 1) == 0
        assert calculate_sum(-5, -3) == -8  # noqa: PLR2004
    
    def test_zero_values(self):
        """ゼロを含む加算テスト"""
        assert calculate_sum(0, 0) == 0
        assert calculate_sum(5, 0) == 5  # noqa: PLR2004
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (-1, 1, 0),
        (100, 200, 300),
        (0, 0, 0),
        (-10, -5, -15),
        (1.5, 2.5, 4.0),  # 浮動小数点数
    ])
    def test_parametrized_addition(self, a, b, expected):
        """パラメータ化テスト - 複数の入力値でテスト"""
        assert calculate_sum(a, b) == expected
    
    @pytest.mark.parametrize("a,b", [
        ("not_a_number", 5),
        (5, "not_a_number"),
        (None, 5),
        (5, None),
    ])
    def test_invalid_input_types(self, a, b):
        """不正な入力型のテスト"""
        with pytest.raises(TypeError):
            calculate_sum(a, b)
```

### 2. 高度なテスト例

#### モックを使用したテスト

```python
# tests/test_services.py
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from backend.services.user_service import UserService
from backend.services.email_service import EmailService


class TestUserService:
    """UserServiceクラスのテスト"""
    
    @pytest.fixture
    def mock_database(self):
        """データベースモック"""
        mock_db = Mock()
        mock_db.get_user.return_value = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com"
        }
        mock_db.save_user.return_value = True
        return mock_db
    
    @pytest.fixture
    def user_service(self, mock_database):
        """UserServiceインスタンス"""
        return UserService(database=mock_database)
    
    def test_get_user_by_id_success(self, user_service, mock_database):
        """IDによるユーザー取得テスト - 成功ケース"""
        # Act
        user = user_service.get_user_by_id(123)
        
        # Assert
        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
        mock_database.get_user.assert_called_once_with(123)
    
    def test_get_user_by_id_not_found(self, user_service, mock_database):
        """IDによるユーザー取得テスト - 見つからない場合"""
        # Arrange
        mock_database.get_user.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            user_service.get_user_by_id(999)
    
    @patch('backend.services.user_service.EmailService')
    def test_send_welcome_email(self, mock_email_service, user_service):
        """ウェルカムメール送信テスト"""
        # Arrange
        mock_email_instance = mock_email_service.return_value
        mock_email_instance.send.return_value = True
        
        # Act
        result = user_service.send_welcome_email("john@example.com")
        
        # Assert
        assert result is True
        mock_email_instance.send.assert_called_once_with(
            to="john@example.com",
            subject="Welcome!",
            template="welcome"
        )
    
    def test_batch_update_users(self, user_service, mock_database):
        """バッチユーザー更新のテスト"""
        # Arrange
        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]
        
        # Act
        user_service.batch_update_users(users)
        
        # Assert - 複数回の呼び出しを確認
        expected_calls = [call(user) for user in users]
        mock_database.save_user.assert_has_calls(expected_calls)
        assert mock_database.save_user.call_count == 3
```

#### 高度なフィクスチャの使用

```python
# tests/conftest.py
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock

@pytest.fixture
def temp_file():
    """一時ファイル作成フィクスチャ"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(json.dumps({"test": "data"}))
        temp_path = f.name
    
    yield Path(temp_path)
    
    # クリーンアップ
    Path(temp_path).unlink(missing_ok=True)

@pytest.fixture
def mock_api_client():
    """APIクライアントモック"""
    client = Mock()
    client.get.return_value = {"status": "success", "data": []}
    client.post.return_value = {"status": "created", "id": 123}
    return client

@pytest.fixture(scope="session")
def database_url():
    """テスト用データベースURL"""
    return "sqlite:///:memory:"

@pytest.fixture(scope="function")
def clean_database(database_url):
    """各テスト前にデータベースをクリーンアップ"""
    # データベース初期化
    setup_test_database(database_url)
    yield database_url
    # テスト後のクリーンアップ
    cleanup_test_database(database_url)

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """複数のデータベースタイプでテスト"""
    return request.param
```

#### 非同期テスト

```python
# tests/test_async_services.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.services.async_user_service import AsyncUserService

class TestAsyncUserService:
    """非同期ユーザーサービスのテスト"""
    
    @pytest.fixture
    def async_service(self):
        return AsyncUserService()
    
    @pytest.mark.asyncio
    async def test_fetch_user_data(self, async_service):
        """非同期ユーザーデータ取得テスト"""
        with patch.object(async_service, '_api_call', new_callable=AsyncMock) as mock_call:
            # Arrange
            mock_call.return_value = {"id": 1, "name": "Alice"}
            
            # Act
            result = await async_service.fetch_user_data(1)
            
            # Assert
            assert result["name"] == "Alice"
            mock_call.assert_called_once_with("/users/1")
    
    @pytest.mark.asyncio
    async def test_concurrent_user_fetch(self, async_service):
        """並行ユーザー取得テスト"""
        with patch.object(async_service, 'fetch_user_data', new_callable=AsyncMock) as mock_fetch:
            # Arrange
            mock_fetch.side_effect = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"},
            ]
            
            # Act
            tasks = [
                async_service.fetch_user_data(1),
                async_service.fetch_user_data(2),
                async_service.fetch_user_data(3),
            ]
            results = await asyncio.gather(*tasks)
            
            # Assert
            assert len(results) == 3
            assert results[0]["name"] == "Alice"
            assert mock_fetch.call_count == 3
```

### 3. テスト戦略

#### テストピラミッド

```
        🔺 E2E Tests (5%)
       🔺🔺 Integration Tests (15%)
      🔺🔺🔺 Unit Tests (80%)
```

#### テスト分類とマーキング

```python
# テストマーカーの定義
pytest_plugins = []

# pytest.ini または pyproject.toml
markers = [
    "unit: Unit tests",
    "integration: Integration tests", 
    "e2e: End-to-end tests",
    "slow: Slow running tests",
    "security: Security related tests",
]

# 使用例
@pytest.mark.unit
def test_calculate_sum():
    """単体テスト"""
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_database_integration():
    """データベース統合テスト"""
    pass

@pytest.mark.security
def test_password_hashing():
    """セキュリティテスト"""
    pass
```

#### テスト実行の最適化

```bash
# 特定のマーカーのみ実行
pytest -m unit                    # 単体テストのみ
pytest -m "not slow"              # 遅いテストを除外
pytest -m "unit or integration"   # 単体・統合テスト

# 並列実行（pytest-xdist）
pytest -n auto                    # 自動並列度
pytest -n 4                       # 4プロセス並列

# 失敗時に即座に停止
pytest -x                         # 最初の失敗で停止
pytest --maxfail=3                # 3回失敗で停止

# カバレッジと結果出力
pytest --cov=backend --cov-report=html --cov-report=term
```

### 4. カバレッジ戦略

#### カバレッジ設定

```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*", 
    "*/__pycache__/*",
    "*/migrations/*",
    "*/scripts/*",
]

[tool.coverage.report]
# 最低カバレッジ要件
fail_under = 80
precision = 2
show_missing = true
skip_covered = false

exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError", 
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

#### カバレッジ目標

| コード分類 | 目標カバレッジ | 説明 |
|-----------|----------------|------|
| **ビジネスロジック** | 95%+ | サービス層、ドメインロジック |
| **ユーティリティ** | 90%+ | 汎用関数、ヘルパー |
| **APIエンドポイント** | 85%+ | REST API、GraphQLリゾルバ |
| **データアクセス** | 80%+ | リポジトリ、ORM操作 |
| **設定・初期化** | 60%+ | 設定ファイル、アプリ初期化 |

## 🔄 CI/CD統合

### 改良版 GitHub Actions ワークフロー

```yaml
# .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install uv
      uses: astral-sh/setup-uv@v6
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/uv
        key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
        restore-keys: |
          ${{ runner.os }}-uv-
    
    - name: Install dependencies
      run: |
        uv venv
        source .venv/bin/activate
        uv pip install -e ".[dev]"
    
    - name: Run pre-commit hooks
      run: |
        source .venv/bin/activate
        pre-commit run --all-files
    
    - name: Type check with MyPy
      run: |
        source .venv/bin/activate
        mypy src
    
    - name: Security scan with Bandit
      run: |
        source .venv/bin/activate
        bandit -r src/ -f json -o bandit-report.json
    
    - name: Run tests with coverage
      run: |
        source .venv/bin/activate
        pytest --cov=backend --cov-report=xml --cov-report=html --junitxml=test-results.xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}
        path: |
          test-results.xml
          htmlcov/
          bandit-report.json
```

### 依存関係管理とセキュリティ

#### 1. 依存関係のバージョン固定

```bash
# 現在の依存関係をrequirements.txtに固定
uv pip freeze > requirements.txt

# 本番環境での再現可能なインストール
uv pip install -r requirements.txt

# セキュリティアップデートのチェック
uv pip list --outdated

# 脆弱性スキャン
pip-audit
```

#### 2. Dependabot設定

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "team-leads"
    labels:
      - "dependencies"
      - "security"
    
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

#### 3. 依存関係のセキュリティポリシー

```toml
# pyproject.toml
[tool.pip-audit]
require-hashes = true
desc = true

[project.optional-dependencies]
# 本番環境依存関係
prod = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "pydantic==2.5.0",
]

# 開発環境依存関係
dev = [
    "ruff>=0.5.0",
    "black>=24.0.0", 
    "mypy>=1.5.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.11.0",
    "pytest-xdist>=3.3.0",  # 並列テスト実行
    "bandit>=1.7.5",
    "pre-commit>=3.3.0",
    "pip-audit>=2.6.0",
]
```

### パフォーマンス最適化

#### 1. プロファイリング

```python
# プロファイリング用デコレータ
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """関数のプロファイリングを行うデコレータ"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        
        stats = pstats.Stats(pr)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return result
    return wrapper

# 使用例
@profile_function
def expensive_operation(data):
    # 重い処理
    return process_data(data)
```

#### 2. メモリ使用量監視

```python
import tracemalloc
from functools import wraps

def monitor_memory(func):
    """メモリ使用量を監視するデコレータ"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
        print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
        
        return result
    return wrapper
```

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

### 公式ドキュメント
- [uv ガイド](https://github.com/astral-sh/uv) - 超高速パッケージマネージャー
- [Ruff ルール一覧](https://docs.astral.sh/ruff/rules/) - リンティングルール完全ガイド
- [Black 設定オプション](https://black.readthedocs.io/en/stable/) - コードフォーマッター
- [Mypy ドキュメント](http://mypy-lang.org/) - 静的型チェッカー
- [pytest ドキュメント](https://docs.pytest.org/en/stable/) - テストフレームワーク
- [Bandit ドキュメント](https://bandit.readthedocs.io/) - セキュリティスキャナー
- [pre-commit ガイド](https://pre-commit.com/) - Git hooks管理

### ベストプラクティス
- [PEP 8 スタイルガイド](https://peps.python.org/pep-0008/) - Pythonコーディング規約
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - 型ヒント公式ガイド
- [Testing Best Practices](https://realpython.com/pytest-python-testing/) - テストのベストプラクティス
- [Security Guidelines](https://python.org/dev/security/) - セキュリティガイドライン

### ツール・拡張機能
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [VS Code Ruff Extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [PyCharm Settings](https://www.jetbrains.com/help/pycharm/configuring-code-style.html)

---

💡 **開発効率向上のコツ**: 
- IDEにRuff、Black、Mypyの拡張機能をインストール
- 保存時の自動フォーマットを有効化
- pre-commitフックでコミット前の品質チェック
- 定期的な依存関係アップデートとセキュリティスキャン