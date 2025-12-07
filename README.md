# Water Body Instance Segmentation API

A FastAPI-based for detecting and segmenting water bodies in images using machine learning. The API accepts image uploads, performs instance segmentation, and returns detailed predictions including bounding boxes and polygon coordinates.

## Features

- 🌊 **Water Body Detection**: Accurate instance segmentation of water bodies in images
- 📤 **Multi-Image Upload**: Process single or multiple images in one request
- ✅ **Input Validation**: File type and size validation
- 🔒 **Type Safety**: Full Pydantic schema validation
- 🚀 **Fast Processing**: Async file handling for optimal performance
- 📊 **Detailed Output**: Returns bounding boxes, confidence scores, and segmentation polygons

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Response Schema](#response-schema)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Omar9965/Instance-Segmentation-for-Water-bodies
cd Instance-Segmentation-for-Water-bodies
```

2. **Create and activate virtual environment**
```bash
python -m venv water
source water/bin/activate  # On Windows: water\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```env
MODEL_API_URL=your-model-id
API_KEY=your-roboflow-api-key
```

## Configuration

The application uses environment variables for configuration. Key settings include:

 API
- Maximum file size: 500 MB (configurable in `models/responses.py`)
- Allowed file types: JPG, PNG, TIFF, JPEG

## Usage

### Starting the Server
```bash
cd src
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once the server is running, access:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Health Check
```http
GET /
```
Returns API status.

**Response:**
```json
{
  "message": "app_name" : "Water Segmentation API"
              "status": "running",
              "version": "0.1.0"
}
```

### Upload and Segment Images
```http
POST /api/v1/upload-and-segment
```

Upload one or more images for water body segmentation.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `files` (one or more image files)

**Supported Formats:** JPG, PNG, TIFF, JPEG  
**Max File Size:** 500 MB per file

**Response:** See [Response Schema](#response-schema)

### Upload Images Only
```http
POST /api/v1/upload
```

Upload images without processing (validation only).

**Response:**
```json
{
  "message": "File was Uploaded Successfully",
  "files": ["filename1.jpg", "filename2.png"],
  "count": 2
}
```

## Response Schema

### Successful Segmentation Response
```json
{
  "predictions": [
    {
      "x": 203.5,
      "y": 255.0,
      "width": 349.0,
      "height": 378.0,
      "confidence": 0.946,
      "class": "water",
      "class_id": 0,
      "detection_id": "d49f9e48-234e-4841-88a8-1adce38883e5",
      "points": [
        {"x": 195.0, "y": 66.572},
        {"x": 194.391, "y": 67.394},
        ...
      ]
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `x` | float | Center X coordinate of bounding box |
| `y` | float | Center Y coordinate of bounding box |
| `width` | float | Width of bounding box |
| `height` | float | Height of bounding box |
| `confidence` | float | Prediction confidence score (0-1) |
| `class` | string | Object class name |
# Instance Segmentation for Water Bodies

Lightweight FastAPI application that performs instance segmentation to detect and visualize water bodies in images using a YOLO model. This repository contains the backend API, a small frontend (static files + template) to upload images and preview segmentation, and the YOLO model artifact.

TL;DR — run the server, open http://127.0.0.1:8000 and use the web UI or POST images to the API.

## What changed (summary)
- Separated inference and visualization: `src/models/YOLO_Model/inference_yolo.py` (model prediction) and `src/models/YOLO_Model/visualize.py` (mask rendering)
- Simple web frontend in `src/templates/index.html` + `src/static/style.css`, `src/static/script.js` for upload and preview
- Main segmentation endpoint: `POST /api/v1/segment-image` (returns processed PNG image)
- Model binary stored in: `src/models/YOLO_Model/best_model.pt`

## Quickstart (Windows PowerShell)
1. Create & activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Start the app (from project root)

```powershell
cd src
python -m uvicorn main:app --reload
```

4. Open the UI in your browser:

- http://127.0.0.1:8000 (web interface)
- API docs: http://127.0.0.1:8000/docs

## Important files & locations
- `src/main.py` — FastAPI app and static/template mounting
- `src/routes/data.py` — upload & segmentation endpoints
- `src/models/YOLO_Model/inference_yolo.py` — runs YOLO `model.predict(...)`
- `src/models/YOLO_Model/visualize.py` — renders masks/overlays for output images
- `src/models/YOLO_Model/best_model.pt` — model weights (tracked here for local testing)
- `src/templates/index.html` — web UI template
- `src/static/style.css`, `src/static/script.js` — frontend styles and JS

## Endpoints
- `GET /` — serves the web UI
- `POST /api/v1/segment-image` — upload one image (multipart/form-data `file`) and receive a rendered PNG image with water masks applied (FileResponse)
- `POST /api/v1/upload-and-segment` — (legacy / JSON) endpoint that returns structured prediction JSON (if present)

Example using `curl` (upload + receive image):

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/segment-image" -F "file=@path/to/image.jpg" --output segmented.png
```

Example using Python `requests`:

```python
import requests

with open('image.jpg', 'rb') as f:
    r = requests.post('http://127.0.0.1:8000/api/v1/segment-image', files={'file': f})
    with open('segmented.png', 'wb') as out:
        out.write(r.content)
```

## Frontend behavior
- The UI (`/`) allows drag-and-drop or click-to-upload. After selecting a file the UI sends it to `/api/v1/segment-image` and displays the original and processed images side-by-side.

## Configuration and environment
- By default the app looks for local model weights at `src/models/YOLO_Model/best_model.pt`. If you use a different path, update the model loader in `inference_yolo.py`.
- Optional environment variables (in `.env`) are used by `src/utils/configs.py` — review that file if you need to expose additional runtime settings.

## Troubleshooting
- 422 Unprocessable Entity on upload: make sure you send multipart/form-data and the form field is named `file` (for `/api/v1/segment-image`) or `files` for the multi-file endpoint.
- Model not found: confirm `best_model.pt` exists in `src/models/YOLO_Model/`
- If the frontend doesn't load styles/scripts, verify the static files are in `src/static/` and `src/main.py` mounts the static folder.


