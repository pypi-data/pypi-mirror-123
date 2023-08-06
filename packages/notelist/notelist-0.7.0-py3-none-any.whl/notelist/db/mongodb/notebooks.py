"""MongoDB notebooks module."""

from typing import Optional

from pymongo import ASCENDING
from pymongo.database import Database

from notelist.db.base.notebooks import NotebookManager


class MongoDbNotebookManager(NotebookManager):
    """MongoDB notebook manager."""

    def __init__(self, root_dm: "MongoDbManager", db: Database, col: str):
        """Initialize instance.

        :param root_dm: Root database manager.
        :param db: MongoDB database name.
        :param col: MongoDB notebooks collection name.
        """
        self._root_dm = root_dm
        self._db = db
        self._col = col

    def get_by_user(self, user_id: str) -> list[dict]:
        """Return all the notebook documents of a given user.

        :param user_id: User ID.
        :return: Notebook documents.
        """
        f = {"user_id": user_id}
        s = [("name", ASCENDING)]
        notebooks = self._db[self._col].find(f, sort=s)

        return list(map(self._root_dm.switch_id, notebooks))

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a notebook document given its ID.

        :param _id: Notebook ID.
        :return: Notebook document if it exists or None otherwise.
        """
        notebook = self._db[self._col].find_one({"_id": _id})

        if notebook is not None:
            notebook = self._root_dm.switch_id(notebook)

        return notebook

    def get_by_name(self, user_id: str, name: str) -> Optional[dict]:
        """Return a notebook document given its user and name.

        :param user_id: Notebook user ID.
        :param name: Notebook name.
        :return: Notebook document if it exists or None otherwise.
        """
        f = {"user_id": user_id, "name": name}
        notebook = self._db[self._col].find_one(f)

        if notebook is not None:
            notebook = self._root_dm.switch_id(notebook)

        return notebook

    def put(self, notebook: dict):
        """Put a notebook document.

        If an existing document has the same ID as `notebook`, the existing
        document is replaced with `notebook`.

        :param notebook: Notebook document.
        """
        notebook = self._root_dm.switch_id(notebook)
        f = {"_id": notebook["_id"]}
        self._db[self._col].replace_one(f, notebook, upsert=True)

    def delete(self, _id: str):
        """Delete a notebook document given its ID.

        :param _id: Notebook ID.
        """
        self._db[self._col].delete_one({"_id": _id})
