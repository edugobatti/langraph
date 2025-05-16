from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agent_generator import generic_agent
from langchain_openai import ChatOpenAI
from settings import MODEL, OPENIA_KEY
import json


caminho_arquivo = 'files/agents.json'

# Abrir e carregar o conteúdo do arquivo
with open(caminho_arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)


agents_create = generic_agent(dados)


supervisor = create_supervisor(
    model=ChatOpenAI(model=MODEL, api_key=OPENIA_KEY),
    agents=list(agents_create.values()),
    prompt=(
        "Você é um supervisor gerenciando agentes:\n"
        "Atribua trabalho a um agente por vez, não ligue para agentes em paralelo.\n"
        "Não faça nenhum trabalho sozinho."
    ),
    add_handoff_back_messages=True,
    output_mode="last_message",
).compile()

print('Quanto é 2+2?')