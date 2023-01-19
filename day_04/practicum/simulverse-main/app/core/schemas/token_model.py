from pydantic import BaseModel, Field, EmailStr

class Token(BaseModel):
    access_token: str | str
    token_type: str | None = None


class TokenData(BaseModel):
    email: str =""