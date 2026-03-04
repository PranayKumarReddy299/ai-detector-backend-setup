"""
Authentication Router
Handles signup, login, OTP verification, password reset
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    OTPRequest, OTPVerify, SignupRequest, SignupResponse,
    LoginRequest, LoginResponse, UserResponse, MessageResponse,
    PasswordResetRequest, PasswordResetConfirm
)
from app.services.auth_service import AuthService
from app.models.otp import OTPPurpose
from app.routers.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/send-otp", response_model=MessageResponse)
async def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """
    Send OTP to email for signup verification
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Send OTP
    await AuthService.send_otp(db, request.email, OTPPurpose.SIGNUP)
    
    return MessageResponse(
        message=f"OTP sent to {request.email}. Valid for 5 minutes.",
        success=True
    )


@router.post("/verify-otp", response_model=MessageResponse)
async def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP without creating account (for checking OTP validity)
    """
    # Check OTP without marking as used
    from app.models.otp import OTPCode
    from datetime import datetime
    
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == request.email,
        OTPCode.otp == request.otp,
        OTPCode.purpose == OTPPurpose.SIGNUP.value,
        OTPCode.is_used == 0
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    if datetime.utcnow() > otp_record.expires_at.replace(tzinfo=None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )
    
    return MessageResponse(message="OTP verified successfully", success=True)


@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Complete signup with OTP verification
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Verify OTP
    if not AuthService.verify_otp(db, request.email, request.otp, OTPPurpose.SIGNUP):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Create user (already verified since OTP passed)
    user = AuthService.create_user(db, request.email, request.password)
    
    return SignupResponse(
        message="Account created successfully",
        user_id=user.id,
        email=user.email
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password
    Only verified users can login
    """
    # Get user
    user = AuthService.get_user_by_email(db, request.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please complete OTP verification."
        )
    
    # Verify password
    if not AuthService.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token = AuthService.create_access_token(user.id, user.email)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    )


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Send password reset OTP
    """
    user = AuthService.get_user_by_email(db, request.email)
    
    if not user:
        # Don't reveal if email exists
        return MessageResponse(
            message="If the email exists, an OTP has been sent.",
            success=True
        )
    
    await AuthService.send_otp(db, request.email, OTPPurpose.PASSWORD_RESET)
    
    return MessageResponse(
        message="Password reset OTP sent to your email.",
        success=True
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Reset password with OTP verification
    """
    # Verify OTP
    if not AuthService.verify_otp(db, request.email, request.otp, OTPPurpose.PASSWORD_RESET):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Update password
    if not AuthService.update_password(db, request.email, request.new_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return MessageResponse(message="Password reset successful", success=True)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user info
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )
