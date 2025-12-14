#!/bin/bash
# Script to help set up a new project from this template
# 
# Usage:
#   ./setup_new_project.sh <project-name>
#   # Or use environment variables:
#   PROJECT_NAME=my-project ./setup_new_project.sh
#   # Or set multiple variables:
#   PROJECT_NAME=my-project PROJECT_DESCRIPTION="My AI Project" ./setup_new_project.sh
#
# Environment Variables:
#   PROJECT_NAME          - Name of the project (required)
#   PROJECT_DESCRIPTION   - Project description (optional)
#   PROJECT_AUTHOR        - Author name (optional)
#   PROJECT_VERSION       - Initial version (default: 1.0.0)
#   SKIP_GIT_INIT         - Set to "true" to skip git initialization
#   SKIP_ENV_SETUP        - Set to "true" to skip .env file creation

set -e

# Load environment variables from .setup.env if it exists
if [ -f ".setup.env" ]; then
    echo "📋 Loading configuration from .setup.env..."
    source .setup.env
fi

# Get project name from argument or environment variable
PROJECT_NAME="${1:-${PROJECT_NAME:-}}"

# If still empty, prompt for it
if [ -z "$PROJECT_NAME" ]; then
    echo "📝 Project setup helper"
    echo ""
    read -p "Enter project name: " PROJECT_NAME
    if [ -z "$PROJECT_NAME" ]; then
        echo "❌ Error: Project name is required"
        echo ""
        echo "Usage: $0 <project-name>"
        echo "   Or: PROJECT_NAME=my-project $0"
        exit 1
    fi
fi

# Set defaults from environment variables or use defaults
PROJECT_DESCRIPTION="${PROJECT_DESCRIPTION:-$PROJECT_NAME}"
PROJECT_AUTHOR="${PROJECT_AUTHOR:-}"
PROJECT_VERSION="${PROJECT_VERSION:-1.0.0}"
SKIP_GIT_INIT="${SKIP_GIT_INIT:-false}"
SKIP_ENV_SETUP="${SKIP_ENV_SETUP:-false}"

echo "🚀 Setting up new project: $PROJECT_NAME"
[ -n "$PROJECT_DESCRIPTION" ] && echo "   Description: $PROJECT_DESCRIPTION"
[ -n "$PROJECT_AUTHOR" ] && echo "   Author: $PROJECT_AUTHOR"
echo "   Version: $PROJECT_VERSION"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Must run this script from the app/ directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Update app.py with project name
echo "📝 Updating app.py..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/AI Up-Skilling Flask App/$PROJECT_NAME/g" app.py
    sed -i '' "s/Welcome to AI Up-Skilling Flask App/Welcome to $PROJECT_NAME/g" app.py
else
    # Linux
    sed -i "s/AI Up-Skilling Flask App/$PROJECT_NAME/g" app.py
    sed -i "s/Welcome to AI Up-Skilling Flask App/Welcome to $PROJECT_NAME/g" app.py
fi

# Update README.md
echo "📝 Updating README.md..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/AI Up-Skilling Flask Application Template/$PROJECT_NAME/g" README.md
    sed -i '' "s/for AI\/ML upskilling programs/for $PROJECT_DESCRIPTION/g" README.md
    if [ -n "$PROJECT_AUTHOR" ]; then
        # Add author to README if provided
        sed -i '' "s/This is a starter template for educational purposes/This is $PROJECT_NAME by $PROJECT_AUTHOR/g" README.md 2>/dev/null || true
    fi
else
    # Linux
    sed -i "s/AI Up-Skilling Flask Application Template/$PROJECT_NAME/g" README.md
    sed -i "s/for AI\/ML upskilling programs/for $PROJECT_DESCRIPTION/g" README.md
    if [ -n "$PROJECT_AUTHOR" ]; then
        sed -i "s/This is a starter template for educational purposes/This is $PROJECT_NAME by $PROJECT_AUTHOR/g" README.md 2>/dev/null || true
    fi
fi

# Create .env from example if it doesn't exist
if [ "$SKIP_ENV_SETUP" != "true" ]; then
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        echo "📝 Creating .env from .env.example..."
        cp .env.example .env
        echo "⚠️  Remember to update .env with your actual values!"
    elif [ -f ".env" ]; then
        echo "ℹ️  .env file already exists, skipping..."
    fi
else
    echo "⏭️  Skipping .env setup (SKIP_ENV_SETUP=true)"
fi

# Initialize git if not already initialized
if [ "$SKIP_GIT_INIT" != "true" ]; then
    if [ ! -d ".git" ]; then
        echo "📝 Initializing git repository..."
        git init
        git add .
        COMMIT_MSG="Initial commit: $PROJECT_NAME setup from template"
        [ -n "$PROJECT_VERSION" ] && COMMIT_MSG="$COMMIT_MSG (v$PROJECT_VERSION)"
        git commit -m "$COMMIT_MSG"
        echo "⚠️  Remember to add your remote: git remote add origin <your-repo-url>"
    else
        echo "ℹ️  Git repository already initialized, skipping..."
    fi
else
    echo "⏭️  Skipping git initialization (SKIP_GIT_INIT=true)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review and update README.md with project-specific details"
echo "  2. Update requirements.txt with your needed libraries"
if [ "$SKIP_ENV_SETUP" != "true" ]; then
    echo "  3. Edit .env with your configuration (if needed)"
fi
echo "  4. Run 'make install' to set up the environment"
echo "  5. Run 'make run' to test the application"
echo ""
echo "💡 Tip: You can customize the setup using environment variables:"
echo "   PROJECT_NAME=my-project PROJECT_DESCRIPTION='My Description' $0"
echo ""
echo "For more information, see docs/TEMPLATE_USAGE.md"

