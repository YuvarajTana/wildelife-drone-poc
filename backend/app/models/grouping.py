"""
Animal Grouping/Clustering Module
Identifies groups and herds based on spatial proximity
"""

import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Dict, Any


class AnimalGrouping:
    """Spatial clustering for animal group detection"""
    
    def __init__(self, eps: float = 100.0, min_samples: int = 2):
        """
        Initialize grouping module
        
        Args:
            eps: Maximum distance between animals in same group (pixels)
            min_samples: Minimum animals to form a group
        """
        self.eps = eps
        self.min_samples = min_samples
    
    def identify_groups(
        self, 
        detections: List[Dict[str, Any]]
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Identify animal groups using spatial clustering
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Tuple of (updated_detections, groups)
        """
        if not detections or len(detections) < 2:
            return detections, []
        
        # Extract bounding box centers
        centers = []
        for det in detections:
            bbox = det['bbox']
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            centers.append([center_x, center_y])
        
        centers = np.array(centers)
        
        # Apply DBSCAN clustering
        clustering = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = clustering.fit_predict(centers)
        
        # Assign group IDs to detections
        for i, det in enumerate(detections):
            if labels[i] >= 0:  # Not noise
                det['group_id'] = int(labels[i])
            else:
                det['group_id'] = None
        
        # Generate group information
        groups = []
        unique_groups = set(labels[labels >= 0])
        
        for group_id in unique_groups:
            group_indices = np.where(labels == group_id)[0]
            group_centers = centers[group_indices]
            
            # Calculate group statistics
            group_center = group_centers.mean(axis=0)
            member_ids = [detections[i]['id'] for i in group_indices]
            
            groups.append({
                'group_id': int(group_id),
                'count': len(group_indices),
                'center': group_center.tolist(),
                'members': member_ids
            })
        
        return detections, groups

