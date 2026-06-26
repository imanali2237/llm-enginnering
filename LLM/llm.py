import os

import ollama
from dotenv import load_dotenv


load_dotenv()


def summarize_with_ollama(
        website_text: str,
        user_prompt: str
):

    model_name = os.getenv("OLLAMA_MODEL", "llama3")

    system_prompt = """
You are an expert website summarization assistant.

Your job:
- Analyze website content carefully.
- Create accurate summaries.
- Organize information using clear headings.
- Use bullet points.
- Include important details as well as minor useful details.
- Do not make up information that is not present in the website content.
- Explain complex topics in beginner-friendly language.
"""


    user_message = f"""
User request:
{user_prompt}


Website content:
{website_text}


Task:
Summarize this website based on the user's request.

Requirements:
- Create a structured summary.
- Use bullet points.
- Cover main points.
- Include supporting details.
- Mention important features, services, or concepts.
"""


    response = ollama.chat(

        model=model_name,

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_message
            }

        ]

    )


    return response["message"]["content"]