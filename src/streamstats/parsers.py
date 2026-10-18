import csv
import json
import sys
from json import JSONDecodeError

from streamstats.analysis import count_invalid_events, update_stats
from streamstats.errors import EmptyFieldError, InvalidLineError
from streamstats.validate import validate_row


def process(row, is_skip_invalid, current_line):
    """Основная функция обработки строки jsonl|csv, преобразованной в словарь Python
    Args:
        row: строчка, преобразованная в словарь
        is_skip_invalid: booelan (если 1, пропускать проблемные строчки с WARNING, иначе завершение работы с кодом 2)
        current_line: номер текущей строчки в файле
    Returns:
        None
        """

    try:
        validate_row(row, current_line)
        update_stats(row)

    except EmptyFieldError as e:
        count_invalid_events()
        if is_skip_invalid:
            print(f"WARNING! {e}", file=sys.stderr)
        else:
            raise
    except InvalidLineError as e:
        count_invalid_events()
        if is_skip_invalid:
            print(f"WARNING! {e}", file=sys.stderr)
        else:
            raise


def process_csv(csv_file, is_skip_invalid):
    """Потоковое чтение csv-файла и обработка
    Args:
        csv_file: csv-файл
        is_skip_invalid: booelan (если 1, пропускать проблемные строчки с WARNING, иначе завершение работы с кодом 2)
    Returns:
        None
        """
    current_line = 1
    with open(csv_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            current_line += 1
            process(row, is_skip_invalid, current_line)


def process_jsonl(jsonl_file, is_skip_invalid):
    """Потоковое чтение jsonl-файла и обработка
    Args:
        jsonl_file: jsonl-файл
        is_skip_invalid: booelan (если 1, пропускать проблемные строчки с WARNING, иначе завершение работы с кодом 2)
    Returns:
        None
        """
    current_line = 0
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            current_line += 1
            try:
                row = json.loads(line)
                process(row, is_skip_invalid, current_line)

            except JSONDecodeError as e:
                message = f"Error of reading line: {line.rstrip()} at line {current_line}"
                count_invalid_events()
                if is_skip_invalid:
                    print(f"WARNING! {message}", file=sys.stderr)
                else:
                    raise InvalidLineError(message) from e
