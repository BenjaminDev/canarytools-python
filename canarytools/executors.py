import warnings
from typing import Any, Dict, Tuple, Type, TypeVar, Union

import httpx
import pydantic
from httpx import HTTPError

from canarytools._protocols import Execute, Executor, RequestBuilder
from canarytools.api import api_endpoints
from canarytools.models.base import (
    APIError,
    AuthFile,
    AuthToken,
    Incidents,
    MDevice,
    MDeviceIPs,
    MDevices,
    MDeviceTxTIPs,
    MFlockNote,
    MFlockSensors,
    MFlockSettings,
    MFlocksList,
    MFlocksMetaData,
    MFlockSummary,
    MFlockUsers,
    QDeviceIPs,
    QDevices,
    QFlocks,
    QFlocksFilter,
    QFlocksFor,
    QFlocksNote,
    QIncidentAction,
    Query,
    Settings,
    SingleIncident,
    ThinkstResult,
)

T = TypeVar("T", bound=pydantic.BaseModel)
import warnings
from textwrap import dedent

from httpx import Response
from pydantic import ValidationError


def check_response(
    response: Union[Response, APIError], return_type: Type[T]
) -> Union[T, APIError]:
    if isinstance(response, APIError):
        return response
    try:
        return return_type(**response.json())
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


def execute(
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
    url = f"{executor.base_url}/api/{executor.api_version}{executor.api_endpoints[(verb, endpoint_name)]}"
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

    def fetch(self, query: QIncidentAction) -> Union[SingleIncident, APIError]:
        verb, endpoint_name = "get", "incident_fetch"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict(exclude_none=True))
        # reveal_type(t)
        # request = IncidentActions.execute(
        #     **self.build_request(verb=verb, endpoint_name=endpoint_name)
        # )
        return check_response(IncidentActions.execute(**request), SingleIncident)

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

    def summaries(self) -> Union[MFlocksSummary, APIError]:
        verb, endpoint_name = "get", "flocks_summary"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        return check_response(FlockQueries.execute(**request), MFlocksSummary)

    def summary(self, query: QFlocks) -> Union[MFlockSummary, APIError]:
        verb, endpoint_name = "get", "flock_summary"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(**query.dict())
        return check_response(FlockQueries.execute(**request), MFlockSummary)

    def list_all(self, query: QFlocks) -> Union[MFlockSensors, APIError]:
        verb, endpoint_name = "get", "flock_list"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlockSensors)

    def settings(self, query: QFlocks) -> Union[MFlockSettings, APIError]:
        verb, endpoint_name = "get", "flock_settings"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlockSettings)

    def users(self, query: QFlocks) -> Union[MFlockUsers, APIError]:
        verb, endpoint_name = "get", "flock_users"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlockUsers)

    def filter(self, query: QFlocksFilter) -> Union[MFlocksMetaData, APIError]:
        verb, endpoint_name = "get", "flocks_filter"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlocksMetaData)

    def list_for(self, query: QFlocksFor) -> Union[MFlocksList, APIError]:
        verb, endpoint_name = "get", "flocks_list"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlocksList)

    def get_note(self, query: QFlocks) -> Union[MFlockNote, APIError]:
        verb, endpoint_name = "get", "flock_note"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), MFlockNote)

    def add_note(self, query: QFlocksNote) -> Union[ThinkstResult, APIError]:
        verb, endpoint_name = "post", "flock_note"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), ThinkstResult)

    def delete_note(self, query: QFlocks) -> Union[ThinkstResult, APIError]:
        verb, endpoint_name = "delete", "flock_note"
        request = self.build_request(verb=verb, endpoint_name=endpoint_name)
        request["params"].update(query.dict())
        return check_response(FlockQueries.execute(**request), ThinkstResult)


# api_endpoints[("post", "flock_note_add"), "/flock/note/add"]
# api_endpoints[("delete", "flock_note_delete"), "/flock/note/delete"]
