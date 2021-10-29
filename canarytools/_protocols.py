from typing import (Any, Callable, Dict, Protocol, Tuple, Union,
                    runtime_checkable)

import httpx
from mypy_extensions import (Arg, DefaultArg, DefaultNamedArg, KwArg, NamedArg,
                             VarArg)

from canarytools.models.base import APIError, AuthToken


@runtime_checkable
class Executor(Protocol):
    auth_token: AuthToken
    base_url: str
    api_version: str
    api_endpoints: Dict[Tuple[str, str], str]

    def __init__(
        self,
        *,
        auth_token: AuthToken,
        base_url: str,
        api_version: str,
        api_endpoints: Dict[Tuple[str, str], str]
    ):
        ...

    def execute(
        self, *, verb: str, url: str, params: Dict[str, str]
    ) -> Union[httpx.Response, APIError]:
        ...


# @runtime_checkable
# class RequestBuilder(Protocol):
#     def __call__(executor:Executor, *, verb:str, endpoint_name:str)-> Dict[str,Any]:
#         ...
RequestBuilder = Callable[
    [Executor, NamedArg(str, "verb"), NamedArg(str, "endpoint_name")], Dict[str, Any]
]


@runtime_checkable
class Execute(Protocol):
    def __call__(
        self, *, verb: str, url: str, params: Dict[str, str]
    ) -> Union[httpx.Response, APIError]:
        ...
