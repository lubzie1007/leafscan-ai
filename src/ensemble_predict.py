import os
import numpy as np
import tensorflow as tf
from PIL import Image

MODELS_DIR = "models"
IMG_SIZE = 224

# Class names — must match training order (sorted alphabetically)
CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# Lazy-load models on first use (so importing this module is fast)
_models = {}


def _load_models():
    """Load both models once, cache them."""
    global _models
    if _models:
        return

    resnet_path = os.path.join(MODELS_DIR, "resnet50_best.h5")
    densenet_path = os.path.join(MODELS_DIR, "densenet_best.h5")

    if not os.path.exists(resnet_path):
        raise FileNotFoundError(f"Missing model: {resnet_path}")
    if not os.path.exists(densenet_path):
        raise FileNotFoundError(f"Missing model: {densenet_path}")

    print("Loading ResNet50...")
    _models["resnet"] = tf.keras.models.load_model(resnet_path, compile=False)
    print("Loading DenseNet...")
    _models["densenet"] = tf.keras.models.load_model(densenet_path, compile=False)
    print("✅ Both models loaded")


def _preprocess(image_input):
    """Accept file path, bytes, or PIL Image. Return (1, 224, 224, 3) array."""
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, (bytes, bytearray)):
        from io import BytesIO
        img = Image.open(BytesIO(image_input))
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        img = Image.open(image_input)

    img = img.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def predict(image_input):
    """
    Returns a dict:
      {
        "disease": "<class name>",
        "confidence": 0.94,
        "resnet_prediction": "<class>",
        "resnet_confidence": 0.93,
        "densenet_prediction": "<class>",
        "densenet_confidence": 0.95,
        "top5": [("<class>", 0.94), ...]
      }
    """
    _load_models()

    arr = _preprocess(image_input)

    resnet_probs = _models["resnet"].predict(arr, verbose=0)[0]
    densenet_probs = _models["densenet"].predict(arr, verbose=0)[0]

    # Ensemble: simple average
    ensemble_probs = (resnet_probs + densenet_probs) / 2

    top_idx = int(np.argmax(ensemble_probs))
    top_conf = float(ensemble_probs[top_idx])

    # Top 5
    top5_idx = np.argsort(ensemble_probs)[::-1][:5]
    top5 = [(CLASS_NAMES[i], float(ensemble_probs[i])) for i in top5_idx]

    return {
        "disease": CLASS_NAMES[top_idx],
        "confidence": top_conf,
        "resnet_prediction": CLASS_NAMES[int(np.argmax(resnet_probs))],
        "resnet_confidence": float(np.max(resnet_probs)),
        "densenet_prediction": CLASS_NAMES[int(np.argmax(densenet_probs))],
        "densenet_confidence": float(np.max(densenet_probs)),
        "top5": top5,
    }


if __name__ == "__main__":
    # Quick test with a real image from the dataset
    import sys
    test_img = sys.argv[1] if len(sys.argv) > 1 else \
        "data/plantvillage/raw/color/Tomato___Early_blight/" + \
        os.listdir("data/plantvillage/raw/color/Tomato___Early_blight")[0]

    print(f"Testing: {test_img}\n")
    result = predict(test_img)
    print(f"Disease:    {result['disease']}")
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print(f"\nModel breakdown:")
    print(f"  ResNet50: {result['resnet_prediction']} ({result['resnet_confidence']*100:.1f}%)")
    print(f"  DenseNet: {result['densenet_prediction']} ({result['densenet_confidence']*100:.1f}%)")
    print(f"\nTop 5:")
    for name, prob in result["top5"]:
        print(f"  {prob*100:5.1f}%  {name}")