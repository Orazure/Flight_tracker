from datetime import datetime

def format_datetime(dt: str) -> str:
    """Format datetime string to ISO8601 format.
    
    Args:
        dt (str): Datetime string.
        
    Returns:
        str: Datetime string in ISO8601 format.
        if no datetime
    Examples:
        >>> format_datetime('2020-01-01 00:00')
        '2020-01-01T00:00:00'
    """
    if dt is None:
        return datetime.now().isoformat()
    return datetime.strptime(dt, '%Y-%m-%d %H:%M').isoformat()


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
    return string.replace('"', ' ').replace("'", ' ').replace('(', '').replace(')', '')