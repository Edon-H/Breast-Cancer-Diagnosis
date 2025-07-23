
# ✅ Authenticate Google Cloud CLI and Docker

gcloud auth login                       # Log in to your Google Cloud account
gcloud auth configure-docker           # Configure Docker to push to Google Container Registry (GCR)

# 💳 Link Billing to Your GCP Project

gcloud beta billing accounts list      # Get your BILLING_ACCOUNT_ID

gcloud beta billing projects link YOUR_PROJECT_ID \
  --billing-account=YOUR_BILLING_ACCOUNT_ID    # Link your project to billing

# 🛠 Set your project and enable required APIs

gcloud config set project YOUR_PROJECT_ID       # Set your active GCP project

# Enable required GCP services
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 🐳 Build Docker Image

# Option A: Build for local testing (Apple Silicon/M1 or general)
docker buildx build --platform linux/amd64 -t breast-cancer-backend .

# Option B: Standard build (default platform)
docker build -t breast-cancer-backend .


# 🏷 Tag the Docker image for Google Cloud


# Tag your image so GCP recognizes it (change PROJECT_ID)
docker tag breast-cancer-backend gcr.io/YOUR_PROJECT_ID/breast-cancer-backend

# OR: Build directly with the correct GCP tag (recommended)
docker buildx build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/breast-cancer-backend .


# 🚀 Push Docker Image to Google Container Registry (GCR)


docker push gcr.io/YOUR_PROJECT_ID/breast-cancer-backend


# 🚀 Deploy to Google Cloud Run


gcloud run deploy breast-cancer-backend \
  --image gcr.io/YOUR_PROJECT_ID/breast-cancer-backend \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi   # You can increase to 4Gi/8Gi if needed for TensorFlow

## After deployment, note the URL shown. It will look like:
### https://breast-cancer-backend-xxxx.a.run.app

## You can then use this in your front-end `.env` file:
### API_URL=https://breast-cancer-backend-xxxx.a.run.app
