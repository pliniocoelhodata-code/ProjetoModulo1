# 📚 Projeto Módulo 1 - API de Livros com Machine Learning

Este projeto desenvolve uma API RESTful com [FastAPI](https://fastapi.tiangolo.com/) para coletar, armazenar e prever a popularidade de livros com base em dados extraídos via *web scraping*. Inclui também um modelo de Machine Learning para classificar livros como populares ou não com base em preço, avaliação e disponibilidade.

---

## 🏗️ Arquitetura do Projeto

```
📁 app/
 ┣ 📂 ml/              # Código do modelo de machine learning
 ┃ ┗ 📄 predict.py
 ┣ 📂 routes/          # Arquivos com as rotas da API
 ┃ ┗ 📄 ml_routes.py
 ┣ 📂 scraper/         # Função de scraping
 ┃ ┗ 📄 scraper.py
 ┣ 📄 main.py          # Inicialização da aplicação FastAPI
 ┣ 📄 database.py      # Conexão com banco de dados SQLite
 ┣ 📄 models.py        # ORM com SQLAlchemy
 ┣ 📄 schemas.py       # Validação com Pydantic
 ┣ 📄 populate_db.py   # Script para popular o banco com scraping
 ┣ 📄 train_model.py   # Script de treino e salvamento do modelo
```

---

## ⚙️ Instalação e Configuração

### ✅ Pré-requisitos

- Python 3.10+
- Git
- pip

### 🔧 Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nome-do-projeto.git
cd nome-do-projeto

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🚀 Execução Local


### 1. Popular o banco de dados com scraping

```bash
python populate_db.py
```

### 2. Iniciar o servidor FastAPI

```bash
uvicorn main:app --reload --port 8000
```

### 3. Treinar o modelo

```bash
python train_model.py
```

Acesse a documentação interativa em:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 Rotas da API

### 📘 `/api/v1/ml/training-data`  
Retorna os dados usados para treinar o modelo de machine learning.

- **Método:** `GET`  
- **Resposta:**
```json
[
  {
    "price": 20.5,
    "rating": 4,
    "availability": "In stock",
    "popular": 1
  }
]
```

---

### 🔧 `/api/v1/ml/features`  
Retorna as features (entradas) utilizadas no modelo de ML.

- **Método:** `GET`

---

### 🤖 `/api/v1/ml/predictions`  
Retorna a previsão de popularidade de um livro.

- **Método:** `POST`  
- **Corpo da requisição:**

```json
{
  "price": 39.90,
  "rating": 5,
  "availability": "In stock"
}
```

- **Resposta:**
```json
{
  "prediction": 1
}
```
> `1` = Popular | `0` = Não popular

---

## 🌐 Frontend com Streamlit

O projeto inclui um frontend simples com [Streamlit](https://streamlit.io/).

### Executar localmente:

```bash
streamlit run streamlit_predict.py
```

---

## 📦 Deploy

O projeto está disponível em produção na plataforma Render:

🔗 [https://projetomodulo1.onrender.com](https://projetomodulo1.onrender.com)

---

## 🧠 Modelo de Machine Learning

- Algoritmo: `LogisticRegression`
- Bibliotecas: `scikit-learn`, `joblib`
- Entradas: `price`, `rating`, `availability`
- Saída: `prediction` (0 ou 1)

---

## 📁 Requisitos

```
fastapi==0.95.2
uvicorn==0.22.0
SQLAlchemy==1.4.44
pydantic==1.10.12
requests==2.31.0
scikit-learn==1.3.0
joblib==1.2.0
streamlit==1.25.0
```

---

## 👨‍💻 Autor

Plínio Ramos Coelho Neto  
[LinkedIn](https://www.linkedin.com/in/seu-perfil) • [GitHub](https://github.com/seu-usuario)
