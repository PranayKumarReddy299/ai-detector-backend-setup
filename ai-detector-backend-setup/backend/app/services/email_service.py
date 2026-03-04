"""
Email Service
Send OTP emails using SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from app.config import settings


async def send_otp_email(to_email: str, otp: str, purpose: str = "signup") -> bool:
    """
    Send OTP email to user
    """
    subject_map = {
        "signup": "Verify Your Email - AI Crop Disease Detector",
        "password_reset": "Reset Your Password - AI Crop Disease Detector"
    }
    
    subject = subject_map.get(purpose, "Your OTP Code")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #10b981, #3b82f6); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .otp-box {{ background: white; border: 2px dashed #10b981; padding: 20px; text-align: center; margin: 20px 0; border-radius: 10px; }}
            .otp-code {{ font-size: 36px; font-weight: bold; color: #10b981; letter-spacing: 8px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            .warning {{ color: #ef4444; font-size: 14px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 AI Crop Disease Detector</h1>
            </div>
            <div class="content">
                <h2>{"Email Verification" if purpose == "signup" else "Password Reset"}</h2>
                <p>Hello,</p>
                <p>{"Please use the following OTP to verify your email address and complete your registration:" if purpose == "signup" else "Please use the following OTP to reset your password:"}</p>
                
                <div class="otp-box">
                    <div class="otp-code">{otp}</div>
                </div>
                
                <p class="warning">⚠️ This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>© 2024 AI Crop Disease Detector. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.EMAIL_FROM
        message["To"] = to_email
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # For production, use actual SMTP
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True
            )
        else:
            # Development: Print OTP to console
            print(f"\n{'='*50}")
            print(f"📧 OTP EMAIL (Development Mode)")
            print(f"To: {to_email}")
            print(f"Purpose: {purpose}")
            print(f"OTP: {otp}")
            print(f"{'='*50}\n")
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        # In development, still return True
        return True
