"""
Image Processing Service
Handles image upload, detection, and annotation
"""

from fastapi import UploadFile
import cv2
import numpy as np
from pathlib import Path
import time
import json
from typing import Dict, Any

from app.config import settings
from app.models.detector import WildlifeDetector
from app.models.grouping import AnimalGrouping
from app.services.metadata_service import MetadataService


class ImageProcessingService:
    """Service for processing wildlife images"""
    
    def __init__(
        self, 
        detector: WildlifeDetector,
        metadata_service: MetadataService
    ):
        """
        Initialize service
        
        Args:
            detector: Wildlife detector instance
            metadata_service: Metadata extraction service
        """
        self.detector = detector
        self.metadata_service = metadata_service
        self.grouping = AnimalGrouping(
            eps=settings.CLUSTERING_EPS,
            min_samples=settings.CLUSTERING_MIN_SAMPLES
        )
    
    async def process_image(
        self,
        file: UploadFile,
        confidence: float = None,
        enable_grouping: bool = True
    ) -> Dict[str, Any]:
        """
        Process uploaded image: detect animals, identify groups, annotate
        
        Args:
            file: Uploaded image file
            confidence: Detection confidence threshold
            enable_grouping: Enable spatial grouping
            
        Returns:
            Processing results dictionary
        """
        start_time = time.time()
        
        # Save uploaded file
        upload_path = Path(settings.UPLOAD_DIR) / file.filename
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Read image
        image = cv2.imread(str(upload_path))
        
        if image is None:
            raise ValueError(f"Could not read image: {file.filename}")
        
        # Extract metadata
        metadata = self.metadata_service.extract_image_metadata(str(upload_path))
        
        # Run detection
        detections = self.detector.detect(image, confidence=confidence)
        
        # Identify groups if enabled
        groups = []
        if enable_grouping and len(detections) > 1:
            detections, groups = self.grouping.identify_groups(detections)
        
        # Annotate image
        annotated_image = self.detector.annotate_image(
            image, 
            detections,
            groups if enable_grouping else None
        )
        
        # Save annotated image
        annotated_filename = f"annotated_{file.filename}"
        annotated_path = Path(settings.RESULTS_DIR) / annotated_filename
        cv2.imwrite(str(annotated_path), annotated_image)
        
        # Save JSON results
        json_filename = f"{Path(file.filename).stem}_results.json"
        json_path = Path(settings.RESULTS_DIR) / json_filename
        
        results_data = {
            "filename": file.filename,
            "detections": detections,
            "groups": groups,
            "metadata": metadata,
            "total_detections": len(detections),
            "total_groups": len(groups)
        }
        
        with open(json_path, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "filename": file.filename,
            "detections": detections,
            "groups": groups,
            "metadata": metadata,
            "annotated_image_url": f"/results/{annotated_filename}",
            "processing_time": processing_time,
            "total_detections": len(detections)
        }

