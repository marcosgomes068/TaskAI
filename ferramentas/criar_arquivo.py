import os
import sys

def criar_arquivo(nome_arquivo, conteudo=""):
    """
    Cria um novo arquivo de texto com conteúdo especificado
    
    Args:
        nome_arquivo (str): Nome do arquivo a ser criado
        conteudo (str): Conteúdo do arquivo (opcional)
    """
    try:
        # Adicionar extensão .txt se não tiver extensão
        if not os.path.splitext(nome_arquivo)[1]:
            nome_arquivo += ".txt"
        
        # Criar o arquivo
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        
        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar arquivo: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nome = sys.argv[1]
        conteudo_arquivo = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        criar_arquivo(nome, conteudo_arquivo)
    else:
        nome = input("Digite o nome do arquivo: ")
        conteudo = input("Digite o conteúdo (opcional): ")
        criar_arquivo(nome, conteudo)