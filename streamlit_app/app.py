import streamlit as st
from PIL import Image
import requests

st.set_page_config(page_title= 'Breast Cancer Diagnosis')

st.title("🧠 Breast Cancer Predictor")
st.write("Upload a histopathology image to get a prediction.")

# Later we will create a .env file and store the API there for safety
API_URL = 'http://127.0.0.1:8000'

# Upload the image, limited formats allowed
uploaded_file = st.file_uploader("📤 Upload a PNG, JPG or JPEG image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Shows the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("✅ Image uploaded successfully!")

    # Gets the API request
    response = requests.get(API_URL)

    if response.status_code == 200:
        result = response.json()
        st.success(result)
    else:
        st.error('Check API!')
