# 🚀 Git/GitHub — Safe Delivery

**Goal**: Do simple, safe pushes with no sensitive data
**Scope**: method

Reference docs in this folder: [GIT_SECURITY.md](GIT_SECURITY.md), [VERSIONING_GUIDE.md](VERSIONING_GUIDE.md), [SECURITY_SUMMARY.md](SECURITY_SUMMARY.md), [GITIGNORE_TEMPLATES.md](GITIGNORE_TEMPLATES.md), [GITHUB_INITIAL_SETUP.md](GITHUB_INITIAL_SETUP.md), [SECRETS_PROTECTION_SETUP.md](SECRETS_PROTECTION_SETUP.md).

---

## 📋 Basic Flow (3 Lines)

```bash
cd <workspace-root>\[PROJECT]
git add . && git commit -m "[Message]" && git push
```

---

## 🛡️ Security

✅ `.gitignore` blocks:
- `.env` (credentials)
- `node_modules/` (dependencies)
- `dist/`, `build/` (compiled output)
- Credentials, secrets, tokens

✅ Before pushing, check:
```bash
git status  # See what will be sent
```

---

## 🔗 Repository URLs

```
1. https://github.com/<github-account>/<docs-repo>
2. https://github.com/<github-account>/<api-repo>
3. https://github.com/<github-account>/<sync-repo>
4. https://github.com/<github-account>/<legacy-repo>
5. https://github.com/<github-account>/<learning-repo>
```

---

## 📚 Standard Messages per Project

```bash
# <docs-project> (documentation)
git commit -m "docs: documentation update"

# <api-project> / <sync-project>
git commit -m "feat: [brief description]"

# <legacy-project> / <learning-project>
git commit -m "chore: legacy code update"
```

---

**Simple, Safe, Effective** 🔐
