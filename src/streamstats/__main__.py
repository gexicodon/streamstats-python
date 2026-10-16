import argparse
from pathlib import Path

from streamstats.errors import (
    EmptyFieldError,
    InputFileError,
    InvalidFormat,
    InvalidLineError,
    MissingFieldError,
    UnmatchedFormatError,
)
from streamstats.parsers import process_csv, process_jsonl
from streamstats.analysis import total_stats
from streamstats.report import stats_to_json



def main():
    """Запускает основной цикл программы и обрабатывает аргументы командной строки.

    Returns:
        None. При возникновении ошибок вызывается sys.exit(2).
    """

    parser = argparse.ArgumentParser(prog="streamstats")
    parser.add_argument('action', default='analyze', help='action to perform')
    parser.add_argument('inputs', metavar='INPUT', nargs='+', help='one or more input files')
    parser.add_argument('--format', required=True, help='input file format')
    parser.add_argument('--output', metavar="REPORT.json", required=True, help='output report file')
    parser.add_argument('--skip-invalid', action='store_true', help='skips problematic lines by logging WARNINGs', required=False)
    args = parser.parse_args()

    try:
        if args.format not in ['csv', 'jsonl']:
            raise InvalidFormat(f"Unsupported format: {args.format}")
        for filename in args.inputs:
            if not Path(filename).is_file():
                raise InputFileError(f"File is not found: {filename}")
            if Path(filename).suffix[1:] not in args.format:
                raise UnmatchedFormatError(f"Unmatched format: {Path(filename).suffix[1:]} in {filename} and {args.format}")


        for file in args.inputs:
            if args.format == 'csv':
                process_csv(file, args.skip_invalid)
                stats_to_json(total_stats, args.output)
            elif args.format == 'jsonl':
                process_jsonl(file, args.skip_invalid)
                stats_to_json(total_stats, args.output)
            else:
                raise InvalidFormat(f"Unsupported format: {args.format}")

    except InputFileError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except InvalidFormat as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except UnmatchedFormatError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except MissingFieldError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except InvalidLineError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except EmptyFieldError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")




if __name__ == '__main__':
    main()
