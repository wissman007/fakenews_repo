import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

# Chargement du modèle et du tokenizer
tokenizer = AutoTokenizer.from_pretrained('dataprediction/tokenizer')
max_len = 512
loaded_model = TFAutoModelForSequenceClassification.from_pretrained('dataprediction/model')
# Chargement du tokenizer
def predict_text(text, threshold=0.5):
    """
    Prédiction sur un texte donné avec le modèle NLP chargé.
    :param text: Texte à analyser
    :param threshold: Seuil de classification (0.5 par défaut)
    :return: Score de probabilité et classe (Fake News ou Non)
    """
    # Tokenisation
    tokenized_input = tokenizer(text=text,
                                max_length=max_len,
                                padding="max_length",
                                truncation=True,
                                return_tensors='tf')

    # Prédiction
    prediction = loaded_model(tokenized_input)

    # Application de la fonction sigmoid (si nécessaire)
    scores = tf.nn.sigmoid(prediction.logits).numpy()

    # Conversion en classe binaire
    predicted_class = (scores > threshold).astype(int)

    return {"score": scores[0][0], "prediction": "FAKE NEWS" if predicted_class[0][0] == 0 else "REAL NEWS"}

if __name__ == "__main__":
    # Exemple de texte à analyser
    sample_text = "Ireland is the latest European country moving to update their travel advice for the United States for its citizens traveling to the country." \
    "The government's website issued guidance for transgender travelers, saying that U.S. ESTA and visa application forms require travelers to declare their sex, which should reflect their biological sex at birth. Travelers with an  marker on their passport or whose gender differs from the one assigned at birth are advised to contact the U.S. Embassy in Dublin for further information on specific entry requirements." \
    "Why It Matters " \
    "This move comes after similar updates from other European countries, such as Finland, Denmark, the UK, and Germany, seemingly in response to President Donald Trump's broad crackdown on illegal immigration and transgender rights." \
    "Since returning to the White House, Trump has enacted a series of executive orders rolling back rights for transgender and nonbinary individuals. On his first day back in office, he signed an order declaring that the government would recognize only two genders: male and female."
    
    # Appel de la fonction de prédiction
    result = predict_text(sample_text)

    # Affichage des résultats
    print(f"Texte: {sample_text}")
    print(f"Score: {result['score']}")
    print(f"Prédiction: {result['prediction']}")