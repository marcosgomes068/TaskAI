from taskai import tki 

result = tki.run_agent(
    name="Orion",
    role="Pesquisador de IA",
    task="Me diga as tendências de inteligência artificial para 2025",
    save="orion.json"
)
print(result)