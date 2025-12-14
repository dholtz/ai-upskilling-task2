# Creating the Repository on GitHub First

If you're getting a 403 error when pushing, the repository likely doesn't exist on GitHub yet. You need to create it first.

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. **Repository name:** `ai-upskilling-template`
3. **Description:** "Flask template for AI upskilling program"
4. **Visibility:** Choose Public or Private
5. **⚠️ IMPORTANT:** Do NOT check any of these:
   - ❌ "Add a README file" (you already have one)
   - ❌ "Add .gitignore" (you already have one)
   - ❌ "Choose a license" (you already have one)
6. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, push your code:

```bash
git push -u origin main
```

When prompted:
- **Username:** `dholtz`
- **Password:** Your Personal Access Token (not your GitHub password)

## Alternative: If Repository Already Exists

If the repository already exists but you're still getting 403:

1. **Check your token has `repo` scope:**
   - Go to: https://github.com/settings/tokens
   - Make sure your token has the `repo` checkbox checked

2. **Try using the token in the URL:**
   ```bash
   git remote set-url origin https://<YOUR_TOKEN>@github.com/dholtz/ai-upskilling-template.git
   git push -u origin main
   ```
   (Replace `<YOUR_TOKEN>` with your actual token)

3. **Or use SSH instead:**
   ```bash
   git remote set-url origin git@github.com:dholtz/ai-upskilling-template.git
   git push -u origin main
   ```

## Quick Check: Does Repository Exist?

You can check if the repository exists by visiting:
https://github.com/dholtz/ai-upskilling-template

If you get a 404, the repository doesn't exist and needs to be created first.

