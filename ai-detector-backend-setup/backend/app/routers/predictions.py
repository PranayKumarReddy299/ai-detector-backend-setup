"""
Predictions Router
Handle crop disease predictions
"""

import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionResponse, PredictionHistory
from app.routers.dependencies import get_current_user
from app.services.ai_service import ai_service
from app.config import settings

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload crop image and get disease prediction
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG, PNG, and WebP images are allowed."
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 10MB."
        )
    
    try:
        # Get prediction from AI service
        result = ai_service.predict(content)
        
        # Save image
        file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(content)
        
        # Save prediction to database
        prediction = Prediction(
            user_id=current_user.id,
            image_url=f"/uploads/{filename}",
            predicted_disease=result["disease_name"],
            confidence=result["confidence"],
            symptoms=result["symptoms"],
            treatment=result["treatment"],
            pesticide=result["pesticide"]
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return PredictionResponse(
            id=prediction.id,
            image_url=prediction.image_url,
            predicted_disease=prediction.predicted_disease,
            confidence=prediction.confidence,
            symptoms=prediction.symptoms,
            treatment=prediction.treatment,
            pesticide=prediction.pesticide,
            created_at=prediction.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/history", response_model=PredictionHistory)
async def get_prediction_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's prediction history
    """
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()
    
    total = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).count()
    
    return PredictionHistory(
        predictions=[PredictionResponse(
            id=p.id,
            image_url=p.image_url,
            predicted_disease=p.predicted_disease,
            confidence=p.confidence,
            symptoms=p.symptoms,
            treatment=p.treatment,
            pesticide=p.pesticide,
            created_at=p.created_at
        ) for p in predictions],
        total=total
    )


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get specific prediction by ID
    """
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    return PredictionResponse(
        id=prediction.id,
        image_url=prediction.image_url,
        predicted_disease=prediction.predicted_disease,
        confidence=prediction.confidence,
        symptoms=prediction.symptoms,
        treatment=prediction.treatment,
        pesticide=prediction.pesticide,
        created_at=prediction.created_at
    )


@router.delete("/{prediction_id}")
async def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a prediction
    """
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    # Delete image file
    if prediction.image_url:
        filepath = prediction.image_url.lstrip('/')
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prediction deleted successfully"}
