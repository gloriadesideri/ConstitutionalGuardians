from http.client import HTTPException
from fastapi import FastAPI, APIRouter, UploadFile
import uvicorn
from models.chat_agent import ChatAgent
import logging
import os
from dotenv import load_dotenv
from pydantic import BaseModel
# import json
import json
import pandas as pd
from io import BytesIO



logging.basicConfig(level=logging.INFO)
load_dotenv()
app = FastAPI() 
router = APIRouter()
agent = None  # Initialize the model outside of request handlers

#available models
available_models = ['google/flan-t5-base']

# body classes
class MessageData(BaseModel):
    message: str
    
class ModelData(BaseModel):
    principle_name: str
    model_name: str
    protection: str
    
# getters

# get available models to test
@router.get('/models')
async def get_models():
    return {"models": available_models}


# get implemented principles
@app.get("/principles")
async def get_principles():
    with open("./ml-service/config.json", "r") as file:
        data = json.load(file)
        principles_dict = {key: value["description"] for key, value in data.items()}
    return principles_dict

# get protections implemented for a principle
@app.get("/protections/{principle}")
async def get_protections(principle: str):
    with open("./ml-service/config.json", "r") as file:
        data = json.load(file)
        protections = data[principle]["protections_level_implemented"]
    return protections
    

# instantiate disembodied agent
@app.post("/instantiate-model")
async def instantiate_model(item: ModelData):
    global agent
    agent = ChatAgent(item.principle_name, item.model_name, item.protection)
    # Store model_instance or do further processing
    return {"message": "Model instantiated successfully"}

# chat with instantiated model
@app.post("/chat")
async def chat_with_model(message: MessageData):
    if agent is None:
        raise HTTPException(status_code=500, detail="Model not instantiated")
    try:
        response = agent.generate(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# take a csv of messages and chat with instantiated model
@app.post("/chat/csv")
async def chat_with_model_csv(file: UploadFile):
    if agent is None:
        raise HTTPException(status_code=500, detail="Model not instantiated")
    
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        
        if 'Agent' not in df.columns or 'Message' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'Agent' and 'Message' columns")
        
        # Filter messages where Agent is 'Human'
        human_messages = df[df['Agent'] == 'Human']['Message'].tolist()
        
        # Interact with the chat model for each human message
        responses = {}
        for i, message in enumerate(human_messages):
            response = agent.generate(message)  # Replace with your model's chat method
            responses[f"message_{i}"] = {
                "input": message,
                "response": response
            }
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# reset instantiated model
@app.get("/reset-model")
async def reset_model():
    if agent is None:
        raise HTTPException(status_code=500, detail="Model not instantiated")
    try:
        agent.reset_memory()
        return {"message": "Memory reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("app:app", port=6000, host='0.0.0.0')




