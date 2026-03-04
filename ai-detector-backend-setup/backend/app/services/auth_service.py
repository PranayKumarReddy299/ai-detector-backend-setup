"""
Authentication Service
Handles user authentication, OTP, and JWT
"""

import random
import string
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import jwt
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.otp import OTPCode, OTPPurpose
from app.config import settings
from app.services.email_service import send_otp_email


class AuthService:
    
    @staticmethod
    def generate_otp() -> str:
        """Generate 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    async def send_otp(db: Session, email: str, purpose: OTPPurpose = OTPPurpose.SIGNUP) -> bool:
        """Generate and send OTP to email"""
        # Delete existing unused OTPs for this email and purpose
        db.query(OTPCode).filter(
            OTPCode.email == email,
            OTPCode.purpose == purpose.value,
            OTPCode.is_used == 0
        ).delete()
        
        # Generate new OTP
        otp = AuthService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Save to database
        otp_record = OTPCode(
            email=email,
            otp=otp,
            purpose=purpose.value,
            expires_at=expires_at
        )
        db.add(otp_record)
        db.commit()
        
        # Send email
        await send_otp_email(email, otp, purpose.value)
        
        return True
    
    @staticmethod
    def verify_otp(db: Session, email: str, otp: str, purpose: OTPPurpose = OTPPurpose.SIGNUP) -> bool:
        """Verify OTP code"""
        otp_record = db.query(OTPCode).filter(
            OTPCode.email == email,
            OTPCode.otp == otp,
            OTPCode.purpose == purpose.value,
            OTPCode.is_used == 0
        ).first()
        
        if not otp_record:
            return False
        
        # Check expiry
        if datetime.utcnow() > otp_record.expires_at.replace(tzinfo=None):
            return False
        
        # Mark as used
        otp_record.is_used = 1
        db.commit()
        
        return True
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, email: str, password: str) -> User:
        """Create new verified user"""
        password_hash = AuthService.hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash,
            is_verified=True  # Verified because OTP was already validated
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_password(db: Session, email: str, new_password: str) -> bool:
        """Update user password"""
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return False
        
        user.password_hash = AuthService.hash_password(new_password)
        db.commit()
        return True
