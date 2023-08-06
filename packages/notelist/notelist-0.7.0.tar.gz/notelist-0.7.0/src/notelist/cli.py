"""CLI (Command Line Interface) module."""

import sys
from typing import Optional

import click
from flask import Flask
from flask.cli import AppGroup

from notelist.tools import get_uuid, get_hash
from notelist.schemas.users import UserSchema
from notelist.db import db


# CLI objects
user_cli = AppGroup("user")

# Schemas
schema = UserSchema()


@user_cli.command("create")
@click.argument("username", type=str)
@click.argument("password", type=str)
@click.argument("admin", type=bool)
@click.argument("enabled", type=bool)
@click.argument("name", type=str, required=False)
@click.argument("email", type=str, required=False)
def create_user(
    username: str, password: str, admin: bool, enabled: bool,
    name: Optional[str] = None, email: Optional[str] = None
):
    """Create a user in the database.

    :param username: Username.
    :param password: Password.
    :param admin: Whether the user is an administrator or not.
    :param enabled: Whether the user is enabled or not.
    :param name: Name (optional).
    :param email: E-mail address (optional).
    """
    if db.users.get_by_username(username):
        sys.exit("Error: User already exists.")

    user = {
        "id": get_uuid(),
        "username": username,
        "password": password,
        "admin": admin,
        "enabled": enabled}

    if name is not None:
        user = user | {"name": name}

    if email is not None:
        user = user | {"email": email}

    try:
        user = schema.load(user)
    except Exception as e:
        sys.exit(str(e))

    user["password"] = get_hash(password)
    db.users.put(user)

    print("User created")


def add_commands(app: Flask):
    """Add the Flask commands.

    :param app: Flask application object.
    """
    app.cli.add_command(user_cli)
