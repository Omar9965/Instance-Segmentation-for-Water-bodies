from pydantic import BaseModel, Field
from typing import List

class Point(BaseModel):
    x: float
    y: float

class Prediction(BaseModel):
    x: float
    y: float
    width: float
    height: float
    confidence: float
    class_: str = Field(..., alias="class")
    points: List[Point]
    class_id: int
    detection_id: str

class ImageResult(BaseModel):
    image: str
    predictions: List[Prediction]

class MultipleImagesResponse(BaseModel):
    results: List[ImageResult]
