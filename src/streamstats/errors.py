class StreamStatsError(Exception):
    """Базовая ошибка приложения"""

class InvalidFormat(Exception):
    """Ошибка неверного формата файла"""

class UnmatchedFormatError(Exception):
    """Ошибка ситуации, когда файл формата csv, а в CLI мы говорим, что это jsonl и наоборот"""

class InputFileError(Exception):
    """Ошибка: не найден файл"""

class InvalidLineError(Exception):
    """Ошибка невалидной строчки"""


class MissingFieldError(Exception):
    """Ошибка пропущенного поля"""

class EmptyFieldError(Exception):
    """Ошибка пустой строки"""


