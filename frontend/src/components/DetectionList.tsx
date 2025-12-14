'use client';

import { Detection } from '@/lib/api';

interface DetectionListProps {
  detections: Detection[];
  detectionSummary: Record<string, number> | null | undefined;
}

export default function DetectionList({ detections, detectionSummary }: DetectionListProps) {
  const summaryEntries = detectionSummary ? Object.entries(detectionSummary) : [];
  const detectionsList = detections || [];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Detection Summary</h2>

      {/* Species Count */}
      {summaryEntries.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          {summaryEntries.map(([species, count]) => (
          <div
            key={species}
            className="flex items-center justify-between bg-gray-50 rounded-lg p-4 border-2 border-gray-200"
          >
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="font-semibold text-gray-800 capitalize">
                {species}
              </span>
            </div>
            <span className="text-2xl font-bold text-green-600">{count}</span>
          </div>
        ))}
        </div>
      )}

      {/* Individual Detections */}
      {detectionsList.length > 0 ? (
        <>
          <h3 className="text-xl font-bold mb-3">All Detections</h3>
          <div className="overflow-auto max-h-96">
            <table className="w-full">
              <thead className="bg-gray-100 sticky top-0">
                <tr>
                  <th className="text-left p-3 font-semibold">#</th>
                  <th className="text-left p-3 font-semibold">Species</th>
                  <th className="text-left p-3 font-semibold">Confidence</th>
                  <th className="text-left p-3 font-semibold">Bounding Box</th>
                </tr>
              </thead>
              <tbody>
                {detectionsList.map((detection, index) => (
              <tr
                key={index}
                className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <td className="p-3 text-gray-600">{index + 1}</td>
                <td className="p-3">
                  <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full font-semibold capitalize">
                    {detection.class}
                  </span>
                </td>
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-[100px]">
                      <div
                        className="bg-green-600 h-2 rounded-full"
                        style={{ width: `${detection.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-700">
                      {(detection.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </td>
                <td className="p-3 text-sm text-gray-600 font-mono">
                  [{detection.bbox.map((v) => Math.round(v)).join(', ')}]
                </td>
              </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="text-gray-500 text-center py-8">No detections found</p>
      )}
    </div>
  );
}
