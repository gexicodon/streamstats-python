from collections import Counter

from streamstats.validate import levels

stats_counter = Counter({"valid_events": 0, "valid_levels":{}, "valid_sources":{}, "errors_in_sources":{},})

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

    if source not in stats_counter["errors_in_sources"]:
        stats_counter["errors_in_sources"][source] = 0

    if row["level"] in ("ERROR", "CRITICAL"):
        stats_counter["errors_in_sources"][source] += 1


def analysis(row):
    count_valid_events()
    count_valid_levels(row["level"])
    count_valid_sources(row["source"])
    count_errors_in_sources(row)