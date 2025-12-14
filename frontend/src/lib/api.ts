import axios, { AxiosProgressEvent } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Detection {
  bbox: [number, number, number, number]; // [x1, y1, x2, y2]
  confidence: number;
  class: string;
  class_id: number;
}

export interface DetectionResult {
  filename: string;
  original_image: string;
  annotated_image: string;
  detections: Detection[];
  total_detections: number;
  detection_summary: Record<string, number>;
  processing_time: number;
  timestamp: string;
}

export interface VideoTrackingResult {
  filename: string;
  annotated_video: string;
  total_frames_processed: number;
  total_detections: number;
  unique_tracks: number;
  tracks: any[];
  detection_summary: Record<string, number>;
  processing_time: number;
  timestamp: string;
}

export interface UploadOptions {
  onUploadProgress?: (progressEvent: AxiosProgressEvent) => void;
}

export const api = {
  // Health check
  async healthCheck() {
    const response = await axios.get(`${API_URL}/health`);
    return response.data;
  },

  // Detect animals in image
  async detectImage(file: File, options?: UploadOptions): Promise<DetectionResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('confidence', '0.25');
    formData.append('enable_grouping', 'true');

    const response = await axios.post(`${API_URL}/api/detect/image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: options?.onUploadProgress,
    });

    return response.data;
  },

  // Track animals in video
  async trackVideo(file: File, options?: UploadOptions): Promise<VideoTrackingResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('confidence', '0.25');
    formData.append('fps', '5');

    const response = await axios.post(`${API_URL}/api/detect/video`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: options?.onUploadProgress,
    });

    return response.data;
  },

  // Get results list
  async getResults() {
    const response = await axios.get(`${API_URL}/api/results`);
    return response.data;
  },

  // Download result file
  async downloadResult(filename: string) {
    const response = await axios.get(`${API_URL}/api/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Delete result
  async deleteResult(filename: string) {
    const response = await axios.delete(`${API_URL}/api/results/${filename}`);
    return response.data;
  },

  // Get image URL
  getImageUrl(path: string): string {
    return `${API_URL}${path}`;
  },
};
