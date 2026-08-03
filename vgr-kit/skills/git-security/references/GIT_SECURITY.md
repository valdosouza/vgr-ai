# 🔐 Git Security — What NOT to Commit

**Critical**: Prevent sensitive data and useless code on GitHub
**Scope**: method

---

## ❌ NEVER Commit (Risk Checklist)

### 🔴 Sensitive Data (CRITICAL)

| What | Why | Solution |
|-------|---------|---------|
| `.env` or `.env.local` | Credentials, tokens, passwords | Add to .gitignore |
| `config/secrets.json` | API keys, DB passwords | Never commit |
| `private_keys/` or `*.pem` | SSH/SSL keys | Always in .gitignore |
| `credentials.json` | GCP, AWS, Azure keys | NEVER commit |
| GitHub/NPM tokens | Authentication | Use environment variables |
| Database backups | Sensitive data | Never in Git |

### 🟠 Useless Code (Build/Dependencies)

| What | Why | Solution |
|-------|---------|---------|
| `node_modules/` | 1000+ unnecessary files | .gitignore |
| `dist/` / `build/` | Compiled code (regenerable) | .gitignore |
| `.next/` / `.vuepress/` | Build artifacts | .gitignore |
| `*.tsbuildinfo` | Typescript cache | .gitignore |
| `coverage/` | Test reports | .gitignore |
| `.cache/` | Local cache | .gitignore |

### 🟡 Local Files (Not Relevant)

| What | Why | Solution |
|-------|---------|---------|
| `.vscode/` | Personal IDE configuration | .gitignore |
| `.idea/` | IntelliJ config | .gitignore |
| `.DS_Store` | macOS system file | .gitignore |
| `Thumbs.db` | Windows system file | .gitignore |
| `*.log` | Log files | .gitignore |
| `*.swp` / `*.swo` | Editor temp files | .gitignore |

---

## 📋 Safe .gitignore — Per Project

### <api-project> / <sync-project> (Node.js)

**MAXIMUM SECURITY**:
```
# ===== CRITICAL: Sensitive Data =====
.env
.env.local
.env.*.local
.env*.production
.env*.development
secrets/
credentials.json
private_keys/
*.pem
*.key
*.crt

# ===== Useless Code =====
node_modules/
dist/
build/
*.tsbuildinfo
.next/
out/
coverage/
.nyc_output/

# ===== Local Files =====
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db

# ===== Logs =====
logs/
*.log
npm-debug.log*
yarn-error.log*
lerna-debug.log*

# ===== Cache =====
.cache/
.eslintcache
.parcel-cache
.turbo/
dist-ssr

# ===== Tests =====
.mocha_output/
test-results/

# ===== Package Lock (optional) =====
# If working in a team:
# package-lock.json  # Keep it so everyone has the same versions
# yarn.lock          # Keep it so everyone has the same versions

# ===== OS Specific =====
*.exe
*.dll
*.so
```

### <legacy-project> (Delphi)

```
# ===== CRITICAL: Sensitive Data =====
*.ini
config.local.*
credentials.*
secrets/

# ===== Build Output =====
__history/
__recovery/
*.dcu
*.o
*.a
Win32/
Win64/
Release/
Debug/

# ===== IDE =====
.idea/
*.local

# ===== OS =====
.DS_Store
Thumbs.db
*.exe
```

### <docs-project> (Documentation)

```
# ===== Temporary Files =====
temp/
tmp/
*.tmp
*.bak

# ===== IDE =====
.vscode/
.idea/

# ===== OS =====
.DS_Store
Thumbs.db
*.swp

# ===== If it contains source code =====
node_modules/
dist/
```

---

## 🛡️ Additional Protection: Pre-commit Hooks

### Install Husky + Lint-staged

```bash
npm install --save-dev husky lint-staged
npx husky install
```

### Create the `.husky/pre-commit` file

```bash
#!/bin/sh

# Runs checks BEFORE committing

echo "🔐 Checking for sensitive data..."
if git diff --cached | grep -E "(\.env|AWS_|DATABASE_|SECRET_|PASSWORD_|API_KEY|TOKEN=)" ; then
    echo "❌ ERROR: Sensitive data detected!"
    echo "Check .env and use environment variables"
    exit 1
fi

echo "📦 Checking for node_modules..."
if git diff --cached --name-only | grep "node_modules/" ; then
    echo "❌ ERROR: node_modules/ must not be committed!"
    exit 1
fi

echo "✅ Pre-checks OK"
exit 0
```

### Run automatically

```bash
chmod +x .husky/pre-commit
```

**Result**: Git will refuse the commit if it finds .env or node_modules

---

## 🔍 Verify Before Push

### 1. See what will be pushed

```bash
# Show files that will be sent
git diff --cached --name-only

# Show the content of the changes
git diff --cached
```

### 2. Search for sensitive data

```bash
# Search for dangerous patterns
git diff --cached | grep -i "password\|secret\|token\|api_key"

# Search for .env
git diff --cached | grep "\.env"

# Search for node_modules
git ls-files | grep "node_modules"
```

### 3. Safe Verification Script

```bash
#!/bin/bash
# Save as: scripts/pre-push-check.sh

echo "🔍 Checking security before push..."

# Check for .env
if git ls-files | grep -E "\.env|secrets/|credentials" ; then
    echo "❌ CRITICAL: Sensitive files detected!"
    exit 1
fi

# Check for node_modules
if git ls-files | grep "node_modules/" ; then
    echo "❌ CRITICAL: node_modules/ in the repository!"
    exit 1
fi

# Check for dist
if git ls-files | grep "^dist/" ; then
    echo "⚠️ WARNING: dist/ is versioned (consider .gitignore)"
fi

echo "✅ Checks passed!"
exit 0
```

**Usage**:
```bash
bash scripts/pre-push-check.sh
```

---

## 🚨 If You Made a Mistake (Remove Sensitive Data)

### Option 1: If you have not pushed yet

```bash
# Remove file from staging
git reset HEAD .env

# Or remove from the last commit (before push)
git rm --cached .env
git commit --amend -m "feat: remove sensitive files"
```

### Option 2: If you already pushed (EMERGENCY)

```bash
# NEVER force push without warning the team!
# Better: Make a new commit that removes the file

git rm --cached .env
git commit -m "fix: remove .env file from repository"
git push origin main

# Then: Regenerate tokens/passwords (they were exposed!)
```

### Option 3: Use BFG Repo-Cleaner (Removes from History)

```bash
# Install
brew install bfg  # macOS
choco install bfg  # Windows

# Remove the .env file from the entire history
bfg --delete-files .env

# Push
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

**⚠️ DANGEROUS**: Force push affects the whole team

---

## ✅ PRE-COMMIT Security Checklist

Always check BEFORE running `git push`:

- [ ] `.env` is **NOT** in the commit
- [ ] `credentials.json` is **NOT** there
- [ ] `*.pem` / `*.key` is **NOT** there
- [ ] `node_modules/` is **NOT** there
- [ ] `dist/` is **NOT** there (if in .gitignore)
- [ ] `.vscode/` is **NOT** there
- [ ] `*.log` is **NOT** there
- [ ] No password/API key in code
- [ ] `git diff --cached` is clean
- [ ] I ran pre-push-check.sh ✅

---

## 🎯 Safe Commands

### See what will be committed
```bash
git diff --cached --stat
```

### Remove a file before committing
```bash
git reset HEAD sensitive-file.env
```

### Review changes before push
```bash
git log --oneline -5  # See commits
git diff origin/main  # See differences before push
```

### Undo the last commit (before push)
```bash
git reset --soft HEAD~1
# Files go back to staging; you can review and redo
```

---

## 📌 Recommended Configuration in `package.json`

```json
{
  "scripts": {
    "pre-push": "bash scripts/pre-push-check.sh",
    "pre-commit": "husky install && lint-staged"
  },
  "lint-staged": {
    "*.ts": "eslint --fix",
    "*.md": "prettier --write"
  }
}
```

---

## 🔐 GitHub: Additional Protection

### Settings → Secrets and variables

1. Create secrets on GitHub (not in code):
   - DATABASE_URL
   - API_KEY
   - JWT_SECRET

2. Use them in CI/CD:
```yaml
# .github/workflows/deploy.yml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}
```

---

## 📚 Documentation for the Team

Add to the `README.md` of each project:

```markdown
## 🔐 Security

- **NEVER** commit `.env` files
- **NEVER** commit `node_modules/`
- **NEVER** commit credentials or API keys
- **ALWAYS** use `.gitignore`
- **ALWAYS** check `git diff --cached` before push

See [GIT_SECURITY.md](../GIT_SECURITY.md) for details.
```

---

## ✨ Summary: Is the System Secure?

| Protection | Status | Action |
|----------|--------|------|
| .gitignore configured | ✅ Yes | Use the provided template |
| Pre-commit hooks | ⏳ Optional | Install Husky |
| Pre-push check script | ⏳ Create | Add to scripts/ |
| GitHub branch protection | ⏳ Setup | Enable in Settings |
| Secrets on GitHub | ⏳ Setup | Create secrets |
| Team awareness | ⏳ Document | Share GIT_SECURITY.md |

---

**Created**: 2026-07-04  
**Critical**: Read before the first push  
**Owner**: <owner> + Git/GitHub Specialist Agent
