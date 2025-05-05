from pydantic import BaseModel
from bson import ObjectId
from typing import List

class Sha1HashItem(BaseModel):
    hashes_message: str
    original_message: str
    id: str

    class Config:
        json_encoders = {
            ObjectId: str
        }

class Sha1HashListResponse(BaseModel):
    hashes: List[Sha1HashItem]
    success: str


