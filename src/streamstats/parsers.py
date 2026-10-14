import csv
import json
import sys
from json import JSONDecodeError

from streamstats.errors import InvalidLineError
from streamstats.validate import validate_row


def process(row, is_skip_invalid):
    try:
        validate_row(row)
        print(row)

    except InvalidLineError as e:
        if is_skip_invalid:
            print(f"WARNING! {e}", file=sys.stderr)
        else:
            raise


def process_csv(csv_file, is_skip_invalid):
    with open(csv_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            process(row, is_skip_invalid)


def process_jsonl(jsonl_file, is_skip_invalid):
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
                process(row, is_skip_invalid)

            except JSONDecodeError as e:
                message = f"Error of reading line: {line.rstrip()}"

                if is_skip_invalid:
                    print(f"WARNING! {message}", file=sys.stderr)
                else:
                    raise InvalidLineError(message) from e