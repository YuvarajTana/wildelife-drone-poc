"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    """Single detection result"""
    id: int
    class_name: str = Field(..., alias="class")
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    group_id: Optional[int] = None
    
    class Config:
        populate_by_name = True


class Group(BaseModel):
    """Animal group/herd information"""
    group_id: int
    count: int
    center: List[float]  # [x, y]
    members: List[int]  # Detection IDs


class GPSCoordinates(BaseModel):
    """GPS coordinates"""
    latitude: float
    longitude: float
    altitude: Optional[float] = None


class Metadata(BaseModel):
    """Image/Video metadata"""
    gps: Optional[GPSCoordinates] = None
    timestamp: Optional[str] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model: str
    device: str
    version: str


class DetectionResponse(BaseModel):
    """Image detection response"""
    success: bool = True
    filename: str
    detections: List[Detection]
    groups: Optional[List[Group]] = []
    metadata: Optional[Metadata] = None
    annotated_image_url: str
    processing_time: float
    total_detections: int


class Track(BaseModel):
    """Video tracking information"""
    track_id: int
    class_name: str
    first_frame: int
    last_frame: int
    total_frames: int
    confidence_avg: float
    trajectory: List[List[float]]  # [[x, y], [x, y], ...]


class VideoTrackingResponse(BaseModel):
    """Video tracking response"""
    success: bool = True
    filename: str
    total_frames: int
    processed_frames: int
    tracks: List[Track]
    annotated_video_url: str
    processing_time: float
    total_tracks: int
    metadata: Optional[Metadata] = None


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None

