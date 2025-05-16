import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from agents.supervisor import supervisorAgent
supervisor = supervisorAgent()

a = supervisor.call_llm("quanto é (2+3)x2")
print(a)