from canarytools.api import base_url


def test_base_url_expansion():
    burl = base_url.format("hash")
    assert burl == "https://hash.canary.tools"
