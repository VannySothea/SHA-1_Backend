from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.controller.sha1 import create_hash
from app.schemas.hash import HashRequest


router = APIRouter(
    prefix="/hash",
    tags=["SHA1"],
    responses={404: {"description": "Not found"}},
)

@router.post("/sha1")
async def create_sha1_hash(data: HashRequest):
    return await create_hash(data)
    

