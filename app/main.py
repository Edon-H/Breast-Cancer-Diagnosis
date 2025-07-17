from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from io import BytesIO

app = FastAPI()

# Loads the trained model
model = load_model("model/model.keras")

# Should match the input size used during model training
IMG_SIZE = 256

@app.get("/")
def root():
    return {"message": "Welcome to the Breast Cancer Prediction API!"}

# Creates an endpoint for image upload and prediction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess the image
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image = image.resize((IMG_SIZE, IMG_SIZE))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Get prediction probabilities
        prediction = model.predict(image_array)
        benign_prob, malignant_prob = float(prediction[0][0]), float(prediction[0][1])

        # Determine class
        predicted_class = "Malignant" if malignant_prob > benign_prob else "Benign"
        probability = round(max(benign_prob, malignant_prob), 4)

        return {
            "predicted_class": predicted_class,
            "probability": probability
        }

    except Exception as e:
        return {"error": str(e)}
