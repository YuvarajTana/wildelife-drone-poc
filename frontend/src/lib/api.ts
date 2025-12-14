import axios, { AxiosProgressEvent } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export interface Detection {
  id: number;
  class: string;
  confidence: number;
  bbox: number[];
  group_id?: number;
}

export interface Group {
  group_id: number;
  count: number;
  center: number[];
  members: number[];
}

export interface GPSCoordinates {
  latitude: number;
  longitude: number;
  altitude?: number;
}

export interface Metadata {
  gps?: GPSCoordinates;
  timestamp?: string;
  camera_make?: string;
  camera_model?: string;
  width?: number;
  height?: number;
}

export interface ImageDetectionResponse {
  success: boolean;
  filename: string;
  detections: Detection[];
  groups: Group[];
  metadata?: Metadata;
  annotated_image_url: string;
  processing_time: number;
  total_detections: number;
}

export interface Track {
  track_id: number;
  class_name: string;
  first_frame: number;
  last_frame: number;
  total_frames: number;
  confidence_avg: number;
  trajectory: number[][];
}

export interface VideoTrackingResponse {
  success: boolean;
  filename: string;
  total_frames: number;
  processed_frames: number;
  tracks: Track[];
  annotated_video_url: string;
  processing_time: number;
  total_tracks: number;
  metadata?: Metadata;
}

export interface UploadOptions {
  onUploadProgress?: (progressEvent: AxiosProgressEvent) => void;
}

export const api = {
  async healthCheck() {
    const response = await axios.get(`${API_URL}/health`);
    return response.data;
  },

  async detectImage(
    file: File, 
    options?: UploadOptions & { confidence?: number; enableGrouping?: boolean }
  ): Promise<ImageDetectionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options?.confidence) {
      formData.append('confidence', options.confidence.toString());
    }
    if (options?.enableGrouping !== undefined) {
      formData.append('enable_grouping', options.enableGrouping.toString());
    }

    const response = await apiClient.post<ImageDetectionResponse>(
      '/api/detect/image',
      formData,
      {
        onUploadProgress: options?.onUploadProgress,
      }
    );
    
    return response.data;
  },

  async trackVideo(
    file: File,
    options?: UploadOptions & { confidence?: number; fps?: number; maxFrames?: number }
  ): Promise<VideoTrackingResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options?.confidence) {
      formData.append('confidence', options.confidence.toString());
    }
    if (options?.fps) {
      formData.append('fps', options.fps.toString());
    }
    if (options?.maxFrames) {
      formData.append('max_frames', options.maxFrames.toString());
    }

    const response = await apiClient.post<VideoTrackingResponse>(
      '/api/detect/video',
      formData,
      {
        onUploadProgress: options?.onUploadProgress,
      }
    );
    
    return response.data;
  },

  async listResults() {
    const response = await axios.get(`${API_URL}/api/results`);
    return response.data;
  },

  async downloadResult(filename: string) {
    const response = await axios.get(`${API_URL}/api/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  getResultUrl(path: string) {
    return `${API_URL}${path}`;
  },
};

