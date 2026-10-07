import csv
import json
from io import StringIO

from streamstats.errors import InvalidLineError
def line_parse(line, type_of_file, skip_invalid):
    if type_of_file == "csv":
        line = StringIO(line)
        reader = csv.reader(line)
        for row in reader:
            return row
    elif type_of_file == "jsonl":
        try:
            line = json.loads(line)
            return line
        except json.decoder.JSONDecodeError as e:
            if skip_invalid:
                print(f"WARNING! Invalid line: {line} ")
            else:
                raise InvalidLineError(f"Ошибка JSON: {e}")

