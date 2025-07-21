install:
	pip install -r requirements.txt

run-api:
	uvicorn app.main:app --reload

run-streamlit:
	streamlit run streamlit_app/app.py

docker-build:
# For MacOS Apples M1 u need to use buildx, otherwise you use build
	docker buildx build --platform linux/amd64 -t breast-cancer-api .
# docker build -t breast-cancer-api .

docker-run-api:
	docker run -p 8080:8080 breast-cancer-api
