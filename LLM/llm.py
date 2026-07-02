import json
import os
import re

import ollama
from dotenv import load_dotenv



load_dotenv()


def _get_model_name() -> str:
    return os.getenv("OLLAMA_MODEL", "gemma3:270m")


def _ollama_chat(system_prompt: str, user_message: str) -> str:
    response = ollama.chat(
        model=_get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        stream=False,
    )

    return response["message"]["content"]


def _parse_json_array(text: str, fallback: list[str]) -> list[str]:
    cleaned = text.strip()

    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return fallback

    try:
        parsed = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        return fallback

    if not isinstance(parsed, list):
        return fallback

    allowed = set(fallback)
    selected = [item for item in parsed if isinstance(item, str) and item in allowed]
    return selected or fallback[:5]


def filter_brochure_links(website_url: str, links: list[str]) -> list[str]:
    system_prompt = """
You are a business content strategist.

Your job is to choose only the website links that are useful for creating a professional business brochure.

Keep links about:
- About the company
- Services or products
- Pricing or plans
- Contact or locations
- Team or leadership
- Case studies, portfolio, or testimonials

Remove links about:
- Login, signup, cart, checkout, account pages
- Legal boilerplate only pages unless they add business value
- Blog archives, tags, categories, pagination
- Social media, app stores, external platforms
- Duplicate utility pages

Return ONLY a JSON array of selected URLs.
Do not include markdown or explanations.
"""

    user_message = f"""
Website URL:
{website_url}

Candidate links:
{json.dumps(links, indent=2)}

Task:
Select the most important links for building a business brochure.
Return only a JSON array of URLs chosen from the candidate list.
"""

    response = _ollama_chat(system_prompt, user_message)
    return _parse_json_array(response, links[:5])


def _clean_html_output(text: str) -> str:
    cleaned = text.strip()

    fence_match = re.search(r"```(?:html)?\s*(.*?)\s*```", cleaned, re.DOTALL | re.IGNORECASE)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    return cleaned


def generate_brochure(
    website_url: str,
    pages_content: dict[str, str],
) -> str:
    system_prompt = """
You are an expert business brochure designer and copywriter.

Your job:
- Create a complete, polished business brochure as a single HTML document.
- Include <!DOCTYPE html>, <html>, <head>, and <body> tags.
- Add simple embedded CSS in a <style> tag for a clean, professional brochure layout.
- Use semantic HTML sections such as hero, about, services, highlights, contact, and call-to-action when relevant.
- Write concise, professional marketing copy based only on the provided website content.
- Do not invent facts, pricing, testimonials, or contact details that are not supported by the content.
- Do not output markdown, explanations, templates, or outlines.
- Do not wrap the result in markdown or HTML code fences.
- Return only raw HTML suitable for opening directly in a browser.
"""

    formatted_pages = "\n\n".join(
        f"URL: {page_url}\nContent:\n{content}"
        for page_url, content in pages_content.items()
    )

    user_message = f"""
Primary website:
{website_url}

Collected website content:
{formatted_pages}

Task:
Write the final business brochure for this specific company using the content above.
Return one complete HTML document with real company details, not a generic brochure template.
"""

    response = _ollama_chat(system_prompt, user_message).strip()
    return _clean_html_output(response)


def summarize_with_ollama(
        website_text: str,
        user_prompt: str
):

    model_name = os.getenv("OLLAMA_MODEL", "gemma3:270m")

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

