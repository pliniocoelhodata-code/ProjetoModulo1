from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(prefix="/api/v1/scraping", tags=["SCRAPING"])

# 🟢 . Trigger
@router.post("/trigger")
def trigger_scraping(current_user: dict = Depends(get_current_user)):
    # Simulação de scraping
    return {"message": f"Scraping iniciado pelo usuário {current_user['username']}"}