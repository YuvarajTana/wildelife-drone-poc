# 🦌 Wildlife Detection & Tracking from Drone Footage - Production PoC

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Demo Guide](#demo-guide)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)

---

## 🎯 Overview

A **production-ready Proof of Concept (PoC)** to analyze **drone-captured images and videos** over forests/jungles with AI-powered wildlife detection and tracking capabilities.

### Key Capabilities:
- ✅ Detect animals in images and videos using **YOLO11** (latest state-of-the-art model)
- ✅ Identify animal **groups/herds** using spatial clustering
- ✅ Track animals across video frames in real-time
- ✅ Associate detections with **GPS coordinates** and metadata
- ✅ Modern **Next.js web interface** for demonstrations
- ✅ RESTful API for integration with other systems
- ✅ Optimized for **Apple Silicon (M4)** with Metal Performance Shaders (MPS)
- ✅ AWS-ready architecture for cloud deployment

### Demo Outputs:
- 📸 Annotated images/videos with bounding boxes
- 🎯 Species classification with confidence scores
- 🐾 Group/herd identification
- 📍 GPS-tagged detections
- 📊 Real-time tracking visualization
- 📄 JSON/CSV export for data analysis

---

## 🚀 Features

### Phase 1: Image Detection ✅
- Upload single or multiple drone images
- Real-time animal detection with YOLO11
- Visual bounding boxes with species labels
- Confidence scoring
- Export results as JSON

### Phase 2: Grouping & Clustering ✅
- Spatial clustering algorithm (DBSCAN/HDBSCAN)
- Automatic herd/group identification
- Group statistics (count, spread, density)

### Phase 3: Video Tracking ✅
- Frame-by-frame processing
- Multi-object tracking (ByteTrack)
- Trajectory visualization
- Track persistence across occlusions

### Phase 4: Location Intelligence ✅
- GPS metadata extraction (EXIF)
- Drone telemetry integration
- Geospatial mapping of detections
- Altitude and timestamp correlation

---

## 🛠 Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **Ultralytics YOLO11** - Latest object detection model
- **PyTorch 2.x** - Deep learning framework (MPS backend for Mac)
- **OpenCV** - Computer vision operations
- **ByteTrack** - Multi-object tracking
- **Scikit-learn** - Clustering algorithms
- **Pillow & ExifRead** - Image processing and metadata

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn/ui** - UI components
- **React Query** - Data fetching
- **Axios** - HTTP client
- **React Dropzone** - File uploads
- **Leaflet** - Map visualization

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy (production)
- **AWS S3** - File storage (cloud deployment)
- **AWS ECS/Fargate** - Container orchestration (cloud deployment)

---

## 📁 Project Structure

```
wildlife-drone-poc/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── detector.py         # YOLO11 detection
│   │   │   ├── tracker.py          # ByteTrack tracking
│   │   │   └── grouping.py         # Clustering logic
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── image_service.py    # Image processing
│   │   │   ├── video_service.py    # Video processing
│   │   │   └── metadata_service.py # GPS extraction
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # API endpoints
│   │   │   └── schemas.py          # Pydantic models
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_handler.py
│   │       └── visualization.py
│   ├── weights/                     # YOLO11 model weights
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Home page
│   │   │   ├── layout.tsx          # Root layout
│   │   │   ├── upload/
│   │   │   │   └── page.tsx        # Upload interface
│   │   │   ├── results/
│   │   │   │   └── page.tsx        # Results visualization
│   │   │   └── api/                # API routes (if needed)
│   │   ├── components/
│   │   │   ├── ui/                 # Shadcn components
│   │   │   ├── UploadZone.tsx      # Drag & drop upload
│   │   │   ├── ResultsViewer.tsx   # Detection results
│   │   │   ├── VideoPlayer.tsx     # Video with tracking
│   │   │   ├── MapViewer.tsx       # GPS visualization
│   │   │   └── StatsPanel.tsx      # Analytics dashboard
│   │   ├── lib/
│   │   │   ├── api.ts              # API client
│   │   │   └── utils.ts            # Utilities
│   │   └── types/
│   │       └── index.ts            # TypeScript types
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── Dockerfile
│   └── README.md
│
├── data/
│   ├── raw/                        # Original uploads
│   ├── frames/                     # Extracted video frames
│   ├── processed/                  # Annotated outputs
│   └── results/                    # JSON/CSV exports
│
├── docker/
│   └── docker-compose.yml          # Multi-container setup
│
├── scripts/
│   ├── download_models.py          # Download YOLO11 weights
│   └── test_detection.py           # Quick test script
│
├── tests/
│   ├── test_backend.py
│   └── test_frontend.py
│
├── .env.example
├── .gitignore
├── README.md
└── PROJECT_SETUP_GUIDE.md          # This file
```

---

## 📋 Prerequisites

### System Requirements
- **OS**: macOS (Apple Silicon M4 recommended) or Linux
- **RAM**: 16GB minimum, 48GB recommended
- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **Git**: Latest version

### Optional
- **Docker Desktop**: For containerized deployment
- **CUDA GPU**: For NVIDIA GPU acceleration (Linux/Windows)

---

## 💻 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd wildlife-drone-poc
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2.2 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.3 Download YOLO11 Model Weights

```bash
# Run the download script
python ../scripts/download_models.py

# Or manually download using Python
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

Available YOLO11 models (from fastest to most accurate):
- `yolo11n.pt` - Nano (fastest, ~6MB)
- `yolo11s.pt` - Small (~22MB)
- `yolo11m.pt` - Medium (~50MB)
- `yolo11l.pt` - Large (~100MB)
- `yolo11x.pt` - Extra Large (most accurate, ~200MB)

**Recommendation**: Start with `yolo11m.pt` for balanced performance.

#### 2.4 Configure Environment Variables

```bash
# Copy example environment file
cp ../.env.example .env

# Edit .env with your settings
nano .env
```

**Example `.env` file:**
```env
# Backend Configuration
PYTHON_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Model Configuration
YOLO_MODEL_PATH=weights/yolo11m.pt
CONFIDENCE_THRESHOLD=0.25
IOU_THRESHOLD=0.45
MAX_DETECTIONS=300

# Storage Configuration
UPLOAD_DIR=../data/raw
PROCESSED_DIR=../data/processed
RESULTS_DIR=../data/results

# Tracking Configuration
TRACKER_TYPE=bytetrack
TRACK_BUFFER=30
MATCH_THRESHOLD=0.8

# Performance
DEVICE=mps  # Use 'mps' for Mac, 'cuda' for NVIDIA GPU, 'cpu' for CPU
BATCH_SIZE=1
NUM_WORKERS=4
```

### Step 3: Frontend Setup

#### 3.1 Install Node.js Dependencies

```bash
cd ../frontend
npm install
# Or use yarn/pnpm
# yarn install
# pnpm install
```

#### 3.2 Configure Frontend Environment

```bash
cp .env.example .env.local
nano .env.local
```

**Example `.env.local` file:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Wildlife Drone Tracker
NEXT_PUBLIC_MAX_FILE_SIZE=100  # MB
NEXT_PUBLIC_SUPPORTED_FORMATS=jpg,jpeg,png,mp4,mov,avi
```

### Step 4: Create Required Directories

```bash
cd ..
mkdir -p data/{raw,frames,processed,results}
mkdir -p backend/weights
```

---

## 🎬 Running the Application

### Option 1: Manual Run (Development)

#### Terminal 1: Start Backend

```bash
cd backend
source venv/bin/activate
python app/main.py

# Or use uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: **http://localhost:8000**
API documentation: **http://localhost:8000/docs**

#### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:3000**

### Option 2: Docker Compose (Production-like)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎨 Demo Guide for Customer Presentation

### Preparation Checklist

1. **Download Sample Drone Footage**
   ```bash
   # Place sample files in data/raw/
   # Recommended: 2-3 images and 1 short video (30-60 seconds)
   ```

2. **Test the System**
   ```bash
   cd scripts
   python test_detection.py
   ```

3. **Prepare Demo Script** (see below)

### Demo Flow (15-20 minutes)

#### Part 1: System Overview (3 mins)
- Show the landing page
- Explain the use case: wildlife monitoring from drones
- Highlight key features

#### Part 2: Image Detection (5 mins)
1. Navigate to Upload page
2. Upload a drone image with visible animals
3. Click "Analyze"
4. Show real-time detection results:
   - Bounding boxes around animals
   - Species classification
   - Confidence scores
5. Download JSON results
6. Explain grouping/clustering visualization

#### Part 3: Video Tracking (7 mins)
1. Upload a short video clip
2. Show processing progress
3. Display tracking results:
   - Each animal assigned unique ID
   - Tracking paths/trajectories
   - Frame-by-frame playback
4. Export tracking data

#### Part 4: GPS & Metadata (3 mins)
1. Upload image with GPS metadata
2. Show detection mapped on geographical view
3. Display metadata panel:
   - Coordinates
   - Altitude
   - Timestamp
4. Export georeferenced data

#### Part 5: Q&A and Technical Deep Dive (5 mins)
- Show API documentation
- Discuss accuracy metrics
- Explain scalability (AWS deployment)
- Answer customer questions

### Demo Tips
✅ Use high-quality drone footage with clear animal visibility
✅ Pre-load files to avoid upload delays
✅ Have backup samples ready
✅ Practice the flow beforehand
✅ Keep technical jargon minimal unless asked
✅ Focus on business value and ROI

---

## 📚 API Documentation

### Core Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model": "yolo11m",
  "device": "mps",
  "version": "1.0.0"
}
```

#### 2. Upload & Detect Image
```http
POST /api/detect/image
Content-Type: multipart/form-data

file: <image_file>
confidence: 0.25 (optional)
```

**Response:**
```json
{
  "success": true,
  "filename": "drone_image.jpg",
  "detections": [
    {
      "id": 1,
      "class": "deer",
      "confidence": 0.87,
      "bbox": [150, 200, 300, 400],
      "group_id": 1
    }
  ],
  "groups": [
    {
      "group_id": 1,
      "count": 3,
      "center": [225, 300]
    }
  ],
  "metadata": {
    "gps": {"lat": 37.7749, "lon": -122.4194},
    "altitude": 120.5,
    "timestamp": "2025-12-14T10:30:00Z"
  },
  "annotated_image_url": "/results/annotated_drone_image.jpg"
}
```

#### 3. Upload & Track Video
```http
POST /api/detect/video
Content-Type: multipart/form-data

file: <video_file>
confidence: 0.25 (optional)
fps: 5 (optional, frames to process per second)
```

**Response:**
```json
{
  "success": true,
  "filename": "drone_video.mp4",
  "total_frames": 300,
  "processed_frames": 150,
  "tracks": [
    {
      "track_id": 1,
      "class": "elephant",
      "first_frame": 10,
      "last_frame": 145,
      "trajectory": [[x1, y1], [x2, y2], ...]
    }
  ],
  "annotated_video_url": "/results/tracked_drone_video.mp4"
}
```

#### 4. Export Results
```http
GET /api/export/{job_id}?format=json|csv
```

#### 5. List Results
```http
GET /api/results
```

For complete API documentation, visit **http://localhost:8000/docs** when the backend is running.

---

## 🌐 Deployment

### AWS Deployment Architecture

#### Infrastructure Components:
- **ECS Fargate**: Container orchestration
- **S3**: File storage for uploads and results
- **CloudFront**: CDN for frontend
- **ALB**: Load balancing
- **RDS/DynamoDB**: Metadata storage (optional)
- **CloudWatch**: Logging and monitoring

#### Deployment Steps:

1. **Build Docker Images**
   ```bash
   docker build -t wildlife-backend:latest ./backend
   docker build -t wildlife-frontend:latest ./frontend
   ```

2. **Push to ECR**
   ```bash
   aws ecr create-repository --repository-name wildlife-backend
   aws ecr create-repository --repository-name wildlife-frontend
   
   # Tag and push
   docker tag wildlife-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/wildlife-backend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/wildlife-backend:latest
   ```

3. **Deploy with Terraform/CloudFormation** (create IaC scripts)

4. **Configure Environment Variables** in ECS Task Definitions

---

## 📊 Performance Optimization

### Mac M4 Optimization:
- ✅ Metal Performance Shaders (MPS) enabled
- ✅ Batch processing for multiple images
- ✅ Async video processing
- ✅ Optimized model size (yolo11m recommended)

### Expected Performance:
- **Image Detection**: ~200-300ms per image
- **Video Tracking**: ~5-10 FPS processing speed
- **Memory Usage**: ~4-6GB during inference

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🆘 Troubleshooting

### Issue: YOLO model not found
**Solution**: Run `python scripts/download_models.py`

### Issue: MPS not available on Mac
**Solution**: Update PyTorch to latest version, set `DEVICE=cpu` in `.env`

### Issue: Frontend can't connect to backend
**Solution**: Check CORS settings, ensure backend is running on port 8000

### Issue: Out of memory during video processing
**Solution**: Reduce batch size, process fewer frames per second

---

## 📞 Support

For questions or issues:
- Create a GitHub Issue
- Email: support@example.com

---

**Built with ❤️ using YOLO11, Next.js, and FastAPI**

