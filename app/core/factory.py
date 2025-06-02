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
    app = FastAPI(title="rpn calculator server")

    # Attach services to app.state
    app.state.services = services

    # Routers
    app.include_router(api_router)

    # Startup/Shutdown Events
    @app.on_event("startup")
    async def on_startup():
        services["logger"].info(f"{app.title} has started...")

    @app.on_event("shutdown")
    async def on_shutdown():
        services["logger"].info(f"{app.title} has shutdown...")

    return app
