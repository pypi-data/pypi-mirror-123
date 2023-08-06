from pytest_mock import MockFixture  # type: ignore

from generate import generate


def test_generate_should_call_append_to_info_file_if_filepath_startswith_plus(mocker: MockFixture):
    insert_info_spy = mocker.patch("component_generator.generate.append_to_info_file")
    generate({"+append_info": "dummy"}, {})
    insert_info_spy.assert_called_once_with("apppend_info", "dummy", {})


def test_generate_should_call_generate_file_if_filepath_not_startswith_plus(mocker: MockFixture):
    generate_file_spy = mocker.patch("component_generator.generate.generate_file")
    generate({"generate": "dummy"}, {})
    generate_file_spy.assert_called_once_with("generate", "dummy", {})
