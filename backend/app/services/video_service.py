"""
Video Processing Service  
Handles video upload, detection, tracking, and annotation
"""

from fastapi import UploadFile
import cv2
import numpy as np
from pathlib import Path
import time
import json
from typing import Dict, Any, List
from collections import defaultdict

from app.config import settings
from app.models.detector import WildlifeDetector
from app.services.metadata_service import MetadataService


class VideoProcessingService:
    """Service for processing wildlife videos with tracking"""
    
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
    
    async def process_video(
        self,
        file: UploadFile,
        confidence: float = None,
        process_fps: int = 5,
        max_frames: int = None
    ) -> Dict[str, Any]:
        """
        Process uploaded video: detect and track animals
        
        Args:
            file: Uploaded video file
            confidence: Detection confidence threshold
            process_fps: Process every Nth frame (higher = faster but less accurate)
            max_frames: Maximum frames to process
            
        Returns:
            Processing results dictionary
        """
        start_time = time.time()
        
        # Save uploaded file
        upload_path = Path(settings.UPLOAD_DIR) / file.filename
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Open video
        cap = cv2.VideoCapture(str(upload_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {file.filename}")
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate frames to process
        frame_skip = max(1, int(fps / process_fps))
        frames_to_process = total_frames // frame_skip
        if max_frames:
            frames_to_process = min(frames_to_process, max_frames)
        
        # Setup output video
        output_filename = f"tracked_{file.filename}"
        output_path = Path(settings.RESULTS_DIR) / output_filename
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Track data
        track_history = defaultdict(list)  # track_id -> [(frame, bbox, class), ...]
        processed_frames = 0
        frame_count = 0
        
        # Process video with tracking
        results = self.detector.detect_and_track(
            str(upload_path),
            confidence=confidence,
            tracker=f"{settings.TRACKER_TYPE}.yaml"
        )
        
        for result in results:
            # Skip frames if needed
            if frame_count % frame_skip != 0:
                frame_count += 1
                continue
            
            frame = result.orig_img.copy()
            
            # Extract tracking information
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy().astype(int)
                
                # Get track IDs if available
                if hasattr(result.boxes, 'id') and result.boxes.id is not None:
                    track_ids = result.boxes.id.cpu().numpy().astype(int)
                else:
                    track_ids = list(range(len(boxes)))
                
                # Update track history
                for track_id, box, conf, cls_id in zip(track_ids, boxes, confidences, class_ids):
                    class_name = self.detector.model.names[cls_id]
                    track_history[track_id].append({
                        'frame': frame_count,
                        'bbox': box.tolist(),
                        'class': class_name,
                        'confidence': float(conf)
                    })
                    
                    # Draw on frame
                    x1, y1, x2, y2 = map(int, box)
                    
                    # Different color per track
                    color = self._get_track_color(track_id)
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw label
                    label = f"ID:{track_id} {class_name} {conf:.2f}"
                    (label_width, label_height), _ = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                    )
                    cv2.rectangle(
                        frame, 
                        (x1, y1 - label_height - 10), 
                        (x1 + label_width, y1), 
                        color, 
                        -1
                    )
                    cv2.putText(
                        frame, 
                        label, 
                        (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, 
                        (255, 255, 255), 
                        2
                    )
                    
                    # Draw trajectory
                    if len(track_history[track_id]) > 1:
                        points = []
                        for det in track_history[track_id][-30:]:  # Last 30 points
                            bbox = det['bbox']
                            center_x = int((bbox[0] + bbox[2]) / 2)
                            center_y = int((bbox[1] + bbox[3]) / 2)
                            points.append((center_x, center_y))
                        
                        for i in range(1, len(points)):
                            cv2.line(frame, points[i-1], points[i], color, 2)
            
            # Write frame
            out.write(frame)
            
            processed_frames += 1
            frame_count += 1
            
            if max_frames and processed_frames >= max_frames:
                break
        
        cap.release()
        out.release()
        
        # Generate track summaries
        tracks = []
        for track_id, detections in track_history.items():
            if not detections:
                continue
            
            frames = [d['frame'] for d in detections]
            confidences = [d['confidence'] for d in detections]
            
            trajectory = []
            for det in detections:
                bbox = det['bbox']
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                trajectory.append([center_x, center_y])
            
            tracks.append({
                'track_id': int(track_id),
                'class_name': detections[0]['class'],
                'first_frame': int(min(frames)),
                'last_frame': int(max(frames)),
                'total_frames': len(detections),
                'confidence_avg': float(np.mean(confidences)),
                'trajectory': trajectory
            })
        
        # Save JSON results
        json_filename = f"{Path(file.filename).stem}_tracking.json"
        json_path = Path(settings.RESULTS_DIR) / json_filename
        
        metadata = {
            'width': width,
            'height': height,
            'fps': fps,
            'total_frames': total_frames
        }
        
        results_data = {
            "filename": file.filename,
            "total_frames": total_frames,
            "processed_frames": processed_frames,
            "tracks": tracks,
            "metadata": metadata,
            "total_tracks": len(tracks)
        }
        
        with open(json_path, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        processing_time = time.time() - start_time
        
        # Calculate detection summary (species count across all tracks)
        detection_summary = {}
        total_detections = 0
        for track in tracks:
            class_name = track.get('class_name', 'unknown')
            detection_summary[class_name] = detection_summary.get(class_name, 0) + 1
            total_detections += track.get('total_frames', 0)
        
        from datetime import datetime
        
        return {
            "success": True,
            "filename": file.filename,
            "annotated_video": f"/results/{output_filename}",
            "annotated_video_url": f"/results/{output_filename}",  # Keep for backward compatibility
            "total_frames_processed": processed_frames,
            "total_frames": total_frames,
            "processed_frames": processed_frames,
            "total_detections": total_detections,
            "unique_tracks": len(tracks),
            "tracks": tracks,
            "processing_time": processing_time,
            "total_tracks": len(tracks),
            "detection_summary": detection_summary,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
    
    def _get_track_color(self, track_id: int) -> tuple:
        """Generate consistent color for track ID"""
        np.random.seed(track_id)
        return tuple(np.random.randint(0, 255, 3).tolist())

