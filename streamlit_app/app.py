import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.api import send_image_for_prediction
import base64

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

dna_base64 = get_base64_image("assets/background/dna.png")
microscope_base64 = get_base64_image("assets/background/microscope.png")
beaker_base64 = get_base64_image("assets/background/beaker.png")
logo_base64 = get_base64_image("assets/background/logo-2.png")

def render_member(member):
    img_base64 = base64.b64encode(open(member['image'], "rb").read()).decode()
    return f"""
        <div class="team-card">
            <img src="data:image/jpeg;base64,{img_base64}" class="team-img">
            <div class="team-name">{member['name']}</div>
            <div class="team-role">{member['role']}</div>
        </div>
    """

# Load CSS
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# App setup

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []
if "show_project_info" not in st.session_state:
    st.session_state.show_project_info = False




st.set_page_config(page_title='Breast Cancer Diagnosis', layout='centered')
load_dotenv()
load_css()

# GitHub link + info inside .stApp
st.markdown("""
    <div class="stapp-github-container">
        <a href="https://github.com/HarshvardhanRathore/your-repo" target="_blank" title="View on GitHub">
            <svg class="github-icon" xmlns="http://www.w3.org/2000/svg" fill="#8B004D" viewBox="0 0 24 24">
                <path d="M12 .3C5.37.3 0 5.67 0 12.3c0 5.29 3.438 9.777 8.205 11.387.6.111.82-.26.82-.577
                0-.285-.011-1.04-.017-2.04-3.338.726-4.042-1.614-4.042-1.614
                -.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.082-.729.082-.729
                1.205.084 1.84 1.237 1.84 1.237 1.07 1.834 2.809 1.304 3.495.997
                .108-.775.418-1.304.762-1.604-2.665-.305-5.467-1.334-5.467-5.932
                0-1.311.469-2.382 1.236-3.221-.124-.303-.536-1.527.117-3.176
                0 0 1.008-.322 3.3 1.23a11.48 11.48 0 0 1 3.003-.404
                c1.02.005 2.047.138 3.003.404 2.291-1.552 3.297-1.23 3.297-1.23
                .655 1.649.243 2.873.12 3.176.77.839 1.235 1.91 1.235 3.221
                0 4.61-2.807 5.624-5.48 5.921.43.371.823 1.103.823 2.222
                0 1.606-.014 2.899-.014 3.293 0 .32.216.694.825.576
                C20.565 22.073 24 17.592 24 12.3 24 5.67 18.63.3 12 .3z"/>
            </svg>
        </a>
    </div>
""", unsafe_allow_html=True)

   
st.markdown(f"""
<div class="background-lab-icons">
    <img src="data:image/png;base64,{dna_base64}" class="lab-icon float1" style="top: 5%; left: 5%; width: 150px;">
    <img src="data:image/png;base64,{microscope_base64}" class="lab-icon float2" style="top: 15%; left: 95%; width: 90px;">
    <img src="data:image/png;base64,{beaker_base64}" class="lab-icon float3" style="top: 75%; left: 15%; width: 100px;">
    <img src="data:image/png;base64,{logo_base64}" class="lab-icon float3" style="top: 75%; left: 75%; width: 150px;">
    <img src="data:image/png;base64,{dna_base64}" class="lab-icon float3" style="top: 50%; left: 85%; width: 200px;">
    <img src="data:image/png;base64,{microscope_base64}" class="lab-icon float3" style="top: 35%; left: 10%; width: 170px;">
    <img src="data:image/png;base64,{beaker_base64}" class="lab-icon float3" style="top: 5%; left: 80%; width: 150px;">
    <img src="data:image/png;base64,{logo_base64}" class="lab-icon float3" style="top: 65%; left: 5%; width: 100px;">
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([5, 4, 4])
with col2:# Logo (optional)
    st.image("assets/breast-cancer-vector.png", width=200)

# Title and description
st.markdown("<h1 class='main-title'>Breast Cancer Diagnosis</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>The Sooner You Know, The Safer You Are</p>", unsafe_allow_html=True)

st.markdown("<p class='sub-title'>Upload a histopathology image to get an instant prediction</p>", unsafe_allow_html=True)


# Upload image
# 🔄 Image Upload
if st.session_state.uploaded_file is None:
    uploaded = st.file_uploader("📤 Upload a PNG image", type="png")
    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.rerun()
else:
    uploaded_file = st.session_state.uploaded_file
    image = Image.open(uploaded_file)
    
    st.success("✅ Image uploaded successfully!")
    col01, col02 = st.columns([1, 1])
    with col01:
        st.image(image, width=250)

    # 🚀 Predict or 🔁 New Prediction
    if st.session_state.prediction_result is None:
        if st.button("🔍 Predict"):
            with st.spinner("🧬 Analyzing the image..."):
                API_URL = os.getenv("API_URL")
                response = send_image_for_prediction(API_URL, uploaded_file)

                if isinstance(response, Exception):
                    with col02:
                        st.error(f"🚨 API Error: {response}")
                elif response.status_code == 200:
                    with col02:
                        result = response.json()
                        st.session_state.prediction_result = result
                        st.rerun()
                else:
                    with col02:
                        st.error(f"❌ Error {response.status_code}: Could not get prediction.")
    else:
        # ✅ Show Result
        with col02:
            result = st.session_state.prediction_result
            st.success(f"✅ Prediction: {result['predicted_class']}")
            st.info(f"📊 Probability: {result['probability']}")

        # 🔁 Reset
        if st.button("🔁 New Prediction"):
            # Save current to history
            st.session_state.prediction_history.append({
                "filename": st.session_state.uploaded_file.name,
                "image": st.session_state.uploaded_file.getvalue(),
                "predicted_class": st.session_state.prediction_result["predicted_class"],
                "probability": st.session_state.prediction_result["probability"]
            })
            # Reset for new input
            st.session_state.uploaded_file = None
            st.session_state.prediction_result = None
            st.rerun()

if st.session_state.prediction_history:
    st.markdown("<hr><h3 style='color: #8B004D;'>Previous Predictions</h3>", unsafe_allow_html=True)

    history = list(reversed(st.session_state.prediction_history))

    for i in range(0, len(history), 2):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        # Left side (first in pair)
        item1 = history[i]
        with col1:
            st.image(item1["image"], width=100)
        with col2:
            st.markdown(f"**Prediction {len(history)-i}:** {item1['predicted_class']}")
            st.markdown(f"**Probability:** {item1['probability']}")

        # Right side (second in pair, if exists)
        if i + 1 < len(history):
            item2 = history[i + 1]
            with col3:
                st.image(item2["image"], width=100)
            with col4:
                st.markdown(f"**Prediction {len(history)-(i+1)}:** {item2['predicted_class']}")
                st.markdown(f"**Probability:** {item2['probability']}")

        # Horizontal line across the row (optional, full width)
        st.markdown("<hr>", unsafe_allow_html=True)



team = [
    {"name": "Edon", "role": "Chief Diagnostician", "image": "assets/team/edon.png"},
    {"name": "Liam", "role": "Data Whisperer", "image": "assets/team/liam.png"},
    {"name": "Elise", "role": "Model Magician", "image": "assets/team/elise.png"},
    {"name": "Rudolph", "role": "Ops Overlord", "image": "assets/team/rudolph.png"},
    {"name": "Harsh", "role": "Pipeline Plumber", "image": "assets/team/harsh.png"},
]

st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([5, 4, 5])
with col2:
    if st.button("About the Project", key="about_project_btn", use_container_width=True):
        st.session_state.show_project_info = not st.session_state.show_project_info


if st.session_state.get("show_project_info", False):
    with open("assets/project_info.md", "r") as md_file:
        md_content = md_file.read()

    st.markdown("<h3 style='text-align:center; color:#8B004D;'>Project Overview</h3>", unsafe_allow_html=True)

  
        #st.image("assets/project-image.png", use_container_width=True)  # Optional banner image
        # Embed markdown content inside styled div
    st.markdown(f"<div class='project-description'>{md_content}</div>", unsafe_allow_html=True)



st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)
       
# Header
col1, col2, col3 = st.columns([5, 3, 5])
with col2:
    if st.button("Meet the Team", use_container_width=True):
        st.session_state.show_team = not st.session_state.get("show_team", False)

if st.session_state.get("show_team", False):
    cols_top = st.columns(3)
    for col, member in zip(cols_top, team[:3]):
        with col:
            st.markdown(render_member(member), unsafe_allow_html=True)

    # Row 2: center 2 members
    cols_bottom = st.columns([1, 1, 1, 1, 1])  # 5 cols for spacing
    for idx, member in enumerate(team[3:]):
        with cols_bottom[1 + idx*2]:  # Place in 2nd and 4th columns
            st.markdown(render_member(member), unsafe_allow_html=True)
        
# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p>🧠 Powered by <strong>Deep Learning</strong> & <strong>FastAPI</strong> | 💻 Built with <strong>Streamlit</strong></p>
    <p>Made with ❤️ by <strong>Team BCD</strong> | <a href="https://github.com/HarshvardhanRathore/your-repo" target="_blank">GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)

