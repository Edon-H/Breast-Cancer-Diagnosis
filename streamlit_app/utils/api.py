import requests

def send_image_for_prediction(api_url, uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(f"{api_url}/predict", files=files)
        return response
    except Exception as e:
        return e
