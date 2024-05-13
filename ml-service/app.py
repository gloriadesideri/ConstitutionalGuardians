from fastapi import FastAPI, APIRouter
import uvicorn
from model import Model
import logging
import os
from dotenv import load_dotenv
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
load_dotenv()
app = FastAPI() 
router = APIRouter()
model_name = os.getenv("MODEL_NAME")
model = Model(model_name)  # Initialize the model outside of request handlers

class Item(BaseModel):
    name: str

@router.get('/predict')
async def home():
    return {"message": "Welcome to the model API"}



@router.post('/generate')
async def generate_data(item: Item):
    try:
        return {"message": model.generate(item.name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("app:app", port=6000, host='0.0.0.0')

# @router.post('/predict')
# async def data(data: str):
#     try:
#         prediction = Classifier.generate_and_get_response_severity(data)
#         return {"prediction": prediction["response"], "severity": prediction.severity}
#     except Exception as e:
#         logging.error(f"Error: {e}")
#         return {"error": "An error occurred"}

# @router.post('/predict_batch')
# async def data(data: list):
#     try:
#         predictions = []
#         severity = []
#         for d in data:
#             prediction = Classifier.generate_and_get_response_severity(d)
#             predictions.append( prediction["response"] )
#             severity.append( prediction["severity"] )
#         return {"predictions": predictions, "severity": severity}
#     except Exception as e:
#         logging.error(f"Error: {e}")
#         return {"error": "An error occurred"}
# app.include_router(router)


