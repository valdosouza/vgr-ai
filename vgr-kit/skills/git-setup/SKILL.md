---
name: git-setup
description: Use when making the first commit of a project, migrating a project to Git/GitHub, configuring a new repository, or adding a .gitignore.
---

# Skill: Git Setup — Initialize a Repository

**Goal**: Configure a project for Git versioning with GitHub  
**Time**: ~10 minutes  
**Prerequisite**: Git installed
**Scope**: method

---

## 🎯 When to Use

- ✅ First commit of a project
- ✅ Migrating a project to Git/GitHub
- ✅ Configuring a new repository
- ✅ Adding a .gitignore

---

## 📋 Flow

### Step 1: Prepare the Environment

```bash
# 1. Go to the project folder
cd <workspace-root>\<api-project>

# 2. Check whether Git is already initialized
git status
# If it returns the error: "not a git repository" → continue
```

### Step 2: Initialize Git

```bash
# 1. Initialize the local repository
git init

# 2. Create the appropriate .gitignore (see examples below)
# Copy according to the project type

# 3. Configure Git (if not done globally yet)
git config user.name "<owner>"
git config user.email "<email>"
```

### Step 3: Add the GitHub Remote

```bash
# 1. Create the repository on GitHub FIRST
#    https://github.com/new
#    Name: <api-repo> (example)
#    Description: Node.js API for multi-tenant ERP
#    Private/Public: your choice

# 2. Add it as a remote
git remote add origin https://github.com/<github-account>/<api-repo>.git

# 3. Verify the remote
git remote -v
# Should show:
# origin  https://github.com/<github-account>/<api-repo>.git (fetch)
# origin  https://github.com/<github-account>/<api-repo>.git (push)
```

### Step 4: First Commit

```bash
# 1. Add files
git add .

# 2. Initial commit
git commit -m "Initial commit: Project setup"

# 3. Rename branch (if needed)
git branch -M main

# 4. Push to GitHub
git push -u origin main
# -u flag: sets 'main' as upstream (default)
```

---

## 📄 .gitignore by Project Type

### <api-project> / <sync-project> (Node.js + TypeScript)

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
logs/
*.log
npm-debug.log*
yarn-error.log*

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
*.swp

# OS
.DS_Store
Thumbs.db
```

### <docs-project> / Documentation (Markdown)

```
# OS
.DS_Store
Thumbs.db
*.swp

# IDE
.vscode/
.idea/

# Temp
temp/
tmp/
*.tmp
```

---

## ✅ Post-Setup Checklist

- [ ] Git initialized (`git status` returns "On branch main")
- [ ] .gitignore created and committed
- [ ] Remote configured (`git remote -v` shows origin)
- [ ] First commit made
- [ ] Push successful (code visible on GitHub)
- [ ] main branch created on GitHub
- [ ] Repository visible at github.com/<github-account>

---

## 🐛 Troubleshooting

### "fatal: not a git repository"
→ Run `git init` in the folder

### "Permission denied" when pushing
→ Check your GitHub token or SSH key
→ Configure credentials: `git config credential.helper store`

### "The remote origin already exists"
→ `git remote remove origin` and redo it

### Empty folder does not appear in Git
→ Git only tracks files. Create `.gitkeep` in empty folders

---

## 🚀 Next Step

After setup, use the `git-commit-push` skill (`skills/git-commit-push/SKILL.md`) for daily commits

---

*Skill created: 2026-07-04*  
*Responsible agent: Git/GitHub Specialist*
