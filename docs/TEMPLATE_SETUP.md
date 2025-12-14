# Setting Up This Repository as a Template

This guide explains how to prepare and share this repository as a template for the AI upskilling program.

## 🎯 Recommended Approach

### Option 1: GitHub Template Repository (Best for Teams)

**Pros:**
- One-click "Use this template" button on GitHub
- Clean separation between template and projects
- Easy to update and version
- No confusion with actual project work

**Steps:**

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Initial template setup"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Enable Template Repository**:
   - Go to your repository on GitHub
   - Click **Settings** → **General**
   - Scroll to **Template repository**
   - Check the box: **"Template repository"**
   - Click **Update**

3. **Add Description**:
   - Update repository description: "Flask template for AI upskilling program"
   - Add topics: `flask`, `ai`, `template`, `python`, `docker`

4. **Create Initial Release**:
   ```bash
   git tag -a v1.0.0 -m "Initial template release"
   git push origin v1.0.0
   ```

5. **Share with Team**:
   - Share the repository URL
   - Instruct users to click "Use this template" button
   - Point them to `docs/TEMPLATE_USAGE.md`

### Option 2: Organization Template (Best for Large Programs)

If you have a GitHub organization:

1. **Create in Organization**:
   - Create repository in your organization
   - Name it: `flask-ai-template` or `ai-upskilling-starter`

2. **Enable Template**:
   - Same as Option 1, but in organization settings

3. **Add to Template List**:
   - Organization members will see it in "New repository" → "Repository template"

### Option 3: Fork/Clone Approach (Simple but Less Clean)

**Pros:**
- Simple, no special setup needed
- Works with any git hosting

**Cons:**
- Users need to manually clean up git history
- Can be confusing (fork vs. template)

**Steps for Users:**
```bash
git clone <template-repo> my-project
cd my-project
rm -rf .git
git init
git add .
git commit -m "Initial commit"
```

## 📋 Pre-Publish Checklist

Before sharing the template, ensure:

- [ ] **All sensitive files are in .gitignore**
  ```bash
  make check-secrets
  ```

- [ ] **No hardcoded secrets in code**
  - Check for API keys, passwords, tokens
  - Use environment variables only

- [ ] **Documentation is complete**
  - README.md is clear and helpful
   - docs/TEMPLATE_USAGE.md explains how to use it
   - docs/SECURITY.md is included
   - docs/LOCAL_SETUP.md is included

- [ ] **Example files are safe to commit**
  - `.env.example` exists (not `.env`)
  - No real credentials in examples

- [ ] **Certificate setup is documented**
  - Users know where to put certificates
  - Dockerfile handles it correctly

- [ ] **Version is tagged**
  ```bash
  git tag -a v1.0.0 -m "Initial template release"
  ```

- [ ] **Repository is clean**
  ```bash
  git status  # Should be clean
  ```

## 🚀 Publishing Steps

### 1. Final Review

```bash
# Check what will be committed
git status

# Run security check
make check-secrets

# Verify .gitignore is working
git check-ignore venv/ .env
```

### 2. Commit Everything

```bash
git add .
git commit -m "Template setup complete - ready for sharing"
```

### 3. Push to GitHub

```bash
git push origin main
```

### 4. Enable Template Feature

- Go to GitHub repository
- Settings → General → Template repository
- Enable it

### 5. Create Release

```bash
git tag -a v1.0.0 -m "Initial template release"
git push origin v1.0.0
```

On GitHub:
- Go to Releases → Create a new release
- Tag: v1.0.0
- Title: "Initial Template Release"
- Description: "First release of the AI upskilling Flask template"

## 📢 Sharing with Your Team

### Email/Announcement Template

```
Subject: AI Upskilling Program - Project Template Available

Hi Team,

I've created a starter template for our AI upskilling projects. 

📍 Repository: [link]
📖 Usage Guide: See docs/TEMPLATE_USAGE.md in the repo

To start a new project:
1. Go to the repository
2. Click "Use this template"
3. Create your new repository
4. Follow docs/TEMPLATE_USAGE.md

The template includes:
- Flask application structure
- Docker setup
- Makefile for common tasks
- Security best practices
- Comprehensive documentation

Questions? Let me know!

Best,
[Your name]
```

### README Addition

Add to your main README or course materials:

```markdown
## Getting Started

For each new project, use our starter template:

1. Go to [template repository]
2. Click "Use this template"
3. Name your project
4. Clone and start coding!

See [docs/TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) for detailed instructions.
```

## 🔄 Maintaining the Template

### When to Update

- Fix bugs or security issues
- Add new features that benefit all projects
- Update dependencies
- Improve documentation

### How to Update

1. **Make changes** in a branch:
   ```bash
   git checkout -b update-template
   # Make changes
   git commit -m "Add feature X"
   ```

2. **Test the changes**:
   - Create a test project from template
   - Verify everything works

3. **Merge and tag**:
   ```bash
   git checkout main
   git merge update-template
   git tag -a v1.1.0 -m "Added feature X"
   git push origin main --tags
   ```

4. **Notify users**:
   - Update docs/CHANGELOG.md
   - Announce updates to team

### Versioning Strategy

- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, small improvements

## 🎓 For Course Instructors

### Best Practices

1. **Keep it simple**: Don't over-engineer the template
2. **Document well**: Clear instructions prevent confusion
3. **Version releases**: Tag releases for stability
4. **Gather feedback**: Ask students what would help
5. **Iterate**: Improve based on usage

### Common Customizations

Students might want to:
- Remove Docker if not needed
- Add specific AI libraries
- Customize project structure
- Add database support

Consider creating:
- **Minimal version**: Just Flask, no Docker
- **Full version**: Everything included (current)
- **Database version**: With SQLAlchemy setup

## 📝 Template Metadata

Add this to your repository description:

```
Flask template for AI upskilling program. Includes Docker, Makefile, security best practices, and comprehensive documentation. Perfect starting point for AI/ML projects.
```

**Topics/Tags:**
- `flask`
- `python`
- `docker`
- `ai`
- `machine-learning`
- `template`
- `starter-template`
- `upskilling`

## ✅ Final Checklist

Before announcing the template:

- [ ] Repository is pushed to GitHub
- [ ] Template feature is enabled
- [ ] Initial release is tagged
- [ ] Documentation is complete
- [ ] Security check passes
- [ ] Tested by creating a new project
- [ ] Team is notified
- [ ] Usage instructions are clear

---

**You're ready to share!** 🎉

