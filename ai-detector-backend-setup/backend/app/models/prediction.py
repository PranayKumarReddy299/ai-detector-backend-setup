"""
Prediction Model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    predicted_disease = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    symptoms = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    pesticide = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, disease={self.predicted_disease}, confidence={self.confidence})>"
