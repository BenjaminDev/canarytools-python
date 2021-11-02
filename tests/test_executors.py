import pytest

from canarytools.executors import API, Executor, FlockQueries
from canarytools.models.base import AuthToken


def test_api_type():
    api = API(auth_token=AuthToken(auth_token="e" * 32), base_url="")
    assert isinstance(api, API)
    assert isinstance(api, Executor)


def test_flock_queries_type():
    api = FlockQueries(auth_token=AuthToken(auth_token="e" * 32), base_url="")
    assert isinstance(api, FlockQueries)
    assert isinstance(api, Executor)
