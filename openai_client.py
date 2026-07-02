import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def ollama_chat(messages, model="gemma3:270m"):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": messages,
            "stream": False
        }
    )

    return response.json()["message"]["content"]