#!/bin/bash

# Configuration
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="Test run at ${TIMESTAMP}"

echo "🚀 Starting auto-commit and push for branch: ${BRANCH}"

# 1. Add all changes (respects .gitignore)
git add .

# 2. Check if there are any changes to commit
if git diff --cached --quiet; then
    echo "ℹ️ No changes to commit."
else
    # 3. Commit
    echo "📝 Committing changes..."
    git commit -m "${COMMIT_MESSAGE}"
    
    # 4. Push
    echo "📤 Pushing to remote..."
    git push origin "${BRANCH}"
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully synced with remote."
    else
        echo "❌ Push failed. Please check your connection or remote status."
        exit 1
    fi
fi
