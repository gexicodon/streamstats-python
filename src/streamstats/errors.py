class StreamStatsError(Exception):
    """Базовая ошибка приложения"""

class InvalidFormat(Exception):
    """Ошибка неверного формата файла"""
    pass

class UnmatchedFormatError(Exception):
    """Ошибка ситуации, когда файл формата csv, а в CLI мы говорим, что это jsonl и наоборот"""
    pass

class InputFileError(Exception):
    """Ошибка: не найден файл"""
    pass

class InvalidLineError(Exception):
    """Ошибка невалидной строчки"""
    pass


class MissingFieldError(Exception):
    """Ошибка пропущенного поля"""
    pass


