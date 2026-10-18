import argparse
from pathlib import Path

from streamstats.analysis import total_stats
from streamstats.errors import (
    InputFileError,
    InvalidFormat,
    StreamStatsError,
    UnmatchedFormatError,
)
from streamstats.parsers import process_csv, process_jsonl
from streamstats.report import print_stats, stats_to_csv, stats_to_json


def main():
    """Запускает основной цикл программы и обрабатывает аргументы командной строки.

    Returns:
        None. При возникновении ошибок вызывается sys.exit(2).
    """

    parser = argparse.ArgumentParser(prog="streamstats")
    parser.add_argument('action', default='analyze', help='action to perform')
    parser.add_argument('inputs', metavar='INPUT', nargs='+', help='one or more input files')
    parser.add_argument('--format', required=True, help='input file format')
    parser.add_argument('--output', metavar="REPORT.[json|csv]", required=False, help='output report file')
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


        for file in set(args.inputs):
            print(f"Processing file: {file}")
            if args.format == 'csv':
                process_csv(file, args.skip_invalid)
            elif args.format == 'jsonl':
                process_jsonl(file, args.skip_invalid)
            else:
                raise InvalidFormat(f"Unsupported format: {args.format}")
        if args.output is None:
            print_stats(total_stats)
        else:
            if Path(args.output).suffix.lower() == '.csv':
                stats_to_csv(total_stats, args.output)
            elif Path(args.output).suffix.lower() == '.json':
                stats_to_json(total_stats, args.output)
            else:
                raise InvalidFormat(f"Unsupported format: {args.output}")

    except StreamStatsError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")

if __name__ == '__main__':
    main()
