"""
Test Comic module.

This module contains tests for Comic objects.
"""
import datetime
from decimal import Decimal

import pytest
import requests_mock

from serifan import api, comics_list, exceptions, session, utils


def test_comics_list(comic_list_response):
    """Test for comics_list."""
    res = comics_list.ComicsList(comic_list_response)
    comic_iter = iter(res)
    assert next(comic_iter).title == "BITTER ROOT #15 CVR A GREENE (MR)"
    assert next(comic_iter).title == "BITTER ROOT #15 CVR B CONLEY CURIEL (MR)"
    assert len(res) == 3
    assert res[0].publisher == "IMAGE COMICS"
    assert res[1].title == "BITTER ROOT #15 CVR B CONLEY CURIEL (MR)"
    assert res[1].price == Decimal("3.99")
    assert res[1].release_date == datetime.date(2021, 8, 11)
    assert res[1].diamond_id == "MAY210140"
    assert res[2].price == Decimal("0.00")


def test_available_dates(sb_dates_response, mocker):
    """Test available dates api."""
    mocker.patch.object(session.Session, "call", return_value=sb_dates_response)
    sb = api()
    result = sb.available_release_dates()
    assert len(result) == 5
    assert result[0] == datetime.date(2021, 7, 29)


def test_new_releases(comic_list_response, mocker):
    """Test new releases api."""
    mocker.patch.object(session.Session, "call", return_value=comic_list_response)
    sb = api()
    result = sb.new_releases()
    assert len(result) == 3
    assert result[0].title == "BITTER ROOT #15 CVR A GREENE (MR)"


def test_previous_releases(comic_list_response, mocker):
    """Test previous releases api."""
    mocker.patch.object(session.Session, "call", return_value=comic_list_response)
    sb = api()
    result = sb.previous_releases()
    assert len(result) == 3
    assert result[0].title == "BITTER ROOT #15 CVR A GREENE (MR)"


def test_future_releases(comic_list_response, mocker):
    """Test future releases api."""
    mocker.patch.object(session.Session, "call", return_value=comic_list_response)
    sb = api()
    result = sb.future_releases()
    assert len(result) == 3
    assert result[0].title == "BITTER ROOT #15 CVR A GREENE (MR)"


def test_query(comic_list_response, mocker):
    """Test query api."""
    mocker.patch.object(session.Session, "call", return_value=comic_list_response)
    sb = api()
    result = sb.query("Image", "WildC.A.T.S.", None, None)
    assert len(result) == 3
    assert result[0].title == "BITTER ROOT #15 CVR A GREENE (MR)"


def test_bad_response():
    """Test for a bad response."""
    with pytest.raises(exceptions.ApiError):
        comics_list.ComicsList({"comics": {"name": 1}})


def test_list_string_to_date(sb_dates_response):
    """Test the list_string_to_date function."""
    results = utils.list_strings_to_dates(sb_dates_response)
    assert len(results) == 5
    assert results[0] == datetime.date(2021, 7, 29)


def test_for_shortboxed_internal_server_error():
    """Test for Shortboxed 500 response code."""
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, status_code=500, text="Shortboxed Internal Server Error")

        with pytest.raises(exceptions.ApiError):
            sb = api()
            sb.available_release_dates()
