# AI Crop Disease Detector - Backend

FastAPI backend for the AI Crop Disease Detector application.

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── otp.py
│   │   └── prediction.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── prediction.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   └── ai_service.py
│   └── routers/             # API routes
│       ├── __init__.py
│       ├── auth.py
│       ├── predictions.py
│       └── dependencies.py
├── ai_model/
│   └── train_model.py       # Model training script
├── models/                   # Saved AI models
├── uploads/                  # Uploaded images
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

```bash
# Create database
psql -U postgres
CREATE DATABASE crop_disease_db;
\q
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/send-otp` | Send OTP to email |
| POST | `/api/auth/verify-otp` | Verify OTP |
| POST | `/api/auth/signup` | Complete signup with OTP |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with OTP |
| GET | `/api/auth/me` | Get current user |

### Predictions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predictions/predict` | Upload image and get prediction |
| GET | `/api/predictions/history` | Get prediction history |
| GET | `/api/predictions/{id}` | Get specific prediction |
| DELETE | `/api/predictions/{id}` | Delete prediction |

## 🧠 Training the AI Model

1. Prepare your dataset:
   - Organize images into folders by disease class
   - Split into train/validation/test sets

2. Run training:
```bash
python ai_model/train_model.py \
  --train_dir /path/to/train \
  --val_dir /path/to/val \
  --test_dir /path/to/test \
  --output models/crop_disease_model.h5
```

## 🔐 Security Notes

- Always use strong JWT secrets in production
- Enable HTTPS in production
- Keep database credentials secure
- Use app-specific passwords for email SMTP
