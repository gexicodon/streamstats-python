from collections import Counter
from datetime import datetime

from streamstats.validate import levels

stats_counter = Counter({"valid_events": 0, "invalid_events":0 ,"valid_levels":{}, "valid_sources":{}, "errors_count_in_sources":{}})
stats_top_errors_in_sources = []
first_ts = None
last_ts = None

total_stats = {}

for level in levels:
    stats_counter["valid_levels"][level] = 0


def count_valid_events():
    """Счётчик корректных событий"""
    stats_counter['valid_events'] += 1


def count_invalid_events():
    """Счетчик некорректных событий"""
    stats_counter['invalid_events'] += 1
    top = top_sources_by_errors()

    first_last = {
        "first_and_last_ts": {
            "first_ts": str(first_ts) if first_ts is not None else None,
            "last_ts": str(last_ts) if last_ts is not None else None
        }
    }
    total_stats.clear()
    total_stats.update({**stats_counter, **top, **first_last})
    return total_stats


def count_valid_levels(level):
    """Счётчик корректных уровней"""
    stats_counter["valid_levels"][level] += 1

def count_valid_sources(source):
    """Счётчик корректных источников"""
    if source not in stats_counter["valid_sources"]:
        stats_counter["valid_sources"][source] = 0

    stats_counter["valid_sources"][source] += 1


def count_errors_in_sources(row):
    """Счётчик ошибок в источниках"""
    source = row["source"]

    if source not in stats_counter["errors_count_in_sources"]:
        stats_counter["errors_count_in_sources"][source] = 0

    if row["level"] in ("ERROR", "CRITICAL"):
        stats_counter["errors_count_in_sources"][source] += 1

def top_sources_by_errors():
    """Выборка топ-5 источников по колву ошибок"""
    errors_count_in_sources = stats_counter["errors_count_in_sources"]
    top_sources = {"top_sources_by_errors":dict(sorted(errors_count_in_sources.items(), key=lambda item: item[1], reverse=True)[:5])}
    return top_sources

def find_first_last_timestamp(row):
    """Поиск первого и последнего timestamp"""
    global first_ts, last_ts

    current_ts = datetime.fromisoformat(row["timestamp"])
    if first_ts is None or (current_ts < first_ts):
        first_ts = current_ts
    if last_ts is None or (current_ts > last_ts):
        last_ts = current_ts
    return {"first_and_last_ts": {"first_ts": str(first_ts), "last_ts":str(last_ts)}}

def get_default_stats():
    """Получение дефолтной статистики"""
    top = top_sources_by_errors()
    first_last = {
        "first_and_last_ts": {
            "first_ts": str(first_ts) if first_ts is not None else None,
            "last_ts": str(last_ts) if last_ts is not None else None
        }
    }
    return {**dict(stats_counter), **top, **first_last}


def update_stats(row):
    """Обновление статистики"""
    count_valid_events()
    count_valid_levels(row["level"])
    count_valid_sources(row["source"])
    count_errors_in_sources(row)
    top = top_sources_by_errors()
    first_last = find_first_last_timestamp(row)
    total_stats.clear()
    total_stats.update({**stats_counter, **top, **first_last})
    return total_stats
