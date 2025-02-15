from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)