import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

        if not self.api_key:
            raise ValueError("Chave não encontrada")

    def get_daily_data(self, symbol: str) -> dict:

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }

        response = requests.get(
            self.BASE_URL,
            params = params,
            timeout = 10
        )

        response.raise_for_status()

        data = response.json()

        if "Error Message" in data:
            raise ValueError(
                f"Erro: {data['Error Message']}"
            )

        if "Note" in data:
            raise RuntimeError(
                f"Limite da API atingido: {data['Note']}"
            )

        return data