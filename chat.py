import sys
import os
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from taskai import tki
import json

def carregar_configuracao():
    """Carrega as ferramentas e configurações"""
    toolsdir = json.load(open("ferramentas.json"))
    ferramentas_path = "ferramentas"
    tools_path = [os.path.join(ferramentas_path, f) for f in os.listdir(ferramentas_path) if f.endswith(".py")]
    return toolsdir, tools_path

def executar_ferramenta_real(tool_name, params, tools_path):
    """Executa a ferramenta Python de fato"""
    try:
        # Mapear nomes de ferramentas para arquivos
        tool_files = {
            "abrir_apps": "abrir_app.py",
            "abrir_pastas": "abrir_pasta.py", 
            "pesquisar_web": "pesquisar_web.py",
            "criar_arquivo": "criar_arquivo.py"
        }
        
        if tool_name in tool_files:
            script_path = os.path.join("ferramentas", tool_files[tool_name])
            
            if os.path.exists(script_path):
                # Executar o script com o parâmetro
                if params:
                    resultado = subprocess.run([sys.executable, script_path, params], 
                                             capture_output=True, text=True, timeout=30)
                else:
                    resultado = subprocess.run([sys.executable, script_path], 
                                             capture_output=True, text=True, timeout=30)
                
                if resultado.returncode == 0:
                    return f"✅ Executado com sucesso: {resultado.stdout.strip()}"
                else:
                    return f"⚠️ Erro na execução: {resultado.stderr.strip()}"
            else:
                return f"❌ Arquivo {script_path} não encontrado"
        else:
            return f"❌ Ferramenta {tool_name} não mapeada"
            
    except subprocess.TimeoutExpired:
        return "⏰ Timeout: Execução demorou mais que 30 segundos"
    except Exception as e:
        return f"❌ Erro ao executar: {str(e)}"

def chat_taskai():
    """Chat interativo com o TaskAI"""
    print("🤖 === TaskAI Chat Inteligente ===")
    print("💬 Digite suas solicitações em linguagem natural")
    print("ℹ️  Digite 'sair' para encerrar | 'help' para ajuda | 'memoria' para ver histórico\n")
    
    # Configuração
    api_key = "MoHa7qTxBctiVpM9RYpVoNcHAoAsOI0sKIhaAbaJ"  # Substitua pela sua chave
    toolsdir, tools_path = carregar_configuracao()
    
    # Criar agente único para manter memória
    agente_principal = tki("", tools_path, toolsdir, api_key)
    
    while True:
        try:
            # Input do usuário
            user_input = input("Você: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'sair':
                print("Encerrando chat...")
                break
                
            if user_input.lower() == 'help':
                print("📖 === Ajuda TaskAI ===")
                print("🔧 Comandos do sistema:")
                print("   • sair: encerra o chat")
                print("   • help: mostra esta ajuda") 
                print("   • memoria: mostra histórico de conversas\n")
                print("🛠️  Ferramentas disponíveis:")
                for tool_name, tool_info in toolsdir.items():
                    print(f"   • {tool_name}: {tool_info.get('descricao', 'Sem descrição')}")
                print("\n💡 Exemplos de comandos:")
                print("   🚀 Apps: 'abrir calculadora', 'abrir vs code', 'abrir chrome'")
                print("   📁 Pastas: 'abrir pasta documentos', 'abrir pasta downloads'") 
                print("   🔍 Pesquisas: 'pesquisar receitas de bolo', 'procurar noticias'")
                print("   📄 Arquivos: 'criar arquivo notas.txt'")
                print("   🌤️ Sistema: 'abrir configurações', 'ver clima', 'noticias'")
                print("\n⚠️  Nota: O sistema pedirá confirmação antes de executar ações")
                print("🔥 Novo: Win+S pesquisa universal - apps, web, arquivos, tudo!\n")
                continue
                
            if user_input.lower() == 'memoria':
                print("🧠 === Histórico de Conversas ===")
                if agente_principal.memory:
                    for i, mem in enumerate(agente_principal.memory, 1):
                        print(f"   {i}. Você: {mem['user']}")
                        print(f"      TaskAI: {mem['response'][:50]}{'...' if len(mem['response']) > 50 else ''}")
                else:
                    print("   Nenhuma conversa no histórico ainda.")
                print()
                continue
            
            # Usar agente principal com memória
            agente_principal.user_prompt = user_input
            
            # Obtém recomendação inteligente
            print("TaskAI: Analisando sua solicitação...")
            recomendacao = agente_principal.get_tool_recommendation()
            
            # Extrair ferramenta e parâmetros
            tool_name, params = agente_principal.extract_tool_and_params(recomendacao)
            
            if tool_name in toolsdir:
                print(f"TaskAI: 🎯 Ferramenta identificada: {tool_name}")
                if params:
                    print(f"TaskAI: 📋 Parâmetros: {params}")
                
                # Mostrar comando que seria executado
                comando_teorico = agente_principal.execute_tool_smart(recomendacao)
                print(f"TaskAI: 📝 Comando: {comando_teorico}")
                
                # Perguntar se deve executar
                executar = input("TaskAI: 🤖 Executar esta ação? (s/N): ").lower().strip()
                
                if executar in ['s', 'sim', 'y', 'yes']:
                    print("TaskAI: 🚀 Executando...")
                    resultado_real = executar_ferramenta_real(tool_name, params, tools_path)
                    print(f"TaskAI: {resultado_real}")
                else:
                    print("TaskAI: ⏹️ Execução cancelada pelo usuário")
                    
            elif recomendacao and not recomendacao.startswith("Erro"):
                print(f"TaskAI: 🤔 {recomendacao}")
            else:
                print(f"TaskAI: ❌ {recomendacao}")
            
        except KeyboardInterrupt:
            print("\n\nEncerrado pelo usuário.")
            break
        except Exception as e:
            print(f"TaskAI: Erro interno - {e}")

if __name__ == "__main__":
    chat_taskai()