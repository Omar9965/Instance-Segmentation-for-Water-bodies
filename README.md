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

- `MODEL_API_URL`: Your Roboflow model endpoint
- `API_KEY`: Authentication key for the model API
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
| `class_id` | integer | Numeric class identifier |
| `detection_id` | string | Unique identifier for this detection |
| `points` | array | Polygon coordinates for segmentation mask |

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "File type is not supported. Types allowed are jpg, png, tiff, jpeg"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": "Field required"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Segmentation failed: <error message>"
}
```

## Examples

### Python Example
```python
import requests

# Single image
url = "http://127.0.0.1:8000/api/v1/upload-and-segment"
files = {"files": open("water_image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())

# Multiple images
files = [
    ("files", open("image1.jpg", "rb")),
    ("files", open("image2.png", "rb"))
]
response = requests.post(url, files=files)
print(response.json())
```

### cURL Example
```bash
# Single image
curl -X POST "http://127.0.0.1:8000/api/v1/upload-and-segment" \
  -F "files=@water_image.jpg"

# Multiple images
curl -X POST "http://127.0.0.1:8000/api/v1/upload-and-segment" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png"
```


### Health Check
```http
GET /
```
Returns API status.

**Response:**
```json
{
  "app_name": "Water Segmentation API",
  "status": "running",
  "version": "0.1.0"
}
```

...

## Project Structure
```text
src/
│
├── controllers/                     # Business logic and application controllers
│   ├── __init__.py
│   ├── BaseController.py
│   └── DataController.py
│
├── models/                          # Data models and ML model files
│   ├── enums/                       # Enumerations for constants or choices
│   ├── YOLO_Model/                  # YOLO model implementation
│   └── __init__.py
│
├── routes/                          # FastAPI route definitions
│   ├── schemas/                     # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── data.py
│   ├── __init__.py
│   ├── base.py                      # Base API routes
│   └── data.py                      # Data-specific endpoints
│
├── utils/                           # Utility and configuration helpers
│   ├── __init__.py
│   └── configs.py                   # Environment and settings management
│
├── main.py                          # Application entry point
├── .env                             # Environment variables (git-ignored)
├── .env.example                     # Example env file
├── requirements.txt                 # Project dependencies
├── README.md                        # Project documentation
└── .gitignore                       # Git ignore rules
```

...

