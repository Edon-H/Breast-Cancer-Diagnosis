import streamlit as st
from PIL import Image
import requests
import os
from dotenv import load_dotenv

st.set_page_config(page_title='Breast Cancer Diagnosis')

st.title("🧠 Breast Cancer Predictor")
st.write("Upload a histopathology image to get a prediction.")

# Loads the API URL from the .env file
load_dotenv()
API_URL = os.getenv("API_URL")

# Upload the image (PNG)
uploaded_file = st.file_uploader("📤 Upload a PNG image", type="png")

if uploaded_file is not None:

    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼 Uploaded Image", use_container_width=True)
    st.success("✅ Image uploaded successfully!")

    # Add a button to trigger prediction
    if st.button("🔍 Predict"):
        st.info("📡 Sending request to the API...")

        try:
            # Send POST request to FastAPI
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{API_URL}/predict", files=files)

            # Handles the response
            if response.status_code == 200:
                result = response.json()
                st.success(f"🧪 Prediction: **{result['predicted_class']}**")
                st.write(f"🔢 Probability: **{result['probability']}**")
            else:
                st.error(f"❌ API returned an error: {response.status_code}")

        except Exception as e:
            st.error(f"🚨 Failed to connect to API: {e}")
