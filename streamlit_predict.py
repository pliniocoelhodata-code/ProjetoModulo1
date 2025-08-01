import streamlit as st
import requests

st.title("📚 Previsão de Popularidade de Livro")

# Inputs
price = st.number_input("💰 Preço", min_value=0.0)
rating = st.selectbox("⭐ Avaliação", [1, 2, 3, 4, 5])
availability = st.selectbox("📦 Disponibilidade", ["In stock", "Out of stock"])

if st.button("🔮 Prever"):
    payload = {
        "price": price,
        "rating": rating,
        "availability": availability
    }

    try:
        response = requests.post("http://localhost:8000/api/v1/ml/predictions", json=payload)

        if response.status_code == 200:
            prediction = response.json().get("prediction")

            if prediction == 1:
                st.success("📈 Este livro é **Popular**.")
            elif prediction == 0:
                st.info("📉 Este livro é **Não Popular**.")
            else:
                st.warning("🤔 Resultado inesperado da previsão.")
        else:
            st.error(f"Erro da API ({response.status_code}): {response.text}")

    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
