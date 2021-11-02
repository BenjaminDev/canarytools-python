"""
Design: Exploring structural typing as how to default to composition as apposed to inheritance
leveraging mypy to enforce typing is consistent and corretc.
"""

from typing import (Any, Callable, Dict, Protocol, Tuple, Union,
                    runtime_checkable)

import httpx
from mypy_extensions import NamedArg

from canarytools.models.base import APIError, AuthToken


@runtime_checkable
class Executor(Protocol):
    """
    A skeleton of what an executor must provide.
    """

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


RequestBuilder = Callable[
    [Executor, NamedArg(str, "verb"), NamedArg(str, "endpoint_name")], Dict[str, Any]
]


@runtime_checkable
class Execute(Protocol):
    def __call__(
        self, *, verb: str, url: str, params: Dict[str, str]
    ) -> Union[httpx.Response, APIError]:
        ...
