
from streamstats import analysis
from streamstats.parsers import process_csv, process_jsonl


def test_multiple_files_csv(tmp_path):
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    file1.write_text('timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,api,Service started\n2026-10-06T10:00:05+00:00,DEBUG,api,Health check passed\n2026-10-06T10:01:00+00:00,WARNING,db,Slow query: 1200ms\n2026-10-06T10:02:00+00:00,ERROR,db,Connection timeout\n')
    file2.write_text('timestamp,level,source,message\n2026-10-06T10:10:00+00:00,CRITICAL,db,Disk full\n2026-10-06T10:09:00+00:00,DEBUG,worker,Queue size 0\n2026-10-06T10:07:00+00:00,WARNING,db,Replication lag 5s\n')
    process_csv(file1, is_skip_invalid=False)
    process_csv(file2, is_skip_invalid=False)

    assert analysis.stats_counter["valid_events"] == 7
    assert analysis.stats_counter["invalid_events"] == 0

def test_multiple_files_jsonl(tmp_path):
    file1 = tmp_path / "file1.jsonl"
    file2 = tmp_path / "file2.jsonl"
    file1.write_text('{"timestamp":"2026-10-06T12:00:00+00:00","level":"INFO","source":"api","message":"Service started"}\n{"timestamp":"2026-10-06T12:00:01+00:00","level":"DEBUG","source":"api","message":"Health check"}\n{"timestamp":"2026-10-06T12:01:00+00:00","level":"WARNING","source":"db","message":"Slow query"}\n')
    file2.write_text('{"timestamp":"2026-10-06T12:02:00+00:00","level":"ERROR","source":"db","message":"Connection timeout"}\n{"timestamp":"2026-10-06T12:03:00+00:00","level":"CRITICAL","source":"auth","message":"Token service unavailable"}\n{"timestamp":"2026-10-06T12:04:00+00:00","level":"INFO","source":"web","message":"GET /users 200"}\n')
    process_jsonl(file1, is_skip_invalid=False)
    process_jsonl(file2, is_skip_invalid=False)

    assert analysis.stats_counter["valid_events"] == 6
    assert analysis.stats_counter["invalid_events"] == 0

def test_empty_file_csv(tmp_path):
    file = tmp_path / "file.csv"
    file.write_text('')
    process_csv(file, is_skip_invalid=False)

    assert analysis.total_stats == {}

def test_empty_file_jsonl(tmp_path):
    file = tmp_path / "file.jsonl"
    file.write_text('')
    process_csv(file, is_skip_invalid=False)

    assert analysis.total_stats == {}

