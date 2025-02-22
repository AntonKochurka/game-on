from fastapi import FastAPI

from . import auth

def setup_router(app: FastAPI):
    for mod in [
        auth
    ]:
        app.include_router(mod.router)