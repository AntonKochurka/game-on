from . import app, settings

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.BACKEND_HOST, port=settings.BACKEND_PORT)