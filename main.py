from fastapi import FastAPI, Request
from time import time

from database import get_db  # Para injeção de dependência
from auth import get_current_user  # Usado na rota auth_routes
from logger import logger

# Routers
from routers import books, ml, auth_routes, trigger

# 📘 Inicializa o app FastAPI
app = FastAPI(title="Books API")

# 🚏 Inclui os routers separados por responsabilidade
app.include_router(books.router)
app.include_router(ml.router)
app.include_router(auth_routes.router)
app.include_router(trigger.router)

# 🧾 Middleware para logar requisições HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    # Log do corpo da requisição (apenas para POST e PUT)
    if request.method in ("POST", "PUT"):
        body = await request.body()
        logger.info(f"📩 Request body: {body.decode('utf-8')}")

    # Executa a próxima etapa (view/controller)
    response = await call_next(request)

    # Tempo de execução da requisição
    duration = time() - start_time
    logger.info(
        f"➡️ {request.method} {request.url.path} - {response.status_code} - {duration:.2f}s"
    )

    return response
