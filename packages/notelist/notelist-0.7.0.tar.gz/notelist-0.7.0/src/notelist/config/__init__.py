"""Configuration package."""

from os.path import dirname, join
from notelist.config.settings import SettingsManager


# File paths
_dir = dirname(__file__)
settings_path = join(_dir, "settings.json")

# Settings manager object
sm = SettingsManager(settings_path)
