from unittest.mock import call

import pytest  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from info_file import (
    _check_info_file,
    InfoFileNotUpdatableException,
    _append_filedata,
    append_to_info_file,
)


def test_check_info_file():
    _check_info_file("#<!----ANNO#ANNO ---->", "dummy_filepath")
    _check_info_file("#<!----ANNO____#ANNO ---->", "dummy_filepath")


def test_check_info_file_raises_info_file_not_updatable():
    with pytest.raises(InfoFileNotUpdatableException):
        _check_info_file("----ANNO____#ANNO ---->", "dummy_filepath")
    with pytest.raises(InfoFileNotUpdatableException):
        _check_info_file("#<!----ANNO____#ANNO --", "dummy_filepath")


def test_append_filedata():
    assert (
        _append_filedata("#<!----ANNO____#ANNO ---->", "new_part", "dummy_filepath")
        == "#<!----ANNO____\nnew_part\n#ANNO ---->"
    )


def test_append_to_info_file(mocker: MockFixture):
    open_spy = mocker.patch("builtins.open")
    open_spy.return_value.__enter__.return_value.read.return_value = "#<!----ANNO____#ANNO ---->"
    append_to_info_file("${test_filepath}.dat", "new_part", {"test_filepath": "actual_filepath"})
    assert call("actual_filepath.dat", "w") in open_spy.call_args_list
    open_spy.return_value.__enter__.return_value.write.assert_called_once_with(
        "#<!----ANNO____\nnew_part\n#ANNO ---->"
    )
