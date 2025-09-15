import os
import subprocess
import sys

def abrir_pasta(caminho_pasta):
    """
    Abre uma pasta no explorador de arquivos
    
    Args:
        caminho_pasta (str): Caminho da pasta a ser aberta
    """
    try:
        # Mapear algumas pastas comuns
        pastas_comuns = {
            "documentos": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "desktop": os.path.expanduser("~/Desktop"),
            "imagens": os.path.expanduser("~/Pictures"),
            "videos": os.path.expanduser("~/Videos"),
            "musicas": os.path.expanduser("~/Music")
        }
        
        # Verificar se é uma pasta comum
        caminho_final = pastas_comuns.get(caminho_pasta.lower(), caminho_pasta)
        
        # Abrir a pasta
        if os.path.exists(caminho_final):
            subprocess.run(['explorer', caminho_final], shell=True)
            print(f"Pasta '{caminho_final}' aberta com sucesso!")
            return True
        else:
            print(f"Pasta '{caminho_final}' não encontrada!")
            return False
            
    except Exception as e:
        print(f"Erro ao abrir pasta: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        caminho = " ".join(sys.argv[1:])
        abrir_pasta(caminho)
    else:
        pasta = input("Digite o nome/caminho da pasta: ")
        abrir_pasta(pasta)