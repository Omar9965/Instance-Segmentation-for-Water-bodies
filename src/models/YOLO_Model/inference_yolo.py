from ultralytics import YOLO
import os
import cv2
from typing import List, Union, Dict, Any, Tuple
from utils import get_settings, Settings

settings: Settings = get_settings()


best_model = os.path.join(os.path.dirname(__file__), "best_model.pt")

def segment_water(image_paths: Union[str, List[str]]) -> Tuple[Dict[str, Any], List]:
    """
    Segment water bodies in images and return both predictions and raw results.
    
    Returns:
        Tuple of (predictions_dict, raw_results_list)
    """
    single_image = isinstance(image_paths, str)
    if single_image:
        image_paths = [image_paths]
    
    model = YOLO(best_model)
    
    results_per_image = []
    raw_results = []
    
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            continue
        
        # Use predict() for inference
        results = model.predict(image, verbose=False)[0]
        raw_results.append((image_path, results))
        
        image_predictions = []
        
        # Check if masks exist (for instance segmentation)
        if results.masks is not None and len(results.masks) > 0:
            for idx in range(len(results.masks)):
                # Get bounding box
                box = results.boxes[idx]
                xyxy = box.xyxy[0].cpu().numpy()
                x, y, x2, y2 = xyxy
                width = x2 - x
                height = y2 - y
                
                # Get segmentation mask polygon points
                mask = results.masks[idx]
                if hasattr(mask, 'xy') and len(mask.xy) > 0:
                    # mask.xy contains the polygon points
                    polygon_points = mask.xy[0]  # Get first contour
                    points = [
                        {"x": float(point[0]), "y": float(point[1])} 
                        for point in polygon_points
                    ]
                else:
                    # Fallback: create points from bounding box corners
                    points = [
                        {"x": float(x), "y": float(y)},
                        {"x": float(x2), "y": float(y)},
                        {"x": float(x2), "y": float(y2)},
                        {"x": float(x), "y": float(y2)}
                    ]
                
                prediction_dict = {
                    "x": float(x),
                    "y": float(y),
                    "width": float(width),
                    "height": float(height),
                    "confidence": float(box.conf[0].cpu().numpy()),
                    "class": results.names[int(box.cls[0].cpu().numpy())],
                    "class_id": int(box.cls[0].cpu().numpy()),
                    "detection_id": f"{idx}_{int(box.cls[0].cpu().numpy())}",
                    "points": points
                }
                
                image_predictions.append(prediction_dict)
        
        results_per_image.append({
            "image": os.path.basename(image_path),
            "predictions": image_predictions
        })


    return {"results": results_per_image}, raw_results