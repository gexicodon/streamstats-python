import argparse
from pathlib import Path

from streamstats.errors import InputFileError, InvalidFormat, UnmatchedFormatError


def main():
    """парсинг ввода из CLI с помощью argparse и вызов функций анализа"""
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
            with open(file, 'r') as f:
                for line in f:
                    print(line)

    except InputFileError as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except InvalidFormat as e:
        parser.exit(2, f"{parser.prog}: Error: {e}\n")
    except UnmatchedFormatError as e:
        parser.exit(2, f"{parser.prog}: Error:{e}\n")
    # print(args.action, args.inputs, args.format, args.output, args.skip_invalid)


    


if __name__ == '__main__':
    main()
