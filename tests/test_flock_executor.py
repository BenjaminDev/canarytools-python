import pytest

from canarytools.models.base import MFlocksSummary, QFlocks
from .conftest import has_key

from canarytools.console import Console
import os

@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_summaries(console: Console):
    flocks_summary = console.flocks.summaries()
    assert isinstance(flocks_summary, MFlocksSummary)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_summary(console: Console):
    flocks_summary = console.flocks.summary(query=QFlocks())
    assert isinstance(flocks_summary, MFlocksSummary)