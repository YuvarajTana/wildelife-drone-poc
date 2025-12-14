# 🦌 Wildlife Detection & Tracking from Drone Footage

AI-powered wildlife detection and tracking system using **YOLO11** and **Next.js**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![YOLO](https://img.shields.io/badge/YOLO-11-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd wildlife-drone-poc
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download YOLO11 model
cd ..
python scripts/download_models.py

# Copy environment file
cp .env.example backend/.env

# Start backend server
cd backend
python app/main.py
```

Backend runs at: **http://localhost:8000**

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

### 4. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 📋 Features

✅ **Image Detection** - Detect animals in drone images with YOLO11  
✅ **Video Tracking** - Track animals across video frames with ByteTrack  
✅ **Group Analysis** - Identify herds using spatial clustering  
✅ **GPS Tagging** - Extract and display GPS metadata  
✅ **Modern UI** - Beautiful Next.js interface with TypeScript  
✅ **RESTful API** - FastAPI backend with full documentation  
✅ **Apple Silicon Optimized** - MPS acceleration for M-series Macs  

## 🛠 Tech Stack

**Backend:**
- Python 3.11, FastAPI, Ultralytics YOLO11
- PyTorch with MPS/CUDA support
- OpenCV, ByteTrack, Scikit-learn

**Frontend:**
- Next.js 14, React 18, TypeScript
- Tailwind CSS, React Query, Axios

## 📁 Project Structure

```
wildlife-drone-poc/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # Main application
│   │   ├── models/      # YOLO11 detector & grouping
│   │   └── services/    # Image & video processing
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages & routes
│   │   ├── components/ # React components
│   │   └── lib/        # API client
│   └── package.json
├── data/               # Upload & results
├── scripts/            # Helper scripts
└── PROJECT_SETUP_GUIDE.md  # Detailed documentation
```

## 📖 Documentation

For detailed documentation, see [PROJECT_SETUP_GUIDE.md](PROJECT_SETUP_GUIDE.md)

- Installation & Setup
- Running the Application
- API Documentation
- Demo Guide for Customers
- Deployment Instructions

## 🎯 Usage

1. **Upload**: Navigate to Upload page and select image/video
2. **Process**: AI detects and tracks animals automatically
3. **View**: See annotated results with bounding boxes
4. **Export**: Download JSON/CSV with detection data

## 🧪 Testing

Test the detection system:

```bash
python scripts/test_detection.py
```

## 🌐 API Endpoints

- `GET /health` - Health check
- `POST /api/detect/image` - Detect animals in image
- `POST /api/detect/video` - Track animals in video
- `GET /api/results` - List all results
- `GET /docs` - Interactive API documentation

## 📊 Performance

- **Image Detection**: ~200-300ms per image
- **Video Tracking**: ~5-10 FPS processing speed
- **Memory**: ~4-6GB during inference
- **Device**: Optimized for Apple Silicon (MPS)

## 🚢 Deployment

Ready for AWS deployment:
- Docker & Docker Compose included
- AWS ECS/Fargate compatible
- S3 for file storage
- CloudFront for CDN

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please read contributing guidelines.

## 📞 Support

- Documentation: [PROJECT_SETUP_GUIDE.md](PROJECT_SETUP_GUIDE.md)
- Issues: GitHub Issues
- YOLO11 Docs: https://docs.ultralytics.com/

---

**Built with ❤️ using YOLO11, Next.js, and FastAPI**
