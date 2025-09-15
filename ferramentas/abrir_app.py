import subprocess
import time
import pyautogui
import sys

def pesquisar_universal(termo):
    """
    Usa a pesquisa universal do Windows (Win+S) para:
    - Abrir aplicativos
    - Pesquisar na web
    - Encontrar arquivos
    - Acessar configurações
    - E muito mais...
    
    Args:
        termo (str): Termo de pesquisa (app, arquivo, configuração, etc.)
    """
    try:
        # Pressiona Win+S para abrir a pesquisa universal do Windows
        pyautogui.hotkey('win', 's')
        
        # Aguarda a pesquisa aparecer
        time.sleep(1)
        
        # Limpa qualquer texto existente
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        
        # Digite o termo de pesquisa
        pyautogui.write(termo)
        
        # Aguarda os resultados carregarem
        time.sleep(1.5)
        
        # Pressiona Enter para abrir o primeiro resultado
        pyautogui.press('enter')
        
        print(f"Pesquisa por '{termo}' executada com sucesso!")
        print("O Windows irá abrir o melhor resultado encontrado (app, arquivo, web, etc.)")
        return True
        
    except Exception as e:
        print(f"Erro na pesquisa: {e}")
        return False

# Alias para compatibilidade
def abrir_app(nome_app):
    """Alias para compatibilidade com código existente"""
    return pesquisar_universal(nome_app)

# Exemplo de uso
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Usar argumento da linha de comando
        termo = " ".join(sys.argv[1:])
        pesquisar_universal(termo)
    else:
        # Modo interativo
        print("=== Pesquisa Universal do Windows ===")
        print("Exemplos: calculadora, notepad, chrome, configurações,")
        print("          weather, news, spotify, discord, etc.")
        termo = input("Digite o que procura: ")
        pesquisar_universal(termo)