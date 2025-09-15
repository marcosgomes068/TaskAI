import webbrowser
import sys

def pesquisar_web(termo_busca):
    """
    Realiza pesquisa na web usando o navegador padrão
    
    Args:
        termo_busca (str): Termo a ser pesquisado
    """
    try:
        # Criar URL de pesquisa do Google
        url_pesquisa = f"https://www.google.com/search?q={termo_busca.replace(' ', '+')}"
        
        # Abrir no navegador padrão
        webbrowser.open(url_pesquisa)
        
        print(f"Pesquisa por '{termo_busca}' aberta no navegador!")
        return True
        
    except Exception as e:
        print(f"Erro ao pesquisar: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        termo = " ".join(sys.argv[1:])
        pesquisar_web(termo)
    else:
        busca = input("Digite o termo de busca: ")
        pesquisar_web(busca)