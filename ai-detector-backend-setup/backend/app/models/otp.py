"""
OTP Code Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class OTPPurpose(str, enum.Enum):
    SIGNUP = "signup"
    PASSWORD_RESET = "password_reset"


class OTPCode(Base):
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, nullable=False)
    otp = Column(String(6), nullable=False)
    purpose = Column(String(20), default=OTPPurpose.SIGNUP.value)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_used = Column(Integer, default=0)  # 0 = not used, 1 = used
    
    def __repr__(self):
        return f"<OTPCode(id={self.id}, email={self.email}, purpose={self.purpose})>"
