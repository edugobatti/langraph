from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agent_generator import generic_agent

agents_create = generic_agent()


supervisor = create_supervisor(
    model=llm,
    agents=list(agents_create.values()),
    prompt=(
        "Você é um supervisor gerenciando agentes:\n"
        "Atribua trabalho a um agente por vez, não ligue para agentes em paralelo.\n"
        "Não faça nenhum trabalho sozinho."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()