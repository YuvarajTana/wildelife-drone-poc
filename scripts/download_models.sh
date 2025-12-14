#!/bin/bash
# Wrapper script to download YOLO11 models using backend's virtual environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_VENV="$PROJECT_ROOT/backend/venv"

echo "🦌 Wildlife Drone PoC - YOLOv8 Model Downloader"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "$BACKEND_VENV" ]; then
    echo "❌ Virtual environment not found at: $BACKEND_VENV"
    echo ""
    echo "💡 Please set up the backend first:"
    echo "   cd backend"
    echo "   python3.11 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run the script
echo "✅ Using backend virtual environment..."
echo ""

# Use the venv's Python to run the download script
"$BACKEND_VENV/bin/python" "$SCRIPT_DIR/download_models.py"

