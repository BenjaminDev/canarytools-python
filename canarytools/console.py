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
from canarytools.executors import (API, FlockQueries, IncidentActions, ConsoleSettings, Devices,
                                   IncidentQueries)
from canarytools.models.base import (APIError, AuthToken, Incidents, MDevice,
                                     MDeviceIPs, MDevices, QDeviceIPs,
                                     QDevices, Query)
from canarytools.models.settings import AuthFile, Settings, ThinkstResult

# class Api(Protocol):
#     def execute(self, url: str, params: Dict):
#         ...



# Style: Optional[Union[str,AuthToken]] is Union[str, AuthToken,None] which is best??



# @runtime_checkable
# class Executor(Protocol):
#     auth_token:AuthToken
#     base_url:str
#     api_version:str
#     api_endpoints:Dict[Tuple[str,str], str]
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         ...
#     def execute(
#         self, *, verb: str, url: str, params: Dict[str, str]
#     ) -> Union[httpx.Response, APIError]:
#         ...
# @runtime_checkable
# class RequestBuilder(Protocol):
#     def build_request(
#         self:Executor, *, verb: str, url: str, params: Dict[str, str]
#     ) -> Union[httpx.Response, APIError]:
#         ...


# @runtime_checkable
# class Execute(Protocol):
#     def __call__(
#         self, *, verb: str, url: str, params: Dict[str, str]
#     ) -> Union[httpx.Response, APIError]:
#         ...



# def wrapper(method):
#     @wraps(method)
#     def _impl(self, *method_args, **method_kwargs):
#         method_output = method(self, *method_args, **method_kwargs)
#         return method_output + "!"
#     return _imp

# def transformer(verb, endpoint_name, ):
#     def wrapper(f):
#         def _impl(self,*, query=None):
#             url = make_url(base_url=self.base_url,verb=verb,endpoint_name=endpoint_name)
#             params = self.auth_token.secret_dict()
#             if query is not None:
#                 params.update(**query.dict(exclude_none=True))
#             return f(self, verb=verb, url=url, params=params)
#             _impl.__annotations__ = {"test":"ss"}
#         return _impl
#     return wrapper

# def execute(
#     self: Executor, #TODO: this
#     *,
#     verb: str,
#     url: str,
#     params: Dict[str, str],
# ) -> Union[httpx.Response, APIError]:
#     with httpx.Client() as client:
#         result = getattr(client, verb)(url=url, params=params)
#     try:
#         result.raise_for_status()
#     except HTTPError as e:
#         return APIError(
#             status_code=result.status_code, message=result.json(), endpoint=url
#         )
#     return result

# def execute(
#     # self: Executor, #TODO: this
#     *,
#     verb: str,
#     url: str,
#     params: Dict[str, str],
# ) -> Union[httpx.Response, APIError]:
#     with httpx.Client() as client:
#         result = getattr(client, verb)(url=url, params=params)
#     try:
#         result.raise_for_status()
#     except HTTPError as e:
#         return APIError(
#             status_code=result.status_code, message=result.json(), endpoint=url
#         )
#     return result

# def build_request(executor:Executor, *, verb, endpoint_name)-> Tuple[str, str, Dict]:
#     url = f"{executor.base_url}/api/{executor.api_version}/{executor.api_endpoints[(verb, endpoint_name)]}"
#     params = executor.auth_token.secret_dict()
#     return {"verb": verb, "url":url, "params":params}


# def imbue_with(

#     func: Callable,
# ) -> Executor:
#     def inner(cls: Any):
#         setattr(cls, func.__name__, func)
#         return cls
#     return inner
# def add_arg(f):
#     @wraps
#     def inner(*args, **kwargs):
#         args = f.__code__.co_varnames + ("self")
#         return f(**args, **kwargs)
#     return inner


# class ConsoleSettings(Executor):
#     execute:Execute = execute
#     build_request = build_request
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         self.auth_token = auth_token
#         self.base_url = base_url
#         self.api_version = api_version
#         self.api_endpoints = api_endpoints

#     def __call__(self) -> Settings:
#         verb, endpoint_name = "get", "settings"
#         result = ConsoleSettings.execute(**self.build_request(verb=verb, endpoint_name=endpoint_name))
#         return Settings(**result.json())


# class API:
#     execute:Execute = execute
#     build_request:RequestBuilder = build_request
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         self.auth_token = auth_token
#         self.base_url = base_url
#         self.api_version = api_version
#         self.api_endpoints = api_endpoints

#     def enable(self)->ThinkstResult:
#         verb, endpoint_name = "post", "settings_api_enable"
#         result = API.execute(**self.build_request(verb=verb, endpoint_name=endpoint_name))
#         return ThinkstResult(**result.json())

#     def disable(self)->ThinkstResult:
#         verb, endpoint_name = "post", "settings_api_disable"
#         result = API.execute(**self.build_request(verb=verb, endpoint_name=endpoint_name))
#         return ThinkstResult(**result.json())


#     def auth_token_download(self)->AuthFile:
#         verb, endpoint_name = "get", "settings_api_auth_token_download"
#         result = API.execute(**self.build_request(verb=verb, endpoint_name=endpoint_name))
#         if isinstance(result, APIError): return result # TODO: add middleware to handle errors.
#         return AuthFile(auth_token_file_as_bytes=result.content)

# class Actions:
#     execute:Execute = execute
#     build_request:RequestBuilder = build_request
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         self.auth_token = auth_token
#         self.base_url = base_url
#         self.api_version = api_version
#         self.api_endpoints = api_endpoints

#     def fetch(self):
#         verb, endpoint_name = "get", "incident_fetch"
#         result = API.execute(**self.build_request(verb=verb, endpoint_name=endpoint_name))
#         return Incidents(**result.json())


# class IncidentFetcher:
#     execute:Execute = execute
#     build_request:RequestBuilder = build_request
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         self.auth_token = auth_token
#         self.base_url = base_url
#         self.api_version = api_version
#         self.api_endpoints = api_endpoints

#     def acknowledged(self, query: Query):
#         verb, endpoint_name = "get", "incident_acknowledged"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = IncidentFetcher.execute(**request)
#         return Incidents(**result.json())

#     def unacknowledged(self, query: Query):
#         verb, endpoint_name = "get", "incident_unacknowledged"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         # TODO: API. Looks like a doc issue or  console issue.
#         request["params"].pop("incidents_since")
#         result = IncidentFetcher.execute(**request)
#         return Incidents(**result.json())

#     def all(self, *, query: Query):
#         verb, endpoint_name = "get", "incident_all"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = IncidentFetcher.execute(**request)
#         return Incidents(**result.json())

# class Devices:
#     execute:Execute = execute
#     build_request:RequestBuilder = build_request
#     def __init__(self, *, auth_token: AuthToken, base_url: str, api_version:str="v1", api_endpoints:Dict=api_endpoints):
#         self.auth_token = auth_token
#         self.base_url = base_url
#         self.api_version = api_version
#         self.api_endpoints = api_endpoints

#     def all(self, query: QDevices):
#         verb, endpoint_name = "get", "devices_all"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         return MDevices(**result.json())

#     def live(self, query: QDevices) -> MDevices:
#         verb, endpoint_name = "get", "devices_live"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         if isinstance(result, APIError): return result.json()
#         return MDevices(**result.json())

#     def dead(self, query: QDevices) -> MDevices:
#         verb, endpoint_name = "get", "devices_dead"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         if isinstance(result, APIError): return result.json()
#         return MDevices(**result.json())

#     def filter(self, query: QDevices):
#         verb, endpoint_name = "get", "devices_filter"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         if isinstance(result, APIError): return result.json()
#         return MDevices(**result.json())


#     def info(self, query: QDevices) -> MDevice:
#         verb, endpoint_name = "get", "device_info"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         if isinstance(result, APIError): return result.json()
#         result_data: Dict[str,Any] = cast(Dict[str,Any],result.json())
#         return MDevice(**result_data)

#     def ips(self, query: QDeviceIPs) -> MDevice:
#         verb, endpoint_name = "get", "device_ips"
#         request = self.build_request(verb=verb, endpoint_name=endpoint_name)
#         request["params"].update(**query.dict(exclude_none=True))
#         result = Devices.execute(**request)
#         if isinstance(result, APIError): return result.json()
#         if query.download:
#             return result.text
#         result_data: Dict[str,Any] = cast(Dict[str,Any],result.json())
#         return MDeviceIPs(**result_data)


panel_registry = {
    "settings": ConsoleSettings,
    "api": API,
    "devices": Devices,
    "incidents": IncidentQueries,
}


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
        self.devices: Devices = Devices(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        self.flocks: FlockQueries = FlockQueries(
            auth_token=auth_token, base_url=base_url.format(console_hash)
        )
        # reveal_type(self.incidents.acknowledged)

    #     self.api:API = custom_executors.pop("api")
    #     self.settings:ConsoleSettings = custom_executors.pop("settings")
    #     self.devices:Devices = custom_executors.pop("devices")
    #     self.incidents:IncidentFetcher = custom_executors.pop("incidents")
    #     for panel_name, executor in custom_executors.items():
    #         if isinstance(executor, Executor):
    #             setattr(self, panel_name, executor)
    #             # breakpoint()
    #         else:
    #             # Note: this could be a "compile" time check with metaclasses
    #             # but Design: I don't want to force subclassing
    #             raise AssertionError("Custom executors must define 'execute'")
    #     # self.api.__annotations__ = API.__annotations__

    # @staticmethod
    # def make_console(
    #     console_hash: Optional[str] = None,
    #     auth_token: Optional[Union[str, AuthToken]] = None,
    #     panel_registry: Dict[str, Type[Executor]] = panel_registry,
    # ):
    #     console_hash = console_hash
    #     # auth_token = AuthToken(auth_token=auth_token)
    #     base_url = bbs.format(console_hash)
    #     executors: Dict[str, Executor] = {}
    #     for panel_name, cls in panel_registry.items():
    #         executors[panel_name] = cls(auth_token=auth_token, base_url=base_url)

    #     return Console(
    #         console_hash=console_hash, api_key=auth_token, custom_executors=executors
    #     )
