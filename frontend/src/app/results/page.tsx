'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';
import Link from 'next/link';
import { ArrowLeft, Download, Loader2, AlertCircle } from 'lucide-react';
import { DetectionResult, VideoTrackingResult, api } from '@/lib/api';
import DetectionStats from '@/components/DetectionStats';
import DetectionList from '@/components/DetectionList';

function ResultsContent() {
  const searchParams = useSearchParams();
  const type = searchParams.get('type');
  const file = searchParams.get('file');

  const [result, setResult] = useState<DetectionResult | VideoTrackingResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Try to get result from sessionStorage
    const storedResult = sessionStorage.getItem('latestResult');
    if (storedResult) {
      try {
        const parsedResult = JSON.parse(storedResult);
        console.log('Loaded result from storage:', parsedResult);
        
        // Ensure the result has the required fields with defaults
        const safeResult = {
          ...parsedResult,
          total_detections: parsedResult.total_detections || 0,
          detection_summary: parsedResult.detection_summary || {},
          processing_time: parsedResult.processing_time || 0,
        };
        
        setResult(safeResult);
        setLoading(false);
      } catch (err) {
        console.error('Error parsing result:', err);
        setError('Failed to load results');
        setLoading(false);
      }
    } else {
      setError('No results found. Please upload an image or video.');
      setLoading(false);
    }
  }, []);

  const handleDownload = async () => {
    if (!file) return;
    
    try {
      const blob = await api.downloadResult(file);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-green-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="bg-red-50 border-2 border-red-200 rounded-lg p-8 text-center">
        <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-red-800 mb-2">Error</h3>
        <p className="text-red-600">{error || 'Failed to load results'}</p>
        <Link href="/upload">
          <button className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
            Upload New File
          </button>
        </Link>
      </div>
    );
  }

  const isVideo = type === 'video';
  const imageResult = !isVideo ? (result as DetectionResult) : null;
  const videoResult = isVideo ? (result as VideoTrackingResult) : null;

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">
          {isVideo ? 'Video Tracking' : 'Image Detection'} Results
        </h1>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          <Download className="w-4 h-4" />
          Download Results
        </button>
      </div>

      {/* Stats */}
      <DetectionStats
        totalDetections={result.total_detections || 0}
        detectionSummary={result.detection_summary || {}}
        processingTime={result.processing_time || 0}
      />

      {/* Image/Video Display */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">
          {isVideo ? 'Annotated Video' : 'Annotated Image'}
        </h2>
        
        {isVideo && videoResult ? (
          <video
            controls
            className="w-full rounded-lg"
            src={api.getImageUrl(videoResult.annotated_video)}
          >
            Your browser does not support the video tag.
          </video>
        ) : imageResult ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Original Image */}
            <div>
              <h3 className="text-lg font-semibold mb-2 text-gray-700">Original</h3>
              <img
                src={api.getImageUrl(imageResult.original_image)}
                alt="Original"
                className="w-full rounded-lg border-2 border-gray-200"
              />
            </div>
            
            {/* Annotated Image */}
            <div>
              <h3 className="text-lg font-semibold mb-2 text-gray-700">
                Detections ({imageResult.total_detections})
              </h3>
              <img
                src={api.getImageUrl(imageResult.annotated_image)}
                alt="Annotated"
                className="w-full rounded-lg border-2 border-green-200"
              />
            </div>
          </div>
        ) : null}
      </div>

      {/* Detection List (for images) */}
      {imageResult && imageResult.detections && (
        <DetectionList
          detections={imageResult.detections || []}
          detectionSummary={result.detection_summary || {}}
        />
      )}

      {/* Video Tracking Info */}
      {videoResult && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">Tracking Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-600 mb-1">Frames Processed</div>
              <div className="text-2xl font-bold text-gray-800">
                {videoResult.total_frames_processed}
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-600 mb-1">Unique Tracks</div>
              <div className="text-2xl font-bold text-gray-800">
                {videoResult.unique_tracks}
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-600 mb-1">Total Detections</div>
              <div className="text-2xl font-bold text-gray-800">
                {videoResult.total_detections}
              </div>
            </div>
          </div>

          {/* Species Summary */}
          <div className="mt-6">
            <h3 className="text-xl font-bold mb-3">Species Summary</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {Object.entries(result.detection_summary || {}).map(([species, count]) => (
                <div
                  key={species}
                  className="bg-green-50 border-2 border-green-200 rounded-lg p-3 text-center"
                >
                  <div className="text-lg font-bold text-green-600">{count}</div>
                  <div className="text-sm text-gray-700 capitalize">{species}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="bg-gray-50 rounded-lg p-6 mt-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-700">Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Filename:</span>{' '}
            <span className="font-mono text-gray-800">{result.filename}</span>
          </div>
          <div>
            <span className="text-gray-600">Processed:</span>{' '}
            <span className="text-gray-800">
              {new Date(result.timestamp).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/">
        <button className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </button>
      </Link>

      <Suspense
        fallback={
          <div className="flex items-center justify-center min-h-[400px]">
            <Loader2 className="w-12 h-12 text-green-600 animate-spin" />
          </div>
        }
      >
        <ResultsContent />
      </Suspense>
    </div>
  );
}

