"""This module is the start module to generate FastApi app."""

from fastapi import FastAPI, status

from auth.routers import router as auth_router
from candidates import routers as candidate_router
from core.db import db_lifespan
from DIContainer import DIContainer
from users import routers as user_routers


def config_dependencies_wiring(container: DIContainer) -> None:
    """Wiring function for dependency injection.

    This function is responsible to wire the python packages that has @inject decorator
    so the library can inject the required instance.

    Args:
        container (DIContainer): an instance of DeclarativeContainer that has all our class which we need to inject
    """
    container.wire(packages=["candidates", "users"])


def create_app() -> None:
    """This function is the starter function for our server."""
    app = FastAPI(lifespan=db_lifespan)
    app.include_router(user_routers.router)
    app.include_router(candidate_router.candidate_router)
    app.include_router(candidate_router.all_candidate_router)
    app.include_router(candidate_router.generate_report_router)
    app.include_router(auth_router)

    container = DIContainer()
    config_dependencies_wiring(container)

    @app.get("/health", status_code=status.HTTP_200_OK, tags=["health-check"])
    async def health() -> dict:
        """
        Basic route to check if the server is running.

        Returns:
            dict: with a message to confirm that the server is running
        """
        return {"message": "App is running!"}

    return app
