import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFBertForSequenceClassification

def predict_text(text, threshold=0.5):
    """
    Prédiction sur un texte donné avec le modèle NLP chargé.
    :param text: Texte à analyser
    :param threshold: Seuil de classification (0.5 par défaut)
    :return: Score de probabilité et classe (Fake News ou Non)
    """
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained('src/dataprediction/tokenizer')
    max_len = 120

    # Load in HDF5 format 
    tf.keras.utils.get_custom_objects().update({
        'TFBertForSequenceClassification': TFBertForSequenceClassification
    })
    loaded_model = tf.keras.models.load_model("src/dataprediction/model/fakenews_prediction_model.h5")
    
    # Tokenisation
    tokenized_input = tokenizer(text,
                            max_length=max_len,
                            padding="max_length",  
                            truncation=True,
                            add_special_tokens=True,
                            return_token_type_ids=False,
                            return_attention_mask=True,
                            return_tensors='tf')
       
    # Prédiction
    prediction = loaded_model(tokenized_input)
   
    # Récupération des logits
    scores = tf.nn.sigmoid(prediction).numpy()

    # Conversion en classe binaire
    predicted_class = (scores > threshold).astype(float)

    return {"score": scores[0][0], "prediction": "FAKE NEWS" if predicted_class[0][0] == 0 else "REAL NEWS"}

if __name__ == "__main__":
    # Exemple d'utilisation
    text_sample = "Hello, this is a sample text for prediction."
    result = predict_text(text_sample)
    print(result)
