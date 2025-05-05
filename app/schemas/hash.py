from pydantic import BaseModel


class HashRequest(BaseModel):
    message: str