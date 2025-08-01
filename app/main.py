from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from io import BytesIO
from datetime import datetime
from typing import List

session_logs: List[dict] = []

app = FastAPI()

model = load_model("model/model.keras")
IMG_SIZE = 256

@app.get("/")
def root():
    return {"message": "Welcome to the Breast Cancer Prediction API!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image = image.resize((IMG_SIZE, IMG_SIZE))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        prediction = model.predict(image_array)
        benign_prob, malignant_prob = float(prediction[0][0]), float(prediction[0][1])

        predicted_class = "Malignant" if malignant_prob > benign_prob else "Benign"
        probability = round(max(benign_prob, malignant_prob), 4)
        
        # Store in session log
        session_logs.append({
            "filename": file.filename,
            "predicted_class": predicted_class,
            "probability": probability,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "predicted_class": predicted_class,
            "probability": probability
        }

    except Exception as e:
        return {"error": str(e)}
