"""
Design:
This file should contain all data models that the api produces. This first stab at it
has taken a few shortcuts. Ideally, this should show a neat composition of the data structures
that describe Incidents, Events, Settings, Flock Stettings etc...

All these models can export valid schema for additional tooling and provide a true refection of what
canarytools exposes.
"""
from __future__ import annotations

import dataclasses
import json
import re
from datetime import datetime
from typing import (Any, Dict, List, Literal, Mapping, MutableMapping,
                    Optional, Type, Union)

import httpx
from pydantic import (BaseModel, Field, FilePath, HttpUrl, IPvAnyAddress, Json,
                      SecretStr, validator)
from pydantic.error_wrappers import ValidationError

__all__ = [
    "AuthToken",
    "api_auth_token_length",
    "APIError",
    "Query",
    "ThinkstResult",
    "AuthFile",
    "Settings",
    "QDevices",
    "Incidents",
    "MDevice",
    "MDeviceIPs",
    "MDevices",
    "MDeviceTxTIPs",
    "MFlockSensors",
    "MFlockSettings",
    "MFlockSummary",
    "QDeviceIPs",
    "QFlocks",
    "QIncidentAction",
    "SingleIncident",
]
api_auth_token_length = 32


class ThinkstResult(BaseModel):
    result: str


class AuthToken(BaseModel):
    auth_token: SecretStr

    @validator("auth_token")
    def auth_token_must(cls: AuthToken, v: str) -> str:
        if len(v) != api_auth_token_length:
            raise ValueError(
                f"auth_token must be {api_auth_token_length} characters. The one provided is {len(v)}"
            )
        return v

    def secret_dict(self) -> Dict[str, str]:
        # Style: not great check the docs as this might be supported.
        data = self.dict()
        data["auth_token"] = self.auth_token.get_secret_value()
        return data


class AuthFile(BaseModel):
    auth_token_file_as_bytes: bytes
    auth_token_file: Optional[FilePath]


class Settings(BaseModel):
    auth_token: AuthToken
    auth_token_enabled: bool
    canarytokens_user_domains_enable: bool
    canarytokens_webroot_enable: bool
    console_domain: str
    result: str
    # TODO: what is console_settings_change_enable
    console_settings_change_enable: bool
    device_settings_change_enable: bool
    email_notification_enable: bool
    generic_incident_webhooks: List[str]
    globally_enforce_2fa: bool
    hipchat_integration_urls: List[str]

    def __init__(__pydantic_self__, **data: Any) -> None:
        data["auth_token"] = AuthToken(auth_token=data["auth_token"])
        super().__init__(**data)


class APIError(BaseModel):
    status_code: httpx._status_codes.codes
    message: str
    endpoint: str


class QDevices(BaseModel):
    tz: Optional[str] = None
    # filter_str: Optional[str] = None


class QDevicesInfo(QDevices):
    node_id: str
    settings: Optional[bool] = False
    exclude_fixed_settings: Optional[bool] = False


class QDeviceIPs(QDevices):
    download: bool = False
    include_annotations: bool = False
    flock_id: Optional[Union[bool, str]] = None


class MDevice(BaseModel):
    device: Json
    def __init__(__pydantic_self__, **data: Any) -> None:
        # TODO: Add model details - Json should not be used.
        data["device"] = json.dumps(data["device"])
        super().__init__(**data)


class MDeviceIPs(BaseModel):
    ips: Json

    def __init__(__pydantic_self__, **data: Any) -> None:
        # TODO: Add model details - Json should not be used.
        data["ips"] = json.dumps(data["ips"])
        super().__init__(**data)


class MDeviceTxTIPs(BaseModel):
    ips: str


class MDevices(BaseModel):
    devices: Json  # TODO: Complete the model if this lives on.
    result: str  # Should these be enums?
    # TODO: refactor these optional values out.
    feed: Optional[str] = None
    updated: Optional[str] = None  # datetime#"Sun, 26 Apr 2020 20:34:02 GMT",
    updated_std: Optional[str] = None  # datetime #"2020-04-26 20:34:02 UTC+0000",
    updated_timestamp: Optional[str] = None  # datetime# 1587933242
    def __init__(__pydantic_self__, **data: str) -> None:
        # TODO: Add model details - Json should not be used.
        data["devices"] = json.dumps(data["devices"])
        super().__init__(**data)


class Query(BaseModel):
    """
    # TODO: Add docstrings if this becomes long lived.
    """

    node_id: Optional[str]
    flock_id: Optional[str]
    incidents_since: int = 0
    event_limit: int = 1
    limit: int = 1
    cursor: Optional[str]
    shrink: bool = True
    tz: Optional[str]


class QIncidentAction(BaseModel):
    incident: Optional[str] = None
    hash_id: Optional[str] = None
    extended_details: bool = True
    tz: Optional[str] = None

    @validator("hash_id", pre=True, always=True)
    def check_hash_id_or_incident(cls, hash_id:str, values:Dict[str, Any])->str:
        if not values.get("incident", False) and hash_id is None:
            raise ValueError("either hash_id or incident is required")
        return hash_id


class Cursor(BaseModel):
    next: Optional[str]
    next_link: Optional[HttpUrl]
    prev: Optional[str]
    prev_link: Optional[HttpUrl]


from typing import List

# class Port(BaseModel):
#     port: Union[int, str]

#     @validator("port")
#     def check_port(v: Union[int, str]) -> int:
#         v = int(v)
#         if v > 65536 or v < 1 or v == -1: #Hack: why is -1 used. None seems a better option.
#             raise ValueError("Port must be in range: (0, 65536). {v} was used")
#         return v


class IncidentHTTPLoad(BaseModel):
    HOSTNAME: str
    METHOD: str
    PASSWORD: str
    PATH: str
    RESPONSE: int
    SKIN: str
    USERAGENT: str
    USERNAME: str
    timestamp: int
    timestamp_std: datetime


# TODO: Improve name, please ;)
class IncidentTokenEvent(BaseModel):
    canarytoken: str
    dst_port: int
    hostname: str
    src_host: Union[IPvAnyAddress, str]
    timestamp: int
    timestamp_std: str
    type: str


class IncidentCanaryEvent(BaseModel):
    timestamp: int
    timestamp_std: str


class IncidentCanaryDescription(BaseModel):
    acknowledged: bool
    created: int
    created_std: str  # TODO: what? datetime should be enforced.
    description: str
    dst_host: str  # IPvAnyAddress
    dst_port: int
    events: List[IncidentCanaryEvent]
    events_count: int
    events_list: Union[
        int, List[int]
    ]  # TODO: Why/when is this not a list. if this is a timestamp convert it.
    flock_id: str  # TODO: add validation
    flock_name: str
    ip_address: Union[IPvAnyAddress, str]
    ippers: str
    local_time: str
    logtype: str  # Literal["16000"] # TODO: make enum
    mac_address: str
    matched_annotations: Dict[str, Any]
    name: str
    node_id: str
    notified: bool
    src_host: Union[IPvAnyAddress, str]
    src_host_reverse: str
    src_port: int


class IncidentTokenDescription(BaseModel):
    acknowledged: bool
    created: int
    created_std: Optional[str]  # TODO: what? datetime should be enforced.
    description: str
    dst_host: str  # IPvAnyAddress
    dst_port: int
    events: Optional[List[IncidentTokenEvent]]  # TODO: Is this valid as an optional?
    events_count: int
    # events_list: Union[None, int, List[int]] # TODO: Why/when is this not a list. if this is a timestamp convert it.
    flock_id: str  # TODO: add validation
    flock_name: Optional[str]
    local_time: str
    logtype: str  # Literal["16000"] # TODO: make enum
    matched_annotations: Dict[str, Any]
    name: str
    node_id: str
    notified: bool
    src_host: Union[IPvAnyAddress, str]
    src_port: int


class SingleIncident(BaseModel):
    incident: Union[
        IncidentTokenDescription, IncidentCanaryDescription
    ]  # TODO this is wrong in general.

    @validator("incident", pre=True)
    def validate_t(
        cls, value: Dict[str, Any]
    ) -> Union[IncidentTokenDescription, IncidentCanaryDescription]:
        # if isinstance(value, BaseModel):
        #     return value
        # Design:   This is not ideal. Check it's needed once
        #           all models are defined.
        if "canarytoken" == value["sensor"]:
            return IncidentTokenDescription(**value)
        else:
            return IncidentCanaryDescription(**value)


class Incident(BaseModel):
    hash_id: str
    id: str
    summary: str
    updated: str
    updated_id: int
    updated_std: str
    updated_time: str

    description: Union[
        IncidentTokenDescription, IncidentCanaryDescription
    ]  # TODO: ensure schema makes sense for this union. See Field(..., discriminator="description")

    @validator("description", pre=True)
    def validate_t(
        cls, value: Dict[str, Any]
    ) -> Union[IncidentTokenDescription, IncidentCanaryDescription]:
        # if isinstance(value, BaseModel):
        #     return value
        # Design:   This is not ideal. Check it's needed once
        #           all models are defined.
        if "canarytoken" in value["events"][0].keys():
            return IncidentTokenDescription(**value)
        else:
            return IncidentCanaryDescription(**value)


class Incidents(BaseModel):
    cursor: Cursor
    feed: str
    incidents: List[Incident]


#   "feed": "Acknowledged Incidents",
#   "incidents": [
#     {
#       "description": {
#         "acknowledged": "True",
#         "created": "1586338742",
#         "created_std": "2020-04-08 09:39:02 UTC+0000",
#         "description": "HTTP Login Attempt",
#         "dst_host": "<destination_ip>",
#         "dst_port": "80",
#         "events": [
#           {
#           }
#         ],
#         "events_count": "1",
#         "ip_address": "",
#         "ippers": "",
#         "local_time": "2020-04-08 09:39:01",
#         "logtype": "3001",
#         "mac_address": "",
#         "name": "ExampleBird",
#         "node_id": "<node_id>",
#         "notified": "False",
#         "src_host": "<source_ip>",
#         "src_host_reverse": "<source_hostname>",
#         "src_port": "60961"
#       },
#       "hash_id": "<hash_id>",
#       "id": "<incident_key>",
#       "summary": "HTTP Login Attempt",
#       "updated": "Wed, 08 Apr 2020 10:55:09 GMT",
#       "updated_id": 142,
#       "updated_std": "2020-04-08 10:55:09 UTC+0000",
#       "updated_time": "1586343309"
#     }
#   ],
#   "max_updated_id": 142,
#   "result": "success",
#   "updated": "Wed, 08 Apr 2020 10:55:09 GMT",
#   "updated_std": "2020-04-08 10:55:09 UTC+0000",
#   "updated_timestamp": 1586343309
# }


class MFlockSensors(ThinkstResult):
    sensors: List[str]


class QFlocks(BaseModel):
    flock_id: str = "flock:default"


class MFlockSettings(BaseModel):
    settings: Json  # TODO: add details.
    # Dict[str, MFlockSettingBase]
    # notification_info:Json
    # webhooks:Json
    # whitelisting:Json
    def __init__(__pydantic_self__, **data: Any) -> None:
        data["settings"] = json.dumps(data["settings"])
        super().__init__(**data)


class MFlocksSummary(BaseModel):
    flocks_summary: Json

    def __init__(self, **data: str) -> None:
        data["flocks_summary"] = json.dumps(data["flocks_summary"])
        super().__init__(**data)

class TokenStats(BaseModel):
    count: int
    kind: str  # TODO: make this an enum


class MFlockSummary(ThinkstResult):

    different_token_num: int
    disabled_tokens: int
    incident_count: int
    top_tokens: List[TokenStats]
    total_tokens: int
    triggered_tokens: int
