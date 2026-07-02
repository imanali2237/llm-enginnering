from pydantic import BaseModel


class TutorRequest(BaseModel):
    prompt: str