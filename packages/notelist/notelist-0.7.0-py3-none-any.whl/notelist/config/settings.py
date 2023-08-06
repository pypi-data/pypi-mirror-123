"""Settings module."""

from os import environ
import json
from typing import Any


class SettingsManager:
    """Key-value settings manager.

    Each setting is stored as an environment variable where the key and value
    of the setting are the key and value of the environment variable.
    """

    def __init__(self, schema_path: str):
        """Initialize the instance loading the setting schema.

        :param schema_path: Setting schema file path.
        """
        with open(schema_path) as f:
            self._schema = json.load(f)

    @property
    def schema(self) -> dict:
        """Return the setting schema.

        :return: Schema.
        """
        return self._schema.copy()

    def get(self, key: str) -> Any:
        """Return the value of a setting.

        An exception is raised if the setting is not found or not set.

        :param key: Setting key.
        :return: Setting value.
        """
        # Schema
        s = self._schema.get(key)

        if s is None:
            raise Exception(f'"{key}" setting not found')

        typ = s["type"]
        req = s["required"]

        # Environment variable
        val = environ.get(key)

        if req and val is None:
            raise Exception(f'"{key}" setting not set')

        if val is not None:
            if typ == "integer":
                val = int(val)
            elif typ == "float":
                val = float(val)
            elif typ == "bool":
                val = bool(val)
            elif typ != "string":
                raise Exception(f'"{typ}" type not supported')

        return val
