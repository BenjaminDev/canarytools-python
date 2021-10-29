import os
import pickle
from pathlib import Path
from typing import Union

import httpx
import pytest

from canarytools.api import base_url
from canarytools.console import (API, Console, ConsoleSettings, Devices,
                                 IncidentQueries)
from canarytools.models.base import (APIError, AuthToken, Incidents,
                                     MDeviceIPs, MDevices, MDeviceTxTIPs,
                                     QDeviceIPs, QDevices, QDevicesInfo, Query,
                                     api_auth_token_length)
from itertools import product


from .conftest import has_key



# def hash_request(**kwargs):
#     # TODO: if this sticks around make it nicer please >:<
#     unique_request_string = ""
#     for k, v in kwargs.items():
#         if k == "url":
#             v = v.split(".")[-1]
#         if k == "params":
#             unique_request_string += hash_request(**v)
#         unique_request_string += str(k)
#         unique_request_string += str(v)
#     return hashlib.md5(unique_request_string.encode()).hexdigest()


# def replay_execute(*, verb, url, params) -> Union[httpx.Response, APIError]:
#     hashed_request = hash_request(verb=verb, url=url.split(".")[-1], params=params)
#     with open(replay_data_path / hashed_request, mode="rb") as fp:
#         response = pickle.load(fp)
#     return response


# def collect_api_responses(execute):
#     @wraps(execute)
#     def wrapper(*args, **kwargs):
#         response = execute(*args, **kwargs)
#         replay_data_path.mkdir(
#             parents=True, exist_ok=True
#         )  # TODO: fix this or check it's not too much overhead
#         with open(replay_data_path / hash_request(**kwargs), "wb") as fp:
#             pickle.dump(response, fp, protocol=pickle.HIGHEST_PROTOCOL)
#         return response

#     return wrapper


# from enum import IntEnum


# class TruthSource(IntEnum):
#     # TODO: find a better name please.
#     LIVE = 0
#     REPLAY = 1
#     CAPTURE = 2


# @pytest.fixture
# def console() -> Console:
#     test_source = TruthSource(int(os.environ["TEST_SOURCE"]))
#     if test_source == TruthSource.REPLAY:
#         IncidentQueries.execute = replay_execute
#         ConsoleSettings.execute = replay_execute
#         API.execute = replay_execute
#     elif test_source == TruthSource.CAPTURE:
#         IncidentQueries.execute = collect_api_responses(IncidentQueries.execute)
#         ConsoleSettings.execute = collect_api_responses(ConsoleSettings.execute)
#         API.execute = collect_api_responses(API.execute)

#     return Console(
#         console_hash=os.environ["CONSOLE_HASH"],
#         api_key=os.environ["API_KEY"],
#     )


# @pytest.fixture
# def customized_console():
#     test_source = TruthSource(int(os.environ["TEST_SOURCE"]))
#     if test_source == TruthSource.REPLAY:
#         IncidentFetcher.execute = replay_execute
#         ConsoleSettings.execute = replay_execute
#         API.execute = replay_execute
#     elif test_source == TruthSource.CAPTURE:
#         IncidentFetcher.execute = collect_api_responses(IncidentFetcher.execute)
#         ConsoleSettings.execute = collect_api_responses(ConsoleSettings.execute)
#         API.execute = collect_api_responses(API.execute)
#     return Console.make_console(
#         console_hash=os.environ["CONSOLE_HASH"],
#         auth_token=AuthToken(auth_token=os.environ["API_KEY"]),
#     )
# cs = ConsoleSettings(auth_token=AuthToken(auth_token=os.environ["API_KEY"]),base_url=base_url.format(os.environ["CONSOLE_HASH"]))
# return Console(
#     console_hash=os.environ["CONSOLE_HASH"], api_key=os.environ["API_KEY"], custom_executors=[cs]
# )


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_settings(console: Console):
    settings = console.settings()
    assert settings.auth_token.auth_token.get_secret_value() == os.environ["API_KEY"]


# @pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
# def test_custom_console_settings(customized_console):
#     settings = customized_console.settings()
#     assert settings.auth_token.auth_token.get_secret_value() == os.environ["API_KEY"]


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_api_enable(console: Console):
    thinkst_result = console.api.enable()
    assert isinstance(thinkst_result.result, str)


# TODO: Think of a nicer way handle this
@pytest.mark.skipif(
    has_key() or True,
    reason="Don't have a valid api key. Skip test as we get locked out. hehehe",
)
def test_console_api_disbale(console: Console):
    thinkst_result = console.api.disable()
    assert isinstance(thinkst_result.result, str)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_api_auth_token_download(console: Console):
    auth_file = console.api.auth_token_download()
    assert isinstance(auth_file.auth_token_file_as_bytes, bytes)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_query_ackd_incidents(console: Console):
    query = Query()
    incidents_ackd: Incidents = console.incidents.acknowledged(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_query_unackd_incidents(console: Console):
    query = Query()
    incidents_unackd: Incidents = console.incidents.unacknowledged(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_query_all_incidents(console: Console):
    query = Query()
    incidents_all: Incidents = console.incidents.all(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_device_get_all(console: Console):
    query = QDevices()
    devices_all: MDevices = console.devices.all(query=query)
    assert isinstance(devices_all, MDevices)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_device_get_live(console: Console):
    query = QDevices()
    devices_all: MDevices = console.devices.live(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_device_get_dead(console: Console):
    query = QDevices()
    devices_all: MDevices = console.devices.dead(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_device_get_filter(console: Console):
    query = QDevices()
    devices_all: MDevices = console.devices.filter(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
def test_console_device_get_filter_broken_url(console: Console):
    console.devices.base_url = console.devices.base_url + "/broken"
    query = QDevices()
    devices_all: APIError = console.devices.filter(query=query)
    assert isinstance(devices_all, APIError)




@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
# TODO: use hypothesis for to improve input coverage.
@pytest.mark.parametrize(
    "settings,exclude_fixed_settings", [o for o in product([True, False], repeat=2)]
)
def test_console_device_get_info(console, settings, exclude_fixed_settings):
    devices_all: MDevices = console.devices.all(query=QDevices())
    query = QDevicesInfo(
        node_id=devices_all.devices[0]["id"],
        settings=settings,
        exclude_fixed_settings=exclude_fixed_settings,
    )
    devices_all: MDevices = console.devices.info(query=query)


@pytest.mark.skipif(has_key(), reason="Don't have a valid api key.")
@pytest.mark.parametrize(
    "download,include_annotations", [o for o in product([True, False], repeat=2)]
)
def test_console_device_get_ips(download, include_annotations, console: Console):
    query = QDeviceIPs(download=download, include_annotations=include_annotations)
    if query.download:
        device_ips: MDeviceTxTIPs = console.devices.ips(query=query)
    else:
        devices_ips: MDeviceIPs = console.devices.ips(query=query)
