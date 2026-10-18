import pytest

from streamstats import analysis
from streamstats.errors import InvalidLineError
from streamstats.parsers import process_csv, process_jsonl


def test_process_csv_success(tmp_path):
    """тестим, что dictreader правильно читает csv и передаёт в анализатор строки в виде словарей"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,api,Service started\n2026-10-06T10:00:05+00:00,DEBUG,api,Health check passed\n", encoding="utf-8")
    process_csv(str(csv_file), is_skip_invalid=False)

    assert analysis.stats_counter["valid_events"] == 2
    assert analysis.stats_counter["invalid_events"] == 0

def test_process_jsonl_success(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    jsonl_file.write_text('{"timestamp":"2026-10-06T12:00:00+00:00","level":"INFO","source":"api","message":"Service started"}\n{"timestamp":"2026-10-06T12:00:01+00:00","level":"DEBUG","source":"api","message":"Health check"}',encoding="utf-8")
    process_jsonl(str(jsonl_file), is_skip_invalid=False)

    assert analysis.stats_counter["valid_events"] == 2
    assert analysis.stats_counter["invalid_events"] == 0

def test_process_csv_skip_invalid(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text('timestamp,level,source,message\n2026-10-06T11:00:00+00:00,INFO,api,Valid line\nnot-a-date,ERROR,db,Bad timestamp\nnot-a-csv\n')
    process_csv(str(csv_file), is_skip_invalid=True)

    assert analysis.stats_counter["valid_events"] == 1
    assert analysis.stats_counter["invalid_events"] == 2

def test_process_jsonl_skip_invalid(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    jsonl_file.write_text('{"timestamp":"2026-10-06T13:00:00+00:00","level":"INFO","source":"api","message":"Valid line"}\n{not json}\n{"timestamp":"2026-10-06T13:02:00+00:00","level":"TRACE","source":"web","message":"Invalid level"}\n')
    process_jsonl(str(jsonl_file), is_skip_invalid=True)

    assert analysis.stats_counter["valid_events"] == 1
    assert analysis.stats_counter["invalid_events"] == 2

def test_process_json_fail(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    jsonl_file.write_text('{"timestamp":"2026-10-06T13:00:00+00:00","level":"INFO","source":"api","message":"Valid line"}\n{not json}')

    with pytest.raises(InvalidLineError):
        process_jsonl(str(jsonl_file), is_skip_invalid=False)

def test_process_csv_fail(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text('timestamp,level,source,message\nnot-a-csv\n')

    with pytest.raises(InvalidLineError):
        process_csv(str(csv_file), is_skip_invalid=False)

def test_process_csv_fail_timestamp(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text('timestamp,level,source,message\n2026-10-06T11:00:00+00:00,INFO,api,Valid line\nnot-a-date,ERROR,db,Bad timestamp\n')

    with pytest.raises(InvalidLineError):
        process_csv(str(csv_file), is_skip_invalid=False)

def test_process_jsonl_fail_timestamp(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    jsonl_file.write_text('{"timestamp":"2026-10-06T13:02:00+00:00","level":"INFO","source":"web","message":"Invalid level"}\n{"timestamp":"not-a-date","level":"ERROR","source":"db","message":"Bad timestamp"}\n')
    with pytest.raises(InvalidLineError):
        process_jsonl(str(jsonl_file), is_skip_invalid=False)

def test_process_jsonl_fail_level(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    jsonl_file.write_text('{"timestamp":"2026-10-06T13:00:00+00:00","level":"INFO","source":"api","message":"Valid line"}\n{"timestamp":"2026-10-06T13:02:00+00:00","level":"TRACE","source":"web","message":"Invalid level"}\n')
    with pytest.raises(InvalidLineError):
        process_jsonl(str(jsonl_file), is_skip_invalid=False)

def test_process_csv_fail_level(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text('timestamp,level,source,message\n2026-10-06T11:02:00+00:00,TRACE,web,Invalid level\n')
    with pytest.raises(InvalidLineError):
        process_csv(str(csv_file), is_skip_invalid=False)

def test_process_csv_fail_source(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("timestamp,level,source,message\n2026-10-06T11:07:00+00:00,ERROR,,Empty source 2\n")
    with pytest.raises(InvalidLineError):
        process_csv(str(csv_file), is_skip_invalid=False)

def test_process_jsonl_fail_source(tmp_path):
    json_file = tmp_path / "test.jsonl"
    json_file.write_text('{"timestamp":"2026-10-06T13:00:00+00:00","level":"INFO","source":"api","message":"Valid line"}\n{"timestamp":"2026-10-06T13:04:00+00:00","level":"INFO","source":"","message":"Empty source"}\n')
    with pytest.raises(InvalidLineError):
        process_jsonl(str(json_file), is_skip_invalid=False)

