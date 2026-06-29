import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def tokenized_text(text: str):
    tokens = encoding.encode(text)

    token_details = [
        {
            "token_id": token_id,
            "token_text": encoding.decode([token_id])
        }
        for token_id in tokens
    ]

    return {
        "text": text,
        "token_count": len(tokens),
        "tokens": token_details
    }