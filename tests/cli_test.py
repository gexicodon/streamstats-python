import json
import csv
import pytest

from streamstats.__main__ import main


def run_main(monkeypatch, *args):
    monkeypatch.setattr("sys.argv", ["streamstats", *map(str, args)])
    main()


def read_csv_report(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["metric", "key", "value"]
    return {(metric, key): value for metric, key, value in rows[1:]}


def test_cli_success_csv(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,api,ok\n",encoding="utf-8")

    run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out)

    assert json.loads(out.read_text(encoding="utf-8"))["valid_events"] == 1

def test_cli_success_jsonl(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.jsonl"
    out = tmp_path / "report.json"
    f.write_text('{"timestamp":"2026-10-06T12:08:00+00:00","level":"ERROR","source":"api","message":"Rate limit exceeded"}')

    run_main(monkeypatch, "analyze", f, "--format", "jsonl", "--output", out)

    assert json.loads(out.read_text(encoding="utf-8"))["valid_events"] == 1

def test_cli_success_to_csv_jsonl(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.jsonl"
    out = tmp_path / "report.csv"
    f.write_text('{"timestamp":"2026-10-06T12:08:00+00:00","level":"ERROR","source":"api","message":"Rate limit exceeded"}')

    run_main(monkeypatch, "analyze", f, "--format", "jsonl", "--output", out)

    report = read_csv_report(out)
    assert report[("valid_events", "")] == "1"
    assert report[("invalid_events", "")] == "0"
    assert report[("valid_levels", "ERROR")] == "1"
    assert report[("valid_levels", "INFO")] == "0"
    assert report[("valid_sources", "api")] == "1"
    assert report[("errors_count_in_sources", "api")] == "1"
    assert report[("top_sources_by_errors", "api")] == "1"
    assert report[("first_and_last_ts", "first_ts")] == "2026-10-06 12:08:00+00:00"
    assert report[("first_and_last_ts", "last_ts")] == "2026-10-06 12:08:00+00:00"

def test_cli_success_to_csv_csv(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.csv"
    out = tmp_path / "report.csv"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,ERROR,api,ok\n", encoding="utf-8")

    run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out)

    report = read_csv_report(out)
    assert report[("valid_events", "")] == "1"
    assert report[("invalid_events", "")] == "0"
    assert report[("valid_levels", "ERROR")] == "1"
    assert report[("valid_levels", "INFO")] == "0"
    assert report[("valid_sources", "api")] == "1"
    assert report[("errors_count_in_sources", "api")] == "1"
    assert report[("top_sources_by_errors", "api")] == "1"
    assert report[("first_and_last_ts", "first_ts")] == "2026-10-06 10:00:00+00:00"
    assert report[("first_and_last_ts", "last_ts")] == "2026-10-06 10:00:00+00:00"


def test_cli_skip_invalid_csv(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,BOMBOMBOM,api,ok\n", encoding="utf-8")
    run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out, "--skip-invalid")

    assert json.loads(out.read_text(encoding="utf-8"))["invalid_events"] == 1

def test_cli_skip_invalid_jsonl(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.jsonl"
    out = tmp_path / "report.json"
    f.write_text('{"timestamp":"вчера","level":"ERROR","source":"api","message":"Rate limit exceeded"}', encoding="utf-8")
    run_main(monkeypatch, "analyze", f, "--format", "jsonl", "--output", out, "--skip-invalid")

    assert json.loads(out.read_text(encoding="utf-8"))["invalid_events"] == 1


def test_cli_exit_code_2_jsonl(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.jsonl"
    out = tmp_path / "report.json"
    f.write_text('{"timestamp":"вчера","level":"ERROR","source":"api","message":"Rate limit exceeded"}', encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "jsonl", "--output", out)

    assert exc.value.code == 2
    assert "Invalid timestamp" in capsys.readouterr().err

def test_cli_exit_code_2_csv(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,BOMBOMBOM,api,ok\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out)

    assert exc.value.code == 2
    assert "Invalid level" in capsys.readouterr().err

def test_cli_unmatched_format_csv(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,ERROR,api,ok\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "jsonl", "--output", out)

    assert exc.value.code == 2
    assert "Unmatched format" in capsys.readouterr().err

def test_cli_unmatched_format_jsonl(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.jsonl"
    out = tmp_path / "report.json"
    f.write_text('{"timestamp":"2026-10-06T12:08:00+00:00","level":"ERROR","source":"api","message":"Rate limit exceeded"}', encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out)

    assert exc.value.code == 2
    assert "Unmatched format" in capsys.readouterr().err

def test_cli_unsupported_format(tmp_path, monkeypatch, capsys):
    f = tmp_path / "test.tsx"
    out = tmp_path / "report.json"
    f.write_text('<p>not a CSV or json</p>', encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "json", "--output", out)

    assert exc.value.code == 2
    assert "Unsupported format" in capsys.readouterr().err

def test_cli_file_not_found(tmp_path, monkeypatch, capsys):
    out = tmp_path / "report.json"
    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", "file.jsonl", "--format", "jsonl", "--output", out)

    assert exc.value.code == 2
    assert "File is not found" in capsys.readouterr().err

