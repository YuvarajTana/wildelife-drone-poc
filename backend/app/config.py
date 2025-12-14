"""
Configuration settings for the Wildlife Detection API
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    PYTHON_ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Model Configuration
    YOLO_MODEL_PATH: str = "weights/yolov8m.pt"
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45
    MAX_DETECTIONS: int = 300
    
    # Storage Configuration
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    UPLOAD_DIR: str = str(BASE_DIR / "data" / "raw")
    PROCESSED_DIR: str = str(BASE_DIR / "data" / "processed")
    RESULTS_DIR: str = str(BASE_DIR / "data" / "results")
    FRAMES_DIR: str = str(BASE_DIR / "data" / "frames")
    
    # Tracking Configuration
    TRACKER_TYPE: str = "bytetrack"
    TRACK_BUFFER: int = 30
    MATCH_THRESHOLD: float = 0.8
    
    # Performance Configuration
    DEVICE: str = "mps"  # 'mps' for Mac, 'cuda' for NVIDIA, 'cpu' for CPU
    BATCH_SIZE: int = 1
    NUM_WORKERS: int = 4
    
    # Grouping/Clustering
    CLUSTERING_EPS: float = 100.0  # DBSCAN eps parameter (pixels)
    CLUSTERING_MIN_SAMPLES: int = 2  # Minimum animals to form a group
    
    # Video Processing
    DEFAULT_PROCESS_FPS: int = 5  # Process every Nth frame
    MAX_VIDEO_DURATION: int = 300  # Maximum video duration in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

