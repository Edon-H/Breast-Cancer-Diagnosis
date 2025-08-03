# 🧬 Breast Cancer Diagnosis App

This project is a full-stack AI-powered web application that helps doctors and researchers diagnose breast cancer from histopathology images. It leverages Convolutional Neural Networks (CNNs), a FastAPI backend for inference, and a user-friendly Streamlit frontend.

---

## 📌 Project Objective

Breast cancer is one of the most prevalent cancers globally. Early detection can drastically improve treatment outcomes. This project uses deep learning models to automate cancer detection from histopathology slides, making diagnosis faster, more accurate, and accessible even in remote areas.

---

## 🧠 How It Works

The system consists of:

- ✅ A trained CNN model (VGG16)
- 🎯 A FastAPI backend that handles predictions
- 🌐 A Streamlit frontend for uploading images and receiving results
- ☁️ Google Cloud hosting and deployment using Docker

---

## 🚀 Features

- Upload histopathology images via a web interface
- Receive instant prediction (Benign or Malignant)
- See model confidence score
- All hosted securely on Google Cloud

---

## ⚙️ Deployment Guide (GCP + Docker)

### ✅ Authenticate Google Cloud CLI and Docker

```bash
#Log in into your Google Cloud
gcloud auth login
gcloud auth configure-docker

# 💳 Link Billing to Your GCP Project
gcloud beta billing accounts list

gcloud beta billing projects link YOUR_PROJECT_ID \
  --billing-account=YOUR_BILLING_ACCOUNT_ID

# 🛠 Set your project and enable required APIs
gcloud config set project YOUR_PROJECT_ID

# Enable required GCP services
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable containerregistry.googleapis.com
```
# 🐳 Build Docker Image
 First you can **test** it locally by creating a `docker-compose.yml` file:
```bash
services:
  backend:
    build:
      context: ./app
      dockerfile: Dockerfile
    # TODO: At .env file, put GCP_PROJECT_ID=YOUR_PROJECT_NAME
    image: gcr.io/${GCP_PROJECT_ID}/breast-cancer-backend
    container_name: breast-cancer-backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    command: uvicorn main:app --host "0.0.0.0"
  frontend:
    build:
      context: ./streamlit_app
      dockerfile: Dockerfile
    image: gcr.io/${GCP_PROJECT_ID}/breast-cancer-frontend
    container_name: breast-cancer-frontend
    ports:
      - "8501:8501"
    environment:
      - PORT=8501
      - API_URL=http://backend:8000
    command: streamlit run app.py --server.port 8501 --server.address=0.0.0.0
```
---
Then run in terminal:
```bash
 docker-compose --env-file .env up --build
```


---
⚠️ Now that testing is done, delete all previously built images from *`Docker Desktop`* application and manually rebuild the backend image within the `app` directory to avoid deployment issues.

```bash
# The image needs to be named gcr.io/... so the Google Services recognizes it

# This works only for macOS Apple M1+ versions
docker buildx build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/breast-cancer-backend .

# This works for Windows
docker build -t gcr.io/YOUR_PROJECT_ID/breast-cancer-backend .
```
---
From `root` directory, push your image into Google Container Registry and deploy it into Google Cloud Run.
```bash
# 🚀 Push Docker Image to GCR
docker push gcr.io/YOUR_PROJECT_ID/breast-cancer-backend

# 🚀 Deploy to Google Cloud Run
gcloud run deploy breast-cancer-backend \
  --image gcr.io/YOUR_PROJECT_ID/breast-cancer-backend \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi
```
After deployment, note the URL shown. It will look like:
```bash
https://breast-cancer-backend-xxxx.a.run.app
```
You can then use this in your `streamlit_app/.env` file:
```bash
API_URL=https://breast-cancer-backend-xxxx.a.run.app
```
### 🚨🚨 Repeat the same process for the `streamlit_app` (frontend) until you get the deployed URL and use it online. 🚨🚨
