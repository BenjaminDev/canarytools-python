import os

import pytest

from canarytools.console import Console
from canarytools.models.base import (MFlockSensors, MFlockSettings,
                                     MFlocksSummary, MFlockSummary, QFlocks)

from .conftest import has_key


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_summaries(console: Console):
    flocks_summary = console.flocks.summaries()
    assert isinstance(flocks_summary, MFlocksSummary)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_summary(console: Console):
    flocks_summary = console.flocks.summary(query=QFlocks())
    assert isinstance(flocks_summary, MFlockSummary)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_listicle(console: Console):
    flocks_list = console.flocks.listicle(query=QFlocks())
    assert isinstance(flocks_list, MFlockSensors)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_listicle(console: Console):
    flocks_list = console.flocks.settings(query=QFlocks())
    assert isinstance(flocks_list, MFlockSettings)
