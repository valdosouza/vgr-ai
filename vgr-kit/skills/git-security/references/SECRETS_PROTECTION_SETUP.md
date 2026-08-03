# Sensitive Data Protection - Setup and Instructions
**Date:** 2026-07-04  
**Status:** Implementation documentation  
**Scope**: method

---

## 📋 Summary

This document details how to:
1. ✅ Remove already-exposed secrets from the Git history
2. ✅ Configure `.gitignore` for the future
3. ✅ Install pre-commit hooks for prevention
4. ✅ Document for the team

---

## 🔴 CRITICAL CASE: Secrets already exposed

If you accidentally committed secrets:

### Option 1: BFG Repo-Cleaner (RECOMMENDED - Fast)

```bash
# 1. Install BFG
brew install bfg  # macOS
# or
sudo apt-get install bfg  # Linux

# 2. Run the cleanup script
bash scripts/limpar-secrets-git.sh https://github.com/<github-account>/<learning-repo>.git

# 3. Force push (after validating!)
cd <learning-repo>.git
git push --force
```

### Option 2: git filter-branch (Full control)

```bash
# Remove a specific file
git filter-branch --tree-filter 'rm -f lib/firebase_options.dart' --prune-empty -f HEAD

# Clean the history
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
git push origin --force --tags
```

### Option 3: BFG via Docker (no install)

```bash
docker run --rm -v "$(pwd)":/repo codicehorn/bfg-repo-cleaner \
  --delete-files firebase_options.dart
```

---

## ✅ SETUP FOR THE FUTURE

### Step 1: Update .gitignore

Your repository must have this `.gitignore` file at the root:

```gitignore
# Firebase - CRITICAL
firebase_options.dart
google-services.json
GoogleService-Info.plist
lib/firebase_options.dart
android/app/google-services.json

# Environment Variables - CRITICAL
.env
.env.local
.env.*.local
.env.example.local

# Private Keys - CRITICAL
*.pem
*.key
*.jks
*.keystore
*.p12
*.pfx

# Secrets and Credentials - CRITICAL
*secret*
*credential*
*token*
*password*
credentials.json
service-account*.json

# Sensitive configuration
.aws/
.azure/
.gcp/
config/secrets.*
```

**Commit:**
```bash
git add .gitignore
git commit -m "chore: add comprehensive gitignore for sensitive files"
git push
```

---

### Step 2: Install a Pre-Commit Hook

Pre-commit hooks automatically prevent secrets from being committed.

#### Manual installation:
```bash
cp scripts/pre-commit-secrets-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### Installation with the `pre-commit` tool:
```bash
# Install the tool
pip install pre-commit --break-system-packages

# Create .pre-commit-config.yaml at the repo root
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: local
    hooks:
      - id: check-secrets
        name: Check for secrets
        entry: bash scripts/pre-commit-secrets-check.sh
        language: script
        types: [text]
        stages: [commit]
EOF

# Set up the baseline
detect-secrets scan --all-files > .secrets.baseline

# Activate
pre-commit install
```

**Test:**
```bash
# Create a sensitive file (use an example key in the real format)
echo "apiKey: <REMOVED>" > teste.txt

# Try to add it
git add teste.txt

# The commit will be blocked
git commit -m "test"  # ❌ BLOCKED

# Remove and try again
rm teste.txt
git reset
git commit -m "test"  # ✅ OK
```

---

### Step 3: Create .example Files

So devs know the expected structure, create example files **WITHOUT REAL VALUES**:

#### `lib/firebase_options.example.dart`
```dart
// ⚠️ EXAMPLE - COPY TO firebase_options.dart AND FILL IN WITH YOUR VALUES
// Do not commit firebase_options.dart!

import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    // Implement for your platform
    throw UnimplementedError('Configure for your platform');
  }

  // WEB CONFIG
  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'YOUR_WEB_API_KEY_HERE',  // ← Get it from the Firebase Console
    appId: 'YOUR_WEB_APP_ID_HERE',
    messagingSenderId: 'YOUR_MESSAGING_SENDER_ID',
    projectId: 'your-project-id',
    authDomain: 'your-project.firebaseapp.com',
    storageBucket: 'your-project.appspot.com',
    measurementId: 'G-XXXXX',
  );

  // ANDROID CONFIG
  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'YOUR_ANDROID_API_KEY_HERE',  // ← Get it from the Firebase Console
    appId: 'YOUR_ANDROID_APP_ID_HERE',
    messagingSenderId: 'YOUR_MESSAGING_SENDER_ID',
    projectId: 'your-project-id',
    storageBucket: 'your-project.appspot.com',
  );
}
```

#### `android/app/google-services.example.json`
```json
{
  "project_info": {
    "project_number": "123456789",
    "project_id": "your-project-id",
    "storage_bucket": "your-project.appspot.com"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:123456789:android:xxxx",
        "android_client_info": {
          "package_name": "com.yourdomain.app"
        }
      },
      "oauth_client": [
        {
          "client_id": "123456789-xxxxxx.apps.googleusercontent.com",
          "client_type": 3
        }
      ],
      "api_key": [
        {
          "current_key": "YOUR_API_KEY_HERE"
        }
      ]
    }
  ],
  "configuration_version": "1"
}
```

**Commit:**
```bash
git add lib/firebase_options.example.dart android/app/google-services.example.json
git commit -m "docs: add example config files without secrets"
git push
```

---

### Step 4: Document for the Team

Create `SETUP_LOCAL_SECRETS.md` at the root:

```markdown
# Local Secrets Setup

## ⚠️ Important

These files contain sensitive data and must **NEVER be committed**:
- `lib/firebase_options.dart`
- `android/app/google-services.json`
- `.env`
- `.env.local`

## Initial Setup

### 1. Get Firebase Credentials

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings
4. On the "Your app" tab, generate:
   - `lib/firebase_options.dart` (Web + Android)
   - `android/app/google-services.json` (Android)

### 2. Copy the Files

```bash
# Use as a template
cp lib/firebase_options.example.dart lib/firebase_options.dart
cp android/app/google-services.example.json android/app/google-services.json
```

### 3. Fill In Real Values

Edit the copied files with your real credentials (from the Firebase Console).

### 4. Verify .gitignore

Confirm that these files are in `.gitignore`:
```bash
git check-ignore lib/firebase_options.dart  # Must return the path
git check-ignore android/app/google-services.json  # Must return the path
```

## Environment Variables

For additional configuration, copy `.env.example`:

```bash
cp .env.example .env
# Edit .env with your values
```

## If You Accidentally Committed Secrets

1. Notify the team
2. Run: `bash scripts/limpar-secrets-git.sh`
3. Re-clone the repository
4. Revoke/rotate keys in the Google Cloud Console

## Validation

Before pushing, validate that there are no secrets:

```bash
# None of these lines should return results
git diff --staged | grep -i "AIzaSy"
git diff --staged | grep -i "client_secret"
git diff --staged | grep -i "apikey"
```
```

---

## 🚀 GitHub Actions for CI/CD

Add automatic validation on PRs:

### `.github/workflows/check-secrets.yml`

```yaml
name: Detect Secrets

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  detect-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Check for Secrets with detect-secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      - name: Check for Secrets with Yelp detect-secrets
        run: |
          pip install detect-secrets
          detect-secrets scan --all-files --baseline .secrets.baseline
          detect-secrets audit .secrets.baseline
```

**Commit:**
```bash
git add .github/workflows/check-secrets.yml
git commit -m "ci: add automatic secret detection"
git push
```

---

## 📊 Implementation Checklist

- [ ] ✅ Remove secrets from the history (BFG or filter-branch)
- [ ] ✅ Update `.gitignore`
- [ ] ✅ Install the local pre-commit hook
- [ ] ✅ Create `.example` files
- [ ] ✅ Document `SETUP_LOCAL_SECRETS.md`
- [ ] ✅ Configure GitHub Actions for automatic detection
- [ ] ✅ Communicate to the team
- [ ] ✅ (Optional) Rotate keys in Google Cloud

---

## 📚 Quick References

| Tool | Command | Use |
|-----------|---------|-----|
| BFG | `bfg --delete-files FILE` | Remove a file from the history |
| git filter-branch | `git filter-branch --tree-filter 'rm FILE'` | Alternative to BFG |
| pre-commit | `pre-commit install` | Install hooks |
| detect-secrets | `detect-secrets scan` | Find secret patterns |
| trufflehog | `docker run -v /path:/path trufflesecurity/trufflehog filesystem /path` | Deep scan |

---

## ❓ Questions?

1. Check `RELATORIO_DADOS_SENSIVEIS.md`
2. Read the repository `README.md`
3. Consult the team lead
