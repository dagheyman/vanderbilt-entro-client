import pytest

from entro.client import EntroClient


def test_parse_response():
    assert EntroClient.parse_response("        0       6       15704") == [
        "0",
        "6",
        "15704",
    ]
    assert EntroClient.parse_response("     \t0       6       15704") == [
        "0",
        "6",
        "15704",
    ]
    assert EntroClient.parse_response("     \t0       6       15704\n") == [
        "0",
        "6",
        "15704",
    ]
    assert EntroClient.parse_response("        1") == ["1"]
