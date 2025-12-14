'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload, Image as ImageIcon, Video, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import UploadZone from '@/components/UploadZone';
import { api } from '@/lib/api';

export default function UploadPage() {
  const router = useRouter();
  const [uploadType, setUploadType] = useState<'image' | 'video'>('image');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    setProgress(0);

    try {
      if (uploadType === 'image') {
        const result = await api.detectImage(file, {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 100)
            );
            setProgress(percentCompleted);
          },
        });
        
        // Store result in sessionStorage
        sessionStorage.setItem('latestResult', JSON.stringify(result));
        
        // Redirect to results page
        router.push(`/results?type=image&file=${result.filename}`);
      } else {
        const result = await api.trackVideo(file, {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 100)
            );
            setProgress(percentCompleted);
          },
        });
        
        // Store result in sessionStorage
        sessionStorage.setItem('latestResult', JSON.stringify(result));
        
        // Redirect to results page
        router.push(`/results?type=video&file=${result.filename}`);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setUploading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/">
        <button className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </button>
      </Link>

      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-2 text-center">Upload Drone Footage</h1>
        <p className="text-gray-600 mb-8 text-center">
          Upload images or videos captured by drones for wildlife detection
        </p>

        {/* Type Selector */}
        <div className="flex gap-4 mb-8 justify-center">
          <button
            onClick={() => setUploadType('image')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              uploadType === 'image'
                ? 'bg-green-600 text-white shadow-lg'
                : 'bg-white text-gray-600 border-2 border-gray-200 hover:border-green-600'
            }`}
          >
            <ImageIcon className="w-5 h-5" />
            Image
          </button>
          <button
            onClick={() => setUploadType('video')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              uploadType === 'video'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-600 border-2 border-gray-200 hover:border-blue-600'
            }`}
          >
            <Video className="w-5 h-5" />
            Video
          </button>
        </div>

        {/* Upload Zone */}
        <UploadZone
          uploadType={uploadType}
          onUpload={handleUpload}
          disabled={uploading}
        />

        {/* Progress */}
        {uploading && (
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-3 mb-3">
              <Upload className="w-5 h-5 text-green-600 animate-pulse" />
              <span className="font-semibold">
                {progress < 100 ? 'Uploading...' : 'Processing...'}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-2">
              {progress < 100 
                ? `Uploading: ${progress}%` 
                : 'Processing with YOLO11... This may take a moment.'}
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 bg-red-50 border-2 border-red-200 rounded-lg p-4">
            <p className="text-red-800 font-semibold">Error</p>
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Info */}
        <div className="mt-8 bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold mb-2 text-blue-900">📋 Supported Formats</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• <strong>Images:</strong> JPG, JPEG, PNG</li>
            <li>• <strong>Videos:</strong> MP4, MOV, AVI</li>
            <li>• <strong>Max Size:</strong> 100MB per file</li>
            <li>• <strong>Processing Time:</strong> 1-5 minutes depending on file size</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

