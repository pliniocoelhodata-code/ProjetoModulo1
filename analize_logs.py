import re
import pandas as pd
from datetime import datetime

# 🔍 Padrão de log para capturar informações: timestamp, método, path, status e duração
LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \| INFO \| (?P<method>\w+) (?P<path>\S+) - (?P<status>\d{3}) - (?P<duration>\d+\.\d+)s'
)

def parse_log_line(line: str) -> dict | None:
    """
    Analisa uma linha de log e extrai informações estruturadas.

    Args:
        line (str): Linha do log no formato definido pelo LOG_PATTERN.

    Returns:
        dict | None: Um dicionário contendo os dados extraídos 
                     (timestamp, método, path, status, duração),
                     ou None se a linha não corresponder ao padrão.
    """
    match = LOG_PATTERN.match(line)
    if match:
        data = match.groupdict()
        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
        data["status"] = int(data["status"])
        data["duration"] = float(data["duration"])
        return data
    return None


def load_log_data(log_file: str = "logs/app.log") -> pd.DataFrame:
    """
    Carrega os dados de log de um arquivo, analisa e retorna um DataFrame.

    Args:
        log_file (str): Caminho para o arquivo de log. Padrão é "logs/app.log".

    Returns:
        pd.DataFrame: DataFrame contendo os dados extraídos (timestamp, método, path, status, duração).
                      Retorna DataFrame vazio se não houver logs válidos.
    """
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return pd.DataFrame()

    parsed = [parse_log_line(line) for line in lines]
    data = [entry for entry in parsed if entry]
    return pd.DataFrame(data)
