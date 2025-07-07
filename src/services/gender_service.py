import os
import requests

class GenderAPIService:
    def __init__(self):
        self.token = os.getenv("")
        if not self.token:
            raise ValueError("Token GENDER_API_TOKEN não definido nas variáveis de ambiente")

    def inferir_genero(self, nome):
        url = f"https://api.gender-api.com/get?name={nome}&key={self.token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Erro ao consultar API de gênero: {e}")
            return {"gender": "unknown"}
