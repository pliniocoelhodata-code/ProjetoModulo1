import logging
import os

# Garante que a pasta "logs" existe
os.makedirs("logs", exist_ok=True)

# Configura o logger para gravar em logs/app.log
logging.basicConfig(
    filename="logs/app.log",               # <- Arquivo de log
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"                        # <- Evita problemas com acentos
)

logger = logging.getLogger("books_api")