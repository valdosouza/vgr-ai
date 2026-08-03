# 🚀 GitHub Initial Setup — Create Repositories + Authentication

**Goal**: Prepare GitHub to receive code via the agent  
**Time**: ~15 minutes  
**Critical**: Do this BEFORE the agent pushes
**Scope**: method

---

## ✅ Step 1: Create 5 Repositories on GitHub

### Access GitHub

1. Open: https://github.com/new
2. Are you logged in as `<github-account>`? 
   - If NOT: https://github.com/login first

---

### Create Repository 1: <docs-repo>

```
Repository name: <docs-repo>
Description: Project documentation, agents and skills
Visibility: ☐ Public  ☑ Private
Initialize repository: ☐ Add a README file
                       ☐ Add .gitignore
                       ☐ Choose a license

→ Click: "Create repository"
```

**Result**: https://github.com/<github-account>/<docs-repo> (empty ✅)

---

### Create Repository 2: <api-repo>

```
Repository name: <api-repo>
Description: Node.js + TypeScript API for multi-tenant ERP
Visibility: ☐ Public  ☑ Private
Initialize repository: ☐ Everything blank

→ Click: "Create repository"
```

**Result**: https://github.com/<github-account>/<api-repo> (empty ✅)

---

### Create Repository 3: <sync-repo>

```
Repository name: <sync-repo>
Description: Node.js + TypeScript API for data synchronization
Visibility: ☐ Public  ☑ Private
Initialize repository: ☐ Everything blank

→ Click: "Create repository"
```

**Result**: https://github.com/<github-account>/<sync-repo> (empty ✅)

---

### Create Repository 4: <legacy-repo>

```
Repository name: <legacy-repo>
Description: Data synchronizer (Legacy in production)
Visibility: ☑ Private
Initialize repository: ☐ Everything blank

→ Click: "Create repository"
```

**Result**: https://github.com/<github-account>/<legacy-repo> (empty ✅)

---

### Create Repository 5: <learning-repo>

```
Repository name: <learning-repo>
Description: Legacy models for reference and conversion
Visibility: ☑ Private
Initialize repository: ☐ Everything blank

→ Click: "Create repository"
```

**Result**: https://github.com/<github-account>/<learning-repo> (empty ✅)

---

## ✅ Result: 5 Repositories Created

```
✅ https://github.com/<github-account>/<docs-repo>
✅ https://github.com/<github-account>/<api-repo>
✅ https://github.com/<github-account>/<sync-repo>
✅ https://github.com/<github-account>/<legacy-repo>
✅ https://github.com/<github-account>/<learning-repo>
```

---

## 🔐 Step 2: Create a Personal Access Token (Authentication)

**Why a token?** Better for:
- The agent managing multiple repos
- Not exposing your GitHub password
- Revoking without changing your password

### Generate the Token

1. Open: https://github.com/settings/tokens
2. Click: **"Generate new token"** → **"Generate new token (classic)"**

### Configure the Token

```
Token name: <company>-Agent
Expiration: 90 days (or more, your choice)

Scopes (Check):
☑ repo              (Full repository access)
☑ read:user
☑ user:email
☑ admin:public_key
☑ admin:repo_hook

→ Click: "Generate token"
```

### Copy the Token

```
⚠️ IMPORTANT:
- Copy the generated token (it will be shown only once)
- STORE IT IN A SAFE PLACE (do not commit, do not share)
- Examples of where to store it:
  ✅ Password manager (Bitwarden, 1Password)
  ✅ Personal .env file (NOT in the project)
  ✅ Secure note (Notion, personal OneNote)
  ❌ Committed to Git
  ❌ Shared

Token format:
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔐 Step 3: Configure Git to Use the Token

### On Windows (Recommended: Git Credential Manager)

**Option A: Use Git Credential Manager (Automatic)**

Git already ships with a credential manager. When you try to push:

```bash
git push origin main
# It will ask:
# Username: <github-account>
# Password: [Paste the token here]
# 
# Git saves it automatically
```

**Option B: Store the Token Manually**

```bash
# Store credentials in the Windows Credential Manager
git config --global credential.helper manager-core

# The next push will ask for the token once and store it
git push origin main
```

**Option C: Via .git/config (Not recommended)**

```bash
# NOT recommended, but it works:
git config --global user.name "<github-account>"
git config --global user.password "ghp_xxxx...xxxx"
```

---

## ✅ Test Authentication

```bash
# 1. Go to any project folder
cd <workspace-root>\<api-project>

# 2. Try cloning an empty repo
git clone https://github.com/<github-account>/<api-repo> test-clone

# 3. If asked for username/password:
#    Username: <github-account>
#    Password: [Paste the token]

# 4. If it clones without error: ✅ Authentication OK
```

---

## 📋 Pre-Agent Checklist

```
Before the agent starts:

GitHub:
☑ 5 repositories created (empty)
☑ Personal Access Token generated
☑ Token stored in a safe place
☑ Token tested with git clone

Local Configuration:
☑ Git installed
☑ Git configured (user.name, user.email)
☑ Credential manager working

Folders:
☑ <workspace-root>\<api-project> exists
☑ <workspace-root>\<sync-project> exists
☑ <workspace-root>\<legacy-project> exists
☑ <workspace-root>\<docs-project> exists
☑ <workspace-root>\<learning-project> exists

✅ All OK → The agent can proceed
```

---

## 🎯 Repository URLs (Copy)

After creating them, you will have:

```
1. https://github.com/<github-account>/<docs-repo>
2. https://github.com/<github-account>/<api-repo>
3. https://github.com/<github-account>/<sync-repo>
4. https://github.com/<github-account>/<legacy-repo>
5. https://github.com/<github-account>/<learning-repo>
```

---

## 🚀 Next Step

After:
1. ✅ Creating the 5 repositories
2. ✅ Generating and testing the token

Come back here and say:

```
✅ REPOSITORIES CREATED
✅ TOKEN GENERATED AND TESTED

THE AGENT CAN START THE PUSH
```

---

## ⚠️ If You Have Questions

### "Which is better: SSH or Token?"

**SSH** (more secure, but complex):
- Generate an RSA key
- Add it to GitHub
- Use it on each push

**Token (recommended for the agent)**:
- Generate once
- Store securely
- The agent uses it automatically
- Easy to revoke if needed

→ **For the agent to manage: USE A TOKEN** ✅

---

### "Where to store the token?"

```
❌ NOT in:
  - A Git commit
  - Email
  - Text message

✅ YES in:
  - Password manager (Bitwarden, 1Password)
  - Personal local .env file
  - Secure note (personal Notion)
```

---

### "Token expired?"

If the token expired (90 days):

1. Generate a new one: https://github.com/settings/tokens
2. Update it in your password manager
3. Git will ask for the new token on the next push

---

## 📞 Quick Summary

```
1. Create 5 empty repos on GitHub
   → https://github.com/new (5x)

2. Generate a token
   → https://github.com/settings/tokens
   → "Generate new token (classic)"
   → Copy the token (one-time opportunity!)

3. Test authentication
   → git clone https://github.com/<github-account>/<api-repo>
   → Username: <github-account>
   → Password: [token]
   → ✅ If it works, all OK

4. Come back here and report
   → "REPOSITORIES CREATED AND TESTED"
   → The agent starts the push
```

**Time**: ~15 minutes

---

*Guide created: 2026-07-04*  
*For: First setup before the agent*  
*Status: Follow it and come back here when done ✅*
