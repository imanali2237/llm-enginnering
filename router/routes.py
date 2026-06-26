from fastapi import APIRouter

from models.summary_request import SummaryRequest

from utilities.scrapper import scrape_website

from  LLM.llm import summarize_with_ollama


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