import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

def train_cnn_model(dataset_path="dataset", model_save_path="ml/gesture_model.h5"):
    """Trains a CNN model on the collected dataset."""
    
    if not os.path.exists(dataset_path):
        print(f"[ERROR] Dataset directory '{dataset_path}' not found. Run 'ml/collect_data.py' first.")
        return

    # Image parameters
    IMG_HEIGHT = 64
    IMG_WIDTH = 64
    BATCH_SIZE = 32
    
    print("[INFO] Loading images...")
    
    # Data Augmentation (Make model robust to slight rotations/zooms)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        zoom_range=0.1,
        width_shift_range=0.1,  # Added: Shift robustness
        height_shift_range=0.1, # Added: Shift robustness
        validation_split=0.15   # Reduced split to train on more data (200 samples/class is decent)
    )

    train_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    num_classes = len(train_generator.class_indices)
    print(f"[INFO] Detected {num_classes} classes: {train_generator.class_indices}")
    # CRITICAL: Print this mapping! It tells us that 'fist'=0, 'ok_sign'=1, etc.
    # If this order is different from what is in run_recognition.py, predictions will be wrong.
    with open("ml/class_map.txt", "w") as f:
        f.write(str(train_generator.class_indices))

    # --- CNN Architecture (The "Brain") ---
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5), # Prevent overfitting
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Train
    print("[INFO] Starting training...")
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=15, # Increased to 15 for better learning with 200 samples
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE
    )

    # Save
    model.save(model_save_path)
    print(f"[SUCCESS] Model trained and saved to {model_save_path}")

if __name__ == "__main__":
    train_cnn_model()
