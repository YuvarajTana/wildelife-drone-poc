#!/bin/bash

# Script to verify that .pt files have been removed from Git history

set -e

echo "=========================================="
echo "Verifying .pt files removal from Git"
echo "=========================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a Git repository"
    exit 1
fi

echo "Checking for .pt files in Git history..."
echo ""

PT_FILES=$(git log --all --name-only --pretty=format: -- "*.pt" | sort -u | grep -v '^$')

if [ -z "$PT_FILES" ]; then
    echo "✅ SUCCESS: No .pt files found in Git history!"
    echo ""
    echo "Files in .gitignore:"
    grep -E "\.pt" .gitignore || echo "No .pt patterns found in .gitignore"
else
    echo "❌ WARNING: The following .pt files are still in Git history:"
    echo "$PT_FILES"
    echo ""
    echo "You may need to run remove_large_files.sh again or use git-filter-repo"
fi

echo ""
echo "Checking current Git status..."
git status --short | head -10
