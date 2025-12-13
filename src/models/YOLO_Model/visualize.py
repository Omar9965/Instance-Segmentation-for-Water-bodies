import os
import cv2
import numpy as np
from typing import Optional
from utils import get_settings, Settings


settings: Settings = get_settings()

def visualize_water_segmentation(
    image_path: str,
    yolo_results,
    save_path: Optional[str] = None,
) -> str:
    """
    Visualize water body segmentation results on an image using pre-computed YOLO results.
    
    Args:
        image_path: Path to input image
        yolo_results: Pre-computed YOLO results from inference
        save_path: Optional path to save the result. If None, saves to temp location.
        
    Returns:
        Path to the saved segmented image
    """
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from {image_path}")
    
    # Build Supervision Detections from YOLO results
    masks = yolo_results.masks



    if masks is not None and len(masks) > 0:
        # masks.data shape: (N, H, W)
        mask_array = masks.data.cpu().numpy()
    else:
        mask_array = None



    annotated_image = image.copy()

    COLORS = [
        (255, 0, 0),      
        (0, 255, 0),      
        (0, 0, 255),      
        (255, 255, 0),   
        (255, 0, 255),  
        (0, 255, 255),   
        (128, 0, 255),    
        (255, 128, 0),   
        (0, 128, 255),    
        (128, 255, 0),    
        (255, 0, 128),    
        (0, 255, 128), 
    ]

    # Manually draw masks using OpenCV for guaranteed visibility
    if mask_array is not None and len(mask_array) > 0:
        overlay = image.copy()
        img_h, img_w = image.shape[:2]
        
        for i in range(len(mask_array)):
            mask = mask_array[i]
            color_bgr = COLORS[i % len(COLORS)]  # Cycle through colors
            
            # Resize mask to match image dimensions if needed
            if mask.shape != (img_h, img_w):
                mask = cv2.resize(mask, (img_w, img_h), interpolation=cv2.INTER_LINEAR)
            
            # Convert mask to binary (0 or 1)
            binary_mask = (mask > 0.5).astype(np.uint8)
            
            # Apply colored overlay where mask is 1
            mask_indices = binary_mask == 1
            overlay[mask_indices] = cv2.addWeighted(
                overlay[mask_indices], 0.4,
                np.full_like(overlay[mask_indices], color_bgr), 0.6,
                0
            )
        
        annotated_image = overlay
    
 
    
    # Determine save path
    if save_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, 'assets', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(output_dir, f"{name}_segmented{ext}")
    
    # Save the result
    cv2.imwrite(save_path, annotated_image)
    
    return save_path
