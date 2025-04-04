from fastapi import FastAPI, HTTPException
import numpy as np # Charger le modèle
from typing import List
from dataprediction.model_prediction import predict_text
TEXT_SAMPLE="Hello, this is a sample text for prediction."
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI !"}

@app.get("/predict")
def predict_text_endpoint():
    try:
        dictionary = predict_text(TEXT_SAMPLE,0.5)
        if dictionary["score"] > 0.5:
            return {"message": "FAKE NEWS"}
        else:
            return {"message": "REAL NEWS"}
    except Exception as e:
        print(e)


