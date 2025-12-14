# GitHub Authentication Guide

GitHub no longer accepts passwords for Git operations. You need to use a **Personal Access Token** instead.

## Quick Steps

### 1. Create a Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name (e.g., "ai-upskilling-template-push")
4. Select expiration (30 days, 60 days, 90 days, or no expiration)
5. **Select scopes:**
   - ✅ **`repo`** - Full control of private repositories (required for pushing)
6. Click **"Generate token"**
7. **⚠️ IMPORTANT:** Copy the token immediately - you won't be able to see it again!

### 2. Use the Token to Push

When you run `git push`, use the token as your password:

```bash
git push -u origin main
```

When prompted:
- **Username:** `dholtz` (your GitHub username)
- **Password:** `<paste your Personal Access Token here>` (NOT your GitHub password)

### 3. Alternative: Store Credentials (Optional)

To avoid entering the token every time, you can store it:

**macOS:**
```bash
# Store credentials in macOS Keychain
git config --global credential.helper osxkeychain
```

**Linux:**
```bash
# Store credentials in file (less secure)
git config --global credential.helper store
```

Then on your next push, enter the token once and it will be saved.

### 4. Using SSH Instead (Recommended for Frequent Use)

If you'll be pushing frequently, consider setting up SSH keys:

1. **Generate SSH key:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Add to GitHub:**
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your key and save

3. **Update remote to use SSH:**
   ```bash
   git remote set-url origin git@github.com:dholtz/ai-upskilling-template.git
   ```

4. **Test connection:**
   ```bash
   ssh -T git@github.com
   ```

5. **Push (no password needed!):**
   ```bash
   git push -u origin main
   ```

## Troubleshooting

### "Invalid username or token"
- Make sure you copied the entire token (it's long!)
- Check that the token hasn't expired
- Verify you selected the `repo` scope

### "Permission denied"
- Check that the token has the `repo` scope enabled
- Make sure you own the repository or have write access

### Token Expired
- Create a new token and use it
- Or set up SSH keys for a permanent solution

## Security Best Practices

- ✅ Use tokens with appropriate expiration dates
- ✅ Only grant necessary scopes (just `repo` for pushing)
- ✅ Don't commit tokens to git
- ✅ Use SSH keys for frequent use
- ✅ Revoke old/unused tokens regularly

