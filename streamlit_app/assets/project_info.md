
<h2 class='sub-title'>🧬 Breast Cancer Diagnosis App </h2>

This interactive web application enables users to upload histopathology images and receive an instant prediction on whether the sample is **benign** or **malignant**, using a deep learning model trained on histopathology image data.

---

## 📌 Objective

Breast cancer is one of the most prevalent cancers in the world. Early detection can significantly improve treatment outcomes. This project uses **Convolutional Neural Networks (CNNs)** to automate cancer detection from histopathology slides.

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|--------------------------|
| Frontend   | Streamlit                |
| Backend    | FastAPI                  |
| Model      | TensorFlow / Keras (CNN, VGG16)|
| Deployment | Docker & Cloud Cloud Run|
| Storage    | Session-based / In-Memory |

---

## 🔬 How It Works

1. **Upload** a histopathology image (PNG format).
2. The image is sent to a **FastAPI backend** hosted on Cloud Run.
3. The backend preprocesses the image and runs inference using a trained **CNN/VGG16 model**.
4. The prediction (Benign / Malignant) and confidence score are returned and displayed.
5. Prediction history is stored in **memory** per **session** (Streamlit session state).

---

## 📊 Model Performance

- Model: VGG16 (Transfer Learning) with 3 convolutional layers
- Image Size: 128 x 128
- Accuracy: **93.4%**
- Loss: 0.17

### 📈 Metrics Graphs

![Confusion Matrix](assets/team/bob.png)
*Confusion matrix showing true positives and negatives.*

![Training Curve](assets/team/bob.png)
*Model training and validation accuracy over epochs.*

---

## 🌐 Backend API

You can also directly access the model's API:

- **Root Endpoint:**
  `GET /`
  Returns a welcome message

- **Predict Endpoint:**
  `POST /predict`
  Accepts a PNG file and returns a prediction

- **History (optional):**
  `GET /history`
  Returns all predictions from the current session

Example API call (Python):
```python
import requests

with open("test_image.png", "rb") as f:
    res = requests.post("http://localhost:8000/predict", files={"file": f})
    print(res.json())
