import cohere

def cohere_command(prompt, api_key, model="command", max_tokens=100):
    client = cohere.Client(api_key)
    response = client.generate(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens
    )
    return response.generations[0].text if response.generations else ""
