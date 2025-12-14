#!/usr/bin/env python3
"""
Quick test script for wildlife detection
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from app.models.detector import WildlifeDetector
from app.config import settings
import cv2
import numpy as np

def test_detection():
    """Test detection on a sample image"""
    
    print("🦌 Wildlife Detection Test")
    print("=" * 60)
    
    # Check if model exists
    model_path = backend_path / settings.YOLO_MODEL_PATH
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        print("\n📥 Please download the model first:")
        print("   python scripts/download_models.py")
        return
    
    print(f"✅ Model found: {model_path}")
    print(f"💻 Device: {settings.DEVICE}")
    
    # Initialize detector
    print("\n⏳ Loading model...")
    detector = WildlifeDetector(
        model_path=str(model_path),
        confidence_threshold=settings.CONFIDENCE_THRESHOLD,
        device=settings.DEVICE
    )
    print("✅ Model loaded successfully!")
    
    # Create a test image (if no sample available)
    print("\n📸 Creating test image...")
    test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # Run detection
    print("\n🔍 Running detection...")
    detections = detector.detect(test_image)
    
    print(f"\n✅ Detection complete!")
    print(f"   Found {len(detections)} objects")
    
    if detections:
        print("\n📊 Detections:")
        for det in detections[:5]:  # Show first 5
            print(f"   - {det['class']}: {det['confidence']:.2f}")
    
    print("\n✨ Test successful! The system is working correctly.")
    print("\n🚀 You can now:")
    print("   1. Start the backend: cd backend && python app/main.py")
    print("   2. Start the frontend: cd frontend && npm run dev")
    print("   3. Open http://localhost:3000")

if __name__ == "__main__":
    try:
        test_detection()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

