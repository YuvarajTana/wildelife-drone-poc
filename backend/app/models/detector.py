"""
YOLO11 Wildlife Detector
Handles animal detection using Ultralytics YOLO11
"""

from ultralytics import YOLO
import torch
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import cv2


class WildlifeDetector:
    """Wildlife detection using YOLO11"""
    
    def __init__(
        self, 
        model_path: str = "yolo11m.pt",
        confidence_threshold: float = 0.25,
        device: str = "mps"
    ):
        """
        Initialize the detector
        
        Args:
            model_path: Path to YOLO11 model weights
            confidence_threshold: Minimum confidence for detections
            device: Device to run inference on ('mps', 'cuda', 'cpu')
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.device = self._get_device(device)
        
        # Load model
        print(f"Loading YOLO11 model from {model_path}...")
        self.model = YOLO(model_path)
        
        # Move model to device
        if self.device != "cpu":
            self.model.to(self.device)
        
        print(f"✅ Model loaded successfully on {self.device}")
        print(f"📊 Model type: {type(self.model.model).__name__}")
        
    def _get_device(self, preferred_device: str) -> str:
        """Determine the best available device"""
        if preferred_device == "mps" and torch.backends.mps.is_available():
            return "mps"
        elif preferred_device == "cuda" and torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    
    def detect(
        self, 
        image: np.ndarray,
        confidence: float = None,
        iou_threshold: float = 0.45
    ) -> List[Dict[str, Any]]:
        """
        Detect animals in an image
        
        Args:
            image: Input image as numpy array (BGR format)
            confidence: Override confidence threshold
            iou_threshold: IoU threshold for NMS
            
        Returns:
            List of detections with bbox, class, confidence
        """
        conf = confidence if confidence is not None else self.confidence_threshold
        
        # Run inference
        results = self.model.predict(
            image,
            conf=conf,
            iou=iou_threshold,
            device=self.device,
            verbose=False
        )
        
        # Parse results
        detections = []
        result = results[0]  # First image
        
        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for i, (box, conf, cls_id) in enumerate(zip(boxes, confidences, class_ids)):
                detections.append({
                    "id": i,
                    "class": self.model.names[cls_id],
                    "confidence": float(conf),
                    "bbox": box.tolist(),
                    "class_id": int(cls_id)
                })
        
        return detections
    
    def detect_and_track(
        self,
        video_path: str,
        confidence: float = None,
        tracker: str = "bytetrack.yaml"
    ) -> List[Dict[str, Any]]:
        """
        Detect and track animals in a video
        
        Args:
            video_path: Path to video file
            confidence: Override confidence threshold
            tracker: Tracker configuration
            
        Returns:
            Tracking results
        """
        conf = confidence if confidence is not None else self.confidence_threshold
        
        # Run tracking
        results = self.model.track(
            source=video_path,
            conf=conf,
            device=self.device,
            tracker=tracker,
            stream=True,
            verbose=False
        )
        
        return results
    
    def annotate_image(
        self, 
        image: np.ndarray, 
        detections: List[Dict[str, Any]],
        groups: List[Dict[str, Any]] = None
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Input image
            detections: List of detections
            groups: Optional group information
            
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        # Group colors
        group_colors = {}
        if groups:
            for group in groups:
                group_colors[group['group_id']] = tuple(np.random.randint(0, 255, 3).tolist())
        
        # Draw detections
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class']
            confidence = det['confidence']
            group_id = det.get('group_id')
            
            # Choose color based on group
            if group_id is not None and group_id in group_colors:
                color = group_colors[group_id]
            else:
                color = (0, 255, 0)  # Green default
            
            # Draw box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{class_name} {confidence:.2f}"
            if group_id is not None:
                label += f" G{group_id}"
            
            (label_width, label_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                annotated, 
                (x1, y1 - label_height - 10), 
                (x1 + label_width, y1), 
                color, 
                -1
            )
            cv2.putText(
                annotated, 
                label, 
                (x1, y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (255, 255, 255), 
                2
            )
        
        return annotated

