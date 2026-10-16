import json

def stats_to_json(stats, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)