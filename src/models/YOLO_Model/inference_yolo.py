from inference import get_model
import supervision as sv
import cv2
import os
import sys
from typing import List, Union

abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(os.path.join(abs_path, "src"))

from utils import get_settings, Settings

settings: Settings = get_settings()

MODEL_API_URL = settings.MODEL_API_URL
API_KEY = settings.API_KEY


def segment_water(image_paths: Union[str, List[str]], display: bool = True) -> Union[cv2.Mat, List[cv2.Mat]]:
    """
    Perform instance segmentation on water bodies in one or more images.
    
    Args:
        image_paths: Single image path (str) or list of image paths
        display: Whether to display the annotated images (default: True)
    
    Returns:
        Single annotated image or list of annotated images
    """
    # Convert single image path to list for uniform processing
    single_image = isinstance(image_paths, str)
    if single_image:
        image_paths = [image_paths]
    
    # Load the model once
    model = get_model(model_id=MODEL_API_URL, api_key=API_KEY)
    
    # Create annotators once
    mask_annotator = sv.MaskAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    annotated_images = []
    
    for image_path in image_paths:
        # Load image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Warning: Could not read image at {image_path}")
            continue
        
        # Run inference
        results = model.infer(image)[0]
        
        # Load results into supervision Detections
        detections = sv.Detections.from_inference(results)
        
        print(f"\nImage: {os.path.basename(image_path)}")
        print(f"Number of detections: {len(detections)}")
        
        # Annotate the image with segmentation masks
        annotated_image = mask_annotator.annotate(
            scene=image.copy(), detections=detections)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detections)
        
        annotated_images.append(annotated_image)
        
        # Display if requested
        if display:
            sv.plot_image(annotated_image)
    
    # Return single image or list based on input
    return annotated_images[0] if single_image else annotated_images

