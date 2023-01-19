from os.path import dirname, abspath
from pathlib import Path
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ..models.database import db_manager
from ..instance.config import MONGODB_URL, ACCESS_TOKEN_EXPIRE_MINUTES

from ..schemas.user_model import UserRegisterForm, UserModel

router = APIRouter(include_in_schema=False)

db_manager.init_manager(MONGODB_URL, "simulverse")
BASE_DIR = dirname(dirname(abspath(__file__)))

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@router.get("/register/")
def render_register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register/")
async def handle_register(request: Request):
    form = UserRegisterForm(request)
    await form.load_data()
    if await form.is_valid():
        if await db_manager.create_user(form):
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        else:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("auth/register.html", form.__dict__)
            
    return templates.TemplateResponse("auth/register.html", form.__dict__)