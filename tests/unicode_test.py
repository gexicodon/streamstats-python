import pytest
import json

import streamstats.analysis as analysis
from streamstats.parsers import process_csv, process_jsonl
from streamstats.report import stats_to_json


def test_cyrillic_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    csv_file.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,бубубебебе,сервис запущен\n", encoding="utf-8")
    process_csv(str(csv_file), is_skip_invalid=False)
    stats_to_json(analysis.total_stats, out)

    raw = out.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["valid_sources"] == {"бубубебебе": 1}

def test_glagolitic_jsonl(tmp_path):
    jsonl_file = tmp_path / "test.jsonl"
    out = tmp_path / "report.json"
    jsonl_file.write_text('{"timestamp":"2026-10-06T12:00:00+00:00","level":"INFO","source":"ⰄⰙⰁⰓⰠ ⰄⰠⰐⰠⰠ!","message":"Service started"}', encoding="utf-8")
    process_jsonl(str(jsonl_file), is_skip_invalid=False)
    stats_to_json(analysis.total_stats, out)

    raw = out.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["valid_sources"] == {"ⰄⰙⰁⰓⰠ ⰄⰠⰐⰠⰠ!": 1}

def test_glagolitic_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    csv_file.write_text('timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,😂,Service started\n', encoding="utf-8")
    process_csv(str(csv_file), is_skip_invalid=False)
    stats_to_json(analysis.total_stats, out)

    raw = out.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["valid_sources"] == {"😂": 1}

def test_emoji_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    out = tmp_path / "report.json"
    csv_file.write_text("timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,😂,сервис запущен\n", encoding="utf-8")
    process_csv(str(csv_file), is_skip_invalid=False)
    stats_to_json(analysis.total_stats, out)

    raw = out.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["valid_sources"] == {"😂": 1}

