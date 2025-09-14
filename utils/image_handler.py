
import shutil
import os
from datetime import datetime
import uuid
from pathlib import Path
from fastapi import UploadFile
from utils.const_file import UPLOAD_DIR

class ImageHandler:

    def __init__(self, file=None):
        self.file = file
        self.file_path = None
        self.filename = None
        
    def generate_img_name(self):
        """Generate a unique filename for an uploaded image."""
        if not self.file:
            raise ValueError("No file provided")
            
        # Generate a unique filename to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        extension = self.file.filename.rsplit(".", 1)[1].lower()
        
        # Store the generated filename as an instance variable
        self.filename = f"{timestamp}_{unique_id}.{extension}"
        return self.filename

    def save_image(self, file: UploadFile = None):
        """Save an uploaded image to the upload directory with a unique name."""
        if file:
            self.file = file
            
        if not self.file:
            raise ValueError("No file provided")
        
        # Generate a unique filename
        if not self.filename:
            self.generate_img_name()
        
        # Set the file path as an instance variable
        self.file_path = UPLOAD_DIR / self.filename
        
        # Save the file
        with open(self.file_path, "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)
        
        return self.file_path
        
    def delete_image(self, file_path=None):
        """Delete a file from the filesystem."""
        # Use the provided file_path or the instance file_path
        path_to_delete = file_path if file_path else self.file_path
        
        if path_to_delete and os.path.exists(path_to_delete):
            os.remove(path_to_delete)
            # Clear the file_path if we're deleting the instance file
            if path_to_delete == self.file_path:
                self.file_path = None
            return True
        return False
        
    def exists(self):
        """Check if the file exists on the filesystem."""
        return self.file_path and os.path.exists(self.file_path)
        
    def get_file_size(self):
        """Get the size of the file in bytes."""
        if self.exists():
            return os.path.getsize(self.file_path)
        return 0
        
    def get_extension(self):
        """Get the file extension."""
        if self.filename:
            return self.filename.rsplit(".", 1)[1].lower() if "." in self.filename else ""
        return ""
        
    def process_file(self, file: UploadFile = None, auto_delete=False):
        """
        Process a file through the entire workflow: save, return path, and optionally delete.
        
        Args:
            file: The file to process. If None, uses the instance file.
            auto_delete: If True, deletes the file after returning its path.
            
        Returns:
            Path to the saved file (which may have been deleted if auto_delete=True)
        """
        # Save the file
        file_path = self.save_file(file)
        
        # Get a copy of the path before potentially deleting the file
        path_copy = Path(file_path)
        
        # Delete if requested
        if auto_delete:
            self.delete_file()
            
        return path_copy