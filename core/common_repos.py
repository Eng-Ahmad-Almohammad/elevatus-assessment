"""A module that has common repositories to use."""
from typing import Any
from uuid import UUID

from beanie import Document
from fastapi import HTTPException


class AbstractRepo:
    """Basic repo that represent the data layer for the passed model."""

    def __init__(self, model: Document) -> None:
        """Class constructor.

        Args:
            model (Document): an instance of beanie document.
        """
        self.model = model

    async def get_by_uuid(self, uuid: UUID) -> Document | None:
        """Find an element by uuid.

        Args:
            uuid (UUID): uuid of the object.

        Returns:
            Document | None: None if the object is not found else an instance of Document.
        """
        return await self.model.find_one(self.model.uuid == uuid)

    async def get_by_email(self, email: str) -> Document | None:
        """Find an element by email.

        Args:
            email (str)

        Returns:
            Document | None: None if the object is not found else an instance of Document.
        """
        return await self.model.find_one(self.model.email == email)

    async def create(self, model: Document) -> Document:
        """Create the Document in the db.

        Args:
            model (Document): an instance of the required Document to create.

        Returns:
            Document: an instance of created Document.
        """
        return await model.create()

    async def update(self, uuid: UUID, updated_data: dict[str, Any]) -> Document:
        """Update the DB document.

        Args:
            uuid (UUID): uuid of the object.
            updated_data (dict[str, Any]): The new data to replace the old data in DB.

        Raises:
            HTTPException: if the object is not found.

        Returns:
            Document: same document with the new data.
        """
        model_object = await self.get_by_uuid(uuid)
        if not model_object:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} not found",
            )
        await model_object.update({"$set": updated_data})
        return await self.get_by_uuid(uuid)

    async def delete(self, uuid: UUID) -> None:
        """Delete the required document.

        Args:
            uuid (UUID): uuid of the object.

        Raises:
            HTTPException: if the object is not found.
        """
        model_object = await self.get_by_uuid(uuid)
        if not model_object:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} not found",
            )
        await model_object.delete()

    async def get_all(self, filters: dict[str, Any]) -> list[Document] | None:
        """Get all documents based on the provided filters.

        Args:
            filters (dict[str, Any]): A valid MongoDB search criteria

        Returns:
            list[Document] | None: Return None of no objects
            founded else return founded objects.
        """
        return await self.model.find(filters).to_list()
