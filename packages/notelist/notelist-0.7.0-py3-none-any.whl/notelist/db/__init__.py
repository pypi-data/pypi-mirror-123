"""Database package."""

from notelist.config import sm
from notelist.db.mongodb import MongoDbManager
from notelist.db.dynamodb import DynamoDbManager
from notelist.db.localst import LocalStManager


db_sys_key = "NL_DB_SYS"
db_sys = sm.get(db_sys_key)


if db_sys == "mongodb":
    uri = sm.get("NL_MONGODB_URI")        # MongoDB URI
    db = sm.get("NL_MONGODB_DB")          # Database name
    us_col = sm.get("NL_MONGODB_US_COL")  # Users collection name
    nb_col = sm.get("NL_MONGODB_NB_COL")  # Notebooks collection name
    no_col = sm.get("NL_MONGODB_NO_COL")  # Notes collection name
    bl_col = sm.get("NL_MONGODB_BL_COL")  # Block list collection name

    db = MongoDbManager(uri, db, us_col, nb_col, no_col, bl_col)
elif db_sys == "dynamodb":
    ep = sm.get("NL_DYNAMODB_AWS_ENDPOINT")            # AWS endpoint URL
    reg = sm.get("NL_DYNAMODB_AWS_REGION")             # AWS region name
    aki = sm.get("NL_DYNAMODB_AWS_ACCESS_KEY_ID")      # AWS Access Key ID
    sak = sm.get("NL_DYNAMODB_AWS_SECRET_ACCESS_KEY")  # AWS Secret Access Key
    st = sm.get("NL_DYNAMODB_AWS_SESSION_TOKEN")       # AWS Session Token

    us_tab = sm.get("NL_DYNAMODB_US_TAB")  # Users table name
    nb_tab = sm.get("NL_DYNAMODB_NB_TAB")  # Notebooks table name
    no_tab = sm.get("NL_DYNAMODB_NO_TAB")  # Notes table name
    bl_tab = sm.get("NL_DYNAMODB_BL_TAB")  # Block list table name

    db = DynamoDbManager(us_tab, nb_tab, no_tab, bl_tab, ep, reg, aki, sak, st)
elif db_sys == "localst":
    path = sm.get("NL_LOCALST_PATH")  # JSON file path
    db = LocalStManager(path)
else:
    raise Exception(f"Unsupported '{db_sys_key}' value")
