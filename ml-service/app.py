from fastapi import FastAPI, APIRouter
import uvicorn
from model import Model
import logging
import os
from dotenv import load_dotenv
from classifier import Classifier

logging.basicConfig(level=logging.INFO)
load_dotenv()
app = FastAPI() 
router = APIRouter()
model_name = os.getenv("MODEL_NAME")
model= Model(model_name)
clssifier = Classifier()

@router.get('/predict')
async def home():
    return {"message": "Welcome to the model API"}

@router.post('/predict')
async def data(data: str):
    try:
        prediction = Classifier.generate_and_get_response_severity(data)
        return {"prediction": prediction["response"], "severity": prediction.severity}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "An error occurred"}

@router.post('/predict_batch')
async def data(data: list):
    try:
        predictions = []
        severity = []
        for d in data:
            prediction = Classifier.generate_and_get_response_severity(d)
            predictions.append( prediction["response"] )
            severity.append( prediction["severity"] )
        return {"predictions": predictions, "severity": severity}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "An error occurred"}
app.include_router(router)

if __name__== "__main__":
    uvicorn.run("app:app", reload=True, port =6000, host='0.0.0.0')

