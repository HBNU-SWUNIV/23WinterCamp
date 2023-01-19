from fastapi.responses import HTMLResponse
from os.path import dirname, abspath
from pathlib import Path
from fastapi import APIRouter, Depends, Request, Response, responses, HTTPException, status
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.responses import StreamingResponse

from jose import JWTError, jwt
from bson.objectid import ObjectId

from ..models.database import db_manager
from ..instance import config
from ..models.auth_manager import get_current_user
from ..schemas.space_model import CreateSpaceForm, SpaceModel


router = APIRouter(include_in_schema=False)

db_manager.init_manager(config.MONGODB_URL, "simulverse")
BASE_DIR = dirname(dirname(abspath(__file__)))

from fastapi.responses import StreamingResponse

import io

@router.get("/asset/image/{image_id}", 
        responses = {
            200: {
                "content": {"image/png": {}}}
        }, response_class=Response)        
async def image(request: Request, image_id:str, auth_user= Depends(get_current_user)):
    image_bytes, content_type = await db_manager.download_file(ObjectId(image_id))
    return Response(content=image_bytes, media_type=content_type)

