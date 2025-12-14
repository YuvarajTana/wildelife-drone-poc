'use client';

interface DetectionStatsProps {
  totalDetections: number;
  detectionSummary: Record<string, number> | null | undefined;
  processingTime: number;
}

export default function DetectionStats({
  totalDetections,
  detectionSummary,
  processingTime,
}: DetectionStatsProps) {
  const uniqueSpecies = detectionSummary ? Object.keys(detectionSummary).length : 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Total Detections */}
      <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white shadow-lg">
        <div className="text-sm font-semibold uppercase tracking-wide opacity-90 mb-2">
          Total Detections
        </div>
        <div className="text-4xl font-bold">{totalDetections || 0}</div>
      </div>

      {/* Unique Species */}
      <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white shadow-lg">
        <div className="text-sm font-semibold uppercase tracking-wide opacity-90 mb-2">
          Unique Species
        </div>
        <div className="text-4xl font-bold">{uniqueSpecies}</div>
      </div>

      {/* Processing Time */}
      <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white shadow-lg">
        <div className="text-sm font-semibold uppercase tracking-wide opacity-90 mb-2">
          Processing Time
        </div>
        <div className="text-4xl font-bold">
          {processingTime ? processingTime.toFixed(2) : '0.00'}s
        </div>
      </div>
    </div>
  );
}
