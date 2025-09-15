"""
Exemplo básico de uso do TaskAI
Este exemplo mostra como usar a biblioteca para uma recomendação simples
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from taskai import tki
import json

def exemplo_basico():
    """Exemplo de uso básico do TaskAI"""
    
    print("=== Exemplo Básico TaskAI ===\n")
    
    # Configuração
    base_path = os.path.dirname(os.path.dirname(__file__))
    toolsdir = json.load(open(os.path.join(base_path, "ferramentas.json")))
    ferramentas_path = os.path.join(base_path, "ferramentas")
    tools_path = [os.path.join(ferramentas_path, f) for f in os.listdir(ferramentas_path) if f.endswith(".py")]
    api_key = "MoHa7qTxBctiVpM9RYpVoNcHAoAsOI0sKIhaAbaJ"  # Substitua pela sua chave
    
    # Lista de comandos para testar
    comandos = [
        "Quero abrir o notepad",
        "Preciso abrir a calculadora",
        "Abrir pasta de documentos"
    ]
    
    for comando in comandos:
        print(f"🤖 Processando: '{comando}'")
        
        # Criar agente
        agente = tki(comando, tools_path, toolsdir, api_key)
        
        # Obter recomendação
        recomendacao = agente.get_tool_recommendation()
        print(f"   Resposta da IA: {recomendacao}")
        
        # Extrair ferramenta e parâmetros
        tool_name, params = agente.extract_tool_and_params(recomendacao)
        print(f"   Ferramenta: {tool_name}")
        if params:
            print(f"   Parâmetros extraídos: {params}")
        
        # Executar ferramenta com inteligência
        if tool_name in toolsdir:
            resultado = agente.execute_tool_smart(recomendacao)
            print(f"   ✅ Execução: {resultado}")
        else:
            print(f"   ⚠️  Ferramenta '{tool_name}' não encontrada")
        
        print("-" * 50)

if __name__ == "__main__":
    exemplo_basico()