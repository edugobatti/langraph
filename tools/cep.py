from langchain.tools import tool
import requests

@tool
def consulta_cep(cep: str) -> dict:
    """Busca de CEP"""
    consulta_url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(consulta_url)
    if response.status_code == 200:
        return response.json()
    return "erro ao consultar CEP"