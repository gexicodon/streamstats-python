from datetime import datetime

from streamstats.errors import InvalidLineError


def validate_level(row):
    """ Валидирует level строки.
    Args:
        row: строчка

    Returns:
        None
    """
    if "level" not in row:
        raise InvalidLineError('Missing field "level"')

    level = row["level"]

    if level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        raise InvalidLineError(f"Invalid level: {level}")



def validate_timestamp(row):
    """ Валидирует timestamp строки.
    Args:
        row: строчка

    Returns:
        None
    """

    if "timestamp" not in row:
        raise InvalidLineError('Missing field "timestamp"')

    timestamp = row["timestamp"]

    if not isinstance(timestamp, str):
        raise InvalidLineError(
            f"Timestamp must be a string: {timestamp!r}"
        )

    try:
        datetime.fromisoformat(timestamp)
    except ValueError as e:
        raise InvalidLineError(
            f"Invalid timestamp: {timestamp!r}"
        ) from e


def validate_row(row):
    """ Валидирует всю строчку.
    Args:
        row: строчка

    Returns:
        None
    """

    if not isinstance(row, dict):
        raise InvalidLineError(
            f"Expected an object, got: {row!r}"
        )

    validate_timestamp(row)
    validate_level(row)