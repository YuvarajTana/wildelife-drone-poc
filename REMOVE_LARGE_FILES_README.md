# Removing Large Model Files from Git History

This directory contains scripts to remove large `.pt` model files (yolov8n.pt and yolov8x.pt) from Git history.

## Problem

The file `yolov8x.pt` is 130.53 MB, which exceeds GitHub's 100 MB file size limit. These files need to be removed from Git history to allow pushing to the remote repository.

## Scripts

### 1. `remove_large_files.sh` (Main Script)
**What it does:**
- Removes `yolov8n.pt` and `yolov8x.pt` from Git tracking
- Updates `.gitignore` to ignore all `.pt` files
- Removes the files from entire Git history using `git filter-branch`
- Cleans up Git references and garbage collects

**Usage:**
```bash
./remove_large_files.sh
```

**Note:** This script will ask for confirmation before rewriting Git history.

### 2. `verify_removal.sh` (Verification Script)
**What it does:**
- Checks if `.pt` files are still in Git history
- Shows current Git status
- Verifies `.gitignore` patterns

**Usage:**
```bash
./verify_removal.sh
```

Run this after `remove_large_files.sh` to confirm the files are removed.

### 3. `force_push.sh` (Force Push Script)
**What it does:**
- Force pushes the cleaned history to the remote repository
- Requires typing "yes" to confirm (safety measure)

**Usage:**
```bash
./force_push.sh
```

**⚠️ WARNING:** This will overwrite remote history. Only run after verifying removal.

## Step-by-Step Process

1. **Run the main removal script:**
   ```bash
   ./remove_large_files.sh
   ```

2. **Verify the removal:**
   ```bash
   ./verify_removal.sh
   ```
   
   You should see: "✅ SUCCESS: No .pt files found in Git history!"

3. **Force push to remote:**
   ```bash
   ./force_push.sh
   ```

## Important Notes

- **Local files are preserved:** The `.pt` files will remain on your local disk, they're just removed from Git.
- **History rewrite:** This process rewrites Git history. If others have cloned the repo, they'll need to:
  ```bash
  git fetch origin
  git reset --hard origin/main
  ```
  Or re-clone the repository.
- **Backup:** Consider backing up your repository before running these scripts.
- **`.gitignore`:** The `.gitignore` file has been updated to ignore all `.pt` files going forward.

## Alternative: Using git-filter-repo (Recommended for Large Repos)

If `git filter-branch` is too slow, you can use `git-filter-repo`:

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove files from history
git filter-repo --path yolov8n.pt --path yolov8x.pt --invert-paths

# Force push
git push origin main --force
```

## Troubleshooting

- **If verification shows files still in history:** The files might be in a different location. Check with:
  ```bash
  git log --all --name-only --pretty=format: -- "*.pt" | sort -u
  ```

- **If force push fails:** Make sure you have write access to the repository and that no one else is pushing at the same time.

- **If you need to recover:** The original refs are backed up in `.git/refs/original/` (until you run the cleanup step).
