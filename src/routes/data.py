from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from controllers import DataController
from routes import MultipleImagesResponse
from models import segment_water  

router = APIRouter(prefix="/api/v1", tags=["water-segmentation"])

# Initialize controller
data_controller = DataController()

@router.post("/upload-and-segment", response_model=MultipleImagesResponse)
async def upload_and_segment_water(files: List[UploadFile] = File(...)):
    """
    Upload one or more images and perform water segmentation.
    
    Args:
        files: List of image files (jpg, png, tiff, jpeg)
        
    Returns:
        DataSchema with predictions for all water bodies detected
    """
    is_valid, message = await data_controller.validate_images(files)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    temp_paths = []
    
    try:
        # Ensure upload directory exists
        os.makedirs(data_controller.file_dir, exist_ok=True)
        
        # Save uploaded files temporarily
        for file in files:
            random_string = data_controller.generate_random_string()
            ext = file.filename.split('.')[-1].lower()
            temp_filename = f"{random_string}.{ext}"
            temp_path = os.path.join(data_controller.file_dir, temp_filename)
            
            # Save file
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            temp_paths.append(temp_path)
        
        # Run segmentation on all uploaded images
        result = segment_water(temp_paths, display=False)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Segmentation failed: {str(e)}"
        )
    
    finally:
        # Cleanup temporary files
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Failed to remove temp file {temp_path}: {str(e)}")

