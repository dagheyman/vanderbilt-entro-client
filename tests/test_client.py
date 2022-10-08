import pytest

from entro.client import EntroClient
from datetime import datetime


def test_parse_response():
    assert EntroClient.parse_response("        0       6       15704") == ("0", [
        "6",
        "15704",
    ])
    assert EntroClient.parse_response("     \t0       6       15704") == ("0", [
        "6",
        "15704",
    ])
    assert EntroClient.parse_response("     \t0       6       15704\n") == ("0", [
        "6",
        "15704",
    ])
    assert EntroClient.parse_response("        1") == ("1", [])


def test_get_salted_pw():
    assert (
        EntroClient.get_salted_pw("salt", "password")
        == "67a1e09bb1f83f5007dc119c14d663aa"
    )


def test_date_to_timestamp():

    assert (
        EntroClient.date_to_timestamp(datetime.fromisoformat("2022-10-11 17:00"))
        == 1034355600
    )
    assert (
        EntroClient.date_to_timestamp(datetime.fromisoformat("2022-10-11 19:30"))
        == 1034364600
    )
