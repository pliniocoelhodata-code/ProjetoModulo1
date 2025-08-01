import joblib
import numpy as np
import os

def predict_book(features) -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # pega o caminho absoluto de ml/
    model_path = os.path.join(base_dir, "model.joblib")    # ml/model.joblib

    if not os.path.exists(model_path):
        raise ValueError("Modelo não encontrado. Rode train_model.py primeiro.")
    
    model = joblib.load(model_path)

    # Codificar a disponibilidade
    availability_map = {"In stock": 1, "Out of stock": 0}
    availability_encoded = availability_map.get(features.availability.strip(), 0)

    input_array = np.array([[features.price, features.rating, availability_encoded]])
    return int(model.predict(input_array)[0])
