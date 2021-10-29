from __future__ import annotations

import json
import re
from datetime import datetime
from typing import (Any, Dict, List, Mapping, MutableMapping, Optional, Type,
                    Union)

import httpx
from pydantic import (BaseModel, HttpUrl, IPvAnyAddress, Json, SecretStr,
                      validator)
from pydantic.error_wrappers import ValidationError

# from canarytools.models.settings import Settings


__all__ = ["AuthToken", "api_auth_token_length", "APIError", "Query"]
api_auth_token_length = 32


class AuthToken(BaseModel):
    auth_token: SecretStr

    def secret_dict(self) -> Dict[str, str]:
        # Style: not great check th docs as this migh be supported.
        data = self.dict()
        data["auth_token"] = self.auth_token.get_secret_value()
        return data

    @validator("auth_token")
    def auth_token_must(cls: AuthToken, v: str) -> str:
        if len(v) != api_auth_token_length:
            raise ValueError(
                f"auth_token must be {api_auth_token_length} characters. The one provided is {len(v)}"
            )
        return v


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
        data["device"] = json.dumps(data["device"])
        super().__init__(**data)


class MDeviceIPs(BaseModel):
    ips: Json

    def __init__(__pydantic_self__, **data: Any) -> None:
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
        data["devices"] = json.dumps(data["devices"])
        super().__init__(**data)


class Query(BaseModel):
    """
        ### A
        * Query to get info
    """
    node_id: Optional[str]
    flock_id: Optional[str]
    incidents_since: int = 0
    event_limit: int = 1
    limit: int = 1
    cursor: Optional[str]
    shrink: bool = True
    tz: Optional[str]


class Cursor(BaseModel):
    next: Optional[str]
    next_link: Optional[HttpUrl]
    prev: Optional[str]
    prev_link: Optional[HttpUrl]


from typing import List


class Port(BaseModel):
    port: int

    @validator("port")
    def check_port(v: int) -> int:
        if v > 65536 or v < 1:
            raise ValueError("Port must be in range: (0, 65536). {v} was used")
        return v


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


class IncidentDescription(BaseModel):
    acknowledged: bool
    created: int
    created_std: datetime
    description: str
    dst_host: IPvAnyAddress
    dst_port: Optional[Port]
    events: List[Json]

class IncidentDescription(BaseModel):
    hash_id: str
    id: str
    summary: str
    updated: str
    updated_id: int
    updated_std: str
    updated_time: str
    description: Json

    def __init__(self, **data: str) -> None:
        data["description"] = json.dumps(data["description"])
        super().__init__(**data)
class Incidents(BaseModel):
    cursor: Cursor
    feed: str
    incidents: List[IncidentDescription]#Json  # TODO: Create finer graain models. This is a side step for now



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

class QFlocks(BaseModel):
    flock_id:str="flock:default"


class MFlocksSummary(BaseModel):
    flocks_summary:Json
    def __init__(self, **data: str) -> None:
        data["flocks_summary"] = json.dumps(data["flocks_summary"])
        super().__init__(**data)
