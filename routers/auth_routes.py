from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["AUTH"])


# 🟢 . Autenticação de login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 🟢 . Prorrogação de login
@router.post("/refresh")
def refresh_token(current_user: dict = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
