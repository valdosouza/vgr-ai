# 🔄 Versioning Guide — <company> + GitHub

**Goal**: Keep code versioned with Git and published on GitHub  
**Account**: https://github.com/<github-account>  
**Status**: Setup in Progress
**Scope**: method

---

## 📊 Repository Structure

### Projects to Be Versioned

```
GitHub: github.com/<github-account>/

├── <api-repo>                    (Node.js + TypeScript)
│   ├── src/
│   ├── dist/
│   ├── package.json
│   ├── tsconfig.json
│   └── .gitignore
│
├── <sync-repo>                   (Node.js + TypeScript)
│   ├── src/
│   ├── dist/
│   ├── package.json
│   ├── tsconfig.json
│   └── .gitignore
│
├── <legacy-repo>                 (Legacy Delphi)
│   ├── source/
│   ├── exe/
│   ├── lib/
│   └── .gitignore
│
├── <docs-repo>                   (Documentation + Agents + Skills)
│   ├── docs/
│   ├── agents/
│   ├── skills/
│   └── .gitignore
│
└── <learning-repo>               (Legacy models for reference)
    ├── model/
    ├── dataobjects/
    └── .gitignore
```

**Total**: 5 repositories

---

## 🔧 Local Configuration

### 1. Install Git
```bash
# Windows
https://git-scm.com/download/win

# OR via Chocolatey
choco install git
```

### 2. Configure Git Globally
```bash
git config --global user.name "<owner>"
git config --global user.email "<email>"
git config --global core.autocrlf true
```

### 3. GitHub Authentication
```bash
# Option A: Personal Access Token (Recommended)
# 1. GitHub → Settings → Developer settings → Personal access tokens
# 2. Generate a token with: repo, read:user, user:email
# 3. Store the token securely

# Option B: SSH Key
git config --global core.sshCommand "ssh -i ~/.ssh/id_ed25519"
ssh-keygen -t ed25519 -C "<email>"
# Copy the public key to GitHub
```

---

## 📁 Flow: Initialize a Repository Locally

### For each project:

```bash
# 1. Go to the folder
cd <workspace-root>\<api-project>

# 2. Initialize Git
git init

# 3. Add GitHub as remote
git remote add origin https://github.com/<github-account>/<api-repo>.git

# 4. Create .gitignore
echo "node_modules/" > .gitignore
echo "dist/" >> .gitignore
echo ".env" >> .gitignore
echo ".DS_Store" >> .gitignore

# 5. First commit
git add .
git commit -m "Initial commit: Setup <api-project>"

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

---

## 📋 Commit Standard

### Conventional Commits Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Example | Description |
|------|---------|-----------|
| `feat` | `feat(auth): add JWT validation` | New feature |
| `fix` | `fix(db): resolve connection timeout` | Bug fix |
| `docs` | `docs: update README` | Documentation |
| `style` | `style: format code` | Formatting (no logic) |
| `refactor` | `refactor(api): simplify routes` | Refactoring |
| `test` | `test: add unit tests` | Tests |
| `chore` | `chore: update dependencies` | Maintenance |

### Complete Example

```bash
git commit -m "feat(core): implement multi-tenant authentication

- Add JWT parsing with tenantId
- Implement feature flag middleware
- Add tenant context to Request object

Closes #123"
```

---

## 🔄 Daily Flow: Version Code

```bash
# 1. Check status
git status

# 2. Add files
git add src/
git add package.json

# 3. Commit with a clear message
git commit -m "feat(api): add new endpoint /users"

# 4. Push to GitHub
git push origin main
```

---

## 🌿 Branching Strategy (Git Flow)

### Main Branches

```
main/
├── (stable, production-ready)
│
develop/
├── (integration, latest features)
│
feature/new-feature
├── (feature development)
│
hotfix/critical-bug
└── (urgent production fix)
```

### Flow

```bash
# 1. Create a feature branch
git checkout -b feature/nova-funcionalidade

# 2. Develop and commit
git add .
git commit -m "feat: implement new feature"

# 3. Push to origin
git push origin feature/nova-funcionalidade

# 4. Create a Pull Request on GitHub
# → Review → Merge into develop

# 5. When ready for production
# → Merge develop → main
# → Tag release
git tag v1.0.0
git push origin v1.0.0
```

---

## 🏷️ Semantic Versioning

### Format: MAJOR.MINOR.PATCH

| Type | Example | When |
|------|---------|--------|
| **MAJOR** | 1.0.0 → 2.0.0 | Breaking changes |
| **MINOR** | 1.0.0 → 1.1.0 | New feature (compatible) |
| **PATCH** | 1.0.0 → 1.0.1 | Bug fix |

### Examples

```bash
# First release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# Feature release
git tag -a v1.1.0 -m "Add multi-tenant support"
git push origin v1.1.0

# Bug fix
git tag -a v1.0.1 -m "Fix authentication bug"
git push origin v1.0.1
```

---

## 📊 Standard .gitignore

### <api-project> / <sync-project> (Node.js)
```
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Testing
coverage/
.nyc_output/
```

### <legacy-project> (Delphi)
```
# Delphi
*.dcu
*.o
*.a
*.so
__history/
__recovery/
*.local

# Build
Win32/
Win64/

# IDE
.idea/

# OS
.DS_Store
Thumbs.db
```

### <docs-project> (Markdown)
```
# General
.DS_Store
Thumbs.db
*.swp
.vscode/

# Temporary files
temp/
tmp/
*.tmp
```

---

## 🔗 Repository URLs

Create at: https://github.com/new

```
1. <api-repo>
   https://github.com/<github-account>/<api-repo>

2. <sync-repo>
   https://github.com/<github-account>/<sync-repo>

3. <legacy-repo>
   https://github.com/<github-account>/<legacy-repo>

4. <docs-repo>
   https://github.com/<github-account>/<docs-repo>

5. <learning-repo>
   https://github.com/<github-account>/<learning-repo>
```

---

## ✅ Setup Checklist

- [ ] Git installed
- [ ] Git configured (user.name, user.email)
- [ ] GitHub token created
- [ ] 5 repositories created on GitHub
- [ ] <api-project> initialized and pushed
- [ ] <sync-project> initialized and pushed
- [ ] <legacy-project> initialized and pushed
- [ ] <docs-project> initialized and pushed
- [ ] <learning-project> initialized and pushed
- [ ] .gitignore configured in each repo
- [ ] Version tags created

---

## 🚀 Next Step

Use a specialized agent to automate versioning:

```
/SendMessage to: 'agente-git-github'

I want to version <api-project> on GitHub
```

---

**Document Created**: 2026-07-04  
**Status**: Setup Initial Guide
