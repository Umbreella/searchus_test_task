import uvicorn

from app.app import get_asgi_application

if __name__ == '__main__':
    uvicorn.run(**{
        'app': get_asgi_application(),
        'host': '0.0.0.0',
    })
