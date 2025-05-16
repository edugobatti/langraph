from typing import List, Dict, Any, Callable, Union
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import importlib
from langchain.tools import Tool
import sys
from tools.math import add,multiply,divide
from tools.cep import consulta_cep
from config.settings import OPENAI_API_KEY,MODEL

def generic_agent(agent_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Cria dinamicamente agentes com base no array.
    
    Args:
        agent_configs: Lista de dicionários contendo configurações dos agentes
        
    Returns:
        Dicionário com os agentes criados, usando o nome do agente como chave
    """
    agents = {}
    resume ={}
    for config in agent_configs:
        # Extrair informações da configuração
        agent_name = config.get("name", config.get("agent", "unnamed_agent"))
        model_name = config.get(MODEL, "gpt-4o")
        api_key = config.get("api_key", OPENAI_API_KEY)
        prompt = config.get("prompt", "")
        tool_names = config.get("tools", [])  # Lista de nomes de ferramentas (strings)
        
        # Converter nomes de ferramentas em objetos Tool do LangChain
        tools = []
        for tool_name in tool_names:
            # Verificar se o nome da ferramenta é uma string
            if isinstance(tool_name, str):
                # Tentar encontrar a função no escopo global primeiro
                if tool_name in globals():
                    func = globals()[tool_name]
                    # Converter a função em um objeto Tool
                    tool = Tool(
                        name=tool_name,
                        description=f"Tool para {tool_name}",
                        func=func
                    )
                    tools.append(tool)
                else:
                    # Tentar importar do módulo atual
                    try:
                        # Obter o módulo atual
                        current_module = sys.modules[__name__]
                        # Verificar se a função existe no módulo atual
                        if hasattr(current_module, tool_name):
                            func = getattr(current_module, tool_name)
                            # Converter a função em um objeto Tool
                            tool = Tool(
                                name=tool_name,
                                description=f"Tool para {tool_name}",
                                func=func
                            )
                            tools.append(tool)
                        else:
                            print(f"Aviso: Ferramenta {tool_name} não encontrada")
                    except Exception as e:
                        print(f"Erro ao importar {tool_name}: {e}")
            else:
                # Se já é um objeto (não uma string), verificar se tem o atributo 'name'
                if hasattr(tool_name, 'name'):
                    tools.append(tool_name)
                else:
                    # Se é uma função, criar um Tool
                    tool_func_name = tool_name.__name__ if hasattr(tool_name, '__name__') else "tool_func"
                    tool = Tool(
                        name=tool_func_name,
                        description=f"Tool para {tool_func_name}",
                        func=tool_name
                    )
                    tools.append(tool)
        
        # Criar o modelo de linguagem
        llm = ChatOpenAI(model=model_name, api_key=api_key)
        
        # Criar o agente
        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=prompt,
            name=agent_name
        )
        
        # Adicionar ao dicionário de agentes
        agents[agent_name] = agent
        resume[agent_name] = config.get("agent_resume", "")
    
    return agents,resume