import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFBertForSequenceClassification

# Chargement du modèle et du tokenizer
tokenizer = AutoTokenizer.from_pretrained('datapredection_new/model/tokenizer_trained')
max_len = 120
# Load in HDF5 format (alternative)
tf.keras.utils.get_custom_objects().update({
    'TFBertForSequenceClassification': TFBertForSequenceClassification
})
loaded_model = tf.keras.models.load_model("datapredection_new/model/fakenews_prediction_model.h5")
# Chargement du tokenizer


# Chargement du tokenizer
def predict_text(text, threshold=0.5):
    """
    Prédiction sur un texte donné avec le modèle NLP chargé.
    :param text: Texte à analyser
    :param threshold: Seuil de classification (0.5 par défaut)
    :return: Score de probabilité et classe (Fake News ou Non)
    """
    # Tokenisation
    tokenized_input = tokenizer(text,
                            max_length=max_len,
                            padding="max_length",  # Ensures the input is padded to max_len
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
    # Affichage des résultats
    print(f"Scores: {scores}")
    print(f"Classe prédite: {predicted_class}")

    return {"score": scores[0][0], "prediction": "FAKE NEWS" if predicted_class[0][0] == 0 else "REAL NEWS"}


if __name__ == "__main__":
    # Exemple de texte à analyser
    sample_text = "Ireland is the latest European country moving to update their travel advice for the United States for its citizens traveling to the country." \
    "The government's website issued guidance for transgender travelers, saying that U.S. ESTA and visa application forms require travelers to declare their sex, which should reflect their biological sex at birth. Travelers with an  marker on their passport or whose gender differs from the one assigned at birth are advised to contact the U.S. Embassy in Dublin for further information on specific entry requirements." \
    "Why It Matters " 
    # Appel de la fonction de prédiction
    result = predict_text(sample_text)

    # Affichage des résultats
    print(f"Texte: {sample_text}")
    print(f"Score: {result['score']}")
    print(f"Prédiction: {result['prediction']}")