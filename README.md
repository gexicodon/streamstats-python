# streamstats

Потоковый анализатор событий из CSV и JSONL. Читает файлы построчно (память не растёт
с размером файла), проверяет каждое событие и собирает статистический отчёт в JSON или CSV.

## Возможности

- чтение CSV (с заголовком) и JSONL построчно;
- проверка обязательных полей: `timestamp` (ISO 8601), `level`, `source`, `message`;
- статистика: число событий, события по уровням и по источникам, top-5 источников
  по ошибкам (`ERROR`/`CRITICAL`), первая и последняя временная метка;
- объединение статистики по нескольким файлам;
- два режима для некорректных строк: остановка с кодом `2` или пропуск с `WARNING`;
- JSON-отчёт в UTF-8.
- 
## Требования и установка
- Python 3.11 или новее.
- ruff 0.16.10 или новее.
- pytest-9.1.1 или новее.
```bash
git clone https://github.com/gexicodon/streamstats-python.git
python -m venv .venv
.venv\Scripts\activate
cd streamstats-python/src
```
## Быстрый старт
```bash
python -m streamstats analyze data/events_valid.csv --format csv --output report.json
```
## Тесты
В директории ```streamstats-python```

```bash
ruff check .
pytest -v
```
## Использование

```text
python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl [--output REPORT.[json|csv]] [--skip-invalid]
```

| Аргумент | Описание |
|---|---|
| `analyze` | действие (сейчас единственное) |
| `INPUT ...` | один или несколько входных файлов; статистика объединяется |
| `--format` | `csv` или `jsonl`; расширение файла должно совпадать с форматом |
| `--output REPORT.json(.csv)` | файл для JSON(CSV)-отчёта; без этого параметра отчёт печатается в консоль |
| `--skip-invalid` | пропускать некорректные строки, записывая `WARNING` в консоль|

Примеры
```bash
# несколько файлов, отчёт в файл
python -m streamstats analyze logs/a.jsonl logs/b.jsonl --format jsonl --output report.json

# пропускать повреждённые строки
python -m streamstats analyze logs/a.jsonl --format jsonl --skip-invalid
```

### Коды возврата

| Код | Когда |
|---|---|
| `0` | успешно |
| `2` | ошибка: некорректная строка (в режиме по умолчанию), файл не найден, неподдерживаемый формат, расширение не совпадает с `--format`, неверные аргументы |

## Формат входных данных

Модель события:

| Поле | Требование |
|---|---|
| `timestamp` | дата и время в формате ISO 8601, например `2026-10-06T10:00:00+00:00` |
| `level` | один из `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (регистр важен) |
| `source` | непустая строка |
| `message` | строка |

Файлы читаются в кодировке UTF-8.

**CSV** (первая строка заголовок):

```csv
timestamp,level,source,message
2026-10-06T10:00:00+00:00,INFO,api,Service started
2026-10-06T10:00:05+00:00,ERROR,db,Connection timeout
```

**JSONL** (один JSON-объект в строке):

```json
{"timestamp":"2026-10-06T10:00:00+00:00","level":"INFO","source":"api","message":"Service started"}
{"timestamp":"2026-10-06T10:00:05+00:00","level":"ERROR","source":"db","message":"Connection timeout"}
```

## Отчёт

Пример (`events.csv` из четырёх событий):

```json
{
    "valid_events": 4,
    "invalid_events": 0,
    "valid_levels": {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 0,
        "ERROR": 2,
        "CRITICAL": 1
    },
    "valid_sources": {
        "api": 2,
        "db": 2
    },
    "errors_count_in_sources": {
        "api": 1,
        "db": 2
    },
    "top_sources_by_errors": {
        "db": 2,
        "api": 1
    },
    "first_and_last_ts": {
        "first_ts": "2026-10-06 10:00:00+00:00",
        "last_ts": "2026-10-06 10:02:00+00:00"
    }
}
```

| Поле | Смысл |
|---|---|
| `valid_events` | число корректных событий по всем файлам |
| `invalid_events` | число некорректных строк (в режиме `--skip-invalid` это число пропущенных) |
| `valid_levels` | число событий каждого уровня; все пять уровней присутствуют, даже с нулём |
| `valid_sources` | число событий каждого источника |
| `errors_count_in_sources` | число событий `ERROR` и `CRITICAL` по каждому источнику |
| `top_sources_by_errors` | top-5 источников с наибольшим числом ошибок, по убыванию |
| `first_and_last_ts` | самая ранняя и самая поздняя метка времени (`null`, если событий нет) |

# Структура проекта
```text
src/streamstats/
├── __main__.py   CLI: разбор аргументов, проверка файлов, вывод отчёта, коды возврата
├── parsers.py    потоковое чтение CSV и JSONL, обработка строки
├── validate.py   проверка полей события
├── analysis.py   счётчики и сборка итоговой статистики
├── report.py     запись JSON(CSV)-отчёта и вывод в консоль
├── config.py     обязательные поля и допустимые уровни
├── errors.py     исключения приложения
└── models.py     зарезервирован под модель события
```

