import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Générer des données factices (vecteurs numériques représentant des articles)
np.random.seed(42)
X = np.random.rand(1000, 4)  # 1000 articles avec 4 features (ex: TF-IDF, embeddings)
y = np.random.randint(0, 2, size=(1000,))  # 0 = Vraie news, 1 = Fake news

# Séparer en données d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Définition du modèle Keras
model = keras.Sequential([
    keras.layers.Input(shape=(4,)),  # 4 features en entrée
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # 1 sortie (probabilité Fake News)
])

# Compilation du modèle
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Sauvegarde du modèle
model.save("dataprediction/fake_news_classifier.keras")

print("✅ Modèle entraîné et sauvegardé !")
