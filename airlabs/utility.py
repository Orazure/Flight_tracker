from datetime import datetime
from loguru import logger


def format_datetime(dt: str) -> str:
    """Format datetime string to ISO8601 format.

    Args:
        dt (str): Datetime string.

    Returns:
        str: Datetime string in ISO8601 format.
            if no datetime provided, return 1970-01-01T01:00:00 string.
    Examples:
        >>> format_datetime('2020-01-01 00:00')
        '2020-01-01T00:00:00'
    """
    if dt is None:
        logger.warning("No datetime found.")
        return "1970-01-01T01:00:00"
    return datetime.strptime(dt, "%Y-%m-%d %H:%M").isoformat()


def replace_illegal_characters(string: str) -> str:
    """Replace characters that are not allowed in the orion data model.

    Args:
        string (str): The string that need to be sanitized.

    Returns:
        str: The sanitized string.

    Examples:
        >>> replace_illegal_characters('Hello " World')
        'Hello World'
        >>> replace_illegal_characters('Hello (World)')
        'Hello World'
    """
    return string.replace('"', " ").replace("'", " ").replace("(", "").replace(")", "")
