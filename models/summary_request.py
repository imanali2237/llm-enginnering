from pydantic import BaseModel

class SummaryRequest(BaseModel):
    website_url: str
    user_prompt: str