'use client';

import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const type = searchParams.get('type');
  const file = searchParams.get('file');

  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/">
        <button className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </button>
      </Link>

      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Detection Results</h1>
        
        <div className="bg-white rounded-lg shadow-md p-8">
          <p className="text-gray-600">
            Results for: <strong>{file}</strong> ({type})
          </p>
          <p className="text-sm text-gray-500 mt-4">
            Results visualization coming soon...
          </p>
        </div>
      </div>
    </div>
  );
}

