from openai_client import ollama_chat

CHAT_HISTORY = []


def reset_chat():
    global CHAT_HISTORY
    CHAT_HISTORY = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]


def chat_with_memory(user_message: str):
    global CHAT_HISTORY

    # add user message
    CHAT_HISTORY.append({"role": "user", "content": user_message})

    # call Ollama instead of OpenAI
    assistant_message = ollama_chat(CHAT_HISTORY, model="llama3")

    # store assistant response
    CHAT_HISTORY.append({"role": "assistant", "content": assistant_message})

    return {
        "response": assistant_message,
        "history": CHAT_HISTORY
    }


def get_history():
    return CHAT_HISTORY