"""
Constants file for the FastAPI application.
This file contains all the constants used across the application.
"""
from pathlib import Path

# Upload directory configuration
UPLOAD_DIR = Path("uploaded_images")
RESULTS_DIR = Path("results")

# Define allowed image extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}

# Model paths
OBJECT_DETECTION_MODEL_PATH = r"model/yolo11n.pt"
BRAND_DETECTION_MODEL_PATH = r"model/runs/detect/train2/weights/last.pt"