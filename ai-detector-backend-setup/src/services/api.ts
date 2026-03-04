// API Service - Mock implementation for demo
// In production, replace with actual API calls

import { User, Prediction, DiseaseInfo } from '../types';

// API Base URL - used when connecting to real backend
// const API_BASE_URL = 'http://localhost:8000/api';

// Simulated database
let mockUsers: { email: string; password: string; id: number; is_verified: boolean }[] = [];
let mockOTPs: { email: string; otp: string; purpose: string; expiresAt: Date }[] = [];
let mockPredictions: Prediction[] = [];
let nextUserId = 1;
let nextPredictionId = 1;

// Disease database for mock predictions
const DISEASES: DiseaseInfo[] = [
  {
    disease_name: "Tomato Late Blight",
    confidence: 94.5,
    symptoms: "Large, irregular water-soaked spots on leaves. White mold on leaf undersides. Rapid plant collapse.",
    treatment: "Remove infected plants immediately. Avoid overhead watering. Apply fungicides preventatively.",
    pesticide: "Metalaxyl or Chlorothalonil fungicides"
  },
  {
    disease_name: "Apple Scab",
    confidence: 89.2,
    symptoms: "Dark, olive-green to brown lesions on leaves. Velvety or fuzzy texture on leaf undersides. Deformed or cracked fruits.",
    treatment: "Remove and destroy fallen leaves. Prune trees for better air circulation. Apply fungicides during wet spring weather.",
    pesticide: "Captan, Mancozeb, or Myclobutanil fungicides"
  },
  {
    disease_name: "Corn Northern Leaf Blight",
    confidence: 91.8,
    symptoms: "Long, elliptical gray-green lesions. Lesions turn tan as they mature. Can cover entire leaf surface.",
    treatment: "Use resistant hybrids. Rotate crops. Apply fungicides at early infection.",
    pesticide: "Azoxystrobin or Propiconazole fungicides"
  },
  {
    disease_name: "Potato Early Blight",
    confidence: 87.3,
    symptoms: "Dark brown spots with concentric rings (target pattern). Lower leaves affected first. Yellowing around spots.",
    treatment: "Rotate crops. Remove infected plant debris. Apply fungicides preventatively.",
    pesticide: "Chlorothalonil or Mancozeb fungicides"
  },
  {
    disease_name: "Grape Black Rot",
    confidence: 92.1,
    symptoms: "Brown circular lesions with dark borders on leaves. Black mummified berries. Cankers on shoots.",
    treatment: "Remove mummified berries and infected vines. Prune for air circulation. Apply fungicides.",
    pesticide: "Mancozeb, Myclobutanil, or Captan fungicides"
  },
  {
    disease_name: "Healthy Plant",
    confidence: 96.8,
    symptoms: "No disease symptoms detected. Plant appears healthy with normal coloration and growth patterns.",
    treatment: "Continue regular maintenance. Monitor for any changes. Maintain proper watering and nutrition.",
    pesticide: "None required - plant is healthy"
  },
  {
    disease_name: "Rice Leaf Blast",
    confidence: 88.9,
    symptoms: "Diamond-shaped lesions on leaves. Gray-green to white centers. Can kill entire plants.",
    treatment: "Use resistant varieties. Avoid excess nitrogen. Apply fungicides early.",
    pesticide: "Tricyclazole or Isoprothiolane fungicides"
  },
  {
    disease_name: "Wheat Yellow Rust",
    confidence: 90.4,
    symptoms: "Yellow-orange pustules in stripes along leaves. Can spread rapidly in cool weather.",
    treatment: "Use resistant varieties. Apply fungicides early in epidemic.",
    pesticide: "Propiconazole or Triadimefon fungicides"
  }
];

// Helper to generate OTP
const generateOTP = (): string => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

// Helper to simulate network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Auth API
export const authApi = {
  sendOTP: async (email: string): Promise<{ success: boolean; message: string; otp?: string }> => {
    await delay(1000);
    
    // Check if user already exists
    const existingUser = mockUsers.find(u => u.email === email);
    if (existingUser) {
      throw new Error('Email already registered');
    }
    
    // Generate and store OTP
    const otp = generateOTP();
    mockOTPs = mockOTPs.filter(o => o.email !== email || o.purpose !== 'signup');
    mockOTPs.push({
      email,
      otp,
      purpose: 'signup',
      expiresAt: new Date(Date.now() + 5 * 60 * 1000) // 5 minutes
    });
    
    console.log(`📧 OTP for ${email}: ${otp}`); // For demo purposes
    
    return { 
      success: true, 
      message: `OTP sent to ${email}. Valid for 5 minutes.`,
      otp // Return OTP for demo (remove in production)
    };
  },

  verifyOTP: async (email: string, otp: string): Promise<{ success: boolean; message: string }> => {
    await delay(500);
    
    const otpRecord = mockOTPs.find(
      o => o.email === email && o.otp === otp && o.purpose === 'signup'
    );
    
    if (!otpRecord) {
      throw new Error('Invalid OTP');
    }
    
    if (new Date() > otpRecord.expiresAt) {
      throw new Error('OTP has expired');
    }
    
    return { success: true, message: 'OTP verified successfully' };
  },

  signup: async (email: string, otp: string, password: string): Promise<{ user: User; message: string }> => {
    await delay(1000);
    
    // Verify OTP
    const otpRecord = mockOTPs.find(
      o => o.email === email && o.otp === otp && o.purpose === 'signup'
    );
    
    if (!otpRecord) {
      throw new Error('Invalid or expired OTP');
    }
    
    if (new Date() > otpRecord.expiresAt) {
      throw new Error('OTP has expired');
    }
    
    // Create user
    const user = {
      id: nextUserId++,
      email,
      password,
      is_verified: true
    };
    mockUsers.push(user);
    
    // Remove used OTP
    mockOTPs = mockOTPs.filter(o => !(o.email === email && o.purpose === 'signup'));
    
    return {
      user: { id: user.id, email: user.email, is_verified: true, created_at: new Date().toISOString() },
      message: 'Account created successfully'
    };
  },

  login: async (email: string, password: string): Promise<{ token: string; user: User }> => {
    await delay(1000);
    
    const user = mockUsers.find(u => u.email === email && u.password === password);
    
    if (!user) {
      throw new Error('Invalid email or password');
    }
    
    if (!user.is_verified) {
      throw new Error('Email not verified. Please complete OTP verification.');
    }
    
    const token = `mock_jwt_token_${user.id}_${Date.now()}`;
    
    return {
      token,
      user: { id: user.id, email: user.email, is_verified: true, created_at: new Date().toISOString() }
    };
  },

  sendPasswordResetOTP: async (email: string): Promise<{ success: boolean; message: string; otp?: string }> => {
    await delay(1000);
    
    const otp = generateOTP();
    mockOTPs = mockOTPs.filter(o => o.email !== email || o.purpose !== 'password_reset');
    mockOTPs.push({
      email,
      otp,
      purpose: 'password_reset',
      expiresAt: new Date(Date.now() + 5 * 60 * 1000)
    });
    
    console.log(`📧 Password Reset OTP for ${email}: ${otp}`);
    
    return { 
      success: true, 
      message: 'Password reset OTP sent to your email.',
      otp
    };
  },

  resetPassword: async (email: string, otp: string, newPassword: string): Promise<{ success: boolean; message: string }> => {
    await delay(1000);
    
    const otpRecord = mockOTPs.find(
      o => o.email === email && o.otp === otp && o.purpose === 'password_reset'
    );
    
    if (!otpRecord) {
      throw new Error('Invalid or expired OTP');
    }
    
    if (new Date() > otpRecord.expiresAt) {
      throw new Error('OTP has expired');
    }
    
    // Update password
    const user = mockUsers.find(u => u.email === email);
    if (user) {
      user.password = newPassword;
    }
    
    // Remove used OTP
    mockOTPs = mockOTPs.filter(o => !(o.email === email && o.purpose === 'password_reset'));
    
    return { success: true, message: 'Password reset successful' };
  }
};

// Predictions API
export const predictionsApi = {
  predict: async (imageFile: File, _userId: number): Promise<Prediction> => {
    await delay(2000); // Simulate AI processing
    
    // Select random disease for demo
    const disease = DISEASES[Math.floor(Math.random() * DISEASES.length)];
    
    // Create prediction
    const prediction: Prediction = {
      id: nextPredictionId++,
      image_url: URL.createObjectURL(imageFile),
      predicted_disease: disease.disease_name,
      confidence: disease.confidence,
      symptoms: disease.symptoms,
      treatment: disease.treatment,
      pesticide: disease.pesticide,
      created_at: new Date().toISOString()
    };
    
    mockPredictions.unshift(prediction);
    
    return prediction;
  },

  getHistory: async (_userId: number): Promise<{ predictions: Prediction[]; total: number }> => {
    await delay(500);
    
    return {
      predictions: mockPredictions,
      total: mockPredictions.length
    };
  },

  getPrediction: async (predictionId: number): Promise<Prediction | null> => {
    await delay(300);
    return mockPredictions.find(p => p.id === predictionId) || null;
  },

  deletePrediction: async (predictionId: number): Promise<{ success: boolean }> => {
    await delay(500);
    mockPredictions = mockPredictions.filter(p => p.id !== predictionId);
    return { success: true };
  }
};
