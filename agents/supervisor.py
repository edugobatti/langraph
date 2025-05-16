from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from agents.agent_generator import generic_agent
from langchain_core.messages import AIMessage
from config.settings import MODEL, OPENAI_API_KEY,AGENTS_FILE
import json


# Abrir e carregar o conteúdo do arquivo
with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
    dados = json.load(f)

class supervisorAgent:
    def __init__(self):
        agents, resume = generic_agent(dados)
        agents_resume = '\n' + '\n'.join([f"{key} - {value}" for key, value in resume.items()])

        self.supervisor = create_supervisor(
            model=ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY,temperature=0),
            agents=list(agents.values()),
            
            prompt=(f"""
                    \nVocê é um supervisor gerenciando agentes:
                    {agents_resume}
                    \nAtribua trabalho a um agente por vez, não ligue para agentes em paralelo.
                    \nNão faça nenhum trabalho sozinho.
                    """),
            output_mode="last_message",
        ).compile()

    def call_llm(self,query):
        resp_llm = self.supervisor.invoke({"messages": [
            {
                "role": "user",
                "content": query,
            }
        ]}, subgraphs=False)
        ai_messages = [msg for msg in resp_llm["messages"] if isinstance(msg, AIMessage)]
        final_response = next(
            (msg.content for msg in reversed(ai_messages) if msg.content.strip()), 
            None
        )

        return final_response
