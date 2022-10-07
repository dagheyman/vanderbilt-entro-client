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


def test_get_salted_pw():
    assert (
        EntroClient.get_salted_pw("salt", "password")
        == "67a1e09bb1f83f5007dc119c14d663aa"
    )
