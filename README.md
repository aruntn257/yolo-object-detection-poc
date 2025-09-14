# YOLO Object Detection API

A FastAPI-based REST API for object detection using YOLO (You Only Look Once) models. This project provides endpoints to upload images and detect objects in them using pre-trained YOLO models.

## Features

- Upload single or multiple images
- Object detection using YOLOv8 nano model
- Brand detection (for bottles)
- Save detection results as images and JSON
- Retrieve uploaded images
- List all available images

## Project Structure

```
├── DockerFile                # Docker configuration for deployment
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── images/                   # Sample images for testing
├── model/                    # YOLO model files
│   ├── yolo11n.pt            # YOLOv8 nano model
│   ├── train_model.py        # Script for training models
│   └── data_set/             # Training dataset
├── object_detection/         # Object detection modules
│   └── detect_img.py         # Detection functionality
├── results/                  # Storage for detection results
├── uploaded_images/          # Storage for uploaded images
└── utils/                    # Utility functions
    ├── const_file.py         # Constants and configurations
    ├── file_handler.py       # File handling utilities
    └── image_handler.py      # Image processing utilities
```

## Detection Capabilities

The current version can detect the following objects:
1. Cars
2. Bikes
3. Bicycles
4. Bottles (with additional brand detection)

## Installation

### Prerequisites

- Python 3.12
- Virtual environment (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aruntn257/yolo-object-detection-poc.git
   cd yolo-object-detection-poc
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv yolo-venv
   # On Windows:
   yolo-venv\Scripts\Activate.ps1
   # On Linux/Mac:
   source yolo-venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at http://localhost:8000

## Docker Deployment

You can also run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t yolo-detection-api -f DockerFile .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 yolo-detection-api
   ```

## Training Custom YOLO Models

The project includes functionality to train custom YOLO models for specific object detection tasks.

### Training Prerequisites

- Python 3.12 or later
- Ultralytics package installed (pip install ultralytics)
- Training dataset organized in YOLO format
- GPU with CUDA support (recommended for faster training)

### Dataset Structure

The dataset should be organized as follows within the 'model' folder:

```
model/
├── train_model.py          # Training script
├── data_set/
│   ├── data.yaml           # Dataset configuration file
│   ├── train/
│   │   ├── images/         # Training images
│   │   └── labels/         # Training labels in YOLO format
│   ├── valid/
│   │   ├── images/         # Validation images
│   │   └── labels/         # Validation labels in YOLO format
│   └── test/
│       ├── images/         # Test images
│       └── labels/         # Test labels in YOLO format
```

### Model Training Steps

1. Activate your Python environment:
   ```bash
   # Windows
   yolo-venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source yolo-venv/bin/activate
   ```

2. Navigate to the model directory:
   ```bash
   cd model
   ```


3. Run the training script:
   ```bash
   python train_model.py
   ```


6. After training completes, your model will be saved in:
   ```
   model/runs/detect/train/weights/
   ├── best.pt              # Best weights according to validation metrics
   └── last.pt              # Final weights after training
   ```

7. To use your new model, update the model path in utils/const_file.py:
   ```python
   OBJECT_DETECTION_MODEL_PATH = r"model/runs/detect/train/weights/best.pt"
   ```


## Example Usage

### Object Detection

```python
import requests

# API endpoint
url = "http://localhost:8000/detect_img/"

# Image file to upload
files = {"file": ("car.jpg", open("path/to/car.jpg", "rb"), "image/jpeg")}

# Make the request
response = requests.post(url, files=files)

# Print the detection results
print(response.json())
```

Example response:
```json
{
  "image_detected": ["car"],
  "confidence_score": [0.92]
}
```

## Development

The project is organized following best practices for FastAPI applications:
- Core functionality is separated into modules
- Constants are centralized in a single file
- Error handling with proper HTTP status codes
- Type annotations for better IDE support and documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project uses [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for object detection
- Built with [FastAPI](https://fastapi.tiangolo.com/)