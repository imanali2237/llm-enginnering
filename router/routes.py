from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from models.summary_request import SummaryRequest
from models.token_Calculator import TokenCalculator
from models.brochure_request import BrochureRequest
from utilities.scrapper import scrape_website, extract_links, scrape_pages

from LLM.llm import (
    summarize_with_ollama,
    filter_brochure_links,
    generate_brochure,
)
from LLM.titoken import tokenized_text
from LLM.memory_illusion import chat_with_memory
from models.chat_request import ChatRequest

router = APIRouter()


@router.post("/summarize")
def summarize(data: SummaryRequest):


    website_text = scrape_website(
        data.website_url
    )


    summary = summarize_with_ollama(
        website_text,
        data.user_prompt
    )


    return {

        "url": data.website_url,

        "summary": summary

    }

@router.post("/token-calculator")
def token_calculator(data: TokenCalculator):
    return tokenized_text(data.user_prompt)

@router.post("/chat")
def chat(req: ChatRequest):
    return chat_with_memory(req.message)


@router.post("/get-links")
def get_links(url: str):
    return extract_links(url)


@router.post("/generate-brochure", response_class=HTMLResponse)
def generate_brochure_endpoint(data: BrochureRequest):
    website_url = data.website_url

    links = extract_links(website_url, same_domain_only=True)
    selected_links = filter_brochure_links(website_url, links)
    pages_content = scrape_pages(website_url, selected_links)
    brochure_html = generate_brochure(website_url, pages_content)

    return HTMLResponse(content=brochure_html, media_type="text/html")