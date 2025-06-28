# Python + JavaScript Full-Stack Template

🚀 **Production-ready full-stack template with modern best practices for 2025**

A comprehensive, battle-tested template for building full-stack applications with Python backend and JavaScript/TypeScript frontend. Designed with developer experience, code quality, and production readiness in mind.

## ⭐ Key Features

### 🐍 **Modern Python Backend**
- **Python 3.13+** with type hints and strict mypy checking
- **UV package manager** for fast dependency management with lockfile support
- **Ruff** for lightning-fast linting and formatting (replaces Black, Flake8, isort)
- **Pytest** with async support and BDD-style testing
- **Protocol-based architecture** for dependency injection and testability
- **Comprehensive error handling** with custom exception classes

### 📜 **Modern JavaScript Frontend**
- **React 18** with TypeScript and modern JSX transform
- **Vite** for blazing-fast development and optimized builds
- **Bun** as the unified package manager and runtime
- **ESLint 9** with flat config and strict TypeScript rules
- **Prettier** for consistent code formatting
- **Vitest** for unit and integration testing with React Testing Library

### 🔧 **Developer Experience**
- **DevContainer** support for consistent development environment
- **VS Code** optimized settings and extensions
- **Pre-commit hooks** for automated quality checks
- **Comprehensive linting** with auto-fix capabilities
- **Type safety** enforced across the entire stack

### 🚀 **CI/CD & Quality**
- **GitHub Actions** workflows with mise-action for unified tool management
- **CI skip functionality** for minor changes ([skip-ci] tag and skip-ci label)
- **Security scanning** with Bandit and automated dependency updates
- **Code coverage** tracking with detailed reporting
- **AI-powered code review** with Gemini integration
- **Automated testing** with identical tool versions across all environments

## 🏗️ Project Structure

```
├── 📁 backend/          # Python backend
│   ├── 📁 src/backend/  # Source code
│   │   ├── __init__.py
│   │   ├── main.py      # Application entry point
│   │   ├── exceptions.py # Custom exceptions
│   │   ├── 📁 models/   # Data models
│   │   └── 📁 services/ # Business logic
│   ├── 📁 tests/        # Test suite
│   ├── pyproject.toml   # Dependencies & tools config
│   └── uv.lock         # Lockfile for reproducible builds
│
├── 📁 frontend/         # JavaScript/React frontend
│   ├── 📁 src/          # Source code
│   │   ├── App.tsx      # Main application component
│   │   ├── main.tsx     # Application entry point
│   │   └── 📁 components/ # Reusable UI components
│   ├── 📁 tests/        # Test suite
│   ├── package.json     # Dependencies & scripts
│   ├── bun.lockb       # Bun lockfile (generated)
│   ├── vite.config.ts   # Vite configuration
│   ├── tsconfig.json    # TypeScript configuration
│   └── eslint.config.js # ESLint flat config
│
├── 📁 .devcontainer/    # Development container
├── 📁 .github/workflows/ # CI/CD pipelines
├── 📁 .vscode/          # VS Code settings
└── 📁 docs/             # Documentation
```

## 🚀 Quick Start

### Option 1: DevContainer with mise (Recommended for AI Safety)

1. **Prerequisites**: [VS Code](https://code.visualstudio.com/) + [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) + [Docker](https://www.docker.com/)

2. **Open in DevContainer**:
   ```bash
   git clone <your-repo>
   code <repo-name>
   # Press Ctrl+Shift+P → "Dev Containers: Reopen in Container"
   ```

3. **AI-Safe Development Environment**:
   - **Dockerfileless**: Uses DevContainer Features for mise integration
   - **Tool Version Unity**: Same versions as local mise and CI environments
   - **Safe AI Code Execution**: All AI-generated code runs in isolated container
   - **Auto-configured**: Tools, dependencies, and services ready instantly

### Option 2: Local Development with mise

1. **Prerequisites**: Install [mise](https://mise.jdx.dev/) for unified tool management

2. **Shell setup** (one-time):
   ```bash
   # Add to your shell configuration file (~/.bashrc, ~/.zshrc, etc.)
   echo 'eval "$(mise activate bash)"' >> ~/.bashrc  # for bash
   echo 'eval "$(mise activate zsh)"' >> ~/.zshrc    # for zsh
   
   # Or add shims to PATH directly
   echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> ~/.bashrc
   
   # Restart shell or source config
   source ~/.bashrc  # or source ~/.zshrc
   ```

3. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd <repo-name>
   
   # Install all required tools (runtimes + development tools)
   mise install
   ```

4. **Install project dependencies**:
   ```bash
   # Backend setup
   cd backend
   uv sync --all-extras
   
   # Frontend setup  
   cd frontend
   bun install
   ```

> **mise Unified Tool Management**: This project uses `mise.toml` to manage ALL development tools:
> - **Runtimes**: Python 3.13.5, Node.js 20.11.0, Bun 1.1.42
> - **Python tools**: Black, Ruff, MyPy, pytest, Bandit (via pipx)
> - **JS/TS tools**: TypeScript, ESLint, Prettier, Vite (via mise + npm for global tools)
> - **Other tools**: GitHub CLI, uv package manager
> 
> **Tool Management Rules**:
> - ✅ Use `mise exec -- <tool>` to run tools without PATH setup
> - ✅ All global tools managed by mise (no duplicate npm global installs)
> - ✅ Project dependencies still managed by uv (Python) and bun (JavaScript)
> - ❌ Never use `npm install -g` or `pip install --user` for development tools (use mise instead)

## 🛠️ Development Commands

### Python Backend
```bash
cd backend

# Quality checks (via mise-managed tools)
uv run ruff check .          # Lint code
uv run ruff format .         # Format code  
uv run mypy src             # Type checking
uv run bandit -r src/       # Security scan

# Alternative: Direct mise execution
mise exec -- ruff check backend/
mise exec -- black backend/src/
mise exec -- mypy backend/src/

# Testing
uv run pytest              # Run tests
uv run pytest --cov        # With coverage
uv run pytest -x           # Stop on first failure

# All checks
uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest
```

### JavaScript Frontend
```bash
cd frontend

# Quality checks (project dependencies)
bun run lint:check          # Check linting
bun run format:check        # Check formatting
bun run typecheck          # TypeScript check
bun run lint               # Fix linting issues
bun run format             # Format code

# Alternative: Direct mise execution
mise exec -- eslint frontend/src/
mise exec -- prettier frontend/src/ --check
mise exec -- tsc --project frontend/tsconfig.json --noEmit

# Development
bun run dev                # Start dev server
bun run build             # Production build
bun run preview           # Preview build

# Testing
bun run test              # Run tests
bun run test:coverage     # With coverage
bun run test:watch        # Watch mode
```

## 🎯 Code Quality Standards

### Python
- **Type hints required** for all public functions
- **Docstrings required** using Google style
- **Test coverage ≥80%** maintained
- **Security scanning** with Bandit
- **Import sorting** and formatting automated

### JavaScript/TypeScript
- **Strict TypeScript** configuration
- **ESLint rules** for React best practices
- **Accessibility checks** with jsx-a11y
- **Consistent formatting** with Prettier
- **Import organization** automated

## 🚦 CI/CD Workflows

The template includes three optimized GitHub Actions workflows:

### 🐍 Python CI (`python-ci-improved.yml`)
- **mise-action integration** for consistent Python 3.13.5 environment
- Matrix testing across Python 3.12, 3.13
- Unified tool management with mise caching
- Ruff linting and formatting
- MyPy type checking
- Bandit security scanning
- Pytest with coverage reporting
- Codecov integration

### 📜 JavaScript CI (`js-ci-improved.yml`)
- **mise-action integration** for Node.js 20.11.0 and Bun 1.1.42
- Matrix compatibility testing
- Unified tool caching via mise
- ESLint and Prettier checks
- TypeScript compilation
- Vitest testing with coverage
- Build verification
- Codecov integration

### 🤖 AI Code Review (`review-improved.yml`)
- Automated code review with Gemini AI
- Security pattern detection
- Diff analysis and intelligent feedback
- Review artifact uploads

### ⏭️ CI Skip Functionality
- **[skip-ci] tag**: Add to commit messages to skip CI on push events
- **skip-ci label**: Add to PRs to skip CI for all commits in that PR
- **Main branch protection**: CI always runs on main branch regardless of skip settings
- **Usage examples**:
  ```bash
  # Skip CI for documentation updates
  git commit -m "docs: Fix typo in README [skip-ci]"
  
  # Skip CI for PR using label
  gh pr edit --add-label "skip-ci"
  ```

## 🗄️ AI-Safe Development Environment

### DevContainer with mise Integration

- **Dockerfileless Configuration**: Uses DevContainer Features for simplified setup
- **Unified Tool Versions**: Identical to local mise and CI environments  
- **AI Safety**: Isolated container execution for AI-generated code
- **Auto-configured Services**: Ready-to-use development environment

### Development Services (Optional)
The DevContainer can be extended with services like:
- **PostgreSQL**: Database for backend development
- **Redis**: Caching and session storage
- **Automatic service startup** and **data persistence**

## 📚 Architecture Principles

### Backend Architecture
- **Protocol-based design** for testability and flexibility
- **Dependency injection** through constructor parameters
- **Custom exception hierarchy** for precise error handling
- **Service layer pattern** for business logic separation
- **UTC timestamps** for global compatibility

### Frontend Architecture
- **Component composition** over inheritance
- **Custom hooks** for state management
- **Accessibility-first** development
- **TypeScript strict mode** for type safety
- **Testing** with behavior-driven approach

## 🔒 Security Best Practices

- **Input validation** at service boundaries
- **SQL injection prevention** through parameterized queries
- **CSRF protection** considerations
- **Secure headers** in production builds
- **Dependency vulnerability scanning**
- **Secrets detection** in CI/CD

## 📖 Documentation

- [`docs/python-guide.md`](docs/python-guide.md) - Python development guide
- [`docs/javascript-guide.md`](docs/javascript-guide.md) - JavaScript/React guide
- [`docs/testing-guide.md`](docs/testing-guide.md) - Testing strategies
- [`docs/workflows.md`](docs/workflows.md) - CI/CD documentation
- [`.devcontainer/README.md`](.devcontainer/README.md) - DevContainer setup

## 🤝 Contributing

1. **Follow the established patterns** in the codebase
2. **Write tests** for new functionality
3. **Update documentation** for significant changes
4. **Run quality checks** before committing:
   ```bash
   # Backend
   cd backend && uv run ruff check . && uv run mypy src && uv run pytest
   
   # Frontend  
   cd frontend && bun run lint:check && bun run typecheck && bun test
   ```

## 🎯 Production Deployment

### Backend Deployment Checklist
- [ ] Set environment variables for database URLs
- [ ] Configure proper logging levels
- [ ] Set up health check endpoints
- [ ] Configure CORS for frontend domain
- [ ] Set up monitoring and alerting

### Frontend Deployment Checklist
- [ ] Configure API base URLs
- [ ] Set up CDN for static assets
- [ ] Configure CSP headers
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure analytics if needed

## 📄 License

This template is released under the [MIT License](LICENSE).

---

**Happy coding!** 🚀

*This template represents modern full-stack development best practices as of 2025. It's designed to be a solid foundation that grows with your project while maintaining code quality and developer productivity.*
