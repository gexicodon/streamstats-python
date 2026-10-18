class StreamStatsError(Exception):
    """Базовая ошибка приложения"""

class InvalidFormat(StreamStatsError):
    """Ошибка неверного формата файла"""

class UnmatchedFormatError(StreamStatsError):
    """Ошибка ситуации, когда файл формата csv, а в CLI мы говорим, что это jsonl и наоборот"""

class InputFileError(StreamStatsError):
    """Ошибка: не найден файл"""

class InvalidLineError(StreamStatsError):
    """Ошибка невалидной строчки"""


class MissingFieldError(StreamStatsError):
    """Ошибка пропущенного поля"""

class EmptyFieldError(StreamStatsError):
    """Ошибка пустой строки"""


