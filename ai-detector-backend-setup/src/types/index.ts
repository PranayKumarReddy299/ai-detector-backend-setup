// User types
export interface User {
  id: number;
  email: string;
  is_verified: boolean;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Auth request/response types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  otp: string;
  password: string;
}

export interface OTPRequest {
  email: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface MessageResponse {
  message: string;
  success: boolean;
}

// Prediction types
export interface Prediction {
  id: number;
  image_url: string;
  predicted_disease: string;
  confidence: number;
  symptoms: string | null;
  treatment: string | null;
  pesticide: string | null;
  created_at: string;
}

export interface PredictionHistory {
  predictions: Prediction[];
  total: number;
}

// Disease Info
export interface DiseaseInfo {
  disease_name: string;
  confidence: number;
  symptoms: string;
  treatment: string;
  pesticide: string;
}
