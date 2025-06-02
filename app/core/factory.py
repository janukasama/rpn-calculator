from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.boot import boot_services
from app.routes.v1.api import api_router


def create_app() -> FastAPI:
    """
    FastAPI application factory.
    """

    # Boot all the services
    services = boot_services()

    # Initialize the FastAPI app
    app = FastAPI(title="rpn calculator server", lifespan=lifespan)

    # Attach services to app.state
    app.state.services = services

    # Routers
    app.include_router(api_router)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.services["logger"].info(f"{app.title} has started...")
    yield
    app.state.services["logger"].info(f"{app.title} has shutdown...")
