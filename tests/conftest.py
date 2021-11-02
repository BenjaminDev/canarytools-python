import hashlib
import os
import pickle
from functools import wraps
from itertools import product
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

replay_data_path = Path("tests/data")
has_key = lambda: not len(os.environ["API_KEY"]) == api_auth_token_length


def hash_request(**kwargs):
    # TODO: if this sticks around make it nicer please >:<
    unique_request_string = ""
    for k, v in kwargs.items():
        if k == "url":
            v = v.split(".")[-1]
        if k == "params":
            unique_request_string += hash_request(**v)
        unique_request_string += str(k)
        unique_request_string += str(v)
    return hashlib.md5(unique_request_string.encode()).hexdigest()


def replay_execute(*, verb, url, params) -> Union[httpx.Response, APIError]:
    hashed_request = hash_request(verb=verb, url=url.split(".")[-1], params=params)
    with open(replay_data_path / hashed_request, mode="rb") as fp:
        response = pickle.load(fp)
    return response


def collect_api_responses(execute):
    @wraps(execute)
    def wrapper(*args, **kwargs):
        response = execute(*args, **kwargs)
        replay_data_path.mkdir(
            parents=True, exist_ok=True
        )  # TODO: fix this or check it's not too much overhead
        with open(replay_data_path / hash_request(**kwargs), "wb") as fp:
            pickle.dump(response, fp, protocol=pickle.HIGHEST_PROTOCOL)
        return response

    return wrapper


import os
import pickle
from enum import IntEnum
from itertools import product
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


class TruthSource(IntEnum):
    # TODO: find a better name please.
    LIVE = 0
    REPLAY = 1
    CAPTURE = 2


@pytest.fixture
def console() -> Console:
    test_source = TruthSource(int(os.environ["TEST_SOURCE"]))
    if test_source == TruthSource.REPLAY:
        IncidentQueries.execute = replay_execute
        ConsoleSettings.execute = replay_execute
        API.execute = replay_execute
    elif test_source == TruthSource.CAPTURE:
        IncidentQueries.execute = collect_api_responses(IncidentQueries.execute)
        ConsoleSettings.execute = collect_api_responses(ConsoleSettings.execute)
        API.execute = collect_api_responses(API.execute)

    return Console(
        console_hash=os.environ["CONSOLE_HASH"],
        api_key=os.environ["API_KEY"],
    )
