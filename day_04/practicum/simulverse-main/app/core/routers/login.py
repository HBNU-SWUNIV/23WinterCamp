from os.path import dirname, abspath
from pathlib import Path
from datetime import timedelta

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from ..models.database import db_manager
from ..models.auth_manager import auth_manager
from ..instance.config import MONGODB_URL, ACCESS_TOKEN_EXPIRE_MINUTES
from ..schemas.user_model import UserLoginForm, UserModel
from ..libs.resolve_error import resolve_error

router = APIRouter(include_in_schema=False)

db_manager.init_manager(MONGODB_URL, "simulverse")
BASE_DIR = dirname(dirname(abspath(__file__)))

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@router.get("/login/")
def render_login(request: Request):
    errors = []
    if 'errors' in request.query_params:
        errors = [ resolve_error(x) for x in request.query_params['errors'].split('.')]
    return templates.TemplateResponse("auth/login.html", {"request": request, "errors":errors, "login":False})

@router.post("/login/")
async def handle_login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_manager.authenticate_user(form_data.username, form_data.password)
    if user :
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await auth_manager.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        form_data.__dict__.update(msg="Login Successful :)")
        form_data.__dict__.update(request=request)
        form_data.__dict__.update(data={})
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, secure=True, samesite="lax")
        return response

    else:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return templates.TemplateResponse("auth/login.html", {"request": request, "login":False})

@router.get("/logout/")
def protected_route(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response