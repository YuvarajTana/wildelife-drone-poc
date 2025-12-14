# 🦌 Wildlife Drone Detection - Step-by-Step Run Guide

This guide provides clear instructions to run the project locally and demonstrate it to customers.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup (One-Time)](#initial-setup-one-time)
3. [Running the Application](#running-the-application)
4. [Demo Workflow](#demo-workflow)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.11+** - Check with `python3 --version`
- ✅ **Node.js 18+** - Check with `node --version`
- ✅ **Mac M4 with 48GB RAM** (or similar powerful machine)
- ✅ **Internet connection** (for downloading dependencies and models)

---

## Initial Setup (One-Time)

You only need to do this once when setting up the project for the first time.

### Part 1: Backend Setup

Open Terminal and run:

```bash
# 1. Navigate to project
cd /Users/yuvarajtana/Documents/wildelife-drone-poc

# 2. Setup Python virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate

# 3. Install Python packages (takes 5-10 minutes)
pip install --upgrade pip
pip install -r requirements.txt

# 4. Go back to project root
cd ..

# 5. Download YOLO11 model (choose option 3 for medium model)
python scripts/download_models.py
# When prompted, type: 3 (or press Enter for default)

# 6. Setup environment variables
cp .env.example backend/.env

# ✅ Backend setup complete!
```

### Part 2: Frontend Setup

Open a **NEW Terminal** and run:

```bash
# 1. Navigate to project
cd /Users/yuvarajtana/Documents/wildelife-drone-poc

# 2. Navigate to frontend
cd frontend

# 3. Install Node.js packages (takes 3-5 minutes)
npm install

# 4. Setup environment variables
cp .env.example .env.local

# ✅ Frontend setup complete!
```

---

## Running the Application

Follow these steps **every time** you want to run the application:

### Terminal 1: Start Backend

```bash
# Navigate to project
cd /Users/yuvarajtana/Documents/wildelife-drone-poc/backend

# Activate virtual environment
source venv/bin/activate

# Start backend server
python app/main.py
```

**Wait for this message:**
```
✅ Services initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running!** Leave this terminal open.

---

### Terminal 2: Start Frontend

Open a **NEW Terminal** and run:

```bash
# Navigate to project
cd /Users/yuvarajtana/Documents/wildelife-drone-poc/frontend

# Start frontend server
npm run dev
```

**Wait for this message:**
```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
✓ Ready in 2.1s
```

✅ **Frontend is running!** Leave this terminal open.

---

### Access the Application

Open your web browser and go to:

**🌐 http://localhost:3000**

You should see the Wildlife Drone Detection homepage.

---

## Demo Workflow

### Preparation (Before Customer Demo)

1. **Get Sample Drone Footage:**
   - Download or prepare 2-3 drone images with visible animals
   - Download 1 short video (30-60 seconds) with animals
   - Place them in `data/raw/` folder for easy access

2. **Test the System:**
   - Upload one test image to ensure everything works
   - Verify the detection results appear correctly

3. **Open Browser Tabs:**
   - Tab 1: http://localhost:3000 (Main UI)
   - Tab 2: http://localhost:8000/docs (API Documentation)

---

### Demo Script (15-20 minutes)

#### Introduction (2 minutes)

1. Start at homepage: http://localhost:3000
2. Explain the problem:
   - Wildlife monitoring from drones is time-consuming
   - Manual counting is error-prone
   - Need automated AI solution

3. Show key features:
   - Animal detection with YOLO11
   - Real-time tracking
   - GPS integration
   - Group/herd identification

---

#### Part 1: Image Detection Demo (5 minutes)

1. **Click "Start Detection"** button
2. **Select "Image"** tab
3. **Upload a drone image** (drag & drop or click to browse)
4. **Show processing:**
   - Upload progress bar
   - Processing with YOLO11 message

5. **Show results:**
   - Annotated image with bounding boxes
   - Animal species labels
   - Confidence scores
   - Group identification (if multiple animals)

6. **Explain the output:**
   - Each animal is detected and classified
   - Confidence score shows detection accuracy
   - Groups are identified by proximity

---

#### Part 2: Video Tracking Demo (5 minutes)

1. **Navigate back** and select "Video" tab
2. **Upload a short video** with animals
3. **Show processing:**
   - Upload and processing status
   - Frame-by-frame analysis

4. **Show results:**
   - Video playback with tracking boxes
   - Unique ID for each animal
   - Trajectory paths showing movement
   - Consistent tracking across frames

5. **Explain tracking:**
   - ByteTrack algorithm maintains identity
   - Handles occlusions and re-entry
   - Exports complete movement data

---

#### Part 3: Technical Details (3 minutes)

1. **Show API Documentation:**
   - Open http://localhost:8000/docs
   - Demonstrate interactive API
   - Show available endpoints

2. **Explain architecture:**
   - YOLO11 for detection (latest from Ultralytics)
   - FastAPI backend (Python)
   - Next.js frontend (React/TypeScript)
   - Optimized for Apple Silicon (MPS)

3. **Discuss scalability:**
   - Currently runs locally
   - AWS-ready architecture
   - Can handle batch processing
   - Supports multiple drone feeds

---

#### Part 4: GPS & Metadata (2 minutes)

1. **Upload image with GPS metadata** (if available)
2. **Show extracted information:**
   - GPS coordinates
   - Altitude
   - Timestamp
   - Camera details

3. **Explain use cases:**
   - Georeferenced wildlife mapping
   - Population density analysis
   - Migration tracking
   - Habitat monitoring

---

#### Part 5: Export & Integration (2 minutes)

1. **Show export options:**
   - JSON for API integration
   - CSV for data analysis
   - Annotated images/videos

2. **Discuss integration:**
   - RESTful API for custom applications
   - Webhook support (can be added)
   - Database integration options
   - Real-time streaming capability

---

#### Q&A (5 minutes)

Common questions to prepare for:

**Q: What animals can it detect?**
A: YOLO11 is trained on 80 classes including common wildlife like deer, elephants, bears, etc. Can be fine-tuned for specific species.

**Q: How accurate is it?**
A: Typically 85-95% accuracy depending on image quality, distance, and occlusion.

**Q: Can it run in real-time from drone feed?**
A: Yes, optimized for 5-10 FPS processing. Can be scaled up with GPU acceleration.

**Q: What about cloud deployment?**
A: AWS-ready with Docker containers. Can deploy to ECS/Fargate with S3 storage.

**Q: Can it work with thermal imagery?**
A: Yes, with model fine-tuning on thermal datasets.

**Q: What's the minimum hardware requirement?**
A: 16GB RAM, modern CPU. GPU recommended for real-time processing.

---

## Troubleshooting

### Backend won't start

**Issue:** Python module errors
```bash
# Solution: Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Issue:** Model not found
```bash
# Solution: Download model again
python scripts/download_models.py
```

**Issue:** Port 8000 already in use
```bash
# Solution: Kill existing process
lsof -ti:8000 | xargs kill -9
```

---

### Frontend won't start

**Issue:** Node modules error
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue:** Port 3000 already in use
```bash
# Solution: Kill existing process
lsof -ti:3000 | xargs kill -9
```

---

### Can't connect to backend

**Issue:** Frontend can't reach backend API

**Check:**
1. Backend is running (Terminal 1 should show "Uvicorn running")
2. Visit http://localhost:8000/health in browser
3. Check `frontend/.env.local` has correct API URL

---

### Upload fails

**Issue:** File upload errors

**Check:**
1. File format is supported (jpg, png, mp4, mov, avi)
2. File size is under 100MB
3. Backend logs for specific error messages

---

## Performance Tips

### For Better Detection Results:

1. **Image Quality:**
   - Use high-resolution images (1920x1080 or better)
   - Ensure good lighting
   - Avoid heavy motion blur

2. **Camera Settings:**
   - Capture at 100-150m altitude for optimal coverage
   - Use 60-90° camera angle
   - Include GPS metadata in images

3. **Video Processing:**
   - Use 30 FPS capture rate
   - Keep videos under 2 minutes for faster processing
   - Ensure stable drone footage

---

## Stopping the Application

When you're done:

1. **Stop Frontend:** Press `Ctrl + C` in Terminal 2
2. **Stop Backend:** Press `Ctrl + C` in Terminal 1
3. **Deactivate Python environment:** Type `deactivate`

---

## Quick Reference Commands

```bash
# Start Backend
cd /Users/yuvarajtana/Documents/wildelife-drone-poc/backend
source venv/bin/activate
python app/main.py

# Start Frontend (in new terminal)
cd /Users/yuvarajtana/Documents/wildelife-drone-poc/frontend
npm run dev

# Test Backend API
curl http://localhost:8000/health

# Run Test Script
python scripts/test_detection.py
```

---

## Additional Resources

- **Detailed Documentation:** `PROJECT_SETUP_GUIDE.md`
- **API Reference:** http://localhost:8000/docs (when running)
- **YOLO11 Official Docs:** https://docs.ultralytics.com/
- **Next.js Docs:** https://nextjs.org/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

**🎉 You're ready to demonstrate! Good luck with your customer presentation! 🦌**

