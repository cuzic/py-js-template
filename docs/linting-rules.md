# 🔍 リンティングルール詳細

このドキュメントでは、Python（Ruff）とJavaScript/TypeScript（ESLint）の詳細なリンティング設定について説明します。

## 🐍 Python (Ruff) ルール

### 基本設定

```toml
[tool.ruff]
line-length = 88              # Black と同じ行長制限
target-version = "py313"      # Python 3.13 対応

[tool.ruff.lint]
select = [
    # 基本的な品質チェック
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    
    # モダンPython推奨
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    
    # セキュリティと品質
    "DTZ", # flake8-datetimez
    "T10", # flake8-debugger
    "EM",  # flake8-errmsg
    "FA",  # flake8-future-annotations
    "ISC", # flake8-implicit-str-concat
    "ICN", # flake8-import-conventions
    "G",   # flake8-logging-format
    "INP", # flake8-no-pep420
    "PIE", # flake8-pie
    "T20", # flake8-print
    "PT",  # flake8-pytest-style
    "Q",   # flake8-quotes
    "RSE", # flake8-raise
    "RET", # flake8-return
    "SLF", # flake8-self
    "SIM", # flake8-simplify
    "TID", # flake8-tidy-imports
    "TCH", # flake8-type-checking
    "INT", # flake8-gettext
    "PTH", # flake8-use-pathlib
    "ERA", # eradicate
    "PGH", # pygrep-hooks
    "PL",  # Pylint
    "TRY", # tryceratops
    "FLY", # flynt
    "NPY", # NumPy-specific rules
    "PERF", # Perflint
    "RUF", # Ruff-specific rules
]

ignore = [
    "E501",    # line too long (Black が処理)
    "PLR0913", # too many arguments (一部で必要)
]
```

### 重要なルールカテゴリ

#### 1. コードスタイル (E/W)

| ルール | 説明 | 例 |
|--------|------|-----|
| **E101** | インデント（タブ/スペース混在） | ❌ `    ` + `\t` |
| **E111** | インデント幅不正 | ❌ 3スペース |
| **E201** | 括弧内の不要なスペース | ❌ `( 1, 2 )` |
| **E231** | カンマ後のスペース欠如 | ❌ `[1,2,3]` |
| **E302** | 関数間の空行不足 | ❌ 空行なしで関数定義 |
| **W291** | 行末の空白 | ❌ `print("hello") ` |

#### 2. 論理エラー (F)

| ルール | 説明 | 例 |
|--------|------|-----|
| **F401** | 未使用のimport | ❌ `import os` (未使用) |
| **F821** | 未定義変数の使用 | ❌ `print(undefined_var)` |
| **F841** | 未使用のローカル変数 | ❌ `x = 5` (未使用) |
| **F811** | 変数の再定義 | ❌ 同名関数の重複定義 |

#### 3. モダン構文 (UP)

| ルール | 説明 | 推奨する書き方 |
|--------|------|---------------|
| **UP006** | 型アノテーション | `list[str]` (not `List[str]`) |
| **UP007** | Optional型 | `X | None` (not `Optional[X]`) |
| **UP015** | 古いopen()書き方 | `open()` context manager |
| **UP032** | f-string使用推奨 | `f"{name}"` (not `"{}".format(name)`) |

#### 4. バグ回避 (B)

| ルール | 説明 | 問題のあるコード | 修正版 |
|--------|------|----------------|--------|
| **B006** | 可変デフォルト引数 | `def f(x=[]):` | `def f(x=None):` |
| **B007** | 未使用ループ変数 | `for i in range(10):` | `for _ in range(10):` |
| **B008** | 関数呼び出しをデフォルト引数に | `def f(x=time.now()):` | `def f(x=None):` |
| **B904** | 素のexcept内でraise | `except: raise` | `except: raise from None` |

#### 5. return文最適化 (RET)

| ルール | 説明 | 問題のあるコード | 修正版 |
|--------|------|----------------|--------|
| **RET504** | 不要な代入 | `x = calc(); return x` | `return calc()` |
| **RET505** | 不要なelse | `if x: return y; else: return z` | `if x: return y; return z` |
| **RET506** | 複雑な条件式 | `if not x: return False; return True` | `return bool(x)` |

#### 6. テスト関連 (PT)

| ルール | 説明 | 推奨書き方 |
|--------|------|-----------|
| **PT001** | fixture名衝突回避 | pytest fixture名の重複チェック |
| **PT011** | pytest.raises使用 | 例外テストでのcontext manager使用 |
| **PT023** | 正しいassert | `assert a == b` (not `assert a is b`) |

### ファイル別設定

```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = [
    "T20",   # print文許可（デバッグ用）
    "S101",  # assert文許可（テスト用）
    "PLR2004", # マジックナンバー許可（テストデータ）
]
"scripts/*" = [
    "T20",   # print文許可（スクリプト用）
]
"__init__.py" = [
    "F401",  # 未使用import許可（再エクスポート用）
]
```

## 🟨 JavaScript/TypeScript (ESLint) ルール

### 基本設定 (Flat Config)

```javascript
// eslint.config.js
export default tseslint.config(
  {
    extends: [
      js.configs.recommended,           // JavaScript基本ルール
      ...tseslint.configs.recommended,  // TypeScript推奨ルール
      eslintConfigPrettier,            // Prettierとの競合回避
    ],
    plugins: {
      'react': eslintPluginReact,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
  }
);
```

### 重要なルールカテゴリ

#### 1. TypeScript関連

| ルール | 説明 | 例 |
|--------|------|-----|
| **@typescript-eslint/no-explicit-any** | `any`型の使用警告 | ❌ `const x: any = {}` |
| **@typescript-eslint/no-unused-vars** | 未使用変数検出 | ❌ `const unused = 5` |
| **@typescript-eslint/explicit-function-return-type** | 関数戻り値型明示 | ✅ `(): string => "hello"` |
| **@typescript-eslint/prefer-const** | 再代入されない変数 | ✅ `const` over `let` |
| **@typescript-eslint/no-non-null-assertion** | `!` 演算子の警告 | ❌ `obj!.prop` |

#### 2. React関連

| ルール | 説明 | 例 |
|--------|------|-----|
| **react-hooks/rules-of-hooks** | フックの正しい使用 | ✅ コンポーネント内のみ |
| **react-hooks/exhaustive-deps** | 依存関係配列 | ✅ `useEffect(..., [dep])` |
| **react/jsx-uses-react** | React import | ❌ 不要（React 17+） |
| **react/prop-types** | PropTypes | ❌ 不要（TS使用時） |
| **react-refresh/only-export-components** | HMR対応 | ✅ コンポーネントのみexport |

#### 3. 一般的な品質ルール

| ルール | 説明 | 問題のあるコード | 修正版 |
|--------|------|----------------|--------|
| **no-console** | console文チェック | ❌ `console.log()` | ✅ logger使用 |
| **prefer-const** | const使用推奨 | ❌ `let x = 5` (再代入なし) | ✅ `const x = 5` |
| **no-duplicate-imports** | 重複import禁止 | ❌ 2つのimport文 | ✅ 1つに統合 |
| **no-unused-expressions** | 未使用式禁止 | ❌ `x === 5;` | ✅ `if (x === 5)` |
| **sort-imports** | import順序 | ❌ 逆順 | ✅ アルファベット順 |

### カスタム設定

```javascript
{
  rules: {
    // TypeScript設定
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        'argsIgnorePattern': '^_',      // _で始まる引数は許可
        'varsIgnorePattern': '^_',      // _で始まる変数は許可
      },
    ],
    
    // React設定
    'react/jsx-uses-react': 'off',        // React 17+では不要
    'react/react-in-jsx-scope': 'off',    // 自動import
    'react/prop-types': 'off',            // TypeScript使用時は不要
    
    // 一般設定
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'prefer-const': 'error',
    'no-unused-expressions': 'error',
    'no-duplicate-imports': 'error',
    'sort-imports': [
      'error',
      {
        'ignoreCase': true,
        'ignoreDeclarationSort': true,  // import文内の順序のみ
      },
    ],
  },
}
```

### ファイル別設定

```javascript
{
  // テストファイル用設定
  files: ['**/*.{test,spec}.{ts,tsx,js,jsx}'],
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',  // テストではany許可
    'no-console': 'off',                           // デバッグ用console許可
  },
},
{
  // 設定ファイル用
  files: ['*.config.{js,ts}', 'vite.config.ts'],
  rules: {
    'no-console': 'off',                           // 設定ログ許可
  },
}
```

## 🔧 実行コマンド

### Python (Ruff)

```bash
# 基本チェック
ruff check .

# 自動修正
ruff check --fix .

# 特定ルールのみ
ruff check --select=F401 .

# 設定ファイル指定
ruff check --config=custom.toml .

# 統計表示
ruff check --statistics .
```

### JavaScript/TypeScript (ESLint)

```bash
# 基本チェック
bun run lint

# 自動修正
eslint . --fix

# 特定ファイル
eslint src/components/Button.tsx

# 警告を含む詳細表示
eslint . --max-warnings 0

# キャッシュ使用
eslint . --cache
```

## 🚨 よくあるルール違反と修正方法

### Python

```python
# RET504: 不要な変数代入
# ❌ 修正前
def get_name():
    result = user.name
    return result

# ✅ 修正後
def get_name():
    return user.name

# PLR2004: マジックナンバー
# ❌ 修正前
if score > 80:
    return "excellent"

# ✅ 修正後
EXCELLENT_THRESHOLD = 80
if score > EXCELLENT_THRESHOLD:
    return "excellent"

# B006: 可変デフォルト引数
# ❌ 修正前
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ 修正後
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### JavaScript/TypeScript

```typescript
// @typescript-eslint/no-explicit-any
// ❌ 修正前
const data: any = fetchData();

// ✅ 修正後
interface ApiData {
  id: string;
  name: string;
}
const data: ApiData = fetchData();

// react-hooks/exhaustive-deps
// ❌ 修正前
useEffect(() => {
  fetchUser(userId);
}, []); // userId が依存関係にない

// ✅ 修正後
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// prefer-const
// ❌ 修正前
let message = "Hello";
console.log(message);

// ✅ 修正後
const message = "Hello";
console.log(message);
```

## 📚 参考リンク

### Python (Ruff)
- [Ruff ルール一覧](https://docs.astral.sh/ruff/rules/)
- [設定オプション](https://docs.astral.sh/ruff/configuration/)
- [VS Code 拡張機能](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### JavaScript/TypeScript (ESLint)
- [ESLint ルール一覧](https://eslint.org/docs/latest/rules/)
- [TypeScript ESLint](https://typescript-eslint.io/rules/)
- [React ESLint Plugin](https://github.com/jsx-eslint/eslint-plugin-react)
- [React Hooks ESLint](https://www.npmjs.com/package/eslint-plugin-react-hooks)

---

💡 **効率的な開発のコツ**: IDEの拡張機能を活用して、リアルタイムでルール違反を検出・修正すると、コミット時のエラーを大幅に減らせます。