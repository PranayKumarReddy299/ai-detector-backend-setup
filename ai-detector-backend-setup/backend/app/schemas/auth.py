"""
Authentication Schemas (Pydantic)
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# OTP Request
class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


# Signup
class SignupRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    password: str = Field(..., min_length=8, max_length=100)


class SignupResponse(BaseModel):
    message: str
    user_id: int
    email: str


# Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


# Password Reset
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=100)


# User
class UserResponse(BaseModel):
    id: int
    email: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Generic Response
class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    detail: str
    success: bool = False
