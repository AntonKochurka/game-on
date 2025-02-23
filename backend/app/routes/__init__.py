from fastapi import FastAPI

from . import auth, users

def setup_router(app: FastAPI) -> None:
    for mod in [
        auth.router,
        users.router,
    ]:
        app.include_router(mod.router)