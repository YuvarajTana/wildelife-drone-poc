"""
Metadata Extraction Service
Extracts GPS, timestamp, and other metadata from images/videos
"""

import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class MetadataService:
    """Extract metadata from drone images and videos"""
    
    def extract_image_metadata(self, image_path: str) -> Dict[str, Any]:
        """
        Extract metadata from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary containing metadata
        """
        metadata = {}
        
        try:
            # Open image with PIL
            with Image.open(image_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                
                # Extract EXIF data
                exif_data = img._getexif()
                
                if exif_data:
                    # Parse standard EXIF tags
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        
                        if tag == "DateTime":
                            metadata['timestamp'] = str(value)
                        elif tag == "Make":
                            metadata['camera_make'] = str(value)
                        elif tag == "Model":
                            metadata['camera_model'] = str(value)
                        elif tag == "GPSInfo":
                            gps_data = self._parse_gps(value)
                            if gps_data:
                                metadata['gps'] = gps_data
            
        except Exception as e:
            print(f"Warning: Could not extract metadata: {e}")
        
        return metadata
    
    def _parse_gps(self, gps_info: Dict) -> Optional[Dict[str, float]]:
        """
        Parse GPS information from EXIF
        
        Args:
            gps_info: GPS info dictionary from EXIF
            
        Returns:
            Dictionary with latitude, longitude, altitude
        """
        try:
            gps_data = {}
            
            for key, value in gps_info.items():
                tag = GPSTAGS.get(key, key)
                gps_data[tag] = value
            
            # Extract coordinates
            if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                lat = self._convert_to_degrees(gps_data['GPSLatitude'])
                lon = self._convert_to_degrees(gps_data['GPSLongitude'])
                
                # Apply hemisphere
                if gps_data.get('GPSLatitudeRef') == 'S':
                    lat = -lat
                if gps_data.get('GPSLongitudeRef') == 'W':
                    lon = -lon
                
                result = {
                    'latitude': lat,
                    'longitude': lon
                }
                
                # Add altitude if available
                if 'GPSAltitude' in gps_data:
                    altitude = float(gps_data['GPSAltitude'])
                    result['altitude'] = altitude
                
                return result
        
        except Exception as e:
            print(f"Warning: Could not parse GPS data: {e}")
        
        return None
    
    def _convert_to_degrees(self, value) -> float:
        """
        Convert GPS coordinates to degrees
        
        Args:
            value: GPS coordinate in EXIF format
            
        Returns:
            Decimal degrees
        """
        d, m, s = value
        return float(d) + float(m) / 60.0 + float(s) / 3600.0

