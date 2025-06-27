# 🟨 JavaScript/TypeScript 開発ガイド

このガイドでは、React + TypeScriptフロントエンド開発における品質基準、コーディングルール、テスト戦略について説明します。

## 📦 技術スタック

- **ランタイム**: [Bun](https://bun.sh/) - 超高速JavaScript/TypeScriptランタイム
- **フレームワーク**: [React 18](https://react.dev/) - 最新のReactフレームワーク
- **言語**: [TypeScript](https://www.typescriptlang.org/) - 型安全なJavaScript
- **ビルドツール**: [Vite](https://vitejs.dev/) - 高速開発サーバー
- **リンター**: [ESLint](https://eslint.org/) (Flat Config) - 最新のリンティング設定
- **フォーマッター**: [Prettier](https://prettier.io/) - 一貫したコードフォーマット
- **テストフレームワーク**: [Vitest](https://vitest.dev/) - Vite統合テストフレームワーク
- **テストライブラリ**: [Testing Library](https://testing-library.com/) - Reactコンポーネントテスト

## 🏗️ プロジェクト構造

```
frontend/
├── src/
│   ├── components/       # 再利用可能なコンポーネント
│   ├── pages/           # ページコンポーネント
│   ├── hooks/           # カスタムフック
│   ├── utils/           # ユーティリティ関数
│   ├── types/           # 型定義
│   ├── styles/          # グローバルスタイル
│   ├── App.tsx          # ルートコンポーネント
│   └── main.tsx         # エントリーポイント
├── tests/               # テストファイル
├── public/              # 静的ファイル
├── package.json         # プロジェクト設定
├── tsconfig.json        # TypeScript設定
├── vite.config.ts       # Vite設定
├── eslint.config.js     # ESLint設定
└── .prettierrc.json     # Prettier設定
```

## 🔧 環境設定

### 初期セットアップ

```bash
cd frontend

# 依存関係のインストール
bun install

# 開発サーバー起動
bun dev

# プロダクションビルド
bun run build

# プレビュー
bun run preview
```

### 開発用コマンド

```bash
# リンティング
bun run lint

# フォーマット
bun run format

# フォーマットチェック
bun run format:check

# 型チェック
bun run typecheck

# テスト実行
bun test

# テスト（カバレッジ付き）
bun run test:coverage
```

## 📝 コーディングルール

### 1. TypeScript基本方針

- **厳格モード**: `strict: true` を使用
- **型安全性**: `any` の使用は最小限に
- **null安全性**: `strictNullChecks: true`
- **型推論**: 明示的な型注釈は必要な場合のみ

### 2. React コンポーネント設計

#### 関数コンポーネント（推奨）

```typescript
interface CalculatorProps {
  initialValue?: number;
}

function Calculator({ initialValue = 0 }: CalculatorProps) {
  const [count, setCount] = useState(initialValue);

  const increment = () => {
    setCount((prev) => prev + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+1</button>
    </div>
  );
}

export default Calculator;
```

#### Propsの型定義

```typescript
// 基本的なProps
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

// HTMLAttributes を継承
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}
```

### 3. 命名規則

| 要素 | 規則 | 例 |
|------|------|-----|
| **コンポーネント** | PascalCase | `UserProfile`, `NavigationBar` |
| **ファイル名** | PascalCase (コンポーネント) | `UserProfile.tsx` |
| **フック** | camelCase (use始まり) | `useCounter`, `useLocalStorage` |
| **変数・関数** | camelCase | `userName`, `handleClick` |
| **定数** | UPPER_SNAKE_CASE | `API_BASE_URL` |
| **型・インターフェース** | PascalCase | `User`, `ApiResponse` |

### 4. ディレクトリ構造のベストプラクティス

```typescript
// utils/math.ts - ユーティリティ関数
export const add = (a: number, b: number): number => a + b;

// hooks/useCounter.ts - カスタムフック
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);
  
  return { count, increment, decrement, reset };
}

// types/api.ts - 型定義
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
  message?: string;
}
```

## 🔍 ESLint設定詳細

### 有効化されているルール

#### React関連
- `react-hooks/rules-of-hooks`: フックのルール
- `react-hooks/exhaustive-deps`: 依存関係配列のチェック
- `react-refresh/only-export-components`: Hot Reload対応

#### TypeScript関連
- `@typescript-eslint/no-explicit-any`: `any`の使用警告
- `@typescript-eslint/no-unused-vars`: 未使用変数の検出
- `@typescript-eslint/explicit-module-boundary-types`: 関数の戻り値型

#### 一般的な品質ルール
- `no-console`: `console.log`の使用警告（warn/errorは除く）
- `prefer-const`: 再代入されない変数は`const`使用
- `no-duplicate-imports`: 重複importの禁止
- `sort-imports`: import文の並び順

### 設定カスタマイズ

```javascript
// eslint.config.js
export default tseslint.config(
  {
    rules: {
      // カスタムルール
      'react/prop-types': 'off', // TypeScript使用時は不要
      '@typescript-eslint/no-explicit-any': 'warn', // 段階的移行
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  }
);
```

## 🎨 Prettier設定

### フォーマット設定

```json
{
  "semi": true,                    // セミコロン必須
  "trailingComma": "all",         // 末尾カンマ
  "singleQuote": true,            // シングルクォート
  "printWidth": 80,               // 行幅
  "tabWidth": 2,                  // インデント幅
  "useTabs": false,               // スペースインデント
  "arrowParens": "always",        // アロー関数の括弧
  "endOfLine": "lf",              // 改行コード
  "bracketSpacing": true,         // オブジェクトの括弧内スペース
  "jsxSingleQuote": false         // JSXではダブルクォート
}
```

### 自動フォーマット例

```typescript
// Before
const user={name:"John",age:30};
const getName=user=>user.name;

// After
const user = { name: 'John', age: 30 };
const getName = (user) => user.name;
```

## 🧪 テスト戦略

### 1. テストファイル構造

```typescript
// tests/App.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  it('renders with initial count of 0', () => {
    render(<App />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments count when + button is clicked', () => {
    render(<App />);
    const incrementButton = screen.getByText('+1');
    fireEvent.click(incrementButton);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### 2. テスト環境設定

```typescript
// tests/setup.ts
import '@testing-library/jest-dom';

// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
  },
});
```

### 3. テストの種類

#### コンポーネントテスト
```typescript
// ユーザーインタラクションのテスト
it('handles user input correctly', async () => {
  const user = userEvent.setup();
  render(<SearchInput onSearch={mockOnSearch} />);
  
  const input = screen.getByPlaceholderText('Search...');
  await user.type(input, 'test query');
  await user.click(screen.getByText('Search'));
  
  expect(mockOnSearch).toHaveBeenCalledWith('test query');
});
```

#### フックテスト
```typescript
// hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from '../src/hooks/useCounter';

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter(0));
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

#### 統合テスト
```typescript
// API統合テスト
it('fetches and displays user data', async () => {
  const mockUser = { id: '1', name: 'John Doe' };
  vi.mocked(api.getUser).mockResolvedValue(mockUser);
  
  render(<UserProfile userId="1" />);
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
```

### 4. モックとスタブ

```typescript
// APIモック
vi.mock('../src/api/users', () => ({
  getUsers: vi.fn(),
  createUser: vi.fn(),
}));

// 外部ライブラリモック
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
  useParams: () => ({ id: '1' }),
}));
```

## 🔄 CI/CD統合

### GitHub Actions での自動実行

1. **依存関係インストール**: `bun install`
2. **型チェック**: `bun run typecheck`
3. **自動フォーマット**: `bun run format`
4. **自動リント修正**: `bun run lint`
5. **テスト実行**: `bun test`
6. **ビルドテスト**: `bun run build`

### パフォーマンス最適化

```typescript
// 遅延ローディング
const LazyComponent = lazy(() => import('./components/HeavyComponent'));

// メモ化
const MemoizedComponent = memo(({ data }: Props) => {
  return <div>{data.name}</div>;
});

// コールバックメモ化
const handleClick = useCallback((id: string) => {
  onItemClick(id);
}, [onItemClick]);
```

## 🚨 よくある問題と解決方法

### 1. TypeScript エラー

```typescript
// 問題: Property 'xxx' does not exist on type 'unknown'
// 解決: 型ガードまたは型アサーション使用
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value;
}

// 問題: Object is possibly 'null'
// 解決: オプショナルチェーニング使用
const userName = user?.profile?.name ?? 'Anonymous';
```

### 2. React Hook エラー

```typescript
// 問題: Hook called outside of component
// 解決: コンポーネント内またはカスタムフック内で使用

// 問題: Dependencies array missing
// 解決: 依存関係配列を適切に設定
useEffect(() => {
  fetchData(userId);
}, [userId]); // userIdを依存関係に追加
```

### 3. テストエラー

```typescript
// 問題: ReferenceError: document is not defined
// 解決: vitest.config.tsでjsdom環境設定

// 問題: TypeError: Cannot read properties of null
// 解決: コンポーネントの適切なレンダリング確認
render(<Component />);
await waitFor(() => screen.getByText('Expected Text'));
```

## 📚 参考リンク

- [React 公式ドキュメント](https://react.dev/)
- [TypeScript ハンドブック](https://www.typescriptlang.org/docs/)
- [ESLint 設定ガイド](https://eslint.org/docs/latest/use/configure/)
- [Prettier 設定オプション](https://prettier.io/docs/en/configuration.html)
- [Vitest ガイド](https://vitest.dev/guide/)
- [Testing Library ベストプラクティス](https://testing-library.com/docs/guiding-principles/)
- [Bun ドキュメント](https://bun.sh/docs)

---

💡 **開発効率向上のコツ**: VS CodeにESLint、Prettier、TypeScript拡張機能をインストールし、設定で「format on save」を有効にすると、コード品質が自動的に保たれます。