import csv
import json
from json import JSONDecodeError

from streamstats.errors import ReadFileError
from streamstats.validate import validate_row


def process(row):
    if validate_row(row):
        print(row)

def process_csv(csv_file, is_skip_invalid):
    with open(csv_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            process(row)

def process_jsonl(jsonl_file, is_skip_invalid):
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
                process(row)
            except JSONDecodeError as e:
                if is_skip_invalid:
                    print("WARNING! Error of reading file")
                else:
                    raise ReadFileError(f"Error of reading file: {e}")
