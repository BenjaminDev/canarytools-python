from functools import singledispatchmethod, wraps
from typing import (Any, Callable, Collection, Dict, Generic, Mapping, Optional,
                    Protocol, Tuple, Type, TypeVar, Union, cast, final,
                    get_origin, runtime_checkable)

import httpx
import pydantic
from httpx import HTTPError
from mypy_extensions import KwArg, VarArg
from pydantic.main import BaseModel

from canarytools._protocols import Execute, Executor, RequestBuilder
from canarytools.api import api_endpoints, api_version
from canarytools.models.base import (APIError, AuthToken, Incidents, MDevice,
                                     MDeviceIPs, MDevices, MDeviceTxTIPs,
                                     QDeviceIPs, QDevices, Query, QFlocks)
from canarytools.models.settings import AuthFile, Settings, ThinkstResult

T = TypeVar("T", bound=pydantic.BaseModel)
import warnings
from textwrap import dedent

# R = TypeVar('R', bound=httpx.Response)
from httpx import Response
from pydantic import ValidationError

# def check_response(
#     t: Type[T],
# ) -> Callable[[Callable[..., Union[T, APIError]]], Callable[..., Union[T, APIError]]]:
#     @wraps
#     def inner(
#         f: Callable[..., Union[T, APIError]]
#     ) -> Callable[..., Union[T, APIError]]:
#         def wrapper(*args: Any, **kwargs: Any) -> Union[T, APIError]:
#             response = f(*args, **kwargs)
#             # breakpoint()
#             if isinstance(response, APIError):
#                 return response
#             # reveal_type(t)
#             # reveal_type(a)
#             # if isinstance(response, Response):
#             #     response_data = t(**response.json())
#             #     assert isinstance(response_data,t)

#             return t(**response.json())
#             # return t(**cast(Mapping[str,Any], response.json()))
#             # return f.__annotations__['return'].__args__[0](**response.json())

#         return cast(Callable[..., Union[T, APIError]], wrapper)

#     return inner


warnings.warn("deprecated", DeprecationWarning)


def check_response(
    response: Union[Response, APIError], t: Type[T]
) -> Union[T, APIError]:
    if isinstance(response, APIError):
        return response
    try:
        t(**response.json())
    except ValidationError as e:
        warnings.warn(
            dedent(
                f"""Validation error ocurred. The client got unexpected data.
                                 This is most likely a bug in canarytools-python so please
                                 open a github issue and paste this:
                                 {e}
                              """
            ),
            UserWarning,
            stacklevel=2,
        )
        raise
        # return BaseModel(**response.json())  # type: ignore
    else:
        return t(**response.json())


# a = check_response(Incidents)
# reveal_type(a)
# b = a("s")
# reveal_type(b)
# c = b("sss")
# reveal_type(c)


def execute(
    # self: Executor, #TODO: this
    *,
    verb: str,
    url: str,
    params: Dict[str, str],
) -> Union[httpx.Response, APIError]:
    with httpx.Client() as client:
        result = getattr(client, verb)(url=url, params=params)
    try:
        result.raise_for_status()
    except HTTPError as e:
        return APIError(
            status_code=result.status_code, message=result.content, endpoint=url
        )
    return result


def build_request(
    executor: Executor, *, verb: str, endpoint_name: str
) -> Dict[str, Any]:
    url = f"{executor.base_url}/api/{executor.api_version}/{executor.api_endpoints[(verb, endpoint_name)]}"
    params = executor.auth_token.secret_dict()
    return {"verb": verb, "url": url, "params": params}


class ConsoleSettings:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def __call__(self) -> Union[Settings, APIError]:
        verb, endpoint_name = "get", "settings"
        return check_response(
            ConsoleSettings.execute(
                **self.build_request(verb=verb, endpoint_name=endpoint_name)
            ),
            Settings,
        )


class API:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def enable(self) -> Union[ThinkstResult, APIError]:
        verb, endpoint_name = "post", "settings_api_enable"
        response = API.execute(
            **self.build_request(verb=verb, endpoint_name=endpoint_name)
        )
        return check_response(response, ThinkstResult)

    def disable(self) -> Union[ThinkstResult, APIError]:
        verb, endpoint_name = "post", "settings_api_disable"
        response = API.execute(
            **self.build_request(verb=verb, endpoint_name=endpoint_name)
        )
        return check_response(response, ThinkstResult)

    def auth_token_download(self) -> Union[AuthFile, APIError]:
        verb, endpoint_name = "get", "settings_api_auth_token_download"
        result = API.execute(
            **self.build_request(verb=verb, endpoint_name=endpoint_name)
        )
        # Design: API. We return a text response in certain cases and so we all dance now.
        if isinstance(result, APIError):
            return result
        return AuthFile(auth_token_file_as_bytes=result.content)


class IncidentActions:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def fetch(self) -> Union[Incidents, APIError]:
        verb, endpoint_name = "get", "incident_fetch"
        response = IncidentActions.execute(
            **self.build_request(verb=verb, endpoint_name=endpoint_name)
        )
        return check_response(IncidentActions.execute(**response), Incidents)

    # def incident_acknowledge() -> Union[]


class IncidentQueries:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def acknowledged(self, query: Query) -> Union[Incidents, APIError]:
        verb, endpoint_name = "get", "incident_acknowledged"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(IncidentQueries.execute(**request), Incidents)

    def unacknowledged(self, query: Query) -> Union[Incidents, APIError]:
        verb, endpoint_name = "get", "incident_unacknowledged"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        # TODO: API. Looks like a doc issue or  console issue.
        request["params"].pop("incidents_since")
        return check_response(IncidentQueries.execute(**request), Incidents)

    def all(self, *, query: Query) -> Union[Incidents, APIError]:
        verb, endpoint_name = "get", "incident_all"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(IncidentQueries.execute(**request), Incidents)


class Devices:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def all(self, query: QDevices = QDevices()) -> Union[MDevices, APIError]:
        verb, endpoint_name = "get", "devices_all"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(Devices.execute(**request), MDevices)

    def live(self, query: QDevices) -> Union[MDevices, APIError]:
        verb, endpoint_name = "get", "devices_live"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(Devices.execute(**request), MDevices)

    def dead(self, query: QDevices) -> Union[MDevices, APIError]:
        verb, endpoint_name = "get", "devices_dead"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(Devices.execute(**request), MDevices)

    def filter(self, query: QDevices) -> Union[MDevices, APIError]:
        verb, endpoint_name = "get", "devices_filter"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(Devices.execute(**request), MDevices)

    def info(self, query: QDevices) -> Union[MDevice, APIError]:
        verb, endpoint_name = "get", "device_info"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        return check_response(Devices.execute(**request), MDevice)

    def ips(self, query: QDeviceIPs) -> Union[MDeviceIPs, MDeviceTxTIPs, APIError]:
        verb, endpoint_name = "get", "device_ips"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        response = Devices.execute(**request)
        # Design: API. We return a text response in certain cases and so we all dance now.
        if isinstance(response, APIError):
            return response
        if query.download:
            return MDeviceTxTIPs(ips=response.text)
        return check_response(response, MDeviceIPs)

from canarytools.models.base import MFlocksSummary
class FlockQueries:
    execute: Execute = execute
    build_request: RequestBuilder = build_request

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str = "v1",
        api_endpoints: Dict[Tuple[str, str], str] = api_endpoints,
    ):
        self.auth_token = auth_token
        self.base_url = base_url
        self.api_version = api_version
        self.api_endpoints = api_endpoints

    def summaries(self)->MFlocksSummary:
        verb, endpoint_name = "get", "flocks_summary"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        return check_response(FlockQueries.execute(**request), MFlocksSummary)


    def summary(self, query: QFlocks)->MFlocksSummary:
        verb, endpoint_name = "get", "flocks_summary"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        return check_response(FlockQueries.execute(**request), MFlocksSummary)
# api_endpoints[("get", "flock_list")] = "/flock/list"
# api_endpoints[("get", "flock_settings")] = "/flock/settings"
# api_endpoints[("get", "flock_summary")] = "/flock/summary"

# api_endpoints[("get", "flock_users")] = "/flock/users"
# api_endpoints[("get", "flock_filter")] = "/flock/filter"
# api_endpoints[("get", "flocks_list")] = "/flocks/list"