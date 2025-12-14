'use client';

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileImage, FileVideo } from 'lucide-react';

interface UploadZoneProps {
  uploadType: 'image' | 'video';
  onUpload: (file: File) => void;
  disabled?: boolean;
}

export default function UploadZone({ uploadType, onUpload, disabled }: UploadZoneProps) {
  const acceptedFormats = uploadType === 'image' 
    ? { 'image/*': ['.jpg', '.jpeg', '.png'] }
    : { 'video/*': ['.mp4', '.mov', '.avi'] };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFormats,
    maxFiles: 1,
    disabled,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-4 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
        isDragActive
          ? 'border-green-500 bg-green-50'
          : disabled
          ? 'border-gray-300 bg-gray-50 cursor-not-allowed'
          : 'border-gray-300 hover:border-green-500 hover:bg-green-50'
      }`}
    >
      <input {...getInputProps()} />
      
      <div className="flex flex-col items-center gap-4">
        {uploadType === 'image' ? (
          <FileImage className="w-16 h-16 text-green-600" />
        ) : (
          <FileVideo className="w-16 h-16 text-blue-600" />
        )}
        
        {isDragActive ? (
          <p className="text-lg font-semibold text-green-600">
            Drop the {uploadType} here...
          </p>
        ) : (
          <>
            <div>
              <p className="text-lg font-semibold mb-2">
                Drag & drop your {uploadType} here
              </p>
              <p className="text-gray-500">or click to browse</p>
            </div>
            
            <button
              type="button"
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
                uploadType === 'image'
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
              disabled={disabled}
            >
              <Upload className="w-5 h-5" />
              Choose {uploadType === 'image' ? 'Image' : 'Video'}
            </button>
          </>
        )}
      </div>
    </div>
  );
}

