import os

import pytest

from canarytools.console import Console
from canarytools.models.base import (
    MFlockNote,
    MFlockSensors,
    MFlockSettings,
    MFlocksList,
    MFlocksMetaData,
    MFlocksSummary,
    MFlockSummary,
    MFlockUsers,
    QFlocks,
    QFlocksFilter,
    QFlocksFor,
    QFlocksNote,
    ThinkstResult,
)

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
def test_flock_queries_list_all(console: Console):
    flocks_list = console.flocks.list_all(query=QFlocks())
    assert isinstance(flocks_list, MFlockSensors)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_settings(console: Console):
    flocks_list = console.flocks.settings(query=QFlocks())
    assert isinstance(flocks_list, MFlockSettings)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_queries_users(console: Console):
    flocks_users = console.flocks.users(query=QFlocks())
    assert isinstance(flocks_users, MFlockUsers)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_filter(console: Console):
    flocks_metadata = console.flocks.filter(query=QFlocksFilter(filter_str="*"))
    assert isinstance(flocks_metadata, MFlocksMetaData)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_list_for_user(console: Console):
    flocks_metadata = console.flocks.list_for(
        query=QFlocksFor(email="benjamin@thinkst.com")
    )
    assert isinstance(flocks_metadata, MFlocksList)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_add_note(console: Console):
    resp = console.flocks.add_note(query=QFlocksNote(note="Some note dda**4jd"))
    assert isinstance(resp, ThinkstResult)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_get_note(console: Console):
    resp = console.flocks.get_note(query=QFlocks())
    assert isinstance(resp, MFlockNote)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_flock_delete_note(console: Console):
    resp = console.flocks.delete_note(query=QFlocks())
    assert isinstance(resp, ThinkstResult)
