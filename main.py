from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
from object_detection.detect_img import detect_img, detect_brand
from utils.image_handler import ImageHandler
from utils.const_file import UPLOAD_DIR, ALLOWED_EXTENSIONS,RESULTS_DIR

# Create the FastAPI app
app = FastAPI(
    title="Image Upload API",
    description="A simple API to upload and store images locally",
    version="1.0.0"
)

# Create the upload directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


def is_valid_image(filename: str) -> bool:
    """Check if the uploaded file has a valid image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/")
def read_root():
    """Root endpoint that displays API information."""
    try:
        return {"message": "Image Upload API is running", 
                "endpoints": {
                    "POST /upload/": "Upload a single image",
                    "POST /upload/batch/": "Upload multiple images",
                    "GET /images/{image_name}": "Retrieve a specific image",
                    "GET /images/": "List all available images"
                }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/detect_img/")
async def detect_image_route(file: UploadFile = File(...)):
    """
    This app is in development stage. As of now detects only below Images:
    1. Car
    2. Bike
    3. Bicycle
    4. Bottle
    Give a clear picture of these objects for better results.
    """
    try:
        # Validate that the file is an image
        if not is_valid_image(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"File must be an image ({', '.join(ALLOWED_EXTENSIONS)})"
            )
        
        # Create file handler and save the file (without auto-delete)
        file_handler = ImageHandler(file)
        file_path = file_handler.save_image()
        
        try:
            # Run detection on the saved image
            result = detect_img(file_path)
            return result
        finally:
            # Delete the file after detect_img completes (whether it succeeds or fails)
            file_handler.delete_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

@app.post("/detect_img_brand/")
async def detect_image_brand_route(file: UploadFile = File(...)):
    """
    This app is in development stage. As of now detects only "pepsi" brand Images:
    Give a clear picture of these objects for better results.
    """
    try:
        # Validate that the file is an image
        if not is_valid_image(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"File must be an image ({', '.join(ALLOWED_EXTENSIONS)})"
            )
        
        # Create file handler and save the file (without auto-delete)
        file_handler = ImageHandler(file)
        file_path = file_handler.save_image()
        
        try:
            # Run object detection
            img_result = detect_img(file_path)
            
            # Run brand detection with the object detection result
            brand_result = detect_brand(img_result, file_path)
            return brand_result
        finally:
            # Delete the file after all detection operations complete
            file_handler.delete_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)