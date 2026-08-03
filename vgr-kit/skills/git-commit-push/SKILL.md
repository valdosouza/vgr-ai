---
name: git-commit-push
description: Use for daily versioning after finishing a feature, fixing a bug, updating documentation, refactoring, or at the end of the day to commit everything.
---

# Skill: Git Commit & Push — Daily Versioning

**Goal**: Make professional commits and publish to GitHub  
**Time**: ~5-10 minutes  
**Frequency**: Daily (or per feature)
**Scope**: method

---

## 🎯 When to Use

- ✅ Finished a feature
- ✅ Fixed a bug
- ✅ Updated documentation
- ✅ Did a refactoring
- ✅ End of day (commit everything)

---

## 📋 Standard Flow (5 Steps)

### Step 1: Check Status

```bash
cd <workspace-root>\<api-project>
git status
```

**Expected output:**
```
On branch main
Changes not staged for commit:
  modified:   src/app.ts
  modified:   package.json

Untracked files:
  new-file.ts
```

### Step 2: Staging (Choose Files)

```bash
# Option A: All files
git add .

# Option B: Specific file
git add src/app.ts

# Option C: Specific folder
git add src/

# Option D: Interactive (pick)
git add -p
# Press 'y' to include, 'n' to skip
```

### Step 3: Verify What Will Be Committed

```bash
git status
# Should show "Changes to be committed"

# Or view differences
git diff --cached
```

### Step 4: Commit with a Professional Message

**Conventional Commits standard**:
```
<type>(<scope>): <subject>

<description> (optional)

<footer> (optional)
```

**Types**:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `refactor` — Refactoring (no new feature)
- `test` — Tests
- `style` — Formatting
- `chore` — Maintenance (deps, etc)

**Examples**:

```bash
# Simple feature
git commit -m "feat(auth): add JWT token validation"

# With description
git commit -m "feat(api): implement multi-tenant support

- Add tenantId extraction from JWT
- Create tenant context middleware
- Update database connection logic

Closes #42"

# Bug fix
git commit -m "fix(db): resolve connection timeout on startup"

# Documentation
git commit -m "docs: update API endpoints README"

# Refactoring
git commit -m "refactor(service): simplify user service logic"
```

### Step 5: Push to GitHub

```bash
# First time on a branch
git push -u origin main

# Subsequent times
git push
```

---

## 🔄 Full Flow in One Line

```bash
# To do everything at once
cd <workspace-root>\<api-project> && \
git add . && \
git commit -m "feat(core): implement authentication" && \
git push
```

---

## 📊 Patterns by Context

### After Coding (Feature)
```bash
git add src/
git commit -m "feat(payments): add Stripe integration

- Add Stripe client initialization
- Implement payment processing endpoint
- Add webhook handlers"
git push
```

### After Fixing a Bug
```bash
git add src/
git commit -m "fix(api): handle null request body

Previously: Application crashed on empty POST
Now: Returns validation error message"
git push
```

### After Updating Docs
```bash
git add README.md
git add docs/
git commit -m "docs: add API endpoint documentation"
git push
```

### End of Day (Multiple Changes)
```bash
git add .
git commit -m "chore: daily updates

- Updated dependencies
- Refactored user service
- Fixed linting errors"
git push
```

---

## ⚠️ Best Practices

### ✅ Do

- ✅ Commit frequently (at least 1x/day)
- ✅ Descriptive messages
- ✅ Group related changes
- ✅ Include context (why, not just what)
- ✅ Reference issues: "Closes #123"

### ❌ Do NOT

- ❌ Commit without a message (`git commit -m "fix"`)
- ❌ Giant commit (1000+ lines)
- ❌ Mix topics (refactor + feature)
- ❌ Commit .env or sensitive data
- ❌ Force push without a reason

---

## 🔍 View History

```bash
# Last 10 commits
git log --oneline -10

# With more details
git log --oneline --graph --all

# For a specific file
git log --oneline src/app.ts

# Search by message
git log --oneline --grep="auth"
```

---

## 🚨 If You Made a Mistake

### Undo the last commit (file still exists)
```bash
git reset --soft HEAD~1
git add .
git commit -m "feat: correct message"
git push -f origin main
# ⚠️ Force push (dangerous when collaborating)
```

### Undo commits
```bash
# View history
git log --oneline

# Go back 2 commits (keep changes)
git reset --soft HEAD~2

# Go back 2 commits (discard changes)
git reset --hard HEAD~2
```

---

## ✅ Daily Checklist

- [ ] Ran tests before committing
- [ ] Code formatted/linted
- [ ] Clear commit message
- [ ] .env was not committed
- [ ] Push was successful

---

## 🎓 Real Example

```bash
# 1. Finished the authentication feature
cd <workspace-root>\<api-project>

# 2. View changes
git status
# src/auth/auth.middleware.ts
# src/auth/auth.service.ts
# src/types/express.d.ts

# 3. Add files
git add src/auth/
git add src/types/

# 4. Verify
git diff --cached

# 5. Commit
git commit -m "feat(auth): implement JWT validation middleware

- Extract tenantId from JWT token
- Add tenant context to Express request
- Create TenantPayload interface
- Add error handling for invalid tokens

Closes #15"

# 6. Push
git push

# 7. Verify on GitHub
# → github.com/<github-account>/<api-repo>/commits/main
```

---

## 🚀 Next Step

For releases: use the `git-release.md` skill

---

*Skill created: 2026-07-04*  
*Agent: Git/GitHub Specialist*
