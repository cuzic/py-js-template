# 🧪 テスト戦略ガイド

このガイドでは、Python（pytest）とJavaScript/TypeScript（Vitest）における包括的なテスト戦略について説明します。

## 🎯 テスト哲学

### 基本原則

1. **Test Pyramid**: 単体テスト > 統合テスト > E2Eテスト
2. **Fast Feedback**: 高速な実行とCI統合
3. **Maintainability**: 保守しやすいテストコード
4. **Coverage**: 意味のあるカバレッジ目標
5. **Isolation**: テスト間の独立性

### テストレベル

```
    🔺 E2E Tests (少)
   🔺🔺 Integration Tests (中)
  🔺🔺🔺 Unit Tests (多)
```

## 🐍 Python テスト戦略

### 技術スタック

- **pytest**: 柔軟なテストフレームワーク
- **pytest-cov**: カバレッジ測定
- **pytest-mock**: モッキング機能
- **pytest-asyncio**: 非同期テスト対応

### プロジェクト構造

```
backend/
├── src/backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── utils/
└── tests/
    ├── __init__.py
    ├── conftest.py          # 共通設定・フィクスチャ
    ├── test_main.py         # 単体テスト
    ├── test_integration.py   # 統合テスト
    └── fixtures/            # テストデータ
        └── sample_data.json
```

### 基本的なテスト

#### 1. 単体テスト

```python
# tests/test_main.py
import pytest
from backend.main import calculate_sum, hello_world


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
    ])
    def test_parametrized(self, a, b, expected):
        """パラメータ化テスト"""
        assert calculate_sum(a, b) == expected


def test_hello_world():
    """hello_world関数のテスト"""
    result = hello_world()
    assert result == "Hello, World!"
    assert isinstance(result, str)
```

#### 2. フィクスチャの活用

```python
# tests/conftest.py
import pytest
from pathlib import Path
import json


@pytest.fixture
def sample_user():
    """サンプルユーザーデータ"""
    return {
        "id": "123",
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
    }


@pytest.fixture
def sample_users():
    """複数ユーザーデータ"""
    return [
        {"id": "1", "name": "Alice", "email": "alice@example.com"},
        {"id": "2", "name": "Bob", "email": "bob@example.com"},
    ]


@pytest.fixture
def temp_file(tmp_path):
    """一時ファイル"""
    file_path = tmp_path / "test_data.json"
    data = {"key": "value", "number": 42}
    file_path.write_text(json.dumps(data))
    return file_path


@pytest.fixture(scope="session")
def database_connection():
    """データベース接続（セッションスコープ）"""
    # setup
    conn = create_test_database()
    yield conn
    # teardown
    conn.close()
    cleanup_test_database()
```

#### 3. モックとスタブ

```python
# tests/test_services.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.user_service import UserService
from backend.services.email_service import EmailService


class TestUserService:
    
    @pytest.fixture
    def mock_database(self):
        """データベースモック"""
        mock_db = Mock()
        mock_db.get_user.return_value = {
            "id": "123",
            "name": "John Doe",
            "email": "john@example.com"
        }
        return mock_db
    
    @pytest.fixture
    def user_service(self, mock_database):
        """UserServiceインスタンス"""
        return UserService(database=mock_database)
    
    def test_get_user_by_id(self, user_service, mock_database):
        """IDによるユーザー取得テスト"""
        user = user_service.get_user_by_id("123")
        
        assert user["name"] == "John Doe"
        mock_database.get_user.assert_called_once_with("123")
    
    @patch('backend.services.user_service.EmailService')
    def test_send_welcome_email(self, mock_email_service, user_service):
        """ウェルカムメール送信テスト"""
        mock_email_instance = mock_email_service.return_value
        mock_email_instance.send.return_value = True
        
        result = user_service.send_welcome_email("john@example.com")
        
        assert result is True
        mock_email_instance.send.assert_called_once()
    
    def test_api_call_error_handling(self):
        """API呼び出しエラーハンドリング"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("Network error")
            
            with pytest.raises(ServiceException):
                api_client.fetch_data()
```

#### 4. 非同期テスト

```python
# tests/test_async.py
import pytest
import asyncio
from backend.services.async_service import AsyncDataService


@pytest.mark.asyncio
async def test_async_data_fetch():
    """非同期データ取得テスト"""
    service = AsyncDataService()
    data = await service.fetch_data("user123")
    
    assert data is not None
    assert "id" in data


@pytest.mark.asyncio
async def test_concurrent_requests():
    """並行リクエストテスト"""
    service = AsyncDataService()
    
    tasks = [
        service.fetch_data("user1"),
        service.fetch_data("user2"),
        service.fetch_data("user3"),
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 3
    assert all(result is not None for result in results)
```

#### 5. 統合テスト

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """テストクライアント"""
    return TestClient(app)


@pytest.mark.integration
def test_user_creation_flow(client):
    """ユーザー作成フローの統合テスト"""
    # ユーザー作成
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secure_password"
    }
    
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    
    user_id = create_response.json()["id"]
    
    # ユーザー取得
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "John Doe"
    
    # ユーザー更新
    update_data = {"name": "John Smith"}
    update_response = client.put(f"/users/{user_id}", json=update_data)
    assert update_response.status_code == 200
    
    # 更新確認
    final_response = client.get(f"/users/{user_id}")
    assert final_response.json()["name"] == "John Smith"
```

## 🟨 JavaScript/TypeScript テスト戦略

### 技術スタック

- **Vitest**: Vite統合テストフレームワーク
- **@testing-library/react**: Reactコンポーネントテスト
- **@testing-library/jest-dom**: DOM assertion拡張
- **@testing-library/user-event**: ユーザーインタラクション

### プロジェクト構造

```
frontend/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── App.tsx
└── tests/
    ├── setup.ts             # テスト環境設定
    ├── App.test.tsx         # コンポーネントテスト
    ├── components/          # コンポーネント別テスト
    ├── hooks/               # フックテスト
    ├── utils/               # ユーティリティテスト
    └── __mocks__/           # モックファイル
        └── api.ts
```

### 基本的なテスト

#### 1. コンポーネントテスト

```typescript
// tests/App.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

describe('App Component', () => {
  it('renders with initial count of 0', () => {
    render(<App />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments count when + button is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const incrementButton = screen.getByText('+1');
    await user.click(incrementButton);
    
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('decrements count when - button is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const decrementButton = screen.getByText('-1');
    await user.click(decrementButton);
    
    expect(screen.getByText('Count: -1')).toBeInTheDocument();
  });

  it('resets count when Reset button is clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // カウントを変更
    await user.click(screen.getByText('+1'));
    await user.click(screen.getByText('+1'));
    expect(screen.getByText('Count: 2')).toBeInTheDocument();
    
    // リセット
    await user.click(screen.getByText('Reset'));
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});
```

#### 2. フォーム・入力テスト

```typescript
// tests/components/UserForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UserForm from '../../src/components/UserForm';

describe('UserForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders form fields correctly', () => {
    render(<UserForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('submits form with correct data', async () => {
    const user = userEvent.setup();
    render(<UserForm onSubmit={mockOnSubmit} />);
    
    // フォーム入力
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    
    // 送信
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
    });
  });

  it('displays validation errors', async () => {
    const user = userEvent.setup();
    render(<UserForm onSubmit={mockOnSubmit} />);
    
    // 空のまま送信
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

#### 3. カスタムフックテスト

```typescript
// tests/hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter } from '../../src/hooks/useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));
    
    act(() => {
      result.current.decrement();
    });
    
    expect(result.current.count).toBe(4);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    
    act(() => {
      result.current.increment();
      result.current.increment();
    });
    expect(result.current.count).toBe(12);
    
    act(() => {
      result.current.reset();
    });
    expect(result.current.count).toBe(10);
  });
});
```

#### 4. 非同期処理とAPI テスト

```typescript
// tests/components/UserList.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import UserList from '../../src/components/UserList';
import * as api from '../../src/api/users';

// APIモック
vi.mock('../../src/api/users');
const mockApi = vi.mocked(api);

describe('UserList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays loading state initially', () => {
    mockApi.getUsers.mockReturnValue(new Promise(() => {})); // pending promise
    
    render(<UserList />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays users after successful fetch', async () => {
    const mockUsers = [
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ];
    
    mockApi.getUsers.mockResolvedValue(mockUsers);
    
    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
      expect(screen.getByText('Bob')).toBeInTheDocument();
    });
    
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('displays error message on fetch failure', async () => {
    mockApi.getUsers.mockRejectedValue(new Error('API Error'));
    
    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText(/error loading users/i)).toBeInTheDocument();
    });
  });

  it('retries fetch on retry button click', async () => {
    mockApi.getUsers
      .mockRejectedValueOnce(new Error('API Error'))
      .mockResolvedValueOnce([]);
    
    render(<UserList />);
    
    // エラー表示まで待機
    await waitFor(() => {
      expect(screen.getByText(/error loading users/i)).toBeInTheDocument();
    });
    
    // リトライボタンクリック
    const retryButton = screen.getByText(/retry/i);
    await userEvent.setup().click(retryButton);
    
    // 再試行確認
    expect(mockApi.getUsers).toHaveBeenCalledTimes(2);
  });
});
```

#### 5. Context・Provider テスト

```typescript
// tests/contexts/AuthContext.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AuthProvider, useAuth } from '../../src/contexts/AuthContext';

// テスト用コンポーネント
const TestComponent = () => {
  const { user, login, logout, isLoading } = useAuth();
  
  return (
    <div>
      {isLoading && <div>Loading...</div>}
      {user ? (
        <div>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <button onClick={() => login('user@example.com', 'password')}>
          Login
        </button>
      )}
    </div>
  );
};

const renderWithAuth = (children: React.ReactNode) => {
  return render(<AuthProvider>{children}</AuthProvider>);
};

describe('AuthContext', () => {
  it('provides login functionality', async () => {
    const user = userEvent.setup();
    renderWithAuth(<TestComponent />);
    
    const loginButton = screen.getByText('Login');
    await user.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });
  });

  it('provides logout functionality', async () => {
    const user = userEvent.setup();
    renderWithAuth(<TestComponent />);
    
    // ログイン
    await user.click(screen.getByText('Login'));
    await waitFor(() => screen.getByText(/welcome/i));
    
    // ログアウト
    await user.click(screen.getByText('Logout'));
    
    await waitFor(() => {
      expect(screen.getByText('Login')).toBeInTheDocument();
    });
  });
});
```

## 📊 カバレッジとメトリクス

### Python カバレッジ設定

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--cov=backend",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "*/migrations/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]
```

### JavaScript カバレッジ設定

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    },
  },
});
```

## 🔄 CI/CD テスト統合

### GitHub Actions設定

```yaml
# Python CI
- name: Run tests with pytest
  run: |
    source .venv/bin/activate
    pytest -v --cov=backend --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./backend/coverage.xml

# JavaScript CI  
- name: Run tests
  run: bun run test:coverage

- name: Upload coverage reports
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: frontend/coverage/
```

### テスト戦略マトリクス

| テストタイプ | Python | JavaScript | 実行頻度 | カバレッジ目標 |
|-------------|--------|------------|----------|---------------|
| **Unit** | pytest | Vitest | 毎コミット | 90%+ |
| **Integration** | pytest + TestClient | Testing Library | 毎PR | 80%+ |
| **Component** | - | React Testing Library | 毎PR | 85%+ |
| **E2E** | playwright | playwright | 毎リリース | 主要フロー |

## 📚 ベストプラクティス

### 1. テスト命名規則

```python
# Python
def test_should_return_user_when_valid_id_provided():
    """有効なIDが提供された場合、ユーザーを返すべき"""
    pass

def test_should_raise_exception_when_user_not_found():
    """ユーザーが見つからない場合、例外を発生させるべき"""
    pass
```

```typescript
// TypeScript
describe('UserService', () => {
  it('should return user when valid ID is provided', () => {});
  it('should throw error when user is not found', () => {});
});
```

### 2. Arrange-Act-Assert パターン

```python
def test_user_creation():
    # Arrange
    user_data = {"name": "John", "email": "john@example.com"}
    
    # Act
    user = create_user(user_data)
    
    # Assert
    assert user.name == "John"
    assert user.email == "john@example.com"
```

### 3. テストデータ管理

```python
# fixtures/users.py
VALID_USER = {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2023-01-01T00:00:00Z"
}

INVALID_USER = {
    "name": "",  # 空の名前
    "email": "invalid-email"  # 無効なメール
}
```

## 📚 参考リンク

### Python
- [pytest ドキュメント](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://realpython.com/pytest-python-testing/)

### JavaScript/TypeScript
- [Vitest ガイド](https://vitest.dev/guide/)
- [Testing Library](https://testing-library.com/docs/)
- [React Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

💡 **テスト駆動開発のコツ**: 新機能を実装する前にテストを書く習慣をつけると、設計品質が向上し、バグの早期発見が可能になります。