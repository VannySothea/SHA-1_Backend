from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.controller.sha1 import get_hash
from app.responses.hash import Sha1HashListResponse
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="/hash",
    tags=["SHA1"],
    responses={404: {"description": "Not found"}},
)

@router.get("/ping", response_class=PlainTextResponse)
async def uptime_ping():
    return "pong"

@router.get("/sha1", response_model=Sha1HashListResponse, status_code=status.HTTP_200_OK)
async def get_sha1_hash():
    return await get_hash()