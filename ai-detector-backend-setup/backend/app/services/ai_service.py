"""
AI Service
Crop Disease Detection using MobileNetV2
"""

import os
import numpy as np
from typing import Dict, Tuple, Optional
import base64
from io import BytesIO
from PIL import Image

# Disease information database
DISEASE_DATABASE = {
    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "symptoms": "Dark, olive-green to brown lesions on leaves. Velvety or fuzzy texture on leaf undersides. Deformed or cracked fruits with scab-like spots.",
        "treatment": "Remove and destroy fallen leaves. Prune trees for better air circulation. Apply fungicides during wet spring weather.",
        "pesticide": "Captan, Mancozeb, or Myclobutanil fungicides"
    },
    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "symptoms": "Purple spots on leaves that enlarge and turn brown. Rotten brown spots on fruit starting from the blossom end. Cankers on branches.",
        "treatment": "Remove mummified fruits and infected branches. Maintain tree vigor through proper fertilization. Apply fungicides preventatively.",
        "pesticide": "Captan or Thiophanate-methyl fungicides"
    },
    "Apple___Cedar_apple_rust": {
        "name": "Cedar Apple Rust",
        "symptoms": "Yellow-orange spots on leaves. Tube-like structures on leaf undersides. Deformed fruits with spots.",
        "treatment": "Remove nearby cedar trees if possible. Apply fungicides when orange spore horns appear on cedars.",
        "pesticide": "Myclobutanil or Triadimefon fungicides"
    },
    "Apple___healthy": {
        "name": "Healthy Apple",
        "symptoms": "No disease symptoms. Leaves are green and healthy.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Corn_(maize)___Cercospora_leaf_spot": {
        "name": "Corn Gray Leaf Spot",
        "symptoms": "Small, rectangular gray to tan lesions. Lesions run parallel to leaf veins. Severe infections cause leaf blight.",
        "treatment": "Rotate crops. Use resistant hybrids. Tillage to bury infected residue.",
        "pesticide": "Strobilurin or Triazole fungicides"
    },
    "Corn_(maize)___Common_rust": {
        "name": "Corn Common Rust",
        "symptoms": "Small, circular to elongated brown pustules on leaves. Pustules on both leaf surfaces. Yellow halos around pustules.",
        "treatment": "Plant resistant varieties. Apply fungicides if infection is early and severe.",
        "pesticide": "Mancozeb or Propiconazole fungicides"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Northern Corn Leaf Blight",
        "symptoms": "Long, elliptical gray-green lesions. Lesions turn tan as they mature. Can cover entire leaf surface.",
        "treatment": "Use resistant hybrids. Rotate crops. Apply fungicides at early infection.",
        "pesticide": "Azoxystrobin or Propiconazole fungicides"
    },
    "Corn_(maize)___healthy": {
        "name": "Healthy Corn",
        "symptoms": "No disease symptoms. Leaves are green and vigorous.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "symptoms": "Brown circular lesions with dark borders on leaves. Black mummified berries. Cankers on shoots.",
        "treatment": "Remove mummified berries and infected vines. Prune for air circulation. Apply fungicides.",
        "pesticide": "Mancozeb, Myclobutanil, or Captan fungicides"
    },
    "Grape___Esca": {
        "name": "Grape Esca (Black Measles)",
        "symptoms": "Tiger stripe pattern on leaves. Dark spots on berries. Sudden wilting of shoots.",
        "treatment": "Remove infected vines. Avoid stress on vines. No effective chemical control.",
        "pesticide": "No effective fungicides available"
    },
    "Grape___healthy": {
        "name": "Healthy Grape",
        "symptoms": "No disease symptoms. Vines are healthy and productive.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "symptoms": "Dark brown spots with concentric rings (target pattern). Lower leaves affected first. Yellowing around spots.",
        "treatment": "Rotate crops. Remove infected plant debris. Apply fungicides preventatively.",
        "pesticide": "Chlorothalonil or Mancozeb fungicides"
    },
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "symptoms": "Water-soaked spots on leaves. White fuzzy growth on undersides. Rapid plant death. Brown rot in tubers.",
        "treatment": "Destroy infected plants immediately. Use certified seed potatoes. Apply fungicides.",
        "pesticide": "Metalaxyl, Mancozeb, or Chlorothalonil fungicides"
    },
    "Potato___healthy": {
        "name": "Healthy Potato",
        "symptoms": "No disease symptoms. Plants are green and vigorous.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Tomato___Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "symptoms": "Small, water-soaked spots on leaves. Spots turn brown with yellow halos. Raised scab-like spots on fruits.",
        "treatment": "Use disease-free seeds. Avoid overhead irrigation. Apply copper-based bactericides.",
        "pesticide": "Copper hydroxide or Copper sulfate"
    },
    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "symptoms": "Dark spots with concentric rings. Lower leaves affected first. Stem lesions near soil line.",
        "treatment": "Rotate crops. Stake plants for air circulation. Apply fungicides.",
        "pesticide": "Chlorothalonil or Mancozeb fungicides"
    },
    "Tomato___Late_blight": {
        "name": "Tomato Late Blight",
        "symptoms": "Large, irregular water-soaked spots. White mold on leaf undersides. Rapid plant collapse.",
        "treatment": "Remove infected plants. Avoid overhead watering. Apply fungicides preventatively.",
        "pesticide": "Metalaxyl or Chlorothalonil fungicides"
    },
    "Tomato___Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "symptoms": "Pale green to yellow spots on upper leaf surface. Olive-green to brown mold on undersides.",
        "treatment": "Improve air circulation. Reduce humidity. Apply fungicides.",
        "pesticide": "Chlorothalonil or Mancozeb fungicides"
    },
    "Tomato___Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "symptoms": "Small circular spots with dark borders. Gray centers with tiny black dots. Lower leaves affected first.",
        "treatment": "Remove infected leaves. Avoid overhead irrigation. Apply fungicides.",
        "pesticide": "Chlorothalonil or Copper-based fungicides"
    },
    "Tomato___Spider_mites": {
        "name": "Tomato Spider Mites",
        "symptoms": "Tiny yellow or white speckles on leaves. Fine webbing on undersides. Bronzing of leaves.",
        "treatment": "Spray with water to dislodge mites. Introduce predatory mites. Apply miticides.",
        "pesticide": "Abamectin or Bifenthrin miticides"
    },
    "Tomato___Target_Spot": {
        "name": "Tomato Target Spot",
        "symptoms": "Brown spots with concentric rings. Spots on leaves, stems, and fruits. Leaf yellowing and drop.",
        "treatment": "Remove infected plant parts. Improve air circulation. Apply fungicides.",
        "pesticide": "Chlorothalonil or Azoxystrobin fungicides"
    },
    "Tomato___Yellow_Leaf_Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "symptoms": "Upward curling of leaves. Yellowing of leaf margins. Stunted growth. Reduced fruit production.",
        "treatment": "Control whitefly vectors. Remove infected plants. Use resistant varieties.",
        "pesticide": "Imidacloprid or Thiamethoxam for whitefly control"
    },
    "Tomato___healthy": {
        "name": "Healthy Tomato",
        "symptoms": "No disease symptoms. Plants are green and productive.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Rice___Brown_Spot": {
        "name": "Rice Brown Spot",
        "symptoms": "Oval brown spots on leaves. Spots have gray centers. Can affect grains causing discoloration.",
        "treatment": "Use balanced fertilization. Treat seeds before planting. Apply fungicides.",
        "pesticide": "Mancozeb or Propiconazole fungicides"
    },
    "Rice___Leaf_Blast": {
        "name": "Rice Leaf Blast",
        "symptoms": "Diamond-shaped lesions on leaves. Gray-green to white centers. Can kill entire plants.",
        "treatment": "Use resistant varieties. Avoid excess nitrogen. Apply fungicides early.",
        "pesticide": "Tricyclazole or Isoprothiolane fungicides"
    },
    "Rice___healthy": {
        "name": "Healthy Rice",
        "symptoms": "No disease symptoms. Plants are green and healthy.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    },
    "Wheat___Brown_Rust": {
        "name": "Wheat Brown/Leaf Rust",
        "symptoms": "Orange-brown pustules on leaves. Pustules circular and scattered. Leaves turn yellow and dry.",
        "treatment": "Plant resistant varieties. Apply fungicides at first sign of infection.",
        "pesticide": "Propiconazole or Tebuconazole fungicides"
    },
    "Wheat___Yellow_Rust": {
        "name": "Wheat Yellow/Stripe Rust",
        "symptoms": "Yellow-orange pustules in stripes along leaves. Can spread rapidly in cool weather.",
        "treatment": "Use resistant varieties. Apply fungicides early in epidemic.",
        "pesticide": "Propiconazole or Triadimefon fungicides"
    },
    "Wheat___healthy": {
        "name": "Healthy Wheat",
        "symptoms": "No disease symptoms. Plants are green and healthy.",
        "treatment": "Continue regular maintenance and monitoring.",
        "pesticide": "None required"
    }
}

# Class labels (these should match your trained model's classes)
CLASS_LABELS = list(DISEASE_DATABASE.keys())


class AIService:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self):
        """Load the trained model"""
        try:
            import tensorflow as tf
            from app.config import settings
            
            if os.path.exists(settings.MODEL_PATH):
                self._model = tf.keras.models.load_model(settings.MODEL_PATH)
                print("✅ AI Model loaded successfully")
            else:
                print("⚠️ Model file not found. Using mock predictions.")
                self._model = None
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            self._model = None
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for MobileNetV2"""
        # Resize to MobileNetV2 input size
        image = image.resize((224, 224))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to array and preprocess
        img_array = np.array(image)
        img_array = img_array / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_data: bytes) -> Dict:
        """
        Predict disease from image
        Returns disease info with confidence
        """
        try:
            # Load image
            image = Image.open(BytesIO(image_data))
            
            if self._model is not None:
                # Real prediction
                processed = self.preprocess_image(image)
                predictions = self._model.predict(processed)
                class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][class_idx])
                disease_key = CLASS_LABELS[class_idx]
            else:
                # Mock prediction for demo
                # Randomly select a disease for demonstration
                import random
                disease_key = random.choice(CLASS_LABELS)
                confidence = random.uniform(0.75, 0.98)
            
            # Get disease information
            disease_info = DISEASE_DATABASE.get(disease_key, {
                "name": "Unknown Disease",
                "symptoms": "Unable to identify symptoms.",
                "treatment": "Please consult a local agricultural expert.",
                "pesticide": "Not determined"
            })
            
            return {
                "disease_key": disease_key,
                "disease_name": disease_info["name"],
                "confidence": round(confidence * 100, 2),
                "symptoms": disease_info["symptoms"],
                "treatment": disease_info["treatment"],
                "pesticide": disease_info["pesticide"]
            }
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def predict_from_base64(self, base64_string: str) -> Dict:
        """Predict from base64 encoded image"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            image_data = base64.b64decode(base64_string)
            return self.predict(image_data)
        except Exception as e:
            raise Exception(f"Base64 decode error: {str(e)}")


# Singleton instance
ai_service = AIService()
