from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str

    PG_USER: str
    PG_PASSWORD: str 
    PG_HOST: str
    PG_PORT: int
    PG_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
    
    BACKEND_HOST: str
    BACKEND_PORT: int

    VITE_HOST: str
    VITE_PORT: int

    @property
    def FRONTEND_URL(self) -> str:
        return f"http://{self.VITE_HOST}:{self.VITE_PORT}/"


    ACCESS_SECRET: str
    REFRESH_SECRET: str

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()