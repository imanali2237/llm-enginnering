from fastapi import APIRouter

from models.summary_request import SummaryRequest
from models.token_Calculator import TokenCalculator
from utilities.scrapper import scrape_website

from  LLM.llm import summarize_with_ollama
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