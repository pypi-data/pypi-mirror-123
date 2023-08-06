"""MongoDB package."""

from pymongo import MongoClient

from notelist.db.base import MainDbManager
from notelist.db.mongodb.users import MongoDbUserManager
from notelist.db.mongodb.notebooks import MongoDbNotebookManager
from notelist.db.mongodb.notes import MongoDbNoteManager
from notelist.db.mongodb.blocklist import MongoDbBlockListManager


class MongoDbManager(MainDbManager):
    """MongoDB manager."""

    def __init__(
        self, uri: str, db: str, us_col: str, nb_col: str, no_col: str,
        bl_col: str
    ):
        """Initialize instance.

        This method creates the collection indexes if they don't exist.

        :param uri: MongoDB URI ("mongodb://user:password@localhost:port").
        Port is usually 27017.
        :param db: MongoDB database name. E.g. "notelist".
        :param us_col: MongoDB users collection name. E.g. "users".
        :param nb_col: MongoDB notebooks collection name. E.g. "notebooks".
        :param no_col: MongoDB notes collection name. E.g. "notes".
        :param bl_col: MongoDB block list collection name. E.g. "blocklist".
        """
        # Database
        self._db = MongoClient(uri)[db]

        # Managers
        self._users = MongoDbUserManager(self, self._db, us_col)
        self._notebooks = MongoDbNotebookManager(self, self._db, nb_col)
        self._notes = MongoDbNoteManager(self, self._db, no_col)
        self._blocklist = MongoDbBlockListManager(self, self._db, bl_col)

    def switch_id(self, doc: dict) -> dict:
        """Switch the "id" and "_id" keys of a given document.

        :param doc: Original document.
        :return: Result document.
        """
        k1 = "id"
        k2 = "_id"

        if k1 not in doc and k2 not in doc:
            return doc

        old_key = k1 if k1 in doc else k2
        new_key = k2 if old_key == k1 else k1

        _id = doc[old_key]
        doc = doc.copy()
        doc.pop(old_key)

        return {new_key: _id} | doc

    @property
    def users(self) -> MongoDbUserManager:
        """Return the user data manager.

        :return: `MongoDbUserManager` instance.
        """
        return self._users

    @property
    def notebooks(self) -> MongoDbNotebookManager:
        """Return the notebook data manager.

        :return: `MongoDbNotebookManager` instance.
        """
        return self._notebooks

    @property
    def notes(self) -> MongoDbNoteManager:
        """Return the note data manager.

        :return: `MongoDbNoteManager` instance.
        """
        return self._notes

    @property
    def blocklist(self) -> MongoDbBlockListManager:
        """Return the block list manager.

        :return: `MongoDbBlockListManager` instance.
        """
        return self._blocklist
