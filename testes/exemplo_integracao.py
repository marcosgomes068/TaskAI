"""
Exemplo de integração personalizada
Mostra como integrar o TaskAI em uma aplicação personalizada
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from taskai import tki
import json
import time

class TaskAIManager:
    """Classe para gerenciar múltiplos agentes TaskAI"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.toolsdir = json.load(open(os.path.join(base_path, "ferramentas.json")))
        ferramentas_path = os.path.join(base_path, "ferramentas")
        self.tools_path = [os.path.join(ferramentas_path, f) for f in os.listdir(ferramentas_path) if f.endswith(".py")]
        self.agentes_ativos = {}
        self.historico_global = []
    
    def criar_agente(self, nome_agente, prompt_inicial=""):
        """Cria um novo agente com nome específico"""
        agente = tki(prompt_inicial, self.tools_path, self.toolsdir, self.api_key)
        self.agentes_ativos[nome_agente] = agente
        print(f"✅ Agente '{nome_agente}' criado com sucesso")
        return agente
    
    def processar_comando(self, nome_agente, comando):
        """Processa um comando usando um agente específico"""
        if nome_agente not in self.agentes_ativos:
            print(f"❌ Agente '{nome_agente}' não encontrado")
            return None
        
        agente = self.agentes_ativos[nome_agente]
        agente.user_prompt = comando
        
        # Registrar no histórico global
        timestamp = time.strftime("%H:%M:%S")
        self.historico_global.append({
            "timestamp": timestamp,
            "agente": nome_agente,
            "comando": comando
        })
        
        # Processar
        recomendacao = agente.get_tool_recommendation()
        tool_name = agente.extract_tool_name(recomendacao)
        
        resultado = {
            "agente": nome_agente,
            "comando": comando,
            "recomendacao": recomendacao,
            "ferramenta": tool_name,
            "sucesso": tool_name in self.toolsdir
        }
        
        if resultado["sucesso"]:
            resultado["execucao"] = agente.execute_tool(tool_name)
        
        return resultado
    
    def listar_agentes(self):
        """Lista todos os agentes ativos"""
        print(f"🤖 Agentes ativos: {len(self.agentes_ativos)}")
        for nome, agente in self.agentes_ativos.items():
            print(f"   • {nome} (memória: {len(agente.memory)} itens)")
    
    def relatorio_atividade(self):
        """Gera relatório de atividade global"""
        print(f"\n📊 Relatório de Atividade (Total: {len(self.historico_global)} comandos)")
        for item in self.historico_global[-5:]:  # Últimos 5 comandos
            print(f"   {item['timestamp']} | {item['agente']} | {item['comando'][:40]}...")

def exemplo_integracao():
    """Exemplo de uso da integração personalizada"""
    
    print("=== Exemplo de Integração Personalizada ===\n")
    
    # Criar gerenciador
    api_key = "MoHa7qTxBctiVpM9RYpVoNcHAoAsOI0sKIhaAbaJ"  # Substitua pela sua chave
    manager = TaskAIManager(api_key)
    
    # Criar diferentes agentes
    manager.criar_agente("AgentePrincipal", "Sou o agente principal")
    manager.criar_agente("AgenteAuxiliar", "Sou um agente auxiliar")
    
    # Simular diferentes tarefas
    tarefas = [
        ("AgentePrincipal", "Abrir calculadora para fazer contas"),
        ("AgenteAuxiliar", "Abrir notepad para anotações"),
        ("AgentePrincipal", "Agora abrir pasta de documentos"),
        ("AgenteAuxiliar", "Preciso do paint para desenhar")
    ]
    
    print("\n🚀 Executando tarefas distribuídas:\n")
    
    for nome_agente, tarefa in tarefas:
        print(f"📝 Processando: [{nome_agente}] {tarefa}")
        
        resultado = manager.processar_comando(nome_agente, tarefa)
        
        if resultado:
            print(f"   🎯 Ferramenta: {resultado['ferramenta']}")
            if resultado['sucesso']:
                print(f"   ✅ Execução: {resultado['execucao']}")
            else:
                print(f"   ❌ Ferramenta não encontrada")
        
        print()
        time.sleep(1)  # Pausa para visualização
    
    # Mostrar estado final
    print("\n" + "="*50)
    manager.listar_agentes()
    manager.relatorio_atividade()
    
    # Demonstrar análise de memória por agente
    print(f"\n🧠 Análise de Memória por Agente:")
    for nome, agente in manager.agentes_ativos.items():
        print(f"\n   {nome}:")
        if agente.memory:
            for i, mem in enumerate(agente.memory, 1):
                print(f"      {i}. {mem['user'][:30]}... → {mem['response'][:20]}...")
        else:
            print(f"      (sem memória)")

if __name__ == "__main__":
    exemplo_integracao()