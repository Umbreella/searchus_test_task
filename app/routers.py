from fastapi import FastAPI

from routers import doc_router


def add_routers(app: FastAPI):
    app.include_router(**{
        'router': doc_router.router,
        'prefix': '/api/documentation',
    })

    return app
