from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from os.path import dirname, abspath
from pathlib import Path
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from .core.models.database import db_manager
from .core.models.auth_manager import auth_manager
from .core.schemas.token_model import Token
from .core.instance.config import MONGODB_URL, ACCESS_TOKEN_EXPIRE_MINUTES

from app.core.routers import page_view, register, login, create, space, asset

BASE_DIR = dirname(abspath(__file__))
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'core/templates')))

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")
db_manager.init_manager(MONGODB_URL, "simulverse")

app.include_router(register.router, prefix="", tags=["register"])
app.include_router(page_view.router, prefix="", tags=["home"])
app.include_router(login.router, prefix="", tags=["login"])
app.include_router(create.router, prefix="", tags=["create"])
app.include_router(space.router, prefix="", tags=["space"])
app.include_router(asset.router, prefix="", tags=["asset"])

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth_manager.create_access_token(
        data={"sub": user.userid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    response = RedirectResponse("/login/?errors=401", status_code=status.HTTP_302_FOUND)
    return response