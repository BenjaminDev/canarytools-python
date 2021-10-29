import pytest
from pydantic import ValidationError

from canarytools.models import AuthToken


def test_auth_token_invalid():
    auth_token = "thisistooshort"
    with pytest.raises(ValidationError) as e:
        AuthToken(auth_token=auth_token)


def test_auth_token_valid():
    auth_token = "thisisthecorectlengthwhichisgood"
    AuthToken(auth_token=auth_token)
