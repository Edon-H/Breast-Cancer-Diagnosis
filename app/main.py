from fastapi import FastAPI
app = FastAPI()
# Testing
@app.get('/')
def root():
    return 'Benign: 77%'
