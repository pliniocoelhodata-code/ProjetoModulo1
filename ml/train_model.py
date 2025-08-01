import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

def main():
    # 1. Carregar dados da API
    url = "http://127.0.0.1:8000/api/v1/ml/training-data"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

    # 2. Pré-processamento
    df["availability"] = df["availability"].apply(lambda x: 1 if x == "In stock" else 0)
    X = df[["price", "rating", "availability"]]
    y = df["popular"]

    # 3. Dividir os dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Treinar modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Avaliar
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.2f}")

    # 6. Salvar modelo na mesma pasta do script train_model.py (ou seja, dentro da pasta ml/)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # caminho absoluto da pasta ml/
    model_path = os.path.join(base_dir, "model.joblib")    # ml/model.joblib corretamente localizado

    joblib.dump(model, model_path)
    print(f"Modelo salvo em: {model_path}")

if __name__ == "__main__":
    main()