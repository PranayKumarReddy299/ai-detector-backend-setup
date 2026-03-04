"""
Prediction Schemas (Pydantic)
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PredictionRequest(BaseModel):
    image_base64: Optional[str] = None


class DiseaseInfo(BaseModel):
    disease_name: str
    confidence: float
    symptoms: str
    treatment: str
    pesticide: str


class PredictionResponse(BaseModel):
    id: int
    image_url: str
    predicted_disease: str
    confidence: float
    symptoms: Optional[str]
    treatment: Optional[str]
    pesticide: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PredictionHistory(BaseModel):
    predictions: List[PredictionResponse]
    total: int
