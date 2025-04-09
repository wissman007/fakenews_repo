from fastapi import FastAPI, HTTPException
import numpy as np # Charger le modèle
from pydantic import BaseModel
from typing import List
from dataprediction.model_prediction import predict_text
app = FastAPI()

class InputDict(BaseModel):
    id_news: str
    date_reference: str
    title: str
    url: str
    author: str
    source: str
    official_title: str
    real_content: str
    scrapping_status: str
    
    # Option
    score: float = None
    
    class Config:
        extra = "forbid"  # Avoid extra fields

class TextRequest(BaseModel):
    listdict: List[InputDict]

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI !"}

@app.post("/predict")
def predict_text_endpoint(request: TextRequest):
    result = []
    for item in request.listdict:
        try:
            input_text = item.real_content
            
            # Call to the model
            prediction = predict_text(input_text, threshold=0.5)
            
            # New dict with the prediction and all other keys
            item_dict = item.model_dump()
            item_dict["score"] = float(prediction["score"])
            result.append(item_dict)
            
        except Exception as e:
            # Error handling
            print(f"Error while treating: {e}")
            raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")
    
    return result


