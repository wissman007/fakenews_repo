from fastapi import FastAPI, HTTPException
import numpy as np # Charger le modèle
from pydantic import BaseModel
from typing import List
from dataprediction.model_prediction import predict_text
app = FastAPI()

class TextRequest(BaseModel):
    text: str 

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI !"}

@app.post("/predict")
def predict_text_endpoint(request: TextRequest):
    input_text = request.text
    try:
        dictionary = predict_text(input_text,threshold=0.5)
        prediction = dictionary["score"]
        if prediction > 0.5:
            prediction_label="REAL NEWS"
        else:
            prediction_label="FAKE NEWS"
        return {
            "text": input_text,
            "prediction": prediction_label,
            "score": float(prediction)
        }
    except Exception as e:
        print(e)


