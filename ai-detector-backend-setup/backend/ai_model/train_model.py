"""
AI Model Training Script
MobileNetV2 Transfer Learning for Crop Disease Detection
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau


# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.0001

# Disease classes
CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot", 
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn_(maize)___Cercospora_leaf_spot",
    "Corn_(maize)___Common_rust",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca",
    "Grape___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Yellow_Leaf_Curl_Virus",
    "Tomato___healthy",
    "Rice___Brown_Spot",
    "Rice___Leaf_Blast",
    "Rice___healthy",
    "Wheat___Brown_Rust",
    "Wheat___Yellow_Rust",
    "Wheat___healthy"
]

NUM_CLASSES = len(CLASSES)


def create_model():
    """
    Create MobileNetV2 model with custom classification head
    """
    # Load pre-trained MobileNetV2 (without top layers)
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    return model, base_model


def prepare_data(train_dir: str, val_dir: str):
    """
    Prepare data generators with augmentation
    """
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Validation data (no augmentation, just rescaling)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASSES
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASSES
    )
    
    return train_generator, val_generator


def train_model(train_dir: str, val_dir: str, output_path: str = '../models/crop_disease_model.h5'):
    """
    Train the model
    """
    print("🌾 Starting Crop Disease Detection Model Training...")
    print(f"Number of classes: {NUM_CLASSES}")
    
    # Create model
    model, base_model = create_model()
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(model.summary())
    
    # Prepare data
    train_gen, val_gen = prepare_data(train_dir, val_dir)
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        ModelCheckpoint(
            output_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-7
        )
    ]
    
    # Phase 1: Train only the top layers
    print("\n📍 Phase 1: Training classification head...")
    history1 = model.fit(
        train_gen,
        epochs=10,
        validation_data=val_gen,
        callbacks=callbacks
    )
    
    # Phase 2: Fine-tune some layers of base model
    print("\n📍 Phase 2: Fine-tuning base model...")
    
    # Unfreeze last 30 layers of base model
    for layer in base_model.layers[-30:]:
        layer.trainable = True
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE / 10),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history2 = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks
    )
    
    print(f"\n✅ Model saved to {output_path}")
    print(f"Final validation accuracy: {max(history2.history['val_accuracy']):.4f}")
    
    return model, history2


def evaluate_model(model, test_dir: str):
    """
    Evaluate model on test data
    """
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASSES,
        shuffle=False
    )
    
    # Evaluate
    results = model.evaluate(test_generator)
    print(f"\n📊 Test Results:")
    print(f"Loss: {results[0]:.4f}")
    print(f"Accuracy: {results[1]:.4f}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Crop Disease Detection Model')
    parser.add_argument('--train_dir', type=str, required=True, help='Training data directory')
    parser.add_argument('--val_dir', type=str, required=True, help='Validation data directory')
    parser.add_argument('--test_dir', type=str, help='Test data directory (optional)')
    parser.add_argument('--output', type=str, default='../models/crop_disease_model.h5', help='Output model path')
    
    args = parser.parse_args()
    
    # Train
    model, history = train_model(args.train_dir, args.val_dir, args.output)
    
    # Evaluate if test dir provided
    if args.test_dir:
        evaluate_model(model, args.test_dir)
    
    print("\n🎉 Training complete!")
