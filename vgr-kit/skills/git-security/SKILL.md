---
name: git-security
description: Use before every git push, before committing any sensitive file, when configuring a new repository, or when adding a .env file for the first time, to ensure no secret/credential is sent to GitHub.
---

# Skill: Git Security — Verify Before Committing

**Goal**: Ensure no sensitive data is sent to GitHub  
**Time**: ~2 minutes  
**Critical**: Run BEFORE every push
**Scope**: method

---

## 🎯 When to Use

- ✅ ALWAYS before `git push`
- ✅ ALWAYS before `git commit` involving a sensitive file
- ✅ When configuring a new repository
- ✅ When adding `.env` for the first time

---

## 🔐 Quick Check (30 seconds)

### Check for Sensitive Files

```bash
# 1. See what will be committed
git diff --cached --name-only

# 2. Search for sensitive data
git diff --cached | grep -i "password\|secret\|token\|api_key\|\.env"

# 3. Search for .env
git ls-files | grep "\.env"

# 4. Search for node_modules
git ls-files | grep "node_modules/"
```

**If anything is returned**: ❌ **DO NOT PUSH** — Go to "Remove Sensitive File" below

---

## ❌ Sensitive Data Must NOT Be Present

```
❌ .env
❌ .env.local
❌ credentials.json
❌ secrets.json
❌ *.pem (private keys)
❌ *.key (private keys)
❌ config/secrets/
❌ AWS_ACCESS_KEY
❌ DATABASE_PASSWORD
❌ API_KEYS
```

**Solution**: Add to `.gitignore` BEFORE use

---

## 📦 Useless Code Must NOT Be Present

```
❌ node_modules/        (1000+ files)
❌ dist/                (compiled code)
❌ build/               (compiled code)
❌ .next/               (Next.js cache)
❌ coverage/            (test coverage)
❌ *.log                (logs)
```

**Check**:
```bash
git ls-files | wc -l
# If > 10000 files → something wrong is versioned!
```

---

## 🚨 Automatic Verification Script

### Create: `scripts/pre-push-check.sh`

```bash
#!/bin/bash
set -e

echo "🔐 PRE-PUSH Security Check"
echo "===================================="

# 1. Check for sensitive data
echo ""
echo "1️⃣ Searching for sensitive data..."
if git diff origin/main --stat | grep -E "\.env|credentials|secrets|\.pem|\.key" ; then
    echo "❌ ERROR: Sensitive data detected!"
    echo "Remove it before pushing"
    exit 1
fi

# 2. Check for node_modules
echo "2️⃣ Searching for node_modules..."
if git ls-files | grep "node_modules/" ; then
    echo "❌ ERROR: node_modules/ in the repository!"
    echo "Add it to .gitignore and remove it"
    exit 1
fi

# 3. Check for dist/build
echo "3️⃣ Searching for compiled code..."
if git ls-files | grep -E "^dist/|^build/|^\.next/" ; then
    echo "⚠️ WARNING: Compiled code is versioned"
    echo "(optional: add it to .gitignore)"
fi

# 4. Count files
TOTAL_FILES=$(git ls-files | wc -l)
echo ""
echo "4️⃣ Total files: $TOTAL_FILES"
if [ "$TOTAL_FILES" -gt 5000 ] ; then
    echo "❌ WARNING: Too many versioned files!"
    echo "Check whether node_modules or dist/ are included"
    # Does not fail, just warns
fi

# 5. Check for .env
echo "5️⃣ Searching for .env..."
if [ -f ".env" ] ; then
    if git ls-files | grep "\.env$" ; then
        echo "❌ ERROR: .env was committed!"
        exit 1
    else
        echo "✅ .env exists locally but is NOT versioned (correct)"
    fi
fi

echo ""
echo "✅ Checks passed!"
echo "Safe to push"
exit 0
```

**Grant permission**:
```bash
chmod +x scripts/pre-push-check.sh
```

**Use**:
```bash
bash scripts/pre-push-check.sh
```

---

## ❌ Remove Sensitive File from Staging

### If you have NOT committed yet:

```bash
# See what is staged
git status

# Remove file from staging
git reset HEAD .env

# Or remove multiple files
git reset HEAD .env credentials.json
```

### If you have NOT pushed yet:

```bash
# Remove from the last commit (before push)
git rm --cached .env
git add .gitignore
git commit --amend -m "fix: remove .env from repository"

# Do NOT push yet!
# Check: git log --oneline
```

### If you ALREADY pushed (⚠️ Emergency):

```bash
# 1. Regenerate all passwords/tokens (they were exposed!)
# 2. Remove the file from the repository
git rm --cached .env
git commit -m "fix: remove exposed .env from history"
git push origin main

# 3. Notify team: "Regenerate credentials"
```

---

## ✅ PRE-PUSH Checklist

```
BEFORE any `git push`, check:

□ git diff --cached | grep -i "password\|secret\|token\|api_key"
  → If anything appears: ❌ REMOVE

□ git ls-files | grep "\.env"
  → If found: ❌ REMOVE

□ git ls-files | grep "node_modules"
  → If found: ❌ CHECK

□ git ls-files | wc -l
  → If > 5000: ⚠️ INVESTIGATE

□ Run: bash scripts/pre-push-check.sh
  → Must return: ✅ "Safe to push"

□ git log --oneline -5
  → No commit containing credentials

✅ All OK → SAFE for git push
```

---

## 🔍 Investigate an Existing Repository

If you already have a repository and want to verify whether anything was committed:

```bash
# Search for .env in the history
git log --all --source --diff-filter=D -- '*.env'

# Search for credentials
git log -p -S "password" --all

# See large files (could be compressed node_modules)
git rev-list --objects --all | sort -k2 | uniq | sort -rn -k1 | head -20
```

---

## 📊 Configure .gitignore Afterwards (Recovery)

If you already committed without a .gitignore:

```bash
# 1. Create a robust .gitignore
cat > .gitignore << 'EOF'
# Sensitive
.env
.env.local
credentials.json
*.pem
*.key

# Build
node_modules/
dist/
build/
*.tsbuildinfo

# Local
.vscode/
.idea/
*.log
.DS_Store
EOF

# 2. Remove from staging (do not delete locally)
git rm --cached node_modules/ -r
git rm --cached dist/ -r
git rm --cached .env

# 3. Commit
git commit -m "chore: add .gitignore and remove build artifacts"

# 4. Push
git push
```

---

## 🛡️ Permanent Protection: Husky

Install a pre-commit hook that BLOCKS commits with sensitive data:

```bash
# 1. Install Husky
npm install --save-dev husky
npx husky install

# 2. Create hook
npx husky add .husky/pre-commit 'bash scripts/pre-push-check.sh'

# 3. Test
git add .env
git commit -m "test"
# Must FAIL ✅
```

**Result**: Git refuses the commit if .env is staged

---

## 📱 Daily Checklist

```
Every day:

Morning:
□ git pull

Before Commit:
□ Checked that .env is not staged?
□ Checked that node_modules is not staged?
□ Ran pre-push-check.sh?

After Push:
□ Checked on GitHub that no .env appears?
```

---

## 🚨 Emergency: Removing .env from History

If .env was exposed and you regenerated everything:

```bash
# Using BFG Repo-Cleaner (removes from history)
npm install -g bfg

bfg --delete-files .env

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force

# ⚠️ NOTIFY THE TEAM BEFORE FORCE PUSHING
```

---

## 📚 Quick Reference

| Command | What for |
|---------|----------|
| `git diff --cached --name-only` | See files in staging |
| `git reset HEAD .env` | Remove from staging |
| `bash scripts/pre-push-check.sh` | Verify security |
| `git ls-files \| grep "node_modules"` | Search for mistakes |
| `git rm --cached .env` | Remove without deleting locally |

---

## ✨ Summary: What to Do

```
✅ ALWAYS:
  • git diff --cached BEFORE push
  • Check that .env is not versioned
  • Check that node_modules is not versioned
  • Use a robust .gitignore
  • Run pre-push-check.sh

❌ NEVER:
  • Commit .env
  • Commit credentials
  • Commit node_modules
  • Force push without warning

🚨 IF IT HAPPENS:
  • Remove the file
  • Regenerate credentials
  • Notify the team
  • Use BFG if exposed in history
```

---

*Skill created: 2026-07-04*  
*Critical: Read before the first push*  
*Agent: Git/GitHub Specialist*
