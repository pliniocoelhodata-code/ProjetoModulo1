from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

# 🔐 Configurações do JWT
SECRET_KEY: str = "sua_chave_secreta_segura"  # Substitua por uma chave forte em produção
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# 🔑 Configuração para criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔒 Esquema OAuth2 para extração do token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 👤 Usuário fictício para testes
fake_user = {
    "username": "admin",
    "hashed_password": pwd_context.hash("admin123")  # Armazena senha criptografada
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano.
        hashed_password (str): Hash da senha armazenado.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> Dict[str, str] | bool:
    """
    Autentica o usuário comparando credenciais com dados fictícios.

    Args:
        username (str): Nome do usuário.
        password (str): Senha em texto plano.

    Returns:
        dict | bool: Dados do usuário se autenticado com sucesso, ou False caso contrário.
    """
    if username != fake_user["username"]:
        return False
    if not verify_password(password, fake_user["hashed_password"]):
        return False
    return fake_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT com data de expiração.

    Args:
        data (dict): Dados que serão incluídos no token (ex.: {"sub": username}).
        expires_delta (timedelta, opcional): Tempo de expiração do token.

    Returns:
        str: Token JWT gerado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Extrai e valida o usuário a partir do token JWT.

    Args:
        token (str): Token JWT extraído do header Authorization.

    Raises:
        HTTPException: Se o token for inválido ou expirado.

    Returns:
        dict: Dicionário com username do usuário autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception
