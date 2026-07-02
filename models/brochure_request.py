from pydantic import BaseModel


class BrochureRequest(BaseModel):
    website_url: str
