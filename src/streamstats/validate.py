from datetime import datetime

from streamstats.errors import MissingFieldError


def validate_timestamp(row):
    try:
        timestamp = row['timestamp']
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False

    except KeyError:
        raise MissingFieldError('Missing field "timestamp"')


def validate_row(row):
    if validate_timestamp(row):
        return True
    else:
        return False
