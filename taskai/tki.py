class tki:
    def __init__(self, user_prompt, pathtools, toolsdir, api_key):
        self.user_prompt = user_prompt
        self.pathtools = pathtools
        self.toolsdir = toolsdir
        self.api_key = api_key
        self.memory = []  # Histórico de conversas
        self.max_memory = 3  # Limite de memória

    tki_prompt = """
    Você é uma agente especialista em analisar solicitações e extrair informações precisas.
    {toolsdir} essa é sua caixa de ferramentas.

    INSTRUÇÕES IMPORTANTES:
    - Analise o texto do usuário para extrair nomes específicos de apps/pastas/termos
    - Para apps: identifique o nome exato (notepad, calculator, chrome, etc)
    - Para pastas: identifique se é pasta comum (documentos, downloads) ou caminho específico
    - Para pesquisas: extraia o termo exato a ser pesquisado
    - Para arquivos: identifique nome e conteúdo se especificado

    FERRAMENTAS DISPONÍVEIS:
    {toolsdir}

    CONTEXTO DA CONVERSA: {memory}
    CAMINHOS DAS FERRAMENTAS: {pathtools}
    
    SOLICITAÇÃO DO USUÁRIO: {user_prompt}

    FORMATO DE RESPOSTA OBRIGATÓRIO:
    =>nome_da_ferramenta|parametro_especifico<=
    
    IMPORTANTE: Use EXATAMENTE este formato com => no início e <= no final
    
    Exemplos corretos:
    - "abrir notepad" → =>abrir_apps|notepad<=
    - "abrir pasta documentos" → =>abrir_pastas|documentos<=  
    - "pesquisar receitas" → =>pesquisar_web|receitas<=
    - "criar arquivo notas" → =>criar_arquivo|notas<=
    
    NUNCA esqueça o <= no final!
    """

    # Função para decidir qual ferramenta usar
    @staticmethod
    def cohere_command(user_prompt, base_prompt, api_key, model="command", max_tokens=20):
        try:
            import cohere
            if not api_key or not api_key.strip():
                raise ValueError("API key não pode ser vazia")
            client = cohere.Client(api_key)
            full_prompt = f"{base_prompt}\n\n{user_prompt}"
            response = client.generate(prompt=full_prompt, model=model, max_tokens=max_tokens)
            return response.generations[0].text.strip() if response.generations else ""
        except ValueError as ve:
            print(f"Erro de validação: {ve}"); return ""
        except Exception as e:
            print(f"Erro na API Cohere: {e}"); return ""
    
    # Método para obter a recomendação de ferramenta (melhorado)
    def get_tool_recommendation(self, model="command", max_tokens=50):
        try:
            if not self.user_prompt or not self.user_prompt.strip():
                return "Erro: Prompt do usuário vazio"
            if not self.toolsdir:
                return "Erro: Nenhuma ferramenta disponível"
            memory_str = " | ".join([f"U: {item['user']} -> A: {item['response']}" for item in self.memory[-2:]])
            formatted_prompt = self.tki_prompt.format(toolsdir=self.toolsdir, pathtools=self.pathtools, user_prompt=self.user_prompt, memory=memory_str)
            response = self.cohere_command(self.user_prompt, formatted_prompt, self.api_key, model, max_tokens)
            self.add_to_memory(self.user_prompt, response)  # Adiciona à memória
            return response if response else "Erro: Nenhuma resposta obtida"
        except KeyError as ke:
            print(f"Erro de formatação do prompt: {ke}"); return "Erro de configuração"
        except Exception as e:
            print(f"Erro na recomendação: {e}"); return "Erro interno"

    # Método para executar a ferramenta com parâmetros inteligentes
    def execute_tool_smart(self, response):
        try:
            tool_name, params = self.extract_tool_and_params(response)
            
            if tool_name in self.toolsdir:
                base_cmd = self.toolsdir[tool_name].get("caso seja chamada retorne", f"Executando {tool_name}")
                
                if params:
                    # Substituir placeholder genérico pelo parâmetro específico
                    if "nome_do_app" in base_cmd:
                        return base_cmd.replace("nome_do_app", params)
                    elif "caminho_da_pasta" in base_cmd:
                        return base_cmd.replace("caminho_da_pasta", params)
                    elif "termo_de_busca" in base_cmd:
                        return base_cmd.replace("termo_de_busca", params)
                    elif "nome_arquivo" in base_cmd:
                        return base_cmd.replace("nome_arquivo", params)
                    else:
                        return f"{base_cmd} com parâmetro: {params}"
                else:
                    return base_cmd
            return f"Ferramenta '{tool_name}' não encontrada"
        except Exception as e:
            print(f"Erro ao executar ferramenta: {e}"); return "Erro na execução"
    
    # Método compatível para execução simples
    def execute_tool(self, tool_name):
        try:
            if tool_name in self.toolsdir:
                return self.toolsdir[tool_name].get("caso seja chamada retorne", f"Executando {tool_name}")
            return f"Ferramenta '{tool_name}' não encontrada"
        except Exception as e:
            print(f"Erro ao executar ferramenta: {e}"); return "Erro na execução"
    
    # Extrair ferramenta e parâmetros do formato =>ferramenta|parametro<= (versão robusta)
    def extract_tool_and_params(self, response):
        try:
            # Procura por padrão =>...<=
            if "=>" in response:
                start = response.find("=>") + 2
                
                # Se tem <=, usa normal. Se não, pega até o final
                if "<=" in response:
                    end = response.find("<=")
                    content = response[start:end].strip()
                else:
                    # Pega tudo após => até quebra de linha ou final
                    remaining = response[start:].strip()
                    content = remaining.split('\n')[0].strip()
                
                if "|" in content:
                    tool_name, params = content.split("|", 1)
                    return tool_name.strip(), params.strip()
                else:
                    return content.strip(), ""
            
            # Fallback: procura nomes de ferramentas conhecidas
            for tool in self.toolsdir.keys():
                if tool in response.lower():
                    return tool, ""
                    
            return response.strip(), ""
        except Exception as e:
            print(f"Erro na extração: {e}"); return response, ""
    
    # Compatibilidade com método antigo
    def extract_tool_name(self, response):
        tool_name, _ = self.extract_tool_and_params(response)
        return tool_name
    
    # Adicionar interação à memória
    def add_to_memory(self, user_input, response):
        try:
            self.memory.append({"user": user_input, "response": response})
            if len(self.memory) > self.max_memory:
                self.memory.pop(0)  # Remove o mais antigo
        except Exception as e:
            print(f"Erro ao adicionar à memória: {e}")
    
    # Limpar memória
    def clear_memory(self):
        self.memory.clear()
    
    # printar apenas o nome da ferramenta recomendada pela cohere
    def print_tool_recommendation(self):
        recomendacao = self.get_tool_recommendation()
        tool_name = self.extract_tool_name(recomendacao)
        print(f"Ferramenta recomendada: {tool_name}")

# Testar o tki
if __name__ == "__main__":
    import json, os
    toolsdir = json.load(open("C:\\Users\\Gabriel\\Documents\\GitHub\\TaskAI\\test\\ferramentas.json"))
    tools_path = [os.path.join("C:\\Users\\Gabriel\\Documents\\GitHub\\TaskAI\\test\\mytools", f) for f in os.listdir("C:\\Users\\Gabriel\\Documents\\GitHub\\TaskAI\\test\\mytools") if f.endswith(".py")]
    agente = tki("Quero abrir o app do discord", tools_path, toolsdir, "MoHa7qTxBctiVpM9RYpVoNcHAoAsOI0sKIhaAbaJ")
    agente.print_tool_recommendation()