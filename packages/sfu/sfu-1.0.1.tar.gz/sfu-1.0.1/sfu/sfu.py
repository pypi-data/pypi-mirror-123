from __future__ import annotations
from urllib.parse import urlparse, parse_qs


def credentials(uri: str) -> dict:
    """
    Extract configuration data (only credentials) from a URI
    """

    params = {}
    result = urlparse(uri)

    if result.username is not None and result.username != "":
        params["user"] = result.username

    if result.password is not None and result.password != "":

        if ":" not in result.password:
            params["password"] = result.password
        else:
            (password, account) = result.password.split(":")
            params["password"] = password
            params["account"] = account

    return params


def configuration(uri: str, safe: bool = True) -> dict:
    """
    Extract configuration data (both credentials and non-credentials) from a URI
    """

    params = credentials(uri)

    db = for_db(uri)
    if db is not None:
        params["database"] = db

    q_result = parse_qs(urlparse(uri).query)
    for key, values in q_result.items():
        if len(values) == 1:
            if not safe or key == "warehouse":
                params[key] = values[0]

    return params


def for_connection(uri: str, safe: bool = True) -> dict:
    """
    Extract all parameters for a connection constructor
    """
    return configuration(uri, safe)


def for_db(uri: str) -> [str, None]:
    """
    Extract database name for a connection.cursor USE DATABASE <DB> command
    """

    result = urlparse(uri)

    if result.hostname is not None and result.hostname != "":
        return result.hostname
    return None


def for_warehouse(uri: str) -> [str, None]:
    """
    Extract warehouse name for a connection.cursor USE WAREHOUSE <WH> command
    """
    return configuration(uri, False).get("warehouse", None)


def for_table(uri: str) -> [str, None]:
    """
    Extract table name for a connection.cursor SELECT <COLS> FROM <TABLE> command
    """

    result = urlparse(uri)

    if result.path is not None and result.path != "":
        return result.path.lstrip("/")
    return None
