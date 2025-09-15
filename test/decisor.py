from taskai import tki 
from taskai import tools
import json
import os

# Carrega as ferramentas
toolsdir = json.load(open("ferramentas.json"))
tools_path = [os.path.join("mytools", f) for f in os.listdir("mytools") if f.endswith(".py")]
tools = tools  # ou tools = None, se não usar diretamente

user_input = "Quero abrir o app do discord"

# exemplo de uso do decisor
result = tki.decisor(
    user_input,
    toolsdir,
    tools_path  # Passe os caminhos aqui
)