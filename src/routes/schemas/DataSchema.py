from typing import List, Optional
from pydantic import BaseModel, Field

class Point(BaseModel):
    x: float
    y: float

    class Config:
        extra = "allow"  


class Prediction(BaseModel):
    x: float
    y: float
    width: float
    height: float
    confidence: float
    class_: str = Field(..., alias="class")  # accept "class" from JSON
    points: Optional[List[Point]] = None
    class_id: int
    detection_id: str

    class Config:
        extra = "allow"


class DataSchema(BaseModel):
    predictions: List[Prediction]

    class Config:
        extra = "allow"
