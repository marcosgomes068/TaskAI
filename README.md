# TaskAI 🤖

Uma biblioteca Python inteligente para automação de tarefas usando IA. O TaskAI utiliza modelos de linguagem para entender solicitações em linguagem natural e recomendar/executar ferramentas apropriadas automaticamente.

## 🚀 Características

- **IA Integrada**: Usa Cohere API para entender comandos em linguagem natural
- **Sistema de Ferramentas**: Framework extensível para adicionar novas funcionalidades
- **Memória Contextual**: Mantém histórico de conversas para melhor contexto
- **Chat Interativo**: Interface de linha de comando amigável
- **Arquitetura Modular**: Fácil de estender e personalizar

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/marcosgomes068/TaskAI.git
cd TaskAI

# Instale as dependências
pip install cohere pyautogui
```

## 🔧 Configuração

1. **API Key da Cohere**: Obtenha sua chave em [cohere.ai](https://cohere.ai)
2. **Configure suas ferramentas** no arquivo `test/ferramentas.json`
3. **Adicione scripts personalizados** na pasta `test/mytools/`

### Exemplo de configuração (ferramentas.json):

```json
{
    "abrir_apps": {
        "descricao": "Abre um aplicativo no sistema operacional.",
        "quando usar": "sempre que o usuario queira abrir apps na maquina",
        "caso seja chamada retorne": "abrir_apps('nome do app')"
    },
    "abrir_pastas": {
        "descricao": "Abre uma pasta no sistema operacional.",
        "quando usar": "sempre que o usuario queira abrir pastas",
        "caso seja chamada retorne": "abrir_pastas('nome da pasta')"
    }
}
```

## 💻 Uso

### Chat Interativo

```bash
python chat.py
```

```
=== TaskAI Chat ===
Digite 'sair' para encerrar o chat
Digite 'help' para ver comandos disponíveis

Você: abrir calculadora
TaskAI: Analisando sua solicitação...
TaskAI: =>abrir_apps<=
TaskAI: abrir_apps('calculadora')
```

### Uso Programático

```python
from taskai import tki
import json

# Carregar configurações
toolsdir = json.load(open("test/ferramentas.json"))
tools_path = ["test/mytools/abrir_app.py"]

# Criar agente
agente = tki(
    user_prompt="Quero abrir o notepad",
    pathtools=tools_path,
    toolsdir=toolsdir,
    api_key="SUA_API_KEY_AQUI"
)

# Obter recomendação
recomendacao = agente.get_tool_recommendation()
print(f"Ferramenta recomendada: {recomendacao}")

# Extrair nome da ferramenta
tool_name = agente.extract_tool_name(recomendacao)

# Executar ferramenta
resultado = agente.execute_tool(tool_name)
print(f"Resultado: {resultado}")
```

### Executar Ferramentas Diretamente

```bash
# Executar script de abrir aplicativos
cd test/mytools
python abrir_app.py "notepad"
python abrir_app.py "calculator"
python abrir_app.py "Microsoft Excel"
```

## 🛠️ Estrutura do Projeto

```
TaskAI/
├── taskai/                 # Biblioteca principal
│   ├── __init__.py        # Exportações da lib
│   ├── tki.py             # Classe principal do agente
│   └── tools/             # Ferramentas internas
│       ├── __init__.py
│       └── llm.py         # Integração com LLMs
├── test/                   # Arquivos de teste e exemplo
│   ├── decisor.py         # Script de teste básico
│   ├── ferramentas.json   # Configuração das ferramentas
│   └── mytools/           # Scripts de ferramentas personalizadas
│       └── abrir_app.py   # Exemplo: abrir aplicativos
├── chat.py                # Interface de chat interativo
└── README.md              # Este arquivo
```

## 🔧 API da Classe `tki`

### Inicialização

```python
agente = tki(user_prompt, pathtools, toolsdir, api_key)
```

### Métodos Principais

- `get_tool_recommendation()`: Obtém recomendação de ferramenta da IA
- `extract_tool_name(response)`: Extrai nome da ferramenta do formato `=>ferramenta<=`
- `execute_tool(tool_name)`: Executa uma ferramenta específica
- `add_to_memory(user_input, response)`: Adiciona interação à memória
- `clear_memory()`: Limpa histórico de conversas

### Funcionalidades

- **Memória**: Mantém até 3 conversas anteriores para contexto
- **Validação**: Verifica entradas e trata erros automaticamente
- **Flexibilidade**: Parâmetros customizáveis para model e max_tokens

## 🎯 Exemplos de Comandos

| Comando do Usuário | Ferramenta Recomendada | Ação |
|-------------------|----------------------|-------|
| "abrir calculadora" | `abrir_apps` | Abre a calculadora do Windows |
| "abrir pasta documentos" | `abrir_pastas` | Abre a pasta Documentos |
| "quero usar o notepad" | `abrir_apps` | Abre o Bloco de Notas |

## 🚧 Adicionando Novas Ferramentas

1. **Criar script na pasta `test/mytools/`**:
```python
# exemplo_tool.py
def minha_funcao(parametro):
    # Sua lógica aqui
    return f"Executando com {parametro}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resultado = minha_funcao(sys.argv[1])
        print(resultado)
```

2. **Adicionar no `ferramentas.json`**:
```json
{
    "minha_tool": {
        "descricao": "Descrição da sua ferramenta",
        "quando usar": "Quando o usuário fizer X ou Y",
        "caso seja chamada retorne": "minha_tool('parametro')"
    }
}
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Gabriel Marcos** - [marcosgomes068](https://github.com/marcosgomes068)

## 🙏 Agradecimentos

- [Cohere](https://cohere.ai) pela API de IA
- Comunidade Python pela inspiração
- Todos os contribuidores do projeto