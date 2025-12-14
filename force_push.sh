#!/bin/bash

# Script to force push after removing large files
# WARNING: This will overwrite remote history

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${RED}=========================================="
echo "WARNING: Force Push to Remote"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}This will:${NC}"
echo "  • Overwrite the remote repository history"
echo "  • Remove large .pt files from remote"
echo "  • Require others to re-clone the repository"
echo ""
echo -e "${RED}Are you sure you want to continue?${NC}"
read -p "Type 'yes' to confirm: " -r
echo

if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted. No changes pushed."
    exit 1
fi

echo -e "${YELLOW}Pushing to origin/main...${NC}"
git push origin main --force

echo ""
echo -e "${GREEN}=========================================="
echo "Successfully pushed to remote!"
echo "==========================================${NC}"
echo ""
echo "The large files have been removed from the remote repository."
echo "Others who have cloned this repo will need to:"
echo "  git fetch origin"
echo "  git reset --hard origin/main"
echo "  (or re-clone the repository)"
