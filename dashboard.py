import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analize_logs import load_log_data

# 🛠️ Configurações iniciais da página Streamlit
st.set_page_config(page_title="API Performance Dashboard", layout="wide")
st.title("📊 API Performance Dashboard")


def show_metrics_dashboard():
    """
    Exibe o painel de métricas da API utilizando dados de logs processados.

    Funções principais:
    - Exibe métricas gerais: total de requisições, tempo médio de resposta, taxa de erro.
    - Gráfico de barras com contagem por status HTTP.
    - Gráfico de linha mostrando o tempo de resposta ao longo do tempo.
    """
    # 🔍 Carrega dados do arquivo de log
    df = load_log_data()

    if df.empty:
        st.warning("⚠ Nenhum dado encontrado nos logs.")
        return

    # 📌 Métricas principais
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total de Requisições", len(df))

    with col2:
        avg_duration = df["duration"].mean()
        st.metric("⏱ Tempo Médio de Resposta", f"{avg_duration:.2f}s")

    with col3:
        error_rate = (df["status"] >= 400).sum() / len(df) * 100
        st.metric("❌ Erro (%)", f"{error_rate:.1f}%")

    # 📊 Gráfico: Requisições por Status Code
    st.subheader("📌 Requisições por Status Code")
    status_counts = df["status"].value_counts().sort_index()
    st.bar_chart(status_counts)

    # 📈 Gráfico: Tempo de Resposta ao Longo do Tempo
    st.subheader("⏳ Tempo de Resposta ao Longo do Tempo")
    df_sorted = df.sort_values("timestamp")
    st.line_chart(df_sorted.set_index("timestamp")["duration"])
