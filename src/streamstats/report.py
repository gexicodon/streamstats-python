import csv
import json
from pprint import pprint

from streamstats.analysis import get_default_stats


def stats_to_json(stats, filename):
    """Сохраняет статистику в JSON
    Args:
        stats: словарь со статистикой
        filename: имя файла, куда сохранять
    Returns:
        None
    """
    if not stats:
        stats = get_default_stats()

    with open(filename, 'w', encoding='utf8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

def print_stats(stats):
    """Выводит статистику в консоль
    Args:
        stats: словарь со статистикой
    Returns:
        None
    """
    if not stats:
        stats = get_default_stats()
    pprint("--- Итоговая статистика ---")
    pprint(stats, indent=6,width=120, sort_dicts=False)


def stats_to_csv(stats, filename):
    """Сохраняет статистику в CSV
    Args:
        stats: словарь со статистикой
        filename: имя файла, куда сохранять
    Returns:
        None
    """
    if not stats:
        stats = get_default_stats()

    with open(filename, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "key", "value"])
        for metric, value in stats.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    w.writerow([metric, k, v])
            else:
                w.writerow([metric, "", value])
