#!/bin/bash

# Script to remove large .pt model files from Git history
# This will remove yolov8n.pt and yolov8x.pt from Git tracking and history

set -e  # Exit on error

echo "=========================================="
echo "Removing large model files from Git"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a Git repository${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Removing files from Git index (keeping local files)...${NC}"
git rm --cached yolov8n.pt yolov8x.pt 2>/dev/null || {
    echo "Files may not be in current index, continuing..."
}

echo -e "${YELLOW}Step 2: Committing removal...${NC}"
git add .gitignore
git commit -m "Remove large model files from tracking and update .gitignore" || {
    echo "No changes to commit or already committed"
}

echo -e "${YELLOW}Step 3: Removing files from Git history (this may take a while)...${NC}"
echo "This will rewrite Git history to remove yolov8n.pt and yolov8x.pt"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch yolov8n.pt yolov8x.pt" \
  --prune-empty --tag-name-filter cat -- --all

echo -e "${YELLOW}Step 4: Cleaning up Git references...${NC}"
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo -e "${GREEN}=========================================="
echo "Success! Files removed from Git history"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Verify the files are no longer in history:"
echo "   git log --all --name-only --pretty=format: -- '*.pt' | sort -u"
echo ""
echo "2. Force push to remote (WARNING: This rewrites remote history):"
echo "   git push origin main --force"
echo ""
echo -e "${RED}Note: If others have cloned this repo, they'll need to re-clone after you force push.${NC}"
