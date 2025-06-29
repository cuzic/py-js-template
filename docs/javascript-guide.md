# 🟨 JavaScript/TypeScript 開発ガイド（2025年版）

このガイドでは、2025年のモダンなReact + TypeScriptフロントエンド開発における最新のベストプラクティス、品質基準、コーディングルール、テスト戦略について説明します。

## 🚀 2025年版統合技術スタック

### 🏎️ 革命的パフォーマンス向上

2025年現在、JavaScript開発環境は劇的な進化を遂げています：

#### **Bunによる統合開発環境**
- **オールインワンツール**: ランタイム + パッケージマネージャー + バンドラー + テストランナー
- **圧倒的パフォーマンス**: Node.js比で2-3倍高速、npm比で20倍高速インストール
- **TypeScript/JSXネイティブサポート**: トランスパイル不要で直接実行

#### **ESLint Flat Config完全移行**
- **次世代設定方式**: `.eslintrc`廃止、`eslint.config.mjs`が標準
- **柔軟な設定**: ファイル別ルール適用、プラグイン統合の改善
- **TypeScript厳格チェック**: 2025年強化されたルールセット

#### **Prettier 3.6最新機能**
- **高速CLI**: 実験的高速処理エンジン
- **ファイル単位制御**: `@noformat`プラグマサポート
- **改善されたキャッシュ**: 大規模プロジェクト対応

### 📦 採用技術スタック

- **🏎️ ランタイム**: [Bun 1.1+](https://bun.sh/) - 統合JavaScript/TypeScriptランタイム
- **⚛️ フレームワーク**: [React 18.3+](https://react.dev/) - Concurrent Features対応
- **🔷 言語**: [TypeScript 5.7+](https://www.typescriptlang.org/) - 最新型システム
- **⚡ ビルドツール**: [Vite 5.4+](https://vitejs.dev/) - Lightning CSS採用
- **🔍 リンター**: [ESLint 9.15+](https://eslint.org/) - Flat Config専用
- **🎨 フォーマッター**: [Prettier 3.6+](https://prettier.io/) - 高速エンジン
- **🧪 テスト**: [Bun Test](https://bun.sh/docs/cli/test) + [Vitest 2.1+](https://vitest.dev/) - 統合テスト環境
- **📚 テストライブラリ**: [Testing Library 16+](https://testing-library.com/) - 最新React対応
- **🗃️ 状態管理**: [Zustand 5+](https://zustand.docs.pmnd.rs/) / [Jotai 3+](https://jotai.org/) - モダン状態管理
- **♿ アクセシビリティ**: [eslint-plugin-jsx-a11y 6.10+](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) - WCAG 2.2対応

## 🏗️ プロジェクト構造

### Co-location 方式（推奨）

```
frontend/
├── src/
│   ├── components/           # 再利用可能なコンポーネント
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx  # Storybook（オプション）
│   │   │   └── index.ts            # re-export
│   │   ├── Modal/
│   │   │   ├── Modal.tsx
│   │   │   ├── Modal.test.tsx
│   │   │   └── index.ts
│   │   └── index.ts            # 全コンポーネントのre-export
│   ├── pages/                # ページコンポーネント
│   │   ├── Home/
│   │   │   ├── Home.tsx
│   │   │   ├── Home.test.tsx
│   │   │   └── index.ts
│   │   └── About/
│   │       ├── About.tsx
│   │       ├── About.test.tsx
│   │       └── index.ts
│   ├── hooks/                # カスタムフック
│   │   ├── useCounter/
│   │   │   ├── useCounter.ts
│   │   │   ├── useCounter.test.ts
│   │   │   └── index.ts
│   │   └── useLocalStorage/
│   │       ├── useLocalStorage.ts
│   │       ├── useLocalStorage.test.ts
│   │       └── index.ts
│   ├── utils/                # ユーティリティ関数
│   │   ├── math/
│   │   │   ├── math.ts
│   │   │   ├── math.test.ts
│   │   │   └── index.ts
│   │   └── date/
│   │       ├── date.ts
│   │       ├── date.test.ts
│   │       └── index.ts
│   ├── store/                # 状態管理
│   │   ├── userStore.ts
│   │   ├── userStore.test.ts
│   │   └── index.ts
│   ├── types/                # 型定義
│   │   ├── api.ts
│   │   ├── user.ts
│   │   └── index.ts
│   ├── styles/               # グローバルスタイル
│   │   ├── globals.css
│   │   └── theme.ts
│   ├── App.tsx               # ルートコンポーネント
│   ├── App.test.tsx          # ルートコンポーネントテスト
│   └── main.tsx              # エントリーポイント
├── tests/                    # 統合テスト・E2Eテスト
│   ├── setup.ts              # テスト環境設定
│   ├── integration/          # 統合テスト
│   └── e2e/                  # E2Eテスト
├── public/                   # 静的ファイル
├── package.json              # プロジェクト設定
├── tsconfig.json             # TypeScript設定
├── vite.config.ts            # Vite設定
├── eslint.config.mjs         # ESLint Flat Config (2025)
├── prettier.config.mjs       # Prettier 3.6設定
├── bunfig.toml               # Bun統合設定
└── .gitignore
```

### Co-location方式のメリット

- **関連ファイルの集約**: コンポーネントとテストが同じディレクトリに配置され、見つけやすい
- **移動の簡単さ**: コンポーネントを移動する際、テストも一緒に移動できる
- **インポートパスの短縮**: `import Button from './Button'` のように相対パスが短くなる
- **保守性向上**: コンポーネント修正時にテストが隣にあるため、テスト更新を忘れにくい

## 🔧 環境設定

### 2025年版初期セットアップ

#### 🚀 Bun統合ワークフロー

```bash
# プロジェクト初期化（Bunで新規作成時）
bun init frontend-app
cd frontend-app

# 既存プロジェクトの場合
cd frontend

# 依存関係のインストール（npm比20倍高速）
bun install

# 開発サーバー起動（Hot Reload有効）
bun dev                      # Bunランタイムで直接実行
bun run dev:vite             # Viteサーバー使用

# ビルドとデプロイ
bun run build                # 型チェック + ビルド
bun run preview              # プロダクションプレビュー

# テスト実行
bun test                     # Bunネイティブテスト
bun run test:vitest          # Vitest使用
bun run test:watch           # ウォッチモード

# 品質チェック（2025年統合コマンド）
bun run quality:check        # フォーマット + リント + 型チェック
bun run quality:fix          # 自動修正
```

#### 📊 パフォーマンス比較

| 操作 | Bun | npm | 改善倍率 |
|------|-----|-----|----------|
| **インストール** | 2s | 40s | 20x |
| **サーバー起動** | 0.3s | 2s | 6.7x |
| **ホットリロード** | 50ms | 200ms | 4x |
| **テスト実行** | 1s | 5s | 5x |

### 絶対パスインポート設定

#### tsconfig.json
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/utils/*": ["src/utils/*"],
      "@/types/*": ["src/types/*"],
      "@/store/*": ["src/store/*"]
    }
  }
}
```

#### bunfig.toml（2025年新規）

```toml
# Bun統合設定ファイル
[install]
cache = true
optional = true
dev = true

[test]
preload = ["./tests/setup.ts"]
timeout = 30000

[test.coverage]
enabled = true
reporter = ["text", "json", "html"]
threshold = 80

[resolve]
extensions = [".tsx", ".ts", ".jsx", ".js", ".json"]
alias = {
  "@" = "./src",
  "@components" = "./src/components",
  "@hooks" = "./src/hooks",
  "@utils" = "./src/utils",
  "@types" = "./src/types"
}

[dev]
hot = true
port = 3000

[performance]
heap_size = "2gb"
max_old_space_size = 4096
```

#### vite.config.ts（Bun統合版）
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/utils': path.resolve(__dirname, './src/utils'),
      '@/types': path.resolve(__dirname, './src/types'),
      '@/store': path.resolve(__dirname, './src/store'),
    },
  },
});
```

### 2025年版 package.json 設定

#### 📦 パッケージ情報

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "type": "module",
  "packageManager": "bun@1.1.42",
  "engines": {
    "node": ">=18.0.0",
    "bun": ">=1.0.0"
  }
}
```

#### 🚀 2025年版スクリプト設定

```json
{
  "scripts": {
    // 開発サーバー（Bun統合）
    "dev": "bun run --hot src/main.tsx",
    "dev:vite": "vite",
    
    // ビルドシステム
    "build": "bun run typecheck && vite build",
    "preview": "vite preview",
    
    // 品質管理（2025統合）
    "lint": "eslint . --fix",
    "lint:check": "eslint .",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    
    // テスト（Bun + Vitestハイブリッド）
    "test": "bun test",
    "test:vitest": "vitest",
    "test:coverage": "vitest --coverage",
    "test:watch": "bun test --watch",
    
    // 統合品質チェック（2025ベストプラクティス）
    "quality:check": "bun run format:check && bun run lint:check && bun run typecheck",
    "quality:fix": "bun run format && bun run lint",
    
    // Bun特有機能
    "install:bun": "bun install",
    "clean": "rm -rf dist node_modules .bun"
  },
  
  
  // 依存関係（2025最新版）
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  
  // 開発依存関係（2025最新版）
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "eslint": "^8.57.0",
    "eslint-plugin-jsx-a11y": "^6.8.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "eslint-plugin-simple-import-sort": "^10.0.0",
    "jest-axe": "^8.0.0",
    "prettier": "^3.0.0",
    "simple-git-hooks": "^2.9.0",
    "typescript": "^5.0.0",
    "typescript-eslint": "^6.0.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

### Import順序の自動整理について

新しい設定では、`simple-import-sort`プラグインにより以下の順序でimportが自動整理されます：

```typescript
// 1. React関連（最優先）
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

// 2. 外部ライブラリ
import axios from 'axios';
import { z } from 'zod';
import clsx from 'clsx';

// 3. 内部パッケージ（@/ パス）
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { UserService } from '@/services/UserService';

// 4. 相対インポート
import './styles.css';
import { helper } from '../utils/helper';
import { localConfig } from './config';

// 5. 型のみインポート（最後）
import type { User } from '@/types/User';
import type { ComponentProps } from 'react';
```

### 開発用コマンド

```bash
# 開発サーバー起動
bun dev

# 品質チェック（CI用 - チェックのみ）
bun run quality:check

# 品質修正（開発用 - 自動修正）
bun run quality:fix

# 個別チェック
bun run format:check     # フォーマットチェックのみ
bun run lint             # リンティングチェックのみ  
bun run typecheck        # 型チェックのみ

# テスト関連（2025年Bunハイブリッド）
bun test                 # Bunネイティブテスト（高速）
bun run test:vitest      # Vitest使用（統合テスト）
bun run test:coverage    # カバレッジ付きテスト
bun run test:watch       # ウォッチモードでテスト

# パッケージ管理（Bunの威力を体感）
bun install              # npm比20倍高速インストール
bun update               # 依存関係更新
bun clean                # キャッシュクリア
```

## 🗃️ 状態管理戦略

### 1. 状態管理ライブラリの選択指針

| 複雑度 | 推奨ライブラリ | 適用場面 |
|--------|---------------|----------|
| **Simple** | React Context + useReducer | 小規模アプリ、テーマ管理 |
| **Medium** | [Zustand](https://zustand.docs.pmnd.rs/) | 中規模アプリ、クライアント状態 |
| **Complex** | [Jotai](https://jotai.org/) | 大規模アプリ、アトミックな状態管理 |

### 2. React Context パターン（シンプルな場合）

```typescript
// store/ThemeContext.tsx
import { createContext, useContext, useReducer, ReactNode } from 'react';

// 状態の型定義
interface ThemeState {
  theme: 'light' | 'dark';
  fontSize: 'small' | 'medium' | 'large';
}

// アクションの型定義
type ThemeAction = 
  | { type: 'TOGGLE_THEME' }
  | { type: 'SET_FONT_SIZE'; payload: ThemeState['fontSize'] };

// 初期状態
const initialState: ThemeState = {
  theme: 'light',
  fontSize: 'medium',
};

// リデューサー
function themeReducer(state: ThemeState, action: ThemeAction): ThemeState {
  switch (action.type) {
    case 'TOGGLE_THEME':
      return {
        ...state,
        theme: state.theme === 'light' ? 'dark' : 'light',
      };
    case 'SET_FONT_SIZE':
      return {
        ...state,
        fontSize: action.payload,
      };
    default:
      return state;
  }
}

// Context作成
const ThemeContext = createContext<{
  state: ThemeState;
  dispatch: React.Dispatch<ThemeAction>;
} | undefined>(undefined);

// Provider コンポーネント
export function ThemeProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(themeReducer, initialState);

  return (
    <ThemeContext.Provider value={{ state, dispatch }}>
      {children}
    </ThemeContext.Provider>
  );
}

// カスタムフック
export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// 使用例
function App() {
  const { state, dispatch } = useTheme();

  const toggleTheme = () => {
    dispatch({ type: 'TOGGLE_THEME' });
  };

  const changeFontSize = (size: ThemeState['fontSize']) => {
    dispatch({ type: 'SET_FONT_SIZE', payload: size });
  };

  return (
    <div className={`theme-${state.theme} font-${state.fontSize}`}>
      <button onClick={toggleTheme}>
        Switch to {state.theme === 'light' ? 'dark' : 'light'} theme
      </button>
      <button onClick={() => changeFontSize('large')}>
        Large Font
      </button>
    </div>
  );
}
```

### 3. Zustand パターン（中規模アプリ）

```typescript
// store/userStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// 状態の型定義
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface UserState {
  user: User | null;
  users: User[];
  loading: boolean;
  error: string | null;
}

// アクションの型定義
interface UserActions {
  // ユーザー管理
  setUser: (user: User | null) => void;
  updateUser: (updates: Partial<User>) => void;
  
  // ユーザーリスト管理
  setUsers: (users: User[]) => void;
  addUser: (user: User) => void;
  removeUser: (userId: string) => void;
  
  // 非同期アクション
  fetchUser: (userId: string) => Promise<void>;
  fetchUsers: () => Promise<void>;
  
  // ローディング・エラー管理
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // リセット
  reset: () => void;
}

type UserStore = UserState & UserActions;

// 初期状態
const initialState: UserState = {
  user: null,
  users: [],
  loading: false,
  error: null,
};

// Zustand ストア作成
export const useUserStore = create<UserStore>()(
  devtools(
    persist(
      immer((set, get) => ({
        ...initialState,
        
        // 同期アクション
        setUser: (user) =>
          set((state) => {
            state.user = user;
          }),
        
        updateUser: (updates) =>
          set((state) => {
            if (state.user) {
              Object.assign(state.user, updates);
            }
          }),
        
        setUsers: (users) =>
          set((state) => {
            state.users = users;
          }),
        
        addUser: (user) =>
          set((state) => {
            state.users.push(user);
          }),
        
        removeUser: (userId) =>
          set((state) => {
            state.users = state.users.filter((u) => u.id !== userId);
          }),
        
        // 非同期アクション
        fetchUser: async (userId) => {
          const { setLoading, setError, setUser } = get();
          
          setLoading(true);
          setError(null);
          
          try {
            const response = await fetch(`/api/users/${userId}`);
            if (!response.ok) {
              throw new Error('Failed to fetch user');
            }
            const user = await response.json();
            setUser(user);
          } catch (error) {
            setError(error instanceof Error ? error.message : 'Unknown error');
          } finally {
            setLoading(false);
          }
        },
        
        fetchUsers: async () => {
          const { setLoading, setError, setUsers } = get();
          
          setLoading(true);
          setError(null);
          
          try {
            const response = await fetch('/api/users');
            if (!response.ok) {
              throw new Error('Failed to fetch users');
            }
            const users = await response.json();
            setUsers(users);
          } catch (error) {
            setError(error instanceof Error ? error.message : 'Unknown error');
          } finally {
            setLoading(false);
          }
        },
        
        // ユーティリティ
        setLoading: (loading) =>
          set((state) => {
            state.loading = loading;
          }),
        
        setError: (error) =>
          set((state) => {
            state.error = error;
          }),
        
        reset: () => set(initialState),
      })),
      {
        name: 'user-store', // localStorage key
        partialize: (state) => ({ user: state.user }), // 永続化する部分のみ
      }
    ),
    {
      name: 'user-store', // DevTools名
    }
  )
);

// セレクタ（派生状態）
export const useUserSelectors = () => {
  const store = useUserStore();
  
  return {
    // 基本セレクタ
    currentUser: store.user,
    allUsers: store.users,
    isLoading: store.loading,
    error: store.error,
    
    // 派生セレクタ
    isLoggedIn: !!store.user,
    userCount: store.users.length,
    activeUsers: store.users.filter((user) => user.email.includes('@')),
    
    // アクション
    actions: {
      setUser: store.setUser,
      updateUser: store.updateUser,
      fetchUser: store.fetchUser,
      fetchUsers: store.fetchUsers,
      addUser: store.addUser,
      removeUser: store.removeUser,
      reset: store.reset,
    },
  };
};

// 使用例コンポーネント
function UserProfile() {
  const { currentUser, isLoading, error, actions } = useUserSelectors();
  
  useEffect(() => {
    if (!currentUser) {
      actions.fetchUser('current');
    }
  }, [currentUser, actions]);
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!currentUser) return <div>Please log in</div>;
  
  return (
    <div>
      <h1>{currentUser.name}</h1>
      <p>{currentUser.email}</p>
      <button
        onClick={() => actions.updateUser({ name: 'Updated Name' })}
      >
        Update Name
      </button>
    </div>
  );
}
```

### 4. Jotai パターン（大規模・アトミック）

```typescript
// store/atoms.ts
import { atom } from 'jotai';
import { atomWithStorage, atomWithReset } from 'jotai/utils';

// 基本アトム
export const countAtom = atom(0);
export const nameAtom = atom('');

// ローカルストレージ連携
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light');

// リセット可能アトム
export const userFormAtom = atomWithReset({
  name: '',
  email: '',
  bio: '',
});

// 派生アトム（読み取り専用）
export const doubleCountAtom = atom((get) => get(countAtom) * 2);

// 派生アトム（読み書き）
export const uppercaseNameAtom = atom(
  (get) => get(nameAtom).toUpperCase(),
  (get, set, newValue: string) => {
    set(nameAtom, newValue.toLowerCase());
  }
);

// 非同期アトム
export interface User {
  id: string;
  name: string;
  email: string;
}

export const userIdAtom = atom<string | null>(null);

export const userAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  if (!userId) return null;
  
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json() as Promise<User>;
});

// 書き込み専用アトム（アクション）
export const incrementCountAtom = atom(
  null, // 読み取り不要
  (get, set) => {
    const current = get(countAtom);
    set(countAtom, current + 1);
  }
);

export const decrementCountAtom = atom(
  null,
  (get, set) => {
    const current = get(countAtom);
    set(countAtom, current - 1);
  }
);

// 複雑なアクションアトム
export const updateUserAtom = atom(
  null,
  async (get, set, userUpdates: Partial<User>) => {
    const currentUserId = get(userIdAtom);
    if (!currentUserId) throw new Error('No user selected');
    
    const response = await fetch(`/api/users/${currentUserId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userUpdates),
    });
    
    if (!response.ok) {
      throw new Error('Failed to update user');
    }
    
    // ユーザーアトムを再取得させる
    // 依存関係が変更されると自動的に再計算される
  }
);

// ファミリーアトム（動的アトム生成）
export const todoAtomFamily = atomFamily((id: string) =>
  atomWithStorage(`todo-${id}`, {
    id,
    text: '',
    completed: false,
  })
);

// 使用例
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const [doubleCount] = useAtom(doubleCountAtom);
  const [, increment] = useAtom(incrementCountAtom);
  const [, decrement] = useAtom(decrementCountAtom);
  
  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}

function UserComponent() {
  const [userId, setUserId] = useAtom(userIdAtom);
  const [user] = useAtom(userAtom);
  const [, updateUser] = useAtom(updateUserAtom);
  
  return (
    <div>
      <input 
        value={userId || ''} 
        onChange={(e) => setUserId(e.target.value)}
        placeholder="User ID"
      />
      
      <Suspense fallback={<div>Loading user...</div>}>
        {user && (
          <div>
            <h2>{user.name}</h2>
            <p>{user.email}</p>
            <button 
              onClick={() => updateUser({ name: 'Updated Name' })}
            >
              Update Name
            </button>
          </div>
        )}
      </Suspense>
    </div>
  );
}
```

### 5. 状態管理のベストプラクティス

#### 状態の分離原則

```typescript
// ❌ 避けるべき: 全てを1つの大きな状態に
interface AppState {
  user: User;
  products: Product[];
  cart: CartItem[];
  ui: UIState;
  theme: Theme;
  // ... 他にも多数
}

// ✅ 推奨: 責任に応じて分離
const useUserStore = create<UserState>(() => ({ /* ... */ }));
const useProductStore = create<ProductState>(() => ({ /* ... */ }));
const useCartStore = create<CartState>(() => ({ /* ... */ }));
const useUIStore = create<UIState>(() => ({ /* ... */ }));
```

#### 非同期処理の統一

```typescript
// 共通の非同期処理パターン
interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

function createAsyncSlice<T>() {
  return {
    data: null as T | null,
    loading: false,
    error: null as string | null,
    
    setLoading: (state: AsyncState<T>, loading: boolean) => {
      state.loading = loading;
      if (loading) state.error = null;
    },
    
    setData: (state: AsyncState<T>, data: T) => {
      state.data = data;
      state.loading = false;
      state.error = null;
    },
    
    setError: (state: AsyncState<T>, error: string) => {
      state.error = error;
      state.loading = false;
    },
  };
}
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

## 🔍 ESLint設定詳細（2025年版 Flat Config）

### 2025年の主要改善点

#### ESLint Flat Config採用
- **従来の課題**: 複雑な `extends` チェーン、設定の継承問題
- **2025年解決策**: Flat Config による明確で柔軟な設定
- **効果**: ファイル別ルール適用、パーサー・プラグインの細かい制御

#### 包括的なルールセット

##### TypeScript厳格ルール（2025年強化）
```javascript
// strictTypeChecked: より厳格な型チェック
'@typescript-eslint/no-explicit-any': 'error',        // any禁止
'@typescript-eslint/strict-boolean-expressions': 'error', // boolean式の厳格化
'@typescript-eslint/prefer-nullish-coalescing': 'error',   // ?? 演算子推奨
'@typescript-eslint/prefer-optional-chain': 'error',      // ?. 演算子推奨
```

##### React関連（2025年ベストプラクティス）
```javascript
// パフォーマンス重視
'react/jsx-no-bind': 'error',              // レンダー内での関数バインド禁止
'react-hooks/exhaustive-deps': 'error',    // 依存配列の厳格チェック
'react/jsx-curly-brace-presence': 'error', // 不要な{}削除
'react/self-closing-comp': 'error',        // 自己終了タグ強制
```

##### アクセシビリティ強化（2025年重点項目）
```javascript
// 完全なjsx-a11y統合
...jsxA11y.configs.recommended.rules,
'jsx-a11y/no-autofocus': 'error',
'jsx-a11y/click-events-have-key-events': 'error',
'jsx-a11y/no-static-element-interactions': 'error',
```

##### Import整理（2025年パターン）
```javascript
// simple-import-sort による自動整理
'simple-import-sort/imports': ['error', {
  groups: [
    ['^node:'],                    // Node.js builtins
    ['^react', '^@?\\w'],         // React関連
    ['^(@|~)/'],                  // 内部パッケージ
    ['^\\.\\.', '^\\.'],          // 相対インポート
    ['^.+\\.s?css$'],             // スタイル
    ['^.+\\u0000$'],              // 型インポート
  ],
}],
```

#### ファイル別設定（2025年柔軟性）

##### テストファイル専用ルール
```javascript
{
  files: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',     // テストではany許可
    '@typescript-eslint/strict-boolean-expressions': 'off',
    'jsx-a11y/no-autofocus': 'off',                  // テストコンポーネント
  }
}
```

##### 設定ファイル専用ルール
```javascript
{
  files: ['*.config.{js,ts}', 'vite.config.ts'],
  languageOptions: {
    globals: { ...globals.node }
  },
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'off'
  }
}
```

### 設定カスタマイズ（改良版）

#### 必要な依存関係のインストール

```bash
# 必須プラグインのインストール
bun add -D eslint-plugin-simple-import-sort eslint-plugin-jsx-a11y
```

#### 完全なESLint設定

```javascript
// eslint.config.js
import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import simpleImportSort from 'eslint-plugin-simple-import-sort';

export default tseslint.config(
  { ignores: ['dist', 'node_modules', 'coverage'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
      'jsx-a11y': jsxA11y,
      'simple-import-sort': simpleImportSort,
    },
    rules: {
      // React Hooks
      ...reactHooks.configs.recommended.rules,
      
      // アクセシビリティ
      ...jsxA11y.configs.recommended.rules,
      
      // React Refresh
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
      
      // Import順序（自動整理）
      'simple-import-sort/imports': [
        'error',
        {
          groups: [
            // React関連を最初に
            ['^react', '^@?\\w'],
            // 内部パッケージ
            ['^(@|~)/'],
            // 相対インポート
            ['^\\.\\.(?!/?$)', '^\\.\\./?$'],
            ['^\\./(?=.*/)(?!/?$)', '^\\.(?!/?$)', '^\\./?$'],
            // 型インポート
            ['^.+\\u0000$'],
          ],
        },
      ],
      'simple-import-sort/exports': 'error',
      
      // TypeScript厳格化
      '@typescript-eslint/no-explicit-any': 'error', // warn から error に変更
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/explicit-function-return-type': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      
      // 一般的な品質ルール
      'react/prop-types': 'off', // TypeScript使用時は不要
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
      'object-shorthand': 'error',
      'prefer-template': 'error',
      
      // アクセシビリティルールの強化
      'jsx-a11y/no-autofocus': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/no-static-element-interactions': 'error',
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-proptypes': 'error',
      'jsx-a11y/aria-unsupported-elements': 'error',
      'jsx-a11y/heading-has-content': 'error',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      
      // React/Hooks ベストプラクティス
      'react-hooks/exhaustive-deps': 'error',
      'react-hooks/rules-of-hooks': 'error',
    },
  },
  // テストファイル専用の設定
  {
    files: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off', // テストではanyを許可
      'jsx-a11y/no-autofocus': 'off', // テストコンポーネントでは許可
    },
  }
);
```

### simple-git-hooks設定

```json
// .simple-git-hooks.json
{
  "pre-commit": "bun run pre-commit",
  "pre-push": "bun run quality:check && bun run test --run"
}
```

```bash
# セットアップコマンド
bun add -D simple-git-hooks
bun simple-git-hooks  # hooks を有効化
```

## 💫 ESLint Flat Config（2025年標準）

### 🚀 次世代設定方式への完全移行

2025年、ESLint v9でFlat Configが完全標準化され、従来の`.eslintrc`は非推奨となりました。

#### 主要な改善点
- **柔軟な設定**: ファイル別ルール適用が簡単
- **プラグイン統合**: より直感的なプラグイン管理
- **TypeScript厳格チェック**: 2025年強化ルールセット
- **パフォーマンス向上**: 設定解決の高速化

### ⚙️ 設定ファイル構造

```javascript
// eslint.config.mjs - 2025年標準設定
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';
import prettierRecommended from 'eslint-plugin-prettier/recommended';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import simpleImportSort from 'eslint-plugin-simple-import-sort';

export default tseslint.config(
  // 無視パターン
  {
    ignores: ['dist/', 'node_modules/', '**/*.d.ts', 'coverage/'],
  },
  
  // 基本設定
  prettierRecommended,
  eslint.configs.recommended,
  
  // TypeScriptファイル設定
  {
    files: ['**/*.ts', '**/*.tsx'],
    extends: [...tseslint.configs.strictTypeChecked],
    plugins: {
      '@typescript-eslint': tseslint.plugin,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
      'simple-import-sort': simpleImportSort,
    },
    languageOptions: {
      parser: tseslint.parser,
      ecmaVersion: 2025,
      globals: { ...globals.browser, ...globals.es2025 },
      parserOptions: {
        project: './tsconfig.json',
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      // 2025年強化ルール
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'error',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      
      // React Hooks
      ...reactHooks.configs.recommended.rules,
      
      // アクセシビリティ
      ...jsxA11y.configs.recommended.rules,
      
      // インポート整理
      'simple-import-sort/imports': 'error',
      'simple-import-sort/exports': 'error',
    },
  },
  
  // テストファイル用設定
  {
    files: ['**/*.test.{ts,tsx}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/strict-boolean-expressions': 'off',
    },
  }
);
```

## 🎨 Prettier 3.6（2025最新版）

### 🚀 新機能と改善点

#### 2025年の主要アップデート
- **実験的高速CLI**: 大規模プロジェクトでの高速処理
- **ファイル単位無効化**: `@noformat`、`@noprettier`プラグマサポート
- **改善されたキャッシュ戦略**: メモリ使用量とCPU効率の最適化

### 📝 2025年推奨設定

```javascript
// prettier.config.mjs - ESM形式で設定
export default {
  // コアフォーマット
  semi: true,
  singleQuote: true,
  trailingComma: 'all',
  tabWidth: 2,
  printWidth: 100,              // 2025: モダンスクリーン対応で100に増加
  useTabs: false,
  
  // コードスタイル
  arrowParens: 'always',
  endOfLine: 'lf',
  bracketSpacing: true,
  bracketSameLine: false,
  
  // JSX固有
  jsxSingleQuote: false,
  
  // 2025新機能
  experimentalTernaries: false,  // 安定性重視で無効
  
  // プラグイン設定
  plugins: [
    // 'prettier-plugin-tailwindcss', // Tailwind使用時
  ],
  
  // ファイル別設定
  overrides: [
    {
      files: '*.md',
      options: {
        proseWrap: 'always',
        printWidth: 80,
      },
    },
    {
      files: '*.json',
      options: {
        printWidth: 120,
      },
    },
  ],
};
```

### 🔍 ファイル単位無効化（2025新機能）

```typescript
// ファイル全体をフォーマット対象外にする
/* @noformat */
const uglyCode={a:1,b:2,c:3}; // このファイルはPrettierが無視

// 特定部分のみフォーマットを無効化
// prettier-ignore
const matrix = [
  [1,  2,  3],
  [4,  5,  6],
  [7,  8,  9]
];
```

### 📊 2025年パフォーマンス比較

| 項目 | Prettier 3.6 | 旧バージョン | 改善倍率 |
|------|---------------|------------|----------|
| **大規模ファイル** | 2.1s | 5.8s | 2.8x |
| **キャッシュ有効** | 0.3s | 1.2s | 4x |
| **メモリ使用量** | -40% | ベース | 40%削減 |

### 自動フォーマット例（2025設定適用）

```typescript
// Before
const user={name:"John",age:30};
const getName=user=>user.name;

// After
const user = { name: 'John', age: 30 };
const getName = (user) => user.name;
```

## 🧪 テスト戦略（2025年版BDDアプローチ）

### 2025年のテストベストプラクティス

#### 行動駆動テスト（BDD）の採用
- **従来の課題**: 実装詳細に依存したテスト、保守性の低さ
- **2025年解決策**: ユーザー行動に焦点を当てたテスト設計
- **効果**: より分かりやすく、変更に強いテスト

### 1. BDDテストファイル構造（推奨）

```typescript
// LoginForm.test.tsx - BDD アプローチ
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm - User Authentication Behavior', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
  });

  describe('when user attempts to login with valid credentials', () => {
    it('should successfully authenticate and redirect to dashboard', async () => {
      // Given: A user on the login page
      render(<LoginForm />);

      // When: The user enters valid credentials
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/password/i), 'ValidPassword123!');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: The user should be authenticated
      expect(await screen.findByText(/welcome back/i)).toBeInTheDocument();
    });
  });

  describe('when user submits empty form', () => {
    it('should show validation errors', async () => {
      // Given: A user on the login page
      render(<LoginForm />);

      // When: The user submits without filling fields
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: Validation errors should be displayed
      expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
      expect(await screen.findByText(/password is required/i)).toBeInTheDocument();
    });
  });
});
```

### 2. テスト設計原則（2025年版）

#### Given-When-Then構造
```typescript
// ✅ 推奨: 明確な行動記述
it('should display error when API request fails', async () => {
  // Given: API will return an error
  mockApi.getUser.mockRejectedValue(new Error('Network error'));
  
  // When: User loads the profile page
  render(<UserProfile userId="123" />);
  
  // Then: Error message should be displayed
  expect(await screen.findByRole('alert')).toHaveTextContent('Failed to load user');
});

// ❌ 避けるべき: 実装詳細のテスト
it('should call getUserApi with correct parameters', () => {
  render(<UserProfile userId="123" />);
  expect(mockApi.getUser).toHaveBeenCalledWith('123');
});
```

#### 単一責任原則
```typescript
// ✅ 推奨: 一つの行動に集中
describe('when user clicks save button', () => {
  it('should save form data', async () => { /* ... */ });
  it('should show success message', async () => { /* ... */ });
  it('should disable form during save', async () => { /* ... */ });
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
  // Given: A form is rendered
  render(<ContactForm />);
  
  // When: User fills out the form
  await user.type(screen.getByLabelText(/name/i), 'John Doe');
  await user.type(screen.getByLabelText(/email/i), 'john@example.com');
  await user.type(screen.getByLabelText(/message/i), 'Hello world!');
  
  // Then: Form should reflect the input
  expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
  expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
  expect(screen.getByDisplayValue('Hello world!')).toBeInTheDocument();
});

// カスタムフックのテスト（2025年版 BDDアプローチ）
describe('useCounter hook behavior', () => {
  it('should increment count when increment is called', () => {
    // Given: A counter hook initialized with 0
    const { result } = renderHook(() => useCounter(0));
    
    // When: Increment is called
    act(() => {
      result.current.increment();
    });
    
    // Then: Count should be 1
    expect(result.current.count).toBe(1);
  });
});
```

#### 統合テスト（2025年版アプローチ）

```typescript
// 複数コンポーネント間の相互作用テスト
describe('User Registration Flow', () => {
  it('should complete registration from start to finish', async () => {
    // Given: User is on the registration page
    render(<App />, { wrapper: RouterWrapper });
    
    // When: User navigates to registration
    await user.click(screen.getByRole('link', { name: /sign up/i }));
    
    // And: User fills out registration form
    await user.type(screen.getByLabelText(/email/i), 'newuser@example.com');
    await user.type(screen.getByLabelText(/password/i), 'SecurePass123!');
    await user.click(screen.getByRole('button', { name: /create account/i }));
    
    // Then: User should be redirected to dashboard
    expect(await screen.findByText(/welcome to your dashboard/i)).toBeInTheDocument();
  });
});
```

#### アクセシビリティテスト（2025年重点項目）

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('accessibility compliance', () => {
  it('should have no accessibility violations', async () => {
    // Given: A component is rendered
    const { container } = render(<LoginForm />);
    
    // When: Running accessibility checks
    const results = await axe(container);
    
    // Then: No violations should be found
    expect(results).toHaveNoViolations();
  });
  
  it('should be navigable with keyboard', async () => {
    // Given: A form is rendered
    render(<LoginForm />);
    
    // When: User navigates with Tab key
    await user.tab();
    expect(screen.getByLabelText(/email/i)).toHaveFocus();
    
    await user.tab();
    expect(screen.getByLabelText(/password/i)).toHaveFocus();
    
    await user.tab();
    expect(screen.getByRole('button', { name: /sign in/i })).toHaveFocus();
  });
});
```

### 4. モック戦略（2025年ベストプラクティス）

#### API モック

```typescript
// __mocks__/api.ts
import { vi } from 'vitest';
import type { User, ApiResponse } from '@/types/api';

export const mockUserApi = {
  getUser: vi.fn<[string], Promise<ApiResponse<User>>>(),
  updateUser: vi.fn<[string, Partial<User>], Promise<ApiResponse<User>>>(),
  deleteUser: vi.fn<[string], Promise<void>>(),
};

// テストでの使用
beforeEach(() => {
  vi.clearAllMocks();
});

it('should handle API error gracefully', async () => {
  // Given: API will return error
  mockUserApi.getUser.mockRejectedValue(new Error('Server error'));
  
  // When: Component attempts to load user
  render(<UserProfile userId="123" />);
  
  // Then: Error message should be displayed
  expect(await screen.findByRole('alert')).toHaveTextContent('Failed to load user data');
});
```

#### ルーター モック

```typescript
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

it('should navigate to dashboard after login', async () => {
  // Given: User is on login page
  render(<LoginForm />, { wrapper: MemoryRouter });
  
  // When: User submits valid credentials
  await user.type(screen.getByLabelText(/email/i), 'user@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /sign in/i }));
  
  // Then: Navigation should occur
  expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
});
```

### 5. テストカバレッジ目標（2025年基準）

| 分類 | 目標カバレッジ | 重点項目 |
|------|--------------|----------|
| **重要機能** | 95%+ | ユーザー認証、決済、データ変更 |
| **一般コンポーネント** | 80%+ | フォーム、ナビゲーション、表示 |
| **ユーティリティ** | 90%+ | 計算、バリデーション、変換 |
| **統合テスト** | 70%+ | ページ遷移、API連携 |

### 6. テスト実行戦略

```bash
# 開発中の高速テスト
bun test --watch --changed

# CI用の完全テスト
bun test --coverage --reporter=verbose

# アクセシビリティテストのみ
bun test --testNamePattern="accessibility"

# パフォーマンステスト
bun test --testNamePattern="performance"
```

## 🚀 パフォーマンス最適化（2025年版）

### 1. コード分割とレイジーローディング

```typescript
// ルートレベルでの分割
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('@/pages/Dashboard'));
const UserProfile = lazy(() => import('@/pages/UserProfile'));
const Settings = lazy(() => import('@/pages/Settings'));

function App() {
  return (
    <Router>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

// コンポーネントレベルでの分割
const HeavyChart = lazy(() => import('@/components/HeavyChart'));

function DashboardPage() {
  const [showChart, setShowChart] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### 2. メモ化戦略（2025年版）

```typescript
// React.memo で重い再レンダリングを防ぐ
const ExpensiveComponent = React.memo<{
  data: ComplexData[];
  onUpdate: (id: string) => void;
}>(({ data, onUpdate }) => {
  return (
    <div>
      {data.map(item => (
        <ComplexItem 
          key={item.id} 
          item={item} 
          onUpdate={onUpdate}
        />
      ))}
    </div>
  );
}, (prevProps, nextProps) => {
  // カスタム比較関数
  return (
    prevProps.data.length === nextProps.data.length &&
    prevProps.data.every((item, index) => 
      item.id === nextProps.data[index].id &&
      item.updatedAt === nextProps.data[index].updatedAt
    )
  );
});

// useMemo で計算結果をキャッシュ
function DataVisualization({ rawData }: { rawData: RawData[] }) {
  const processedData = useMemo(() => {
    // 重い計算処理
    return rawData
      .filter(item => item.isValid)
      .map(item => ({
        ...item,
        computed: expensiveCalculation(item)
      }))
      .sort((a, b) => a.computed - b.computed);
  }, [rawData]);
  
  return <Chart data={processedData} />;
}

// useCallback で関数の再生成を防ぐ
function ParentComponent() {
  const [items, setItems] = useState<Item[]>([]);
  
  const handleItemUpdate = useCallback((id: string, updates: Partial<Item>) => {
    setItems(prevItems => 
      prevItems.map(item => 
        item.id === id ? { ...item, ...updates } : item
      )
    );
  }, []);
  
  return (
    <ItemList 
      items={items} 
      onUpdate={handleItemUpdate}
    />
  );
}
```

### 3. バンドル最適化

```typescript
// vite.config.ts - 2025年最適化設定
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: 'bundle-analysis.html',
      open: true,
    })
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // 別々のチャンクに分割
          vendor: ['react', 'react-dom'],
          ui: ['@headlessui/react', '@heroicons/react'],
          utils: ['date-fns', 'lodash-es'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
});
```

## 🔒 セキュリティベストプラクティス（2025年版）

### 1. 入力検証とサニタイゼーション

```typescript
import { z } from 'zod';
import DOMPurify from 'dompurify';

// Zodによる型安全な入力検証
const UserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.number().min(18, 'Must be 18 or older').max(120, 'Invalid age'),
});

function UserForm() {
  const handleSubmit = (formData: FormData) => {
    try {
      // 検証の実行
      const validatedData = UserSchema.parse({
        email: formData.get('email'),
        name: formData.get('name'),
        age: parseInt(formData.get('age') as string),
      });
      
      // サニタイゼーション
      const sanitizedData = {
        ...validatedData,
        name: DOMPurify.sanitize(validatedData.name),
      };
      
      // 安全なデータで処理続行
      submitUser(sanitizedData);
    } catch (error) {
      if (error instanceof z.ZodError) {
        setErrors(error.errors);
      }
    }
  };
}
```

### 2. XSS対策

```typescript
// dangerouslySetInnerHTMLの安全な使用
function SafeHtmlContent({ htmlContent }: { htmlContent: string }) {
  const sanitizedHtml = useMemo(() => {
    return DOMPurify.sanitize(htmlContent, {
      ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'a'],
      ALLOWED_ATTR: ['href', 'title'],
    });
  }, [htmlContent]);
  
  return (
    <div 
      dangerouslySetInnerHTML={{ __html: sanitizedHtml }}
    />
  );
}

// CSP (Content Security Policy) の設定
// index.html
<meta 
  http-equiv="Content-Security-Policy" 
  content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
/>
```

## 📚 VS Code統合設定（2025年版）

### IDE統合のメリット

- **リアルタイム品質チェック**: 編集中にESLint/Prettierエラーの即座表示
- **自動修正**: 保存時の自動フォーマット・lint修正
- **型チェック統合**: TypeScriptエラーのリアルタイム表示
- **テスト統合**: エディタ内でのテスト実行・デバッグ

### 推奨拡張機能（2025年更新版）

```json
// .vscode/extensions.json で推奨
{
  "recommendations": [
    // JavaScript/TypeScript開発
    "dbaeumer.vscode-eslint",           // ESLint (Flat Config対応)
    "esbenp.prettier-vscode",           // Prettier
    "bradlc.vscode-tailwindcss",        // Tailwind CSS
    
    // React開発
    "dsznajder.es7-react-js-snippets",  // Reactスニペット
    
    // テスト
    "vitest.explorer",                  // Vitestテストエクスプローラー
    
    // 品質・セキュリティ
    "SonarSource.sonarlint-vscode",     // SonarLint
    "usernamehw.errorlens",             // エラー強調表示
    
    // AI支援 (2025年)
    "github.copilot",                   // GitHub Copilot
    "github.copilot-chat"               // Copilot Chat
  ]
}
```

### ワークスペース設定最適化

設定ファイル `.vscode/settings.json` により、以下が自動実行されます：

- **保存時自動フォーマット**: Prettier による即座整形
- **ESLint自動修正**: 修正可能な問題の自動解決
- **インポート整理**: simple-import-sort による自動並び替え
- **型チェック**: TypeScript エラーのリアルタイム表示

## 📖 まとめ

このJavaScript/TypeScript開発ガイドでは、2025年の最新ベストプラクティスを網羅しています：

### 🎯 主要な改善点

1. **ESLint Flat Config**: より柔軟で理解しやすい設定システム
2. **BDDテストアプローチ**: ユーザー行動に焦点を当てた持続可能なテスト
3. **包括的品質管理**: セキュリティ・アクセシビリティ・パフォーマンスの統合
4. **IDE統合最適化**: リアルタイムフィードバックによる開発効率向上

### 🚀 開発者体験の向上

- **自動化**: フォーマット・lint・テストの自動実行
- **リアルタイム**: VS Code統合によるエラーの即座発見
- **品質保証**: CI/CDでの継続的品質チェック
- **モダンツール**: Bun・Vite・Vitestによる高速開発

### 📈 継続的改善

本ガイドの設定により、コードベースは自動的に：
- **一貫性**: 自動フォーマットによる統一スタイル
- **品質**: 包括的リンティングによるバグ予防
- **安全性**: セキュリティルールによる脆弱性検出
- **アクセシビリティ**: a11yチェックによるユーザビリティ向上

開発チーム全体でこれらのプラクティスを共有し、高品質なReact/TypeScriptアプリケーションを構築しましょう。
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

### GitHub Actions での品質チェック

#### 推奨CI/CDパイプライン（チェック重視）

1. **依存関係インストール**: `bun install`
2. **型チェック**: `bun run typecheck`
3. **フォーマットチェック**: `bun run format:check`
4. **リンティングチェック**: `bun run lint`
5. **テスト実行**: `bun test --coverage`
6. **ビルドテスト**: `bun run build`
7. **アクセシビリティテスト**: axe-core による自動テスト

#### GitHub Actions ワークフロー例

```yaml
# .github/workflows/js-ci.yml
name: JavaScript CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Bun
      uses: oven-sh/setup-bun@v1
      with:
        bun-version: latest
    
    - name: Install dependencies
      run: bun install --frozen-lockfile
      
    - name: Type check
      run: bun run typecheck
      
    - name: Format check
      run: bun run format:check
      
    - name: Lint check
      run: bun run lint
      
    - name: Run tests with coverage
      run: bun run test:coverage
      
    - name: Build check
      run: bun run build
      
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
```

#### 開発環境 vs CI環境

| 環境 | フォーマット | リンティング | 目的 |
|------|-------------|-------------|------|
| **開発環境** | `format` (修正) | `lint:fix` (修正) | 開発効率 |
| **CI環境** | `format:check` (チェック) | `lint` (チェック) | 品質保証 |

## ♿ アクセシビリティテスト

### 1. 自動テストの設定

```typescript
// tests/accessibility.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '../src/App';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  it('should not have any accessibility violations', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  it('should have proper heading hierarchy', async () => {
    const { container } = render(<App />);
    const results = await axe(container, {
      rules: {
        'heading-order': { enabled: true },
      },
    });
    expect(results).toHaveNoViolations();
  });
});
```

### 2. 手動テストチェックリスト

#### キーボード操作
- [ ] Tabキーで全てのインタラクティブ要素にフォーカス可能
- [ ] Shift+Tabで逆順フォーカス移動可能
- [ ] Enterキー/Spaceキーで要素を操作可能
- [ ] Escapeキーでモーダル・ドロップダウンを閉じられる

#### スクリーンリーダー対応
- [ ] 画像にalt属性設定
- [ ] フォーム要素にラベル関連付け
- [ ] ボタンに適切なaria-label
- [ ] 状態変更時のaria-live通知

#### 色とコントラスト
- [ ] 色だけでなく形状・テキストでも情報伝達
- [ ] 最低4.5:1のコントラスト比
- [ ] フォーカス表示の視認性

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

// 仮想化（大量データ表示）
import { FixedSizeList as List } from 'react-window';

function VirtualizedList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {Row}
    </List>
  );
}
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