'use client';

import Link from 'next/link';
import { 
  Camera, 
  Video, 
  Map, 
  BarChart3, 
  Upload,
  Zap,
  Shield,
  Globe
} from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
            🦌 Wildlife Drone Detection
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            AI-powered wildlife detection and tracking from drone footage using YOLO11
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/upload">
              <button className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-all">
                <Upload className="w-5 h-5" />
                Start Detection
              </button>
            </Link>
            <Link href="/results">
              <button className="bg-white hover:bg-gray-50 text-gray-800 px-8 py-3 rounded-lg font-semibold border-2 border-gray-200 transition-all">
                View Results
              </button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <FeatureCard
            icon={<Camera className="w-8 h-8 text-green-600" />}
            title="Image Detection"
            description="Detect animals in drone images with high accuracy using YOLO11"
          />
          <FeatureCard
            icon={<Video className="w-8 h-8 text-blue-600" />}
            title="Video Tracking"
            description="Track animals across video frames with unique IDs and trajectories"
          />
          <FeatureCard
            icon={<Map className="w-8 h-8 text-purple-600" />}
            title="GPS Tagging"
            description="Associate detections with GPS coordinates and metadata"
          />
          <FeatureCard
            icon={<BarChart3 className="w-8 h-8 text-orange-600" />}
            title="Group Analysis"
            description="Identify herds and groups using spatial clustering algorithms"
          />
        </div>

        {/* Tech Stack */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-16">
          <h2 className="text-2xl font-bold mb-6 text-center">Technology Stack</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <TechCard
              icon={<Zap className="w-6 h-6" />}
              title="YOLO11"
              description="Latest state-of-the-art object detection model from Ultralytics"
            />
            <TechCard
              icon={<Shield className="w-6 h-6" />}
              title="FastAPI Backend"
              description="High-performance Python backend with async support"
            />
            <TechCard
              icon={<Globe className="w-6 h-6" />}
              title="Next.js Frontend"
              description="Modern React framework with TypeScript"
            />
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-6 text-center">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-4">
            <Step number={1} title="Upload" description="Upload drone images or videos" />
            <Step number={2} title="Detect" description="AI processes and detects animals" />
            <Step number={3} title="Track" description="System tracks across frames" />
            <Step number={4} title="Analyze" description="View results and export data" />
          </div>
        </div>
      </div>
    </main>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  );
}

function TechCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="flex items-start gap-3">
      <div className="bg-green-100 p-2 rounded-lg">{icon}</div>
      <div>
        <h4 className="font-semibold mb-1">{title}</h4>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
}

function Step({ number, title, description }: { number: number; title: string; description: string }) {
  return (
    <div className="text-center">
      <div className="bg-white text-green-600 w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-3">
        {number}
      </div>
      <h4 className="font-semibold mb-1">{title}</h4>
      <p className="text-sm text-green-100">{description}</p>
    </div>
  );
}

