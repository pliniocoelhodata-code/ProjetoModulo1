import streamlit as st
import requests

# 🎯 Título do aplicativo
st.title("📚 Previsão de Popularidade de Livro")

# 📝 Entrada de dados do usuário
price = st.number_input("💰 Preço", min_value=0.0)
rating = st.selectbox("⭐ Avaliação", [1, 2, 3, 4, 5])
availability = st.selectbox("📦 Disponibilidade", ["In stock", "Out of stock"])

# 🔮 Quando o usuário clicar no botão "Prever"
if st.button("🔮 Prever"):
    # 📦 Prepara os dados para enviar à API
    payload = {
        "price": price,
        "rating": rating,
        "availability": availability
    }

    try:
        # 🚀 Faz a requisição POST para a API de predição
        response = requests.post(
            "https://projetomodulo1.onrender.com/api/v1/ml/predictions", 
            json=payload
        )

        # ✅ Verifica se a resposta foi bem sucedida
        if response.status_code == 200:
            prediction = response.json().get("prediction")

            # 📊 Exibe o resultado da predição para o usuário
            if prediction == 1:
                st.success("📈 Este livro é **Popular**.")
            elif prediction == 0:
                st.info("📉 Este livro é **Não Popular**.")
            else:
                st.warning("🤔 Resultado inesperado da previsão.")
        else:
            # ❌ Caso a API retorne erro, exibe a mensagem
            st.error(f"Erro da API ({response.status_code}): {response.text}")

    except Exception as e:
        # ⚠️ Erro de conexão ou outro erro inesperado
        st.error(f"Erro ao conectar com a API: {e}")
