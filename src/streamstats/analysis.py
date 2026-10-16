from collections import Counter
from datetime import datetime

from streamstats.validate import levels

stats_counter = Counter({"valid_events": 0, "valid_levels":{}, "valid_sources":{}, "errors_count_in_sources":{}})
stats_top_errors_in_sources = []
first_ts = None
last_ts = None

for level in levels:
    stats_counter["valid_levels"][level] = 0


def count_valid_events():
    stats_counter['valid_events'] += 1

def count_valid_levels(level):
    stats_counter["valid_levels"][level] += 1

def count_valid_sources(source):
    if source not in stats_counter["valid_sources"]:
        stats_counter["valid_sources"][source] = 0

    stats_counter["valid_sources"][source] += 1


def count_errors_in_sources(row):
    source = row["source"]

    if source not in stats_counter["errors_count_in_sources"]:
        stats_counter["errors_count_in_sources"][source] = 0

    if row["level"] in ("ERROR", "CRITICAL"):
        stats_counter["errors_count_in_sources"][source] += 1

def top_sources_by_errors():
    errors_count_in_sources = stats_counter["errors_count_in_sources"]
    top_sources = {"top_sources_by_errors":dict(sorted(errors_count_in_sources.items(), key=lambda item: item[1], reverse=True)[:5])}
    return top_sources

def find_first_last_timestamp(row):
    global first_ts, last_ts

    current_ts = datetime.fromisoformat(row["timestamp"])
    if first_ts is None or (current_ts < first_ts):
        first_ts = current_ts
    if last_ts is None or (current_ts > last_ts):
        last_ts = current_ts
    return {"first_and_last_ts": {"first_ts": str(first_ts), "last_ts":str(last_ts)}}

def analysis(row):
    count_valid_events()
    count_valid_levels(row["level"])
    count_valid_sources(row["source"])
    count_errors_in_sources(row)
    top = top_sources_by_errors()
    first_last = find_first_last_timestamp(row)
    total = {**stats_counter, **top, **first_last}
    return total
