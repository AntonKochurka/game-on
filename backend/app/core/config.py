from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "replaceme"
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "gameon"
    
    PROJECT_NAME: str = "GameOn"
    HOST: str = "localhost"
    PORT: int = 4300

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
