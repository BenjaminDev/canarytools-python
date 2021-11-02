from __future__ import annotations

from abc import abstractmethod
from functools import wraps
from typing import (Any, Callable, Dict, Iterable, List, Mapping, Optional,
                    Protocol, Tuple, Type, Union, cast, runtime_checkable)

import httpx
from httpx._exceptions import HTTPError
from pydantic import SecretStr

from canarytools.api import api_endpoints, api_version
from canarytools.api import base_url
from canarytools.api import base_url as bbs
from canarytools.executors import (API, ConsoleSettings, Devices, FlockQueries,
                                   IncidentActions, IncidentQueries)
from canarytools.models.base import (APIError, AuthFile, AuthToken, Incidents,
                                     MDevice, MDeviceIPs, MDevices, QDeviceIPs,
                                     QDevices, Query, Settings, ThinkstResult)


class Console:
    """
    Console object user interface:
    c = Console(...)
    c.settings() -> returns console settings
    c.api.{enable, disable, download} ->
    c.incidents.{acknowledged, unacknowledged, ...} ->
    c.incidents.
    """

    def __init__(
        self,
        *,
        console_hash: str,
        api_key: str,
    ):
        auth_token: AuthToken = AuthToken(auth_token=SecretStr(api_key))
        self.api: API = API(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.settings: ConsoleSettings = ConsoleSettings(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.incidents: IncidentQueries = IncidentQueries(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.incidents_act: IncidentActions = IncidentActions(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.devices: Devices = Devices(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.flocks: FlockQueries = FlockQueries(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )

