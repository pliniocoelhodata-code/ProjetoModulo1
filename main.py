from fastapi import FastAPI, Depends, Request
from database import SessionLocal
from auth import get_current_user  # porque usa no trigger
from routers import books, ml, auth_routes  # seus routers separados
from database import get_db
from time import time
from logger import logger

app = FastAPI(title="Books API")


app.include_router(books.router)
app.include_router(ml.router)
app.include_router(auth_routes.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    # Log do corpo apenas para POST e PUT
    if request.method in ("POST", "PUT"):
        body = await request.body()
        logger.info(f"Request body: {body.decode('utf-8')}")

    response = await call_next(request)

    duration = time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s"
    )

    return response

# 🟢 . Trigger
@app.post("/api/v1/scraping/trigger")
def trigger_scraping(current_user: dict = Depends(get_current_user)):
    # Simulação de scraping
    return {"message": f"Scraping iniciado pelo usuário {current_user['username']}"}
