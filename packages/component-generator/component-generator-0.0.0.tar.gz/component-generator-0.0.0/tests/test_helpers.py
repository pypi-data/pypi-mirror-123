from pytest_mock import MockFixture

from helpers import create_folder_for_filepath, populate_setting_values


def test_create_folder_for_filepath(mocker: MockFixture):
    dummy_folder = "dummy_folder"
    mkdir_spy = mocker.patch("os.makedirs")
    create_folder_for_filepath(f"{dummy_folder}/dummy_file")
    mkdir_spy.assert_called_once_with(dummy_folder)


def test_create_folder_for_filepath_with_nested_folderpath(mocker: MockFixture):
    dummy_folderpath = "dummy/folder/child"
    mkdir_spy = mocker.patch("os.makedirs")
    create_folder_for_filepath(f"{dummy_folderpath}/dummy_file")
    mkdir_spy.assert_called_once_with(dummy_folderpath)


def test_create_folder_for_filepath_doesnt_create_anything_if_no_folderpath(mocker: MockFixture):
    mkdir_spy = mocker.patch("os.makedirs")
    create_folder_for_filepath("dummy_file")
    mkdir_spy.assert_not_called()


def test_create_folder_for_filepath_if_folder_already_exists(mocker: MockFixture):
    mocker.patch("os.makedirs", side_effect=FileExistsError())
    create_folder_for_filepath("already_exists/dummy_file")


def test_populate_setting_values():
    assert (
        populate_setting_values(
            "${this}_${is} ${a} test_${dummy}", {"this": "these", "is": "are", "a": "", "dummy": "dummies"}
        )
        == "these_are  test_dummies"
    )
    assert (
        populate_setting_values(
            "$no} changes\nto{this} ${string", {"no": "none", "this": "these", "string": "strings"}
        )
        == "$no} changes\nto{this} ${string"
    )
