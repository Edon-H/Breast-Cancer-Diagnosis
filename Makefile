# Install dependencies
install:
	pip install -r requirements.txt

# Run inside the app directory
test-api:
	uvicorn app.main:app --reload

# Run inside the streamlit_app directory
test-streamlit:
	streamlit run app.py
