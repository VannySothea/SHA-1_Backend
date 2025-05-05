from fastapi import FastAPI
from app.routes import get_request, post_request
from fastapi.middleware.cors import CORSMiddleware


def create_application():
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(get_request.router)
    application.include_router(post_request.router)

    return application


app = create_application()
