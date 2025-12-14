# 🚀 Quick Setup Instructions

Follow these steps to get the Wildlife Drone Detection system running on your local machine.

## Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] Node.js 18.x or higher installed
- [ ] Git installed
- [ ] At least 16GB RAM (48GB recommended)
- [ ] Apple Silicon Mac (M4) or machine with CUDA GPU (optional, but recommended)

---

## Step-by-Step Setup

### Step 1: Navigate to Project Directory

```bash
cd /Users/yuvarajtana/Documents/wildelife-drone-poc
```

### Step 2: Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create Python virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies (this may take 5-10 minutes)
pip install -r requirements.txt

# Navigate back to root
cd ..

# Download YOLO11 model (choose option 3 for medium model)
python scripts/download_models.py

# Create .env file from example
cp .env.example backend/.env

# Verify the .env file (optional)
cat backend/.env
```

### Step 3: Create Data Directories

```bash
# Create necessary directories for uploads and results
mkdir -p data/raw
mkdir -p data/frames
mkdir -p data/processed
mkdir -p data/results
mkdir -p backend/weights
```

### Step 4: Start Backend Server (Terminal 1)

```bash
cd backend
source venv/bin/activate
python app/main.py
```

**Expected Output:**
```
🚀 Starting Wildlife Detection API...
📊 Model: weights/yolo11m.pt
💻 Device: mps
✅ Services initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Backend is now running at http://localhost:8000**

Keep this terminal running and open a new terminal for the frontend.

---

### Step 5: Frontend Setup (Terminal 2 - New Terminal)

```bash
# Navigate to project directory
cd /Users/yuvarajtana/Documents/wildelife-drone-poc

# Navigate to frontend
cd frontend

# Install Node.js dependencies (this may take 3-5 minutes)
npm install

# Create .env.local file
cp .env.example .env.local

# Verify the .env.local file (optional)
cat .env.local
```

### Step 6: Start Frontend Server (Terminal 2)

```bash
npm run dev
```

**Expected Output:**
```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
- Ready in 2.1s
```

**✅ Frontend is now running at http://localhost:3000**

---

## Step 7: Access the Application

Open your web browser and navigate to:

**🌐 http://localhost:3000**

You should see the Wildlife Drone Detection homepage.

---

## Testing the Setup

### Option 1: Quick Health Check

Open a new terminal and run:

```bash
# Test backend API
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model": "yolo11m.pt",
  "device": "mps",
  "version": "1.0.0"
}
```

### Option 2: Run Test Script

```bash
cd /Users/yuvarajtana/Documents/wildelife-drone-poc
python scripts/test_detection.py
```

---

## Common Issues & Solutions

### Issue 1: Python not found
**Solution:** Install Python 3.11 from https://www.python.org/downloads/

### Issue 2: Node.js not found
**Solution:** Install Node.js from https://nodejs.org/

### Issue 3: Port 8000 or 3000 already in use
**Solution:** 
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9
```

### Issue 4: MPS not available (Mac)
**Solution:** In `backend/.env`, change:
```
DEVICE=cpu
```

### Issue 5: Module not found errors
**Solution:** Make sure virtual environment is activated:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

## Next Steps

1. **Upload Test Image/Video:**
   - Navigate to http://localhost:3000/upload
   - Upload a drone image or video
   - View detection results

2. **View API Documentation:**
   - Open http://localhost:8000/docs
   - Explore interactive API documentation

3. **Prepare for Demo:**
   - Place sample drone footage in `data/raw/`
   - Practice the upload and detection workflow
   - Review results visualization

---

## Stopping the Servers

To stop the servers, press `Ctrl + C` in each terminal where the servers are running.

To deactivate the Python virtual environment:
```bash
deactivate
```

---

## Getting Help

- **Detailed Documentation:** See `PROJECT_SETUP_GUIDE.md`
- **API Reference:** http://localhost:8000/docs (when backend is running)
- **YOLO11 Documentation:** https://docs.ultralytics.com/

---

**🎉 You're all set! Happy wildlife detecting! 🦌**

