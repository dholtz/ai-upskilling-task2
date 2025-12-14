# Security Checklist for Git Repository

## ⚠️ CRITICAL: Never Commit These Files

### 1. **Certificate Files** 🔒
- `*.cer`, `*.crt`, `*.pem`, `*.key`, `*.p12`, `*.pfx`
- Corporate certificates (like `Zscaler_Root_CA.cer`)
- SSL/TLS certificates and private keys
- **Why**: These are sensitive security credentials

### 2. **Environment Variables & Secrets** 🔐
- `.env` files
- `.env.local`, `.env.production`, etc.
- Any file containing:
  - API keys
  - Database passwords
  - Secret keys
  - Access tokens
  - OAuth credentials
- **Why**: These contain sensitive credentials that could compromise your system

### 3. **Credentials & Keys** 🗝️
- Files named `*secret*`, `*key*`, `*credential*`, `*password*`
- SSH private keys (`id_rsa`, `id_ed25519`, etc.)
- AWS credentials (`~/.aws/credentials`)
- **Why**: Direct access to systems and services

### 4. **Database Files** 💾
- `*.db`, `*.sqlite`, `*.sqlite3`
- Database dumps with real data
- **Why**: May contain sensitive user data

### 5. **Log Files** 📝
- `*.log` files
- Application logs
- **Why**: May contain sensitive information, errors, or stack traces

### 6. **Large Model Files** 🤖
- Large ML model files (`.pkl`, `.h5`, `.pt`, `.onnx`)
- **Why**: Usually too large for git, and may contain proprietary models

## ✅ Safe to Commit

- Source code (`.py`, `.js`, etc.)
- Configuration templates (`.env.example`)
- Documentation (`.md`, `.txt`)
- Dockerfile (without secrets)
- Requirements files
- Tests
- Small configuration files (without secrets)

## 🔍 Pre-Commit Checklist

Before committing, verify:

- [ ] No `.env` files are staged
- [ ] No certificate files (`.cer`, `.crt`, `.pem`) are staged
- [ ] No hardcoded secrets in code
- [ ] No API keys in comments or code
- [ ] No database credentials in code
- [ ] No log files with sensitive data
- [ ] Virtual environment (`venv/`) is not tracked
- [ ] Large files are not tracked

## 🛠️ How to Check

### Check what's staged for commit:
```bash
git status
git diff --cached
```

### Search for potential secrets:
```bash
# Search for common secret patterns
grep -r "password\|secret\|api_key\|token" --include="*.py" --include="*.env*" .
```

### Check for accidentally tracked sensitive files:
```bash
git ls-files | grep -E "\.(env|cer|crt|pem|key|log|db)$"
```

## 🚨 If You Accidentally Committed Secrets

### If NOT yet pushed:
```bash
# Remove from staging
git reset HEAD <file>

# Remove from git history (if already committed)
git rm --cached <file>
git commit --amend
```

### If already pushed:
1. **IMMEDIATELY** rotate/revoke the exposed credentials
2. Remove from git history (requires force push - coordinate with team)
3. Consider using `git-filter-repo` or BFG Repo-Cleaner
4. Notify your team/security team

## 📋 Best Practices

1. **Use `.env.example`** - Create a template file with placeholder values:
   ```env
   # .env.example
   PORT=5000
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

2. **Use Environment Variables** - Never hardcode secrets:
   ```python
   # ❌ BAD
   API_KEY = "sk-1234567890"
   
   # ✅ GOOD
   API_KEY = config('API_KEY')
   ```

3. **Use Secret Management** - For production:
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault
   - Kubernetes Secrets

4. **Review Dependencies** - Check `requirements.txt` for known vulnerabilities:
   ```bash
   pip-audit
   safety check
   ```

5. **Use `.gitignore`** - Keep it updated with all sensitive file patterns

6. **Code Reviews** - Always have someone review code before merging

## 🔐 For This Project Specifically

### Files Already Ignored:
- ✅ `.env` and `.flaskenv` (environment variables)
- ✅ `venv/` (virtual environment)
- ✅ `*.log` (log files)
- ✅ Certificate files (`.cer`, `.crt`, `.pem`, `.key`)

### Certificate File Location:
The corporate certificate (`Zscaler_Root_CA.cer`) should be placed in a directory **outside** this repository (typically one level up from the project root). This is correct - certificates should never be in the repo. When building with Docker, ensure the certificate is in the build context directory.

### If You Need to Share Configuration:
Create a `.env.example` file:
```bash
cp .env .env.example
# Edit .env.example to remove actual secrets, use placeholders
```

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security.html)

## ⚡ Quick Commands

```bash
# Check for secrets before committing
make check-secrets  # (if you add this to Makefile)

# View what will be committed
git status
git diff --cached

# Remove accidentally staged sensitive file
git reset HEAD <file>
```

---

**Remember**: When in doubt, don't commit it. It's easier to add something later than to remove sensitive data from git history!

