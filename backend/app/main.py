"""
Wildlife Drone Detection API
FastAPI backend for wildlife detection and tracking from drone footage
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
from typing import Optional
import os
from datetime import datetime

from app.config import settings
from app.models.detector import WildlifeDetector
from app.services.image_service import ImageProcessingService
from app.services.video_service import VideoProcessingService
from app.services.metadata_service import MetadataService
from app.api.schemas import (
    HealthResponse, 
    DetectionResponse, 
    VideoTrackingResponse,
    ErrorResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Wildlife Drone Detection API",
    description="AI-powered wildlife detection and tracking from drone footage using YOLO11",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
for directory in [settings.UPLOAD_DIR, settings.PROCESSED_DIR, settings.RESULTS_DIR]:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Mount static files for serving processed images/videos
app.mount("/results", StaticFiles(directory=settings.RESULTS_DIR), name="results")

# Initialize services
detector = None
image_service = None
video_service = None
metadata_service = MetadataService()


@app.on_event("startup")
async def startup_event():
    """Initialize models and services on startup"""
    global detector, image_service, video_service
    
    print(f"🚀 Starting Wildlife Detection API...")
    print(f"📊 Model: {settings.YOLO_MODEL_PATH}")
    print(f"💻 Device: {settings.DEVICE}")
    
    # Initialize detector
    detector = WildlifeDetector(
        model_path=settings.YOLO_MODEL_PATH,
        confidence_threshold=settings.CONFIDENCE_THRESHOLD,
        device=settings.DEVICE
    )
    
    # Initialize services
    image_service = ImageProcessingService(detector, metadata_service)
    video_service = VideoProcessingService(detector, metadata_service)
    
    print("✅ Services initialized successfully")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Wildlife Drone Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model=settings.YOLO_MODEL_PATH.split("/")[-1],
        device=settings.DEVICE,
        version="1.0.0"
    )


@app.post("/api/detect/image", response_model=DetectionResponse)
async def detect_image(
    file: UploadFile = File(...),
    confidence: Optional[float] = Form(None),
    enable_grouping: bool = Form(True)
):
    """
    Detect animals in an uploaded image
    
    Args:
        file: Image file (jpg, png, jpeg)
        confidence: Detection confidence threshold (0.0-1.0)
        enable_grouping: Enable spatial grouping/clustering
        
    Returns:
        Detection results with bounding boxes, classes, and metadata
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (jpg, png, jpeg)"
            )
        
        # Override confidence if provided
        conf_threshold = confidence if confidence is not None else settings.CONFIDENCE_THRESHOLD
        
        # Process image
        result = await image_service.process_image(
            file=file,
            confidence=conf_threshold,
            enable_grouping=enable_grouping
        )
        
        return DetectionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/api/detect/video", response_model=VideoTrackingResponse)
async def track_video(
    file: UploadFile = File(...),
    confidence: Optional[float] = Form(None),
    fps: Optional[int] = Form(5),
    max_frames: Optional[int] = Form(None)
):
    """
    Detect and track animals in an uploaded video
    
    Args:
        file: Video file (mp4, mov, avi)
        confidence: Detection confidence threshold (0.0-1.0)
        fps: Frames to process per second (default: 5)
        max_frames: Maximum frames to process (None = all)
        
    Returns:
        Tracking results with trajectories and annotated video
    """
    try:
        # Validate file type
        if not file.content_type.startswith('video/'):
            raise HTTPException(
                status_code=400,
                detail="File must be a video (mp4, mov, avi)"
            )
        
        # Override confidence if provided
        conf_threshold = confidence if confidence is not None else settings.CONFIDENCE_THRESHOLD
        
        # Process video
        result = await video_service.process_video(
            file=file,
            confidence=conf_threshold,
            process_fps=fps,
            max_frames=max_frames
        )
        
        return VideoTrackingResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@app.get("/api/results")
async def list_results():
    """List all processed results"""
    results = []
    results_path = Path(settings.RESULTS_DIR)
    
    for file_path in results_path.glob("*"):
        if file_path.is_file():
            results.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                "url": f"/results/{file_path.name}"
            })
    
    return {"results": results, "total": len(results)}


@app.get("/api/download/{filename}")
async def download_result(filename: str):
    """Download a specific result file"""
    file_path = Path(settings.RESULTS_DIR) / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.delete("/api/results/{filename}")
async def delete_result(filename: str):
    """Delete a specific result file"""
    file_path = Path(settings.RESULTS_DIR) / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path.unlink()
    return {"message": f"Deleted {filename}"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.PYTHON_ENV == "development"
    )

