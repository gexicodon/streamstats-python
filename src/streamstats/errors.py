class StreamStatsError(Exception):
    """Базовая ошибка приложения"""

class InvalidFormat(Exception):
    pass

class UnmatchedFormatError(Exception):
    pass

class InputFileError(Exception):
    pass

class InvalidLineError(Exception):
    pass
