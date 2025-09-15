class tki:
    def __init__(self, user_prompt, pathtools, toolsdir):
        self.user_prompt = user_prompt
        self.pathtools = pathtools
        self.toolsdir = toolsdir

    tki_prompt = """
    voce é uma agente especialista em entender o que o usuário está procurando.
    {toolsdir} essa é sua caixa de ferramentas.

    Preste muita atenção nos parâmetros de cada ferramenta:
    - descrição: o que a ferramenta faz
    - quando usar: em quais situações você deve utilizar essa ferramenta
    - caso seja chamada retorne: o que você deve retornar se essa ferramenta for chamada (nenhuma palavra a mais)

    Analise cuidadosamente antes de sugerir uma ferramenta. Considere todos os detalhes e utilize apenas a ferramenta mais adequada para a necessidade do usuário.

    {pathtools} esses são os caminhos das ferramentas
    {user_prompt} essa é a pergunta do usuário

    Responda apenas com o nome da ferramenta que você acha que é a melhor para o usuário (máximo 5 palavras).
    Se nenhuma ferramenta for útil, peça ao usuário mais detalhes.
    """
    
    