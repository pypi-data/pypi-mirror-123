"""MongoDB block list module."""

from datetime import datetime

from pymongo.database import Database

from notelist.db.base.blocklist import BlockListManager


class MongoDbBlockListManager(BlockListManager):
    """MongoDB block list manager."""

    def __init__(self, root_dm: "MongoDbManager", db: Database, col: str):
        """Initialize instance.

        :param root_dm: Root database manager.
        :param db: MongoDB database name.
        :param col: MongoDB block list collection name.
        """
        self._root_dm = root_dm
        self._db = db
        self._col = col

    def contains(self, _id: str) -> bool:
        """Return whether a document with a given ID (JWT token) exists or not.

        If the document exists but is expired, it's deleted and `False` is
        returned.

        :param _id: Block list ID (JWD token).
        :return: Whether the block list contains the ID or not.
        """
        # Get document
        bl = self._db[self._col].find_one({"_id": _id})

        # Check if the document exists
        if bl is None:
            return False

        # Check if the document is expired
        exp = bl["expiration"]
        now = int(datetime.now().timestamp())

        if now > exp:
            self._delete(_id)
            return False

        return True

    def put(self, _id: str, exp: int):
        """Put a block list document.

        :param _id: Block list ID (JWD token).
        :param exp: 10-digit expiration timestamp in seconds.
        """
        f = {"_id": _id}
        bl = {"_id": _id, "expiration": exp}

        self._db[self._col].replace_one(f, bl, upsert=True)

    def _delete(self, _id: str):
        """Delete a block list document given its ID (JWD token).

        :param _id: Block list ID (JWD token).
        """
        self._db[self._col].delete_one({"_id": _id})
