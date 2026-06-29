from pydantic import BaseModel

class TokenCalculator(BaseModel):
    user_prompt: str