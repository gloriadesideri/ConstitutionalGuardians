from fastapi import FastAPI, APIRouter
import uvicorn
from model import Model
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()
app = FastAPI() 
model_name = os.getenv("MODEL_NAME")
model= Model(model_name)

@router.get('/predict')
async def home():
    return {"message": "Welcome to the model API"}

@router.post('/predict')
async def data(data: str):
    try:
        prediction = model.generate(data)
        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "An error occurred"}
@router.porst('/predict_batch')
async def data(data: list):
    try:
        predictions = []
        for d in data:
            prediction = model.generate(d)
            predictions.append(prediction)
        return {"predictions": predictions}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": "An error occurred"}
app.include_router(router)

if __name__== "__main__":
    uvicorn.run("app:app", roload=True, port =6000, host='0.0.0.0')

