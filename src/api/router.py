from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.services.analytics import create_general_dataset, create_comments_dataset

router = APIRouter(
    prefix='/api',
    tags=['api'],
)


@router.get('/comments')
async def get_comments(login: str):
    data = create_comments_dataset(login, to_json=True)
    return JSONResponse(content=data)
    
@router.get('/general')
async def get_general(login: str):
    data = create_general_dataset(login, to_json=True)
    return JSONResponse(content=data)