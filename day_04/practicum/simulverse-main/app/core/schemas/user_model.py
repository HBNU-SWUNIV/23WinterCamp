from fastapi import Request
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class UserModel(BaseModel):
    userid: str  = ""
    email: str = ""

class UserInDB(UserModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    hashed_password: str = ""
    spaces:dict = {}
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
class UserRegisterForm: 
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: str = ""
        self.email: str = ""
        self.password: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")
        self.rpassword = form.get("rpassword")
        self.agreement = form.get("agreement")

    async def is_valid(self):
        if not self.username or not len(self.username) > 3:
            self.errors.append("Username should be > 3 chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be > 4 chars")
        if self.password != self.rpassword:
            self.errors.append("You have entered different password.")
        if self.agreement == None:
            self.errors.append("You should agree Terms of service")
        if not self.errors:
            return True
        return False

class UserLoginForm: 
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.email: str = ""
        self.password: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be > 4 chars")
        if not self.errors:
            return True
        return False