from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email of user")
    password: str = Field(..., min_length=6, description="Password of user")
