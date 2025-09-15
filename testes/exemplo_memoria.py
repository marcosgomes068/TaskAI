"""
Exemplo avançado com memória contextual
Demonstra como o TaskAI mantém contexto entre múltiplas interações
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from taskai import tki
import json

def exemplo_memoria():
    """Exemplo demonstrando o sistema de memória do TaskAI"""
    
    print("=== Exemplo com Memória Contextual ===\n")
    
    # Configuração
    base_path = os.path.dirname(os.path.dirname(__file__))
    toolsdir = json.load(open(os.path.join(base_path, "ferramentas.json")))
    ferramentas_path = os.path.join(base_path, "ferramentas")
    tools_path = [os.path.join(ferramentas_path, f) for f in os.listdir(ferramentas_path) if f.endswith(".py")]
    api_key = "MoHa7qTxBctiVpM9RYpVoNcHAoAsOI0sKIhaAbaJ"  # Substitua pela sua chave
    
    # Criar agente uma única vez para manter memória
    agente = tki("", tools_path, toolsdir, api_key)
    
    # Sequência de comandos relacionados
    conversas = [
        "Quero abrir um aplicativo",
        "Agora quero abrir uma pasta",
        "Preciso abrir o notepad",
        "E também a calculadora"
    ]
    
    print("💭 Demonstração de memória contextual:")
    print("   O agente manterá contexto entre as interações\n")
    
    for i, comando in enumerate(conversas, 1):
        print(f"Interação {i}: '{comando}'")
        
        # Atualizar prompt do usuário
        agente.user_prompt = comando
        
        # Mostrar memória atual
        if agente.memory:
            print("   📚 Memória atual:")
            for mem in agente.memory[-2:]:  # Mostra últimas 2 interações
                print(f"      U: {mem['user'][:30]}... → A: {mem['response'][:30]}...")
        
        # Obter recomendação
        recomendacao = agente.get_tool_recommendation()
        print(f"   🤖 Recomendação: {recomendacao}")
        
        # Extrair e executar
        tool_name = agente.extract_tool_name(recomendacao)
        if tool_name in toolsdir:
            resultado = agente.execute_tool(tool_name)
            print(f"   ✅ Resultado: {resultado}")
        
        print("-" * 60)
    
    print("\n🧠 Estado final da memória:")
    for i, mem in enumerate(agente.memory, 1):
        print(f"   {i}. U: {mem['user']} → A: {mem['response']}")
    
    # Demonstrar limpeza de memória
    print("\n🧹 Limpando memória...")
    agente.clear_memory()
    print(f"   Memória após limpeza: {len(agente.memory)} itens")

if __name__ == "__main__":
    exemplo_memoria()