# 🦌 Wildlife Detection & Tracking from Drone Footage -- Local PoC

## Objective

Build a **local Proof of Concept (PoC)** to analyze **drone-captured
images and videos** over forests/jungles and:

-   Detect animals in each frame
-   Identify animal **groups/herds**
-   Track animals across video frames
-   Associate detections with **approximate location**
-   Present results via a **simple demo UI**

This PoC runs **fully on a local Mac (Apple Silicon M4, 48GB RAM)** and
is designed to be **AWS-ready** later.

------------------------------------------------------------------------

## What This PoC Will Demonstrate (Demo Scope)

### Inputs

-   Drone images (`.jpg`, `.png`)
-   Drone videos (`.mp4`)
-   Optional metadata:
    -   GPS (lat, lon)
    -   Altitude
    -   Timestamp (from EXIF / logs)

### Outputs

-   Bounding boxes around detected animals
-   Species / category (animal, human, vehicle → species if available)
-   Confidence score
-   Group/herd identification
-   Tracking across frames (for videos)
-   Approximate location per detection
-   Visual demo + JSON output

------------------------------------------------------------------------

## High-Level Architecture (Local)

Drone Image / Video\
→ Frame Extraction (for video)\
→ Animal Detection Model (YOLO / MegaDetector)\
→ Tracking (ByteTrack / DeepSORT)\
→ Grouping (Spatial Clustering)\
→ Location Tagging (Drone GPS)\
→ Results (JSON + Visual Overlay)\
→ Demo UI (Streamlit)

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python 3.11
-   PyTorch (Metal / MPS backend on Mac)
-   YOLOv8 or MegaDetector
-   OpenCV
-   FastAPI (optional)
-   Scikit-learn

### UI

-   Streamlit

------------------------------------------------------------------------

## Project Structure

    wildlife-drone-poc/
    ├── backend/
    │   ├── app/
    │   ├── requirements.txt
    │   └── run_local.py
    ├── ui/
    │   └── streamlit_app.py
    ├── data/
    │   ├── raw/
    │   ├── frames/
    │   └── results/
    ├── docker/
    └── README.md

------------------------------------------------------------------------

## Local Environment Setup

``` bash
python3.11 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install torch torchvision torchaudio
pip install ultralytics opencv-python fastapi uvicorn streamlit
pip install numpy pandas scikit-learn pillow exifread
```

------------------------------------------------------------------------

## Phase-wise Implementation

### Phase 1 -- Image Detection

-   Upload image
-   Detect animals
-   Draw bounding boxes
-   Export JSON

### Phase 2 -- Grouping

-   Cluster animals spatially
-   Identify herds/groups

### Phase 3 -- Video Tracking

-   Extract frames
-   Detect per frame
-   Track across frames

### Phase 4 -- Location Tagging

-   Attach drone GPS + timestamp
-   Map detections approximately

------------------------------------------------------------------------

## Demo Using Streamlit

``` bash
streamlit run ui/streamlit_app.py
```

------------------------------------------------------------------------

## Success Criteria

-   Runs locally on Mac M4
-   Detects animals accurately
-   Shows grouping & tracking
-   Produces visual + JSON output
-   Clearly AWS-ready

------------------------------------------------------------------------

## Next Steps

-   Species-level classifier
-   Thermal imagery support
-   Orthomosaic map projection
-   AWS ECS / S3 deployment
