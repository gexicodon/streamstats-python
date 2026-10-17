import pytest
import streamstats.analysis as analysis
from streamstats.config import levels

@pytest.fixture(autouse=True)
def clean_stats():
    """очистка статистики перед каждым тестом"""
    analysis.stats_counter = analysis.Counter({
        "valid_events": 0,
        "invalid_events": 0,
        "valid_levels": {},
        "valid_sources": {},
        "errors_count_in_sources": {}
    })
    for level in levels:
        analysis.stats_counter["valid_levels"][level] = 0
    analysis.total_stats.clear()
    analysis.first_ts = None
    analysis.last_ts = None