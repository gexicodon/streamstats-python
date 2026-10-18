from datetime import datetime

from streamstats.config import levels, required_fields
from streamstats.errors import EmptyFieldError, InvalidLineError


def validate_level(row, current_line):
    """ Валидирует level строки.
    Args:
        row: строчка
        current_line: номер текущей строки

    Returns:
        None
    """

    if "level" not in row:
        raise InvalidLineError(f'Missing field "level" at line {current_line}')

    level = row["level"]
    if level == '':
        raise EmptyFieldError(f'Empty field "level" at line {current_line}')
    if level not in levels:
        raise InvalidLineError(f"Invalid level: {level} at line {current_line}")



def validate_timestamp(row, current_line):
    """ Валидирует timestamp строки.
    Args:
        row: строчка
        current_line: номер текущей строки

    Returns:
        None
    """

    if "timestamp" not in row or row['timestamp'] == '':
        raise InvalidLineError(f'Missing field "timestamp" at line {current_line}')

    timestamp = row["timestamp"]

    if not isinstance(timestamp, str):
        raise InvalidLineError(
            f"Timestamp must be a string: {timestamp} at line {current_line}"
        )

    try:
        datetime.fromisoformat(timestamp)
    except ValueError as e:
        raise InvalidLineError(
            f"Invalid timestamp: {timestamp} at line {current_line}"
        ) from e


def validate_source(row, current_line):
    """Валидирует source строки.
    Args:
        row: строчка
        current_line: номер текущей строки
    Returns:
        None
        """

    if "source" not in row:
        raise InvalidLineError(f'Missing field "source" at line {current_line}')

    source = row["source"]

    if source == '':
        raise EmptyFieldError(f'Empty field "source" at line {current_line}')

def validate_message(row, current_line):
    """Валидирует message строки.

    Args:
        row: строчка
        current_line: номер текущей строки


    Returns:
        None
    """
    if "message" not in row:
        raise InvalidLineError(f'Missing field "message" at line {current_line}')


def validate_row(row, current_line):
    """ Валидирует всю строчку.
    Args:
        row: строчка
        current_line: номер текущей строки

    Returns:
        None
    """

    if not isinstance(row, dict):
        raise InvalidLineError(
            f"Expected an object, got: {row} at line {current_line}"
        )

    missing = [field for field in required_fields if (row.get(field) is None or row.get(field) == "")]
    if missing:
        raise InvalidLineError(f"Missing fields {missing} at line {current_line}")
    validate_timestamp(row, current_line)
    validate_level(row, current_line)
    validate_source(row, current_line)
    validate_message(row, current_line)
