from inference import get_model
import supervision as sv
import os
import cv2
from typing import List, Union, Dict, Any
from utils import get_settings, Settings

settings: Settings = get_settings()

MODEL_API_URL = settings.MODEL_API_URL
API_KEY = settings.API_KEY

def segment_water(image_paths: Union[str, List[str]], display: bool = False) -> Dict[str, Any]:
    single_image = isinstance(image_paths, str)
    if single_image:
        image_paths = [image_paths]
    
    model = get_model(model_id=MODEL_API_URL, api_key=API_KEY)
    
    results_per_image = []
    
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            continue
        
        results = model.infer(image)[0]
        
        image_predictions = []
        if hasattr(results, 'predictions'):
            for pred in results.predictions:
                prediction_dict = {
                    "x": float(pred.x),
                    "y": float(pred.y),
                    "width": float(pred.width),
                    "height": float(pred.height),
                    "confidence": float(pred.confidence),
                    "class": pred.class_name if hasattr(pred, 'class_name') else str(getattr(pred, 'class')),
                    "class_id": int(pred.class_id),
                    "detection_id": pred.detection_id if hasattr(pred, 'detection_id') else str(id(pred)),
                }
                
                if hasattr(pred, 'points') and pred.points is not None:
                    prediction_dict["points"] = [
                        {"x": float(point.x), "y": float(point.y)} for point in pred.points
                    ]
                
                image_predictions.append(prediction_dict)
        
        results_per_image.append({
            "image": os.path.basename(image_path),
            "predictions": image_predictions
        })

    if single_image:
        return results_per_image[0]
    else:
        return {"results": results_per_image}