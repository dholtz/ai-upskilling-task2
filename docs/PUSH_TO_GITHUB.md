# Pushing to GitHub - Quick Guide

## Step 1: Create Repository on GitHub

1. Go to GitHub.com
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Name it (e.g., `flask-ai-template`)
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click **"Create repository"**

## Step 2: Copy the Repository URL

After creating, GitHub will show you a page with commands. Copy the repository URL:
- HTTPS: `https://github.com/yourusername/repo-name.git`
- SSH: `git@github.com:yourusername/repo-name.git`

## Step 3: Run These Commands

Replace `YOUR_REPO_URL` with the URL you copied:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Add the remote (replace with your actual URL)
git remote add origin YOUR_REPO_URL

# Push to GitHub
git push -u origin main
```

## Example

If your repo URL is `https://github.com/david/flask-ai-template.git`:

```bash
git remote add origin https://github.com/david/flask-ai-template.git
git push -u origin main
```

## Troubleshooting

### If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin YOUR_REPO_URL
```

### If you need to authenticate:
- GitHub may ask for your username and password/token
- For HTTPS: Use a Personal Access Token (not your password)
- For SSH: Make sure your SSH key is set up

### To check your remote:
```bash
git remote -v
```

