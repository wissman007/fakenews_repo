from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np # Charger le modèle
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI !"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

#MODEL_PATH = "dataprediction/fake_news_classifier.keras"
#model = tf.keras.models.load_model(MODEL_PATH)
#
#class PredictionInput(BaseModel):
#    data: List[List[float]] = Field(..., example=[[0.8, 0.2, 0.6, 0.1]])
#
#@app.post("/predict")
#def predict(input_data: PredictionInput):
#    try:
#        # Conversion en tableau NumPy
#        input_array = np.array(input_data.data)
#
#        # Vérifier que les données ont la bonne forme
#        if input_array.ndim != 2:
#            raise ValueError("Les données doivent être une liste de listes (matrice 2D).")
#
#        # Prédiction
#        predictions = model.predict(input_array)
#        results = [int(pred[0] > 0.5) for pred in predictions]  # 0 ou 1
#
#        return {"predictions": results}
#
#    except Exception as e:
#        raise HTTPException(status_code=400, detail=str(e))

