#!/usr/bin/env python3
"""
Download YOLO11 model weights
"""

import sys
from pathlib import Path

# Check if ultralytics is installed
try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: 'ultralytics' module not found!")
    print("\n💡 Solution: You need to activate the backend virtual environment first.")
    print("\n📝 Run these commands:")
    print("   cd backend")
    print("   source venv/bin/activate")
    print("   cd ..")
    print("   python scripts/download_models.py")
    print("\nOr install ultralytics in your current environment:")
    print("   pip install ultralytics")
    sys.exit(1)

def download_models():
    """Download YOLO11 models"""
    
    models = {
        'yolov8n': ('yolov8n.pt', 'Nano - Fastest, smallest (6MB)'),
        'yolov8s': ('yolov8s.pt', 'Small - Fast, good accuracy (22MB)'),
        'yolov8m': ('yolov8m.pt', 'Medium - Balanced (50MB) [RECOMMENDED]'),
        'yolov8l': ('yolov8l.pt', 'Large - High accuracy (100MB)'),
        'yolov8x': ('yolov8x.pt', 'Extra Large - Most accurate (130MB)'),
    }
    
    print("🦌 Wildlife Drone PoC - YOLOv8 Model Downloader")
    print("=" * 60)
    print("\nAvailable models:")
    for i, (model_key, (model_file, desc)) in enumerate(models.items(), 1):
        print(f"{i}. {model_file:<15} - {desc}")
    
    print("\n" + "=" * 60)
    choice = input("\nEnter model number to download (or 'all' for all models, default: 3 for medium): ").strip()
    
    if not choice:
        choice = '3'
    
    # Create weights directory
    weights_dir = Path(__file__).parent.parent / 'backend' / 'weights'
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    if choice.lower() == 'all':
        model_keys = list(models.keys())
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                model_keys = [list(models.keys())[idx]]
            else:
                print("❌ Invalid choice. Downloading medium model (yolov8m.pt)")
                model_keys = ['yolov8m']
        except ValueError:
            print("❌ Invalid input. Downloading medium model (yolov8m.pt)")
            model_keys = ['yolov8m']
    
    print("\n📥 Downloading models...")
    for model_key in model_keys:
        model_file, desc = models[model_key]
        print(f"\n⏳ Downloading {model_file}...")
        try:
            # YOLO will automatically download if not found locally
            # Use model key (without .pt) for automatic download
            model = YOLO(model_key)
            print(f"✅ {model_file} downloaded successfully!")
            
            # Save model to weights directory
            dst = weights_dir / model_file
            try:
                # Save the model
                model.save(str(dst))
                print(f"📂 Saved to {dst}")
            except Exception as save_error:
                # Try to find and copy from cache
                import shutil
                possible_locations = [
                    Path.home() / '.cache' / 'ultralytics' / model_file,
                    Path.home() / '.cache' / 'ultralytics' / 'hub' / model_file,
                ]
                
                copied = False
                for src in possible_locations:
                    if src.exists():
                        if not dst.exists():
                            shutil.copy(src, dst)
                            print(f"📂 Copied to {dst}")
                        else:
                            print(f"📂 Model already exists at {dst}")
                        copied = True
                        break
                
                if not copied:
                    print(f"⚠️  Model loaded but couldn't save. Check ~/.cache/ultralytics/")
                    print(f"   Model should work from cache, but you may want to manually copy to {dst}")
                
        except Exception as e:
            print(f"❌ Error downloading {model_file}: {e}")
            print(f"   Make sure you have internet connection and ultralytics is installed correctly.")
    
    print("\n✅ Download complete!")
    print(f"\n📍 Models saved to: {weights_dir}")
    print("\n⚙️  Don't forget to update backend/.env to use the downloaded model:")
    print(f"   YOLO_MODEL_PATH=weights/{model_file}")
    print("\n🚀 You can now start the backend server!")
    print("   cd backend")
    print("   source venv/bin/activate")
    print("   python app/main.py")

if __name__ == "__main__":
    try:
        download_models()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

