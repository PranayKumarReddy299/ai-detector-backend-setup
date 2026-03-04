# 🌾 AI Crop Disease Detector

A full-stack web application that uses AI to detect crop diseases from images and provide treatment recommendations.

![AI Crop Disease Detector](https://img.shields.io/badge/AI-Crop%20Disease%20Detector-green)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)

## 🚀 Features

- **🔐 Secure Authentication** - Email OTP verification mandatory for signup
- **📸 Image Upload** - Drag & drop or click to upload crop images
- **🤖 AI Detection** - MobileNetV2 transfer learning model
- **💊 Treatment Recommendations** - Get symptoms, treatment, and pesticide info
- **📊 History Tracking** - View all past predictions
- **📱 Responsive Design** - Works on mobile, tablet, and desktop

## 🛠️ Tech Stack

### Frontend
- React 18 with TypeScript
- Vite (build tool)
- Tailwind CSS
- React Router v6
- Context API for state management

### Backend
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM
- JWT authentication
- bcrypt password hashing
- Email OTP system

### AI/ML
- TensorFlow/Keras
- MobileNetV2 transfer learning
- 30+ crop diseases supported

## 📁 Project Structure

```
ai-crop-disease-detector/
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── context/        # Auth context
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── App.tsx         # Main app
│   └── index.html
│
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── routers/        # API routes
│   │   ├── main.py         # App entry point
│   │   └── config.py       # Configuration
│   ├── ai_model/           # ML training scripts
│   └── requirements.txt
│
└── README.md
```

## 🔐 Authentication Flow

### Signup (OTP Required)
1. User enters email
2. Backend sends 6-digit OTP to email
3. User enters OTP + password
4. Backend verifies OTP
5. If valid → create verified user

### Login
1. User enters email + password
2. Check: user exists AND password correct AND is_verified = true
3. Return JWT token

### Forgot Password
1. User enters email
2. Send OTP to email
3. User enters OTP + new password
4. Verify OTP → update password

## 🌾 Supported Crops & Diseases

| Crop | Diseases |
|------|----------|
| 🍅 Tomato | Early Blight, Late Blight, Leaf Mold, Bacterial Spot, etc. |
| 🥔 Potato | Early Blight, Late Blight, Healthy |
| 🌽 Corn | Gray Leaf Spot, Common Rust, Northern Leaf Blight |
| 🍎 Apple | Apple Scab, Black Rot, Cedar Apple Rust |
| 🍇 Grape | Black Rot, Esca, Healthy |
| 🌾 Rice | Brown Spot, Leaf Blast, Healthy |
| 🌿 Wheat | Brown Rust, Yellow Rust, Healthy |

## 🚀 Quick Start

### Frontend (React)
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Backend (FastAPI)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run server
uvicorn app.main:app --reload --port 8000
```

### Database Setup (PostgreSQL)
```bash
# Create database
psql -U postgres
CREATE DATABASE crop_disease_db;
\q
```

## 📧 Email Configuration

For Gmail SMTP:
1. Enable 2-Factor Authentication
2. Generate App Password
3. Update `.env`:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🧠 Train AI Model

```bash
cd backend/ai_model

python train_model.py \
  --train_dir /path/to/train \
  --val_dir /path/to/val \
  --output ../models/crop_disease_model.h5
```

Dataset structure:
```
dataset/
├── train/
│   ├── Apple___Apple_scab/
│   ├── Apple___healthy/
│   └── ...
└── val/
    ├── Apple___Apple_scab/
    └── ...
```

## 🔒 Security Features

- ✅ bcrypt password hashing
- ✅ JWT token authentication
- ✅ OTP expiry (5 minutes)
- ✅ Email verification required
- ✅ Pydantic validation
- ✅ CORS protection
- ✅ Environment variables

## 📝 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/send-otp` | Send OTP to email |
| POST | `/api/auth/verify-otp` | Verify OTP code |
| POST | `/api/auth/signup` | Complete signup with OTP |
| POST | `/api/auth/login` | Login with credentials |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset with OTP |
| GET | `/api/auth/me` | Get current user |

### Predictions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predictions/predict` | Upload & predict |
| GET | `/api/predictions/history` | Get user's history |
| GET | `/api/predictions/{id}` | Get specific prediction |
| DELETE | `/api/predictions/{id}` | Delete prediction |

## 🎨 UI Theme

Professional blue + green gradient design:
- Primary: Green (#10b981)
- Secondary: Blue (#3b82f6)
- Background: Gradient green-blue

## 📱 Screenshots

### Login Page
- Clean gradient background
- Email/password form
- Link to signup and forgot password

### Dashboard
- Welcome message with user greeting
- Quick stats (diseases, accuracy, speed)
- Feature cards
- Supported crops grid

### Disease Detection
- Drag & drop image upload
- Image preview
- AI analysis with loading state
- Results with confidence score
- Symptoms, treatment, pesticide recommendations

### History
- List of past predictions
- Click to view details
- Delete predictions

## ⚠️ Important Notes

1. **OTP is MANDATORY for signup** - No account creation without email verification
2. **Demo Mode** - Frontend includes mock API for testing without backend
3. **AI Model** - Train with your own dataset for best results
4. **Production** - Always use HTTPS and strong secrets

## 📄 License

MIT License - Feel free to use for your projects!

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

**Made with ❤️ for farmers worldwide** 🌾
