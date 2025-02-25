from pydantic import BaseModel, Field

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    
    role: str = Field(default="user", frozen=True)

class UserModel(BaseModel):
    id: str
    username: str
    email: str

    role: str

    created_at: str
    updated_at: str