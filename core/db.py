"""A module to handle the db connection."""
from logging import info

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from candidates.models import Candidate
from core.settings import Settings
from users.models import User


async def db_lifespan(app: FastAPI):
    """Function to start the connection with mongo db.

    Args:
        app (FastAPI): instance of FastAPI

    Raises:
        Exception: if the connection failed
    """
    CONNECTION_STRING = Settings().DATABASE_URL
    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        await init_beanie(database=app.database, document_models=[User, Candidate])
        info("Connected to database cluster.")

    yield

    app.mongodb_client.close()
