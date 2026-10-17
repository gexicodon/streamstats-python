import pytest
import json

from streamstats.__main__ import main

def run_main(monkeypatch, *args):
    monkeypatch.setattr("sys.argv", ["streamstats", *map(str, args)])
    main()


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
    out = tmp_path / "report.csv"
    f.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,BOMBOMBOM,api,ok\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        run_main(monkeypatch, "analyze", f, "--format", "csv", "--output", out)

    assert exc.value.code == 2
    assert "Invalid level" in capsys.readouterr().err



