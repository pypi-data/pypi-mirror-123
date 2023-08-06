from typing import Dict

from helpers import populate_setting_values

START_BLOCK = "#<!----ANNO"
END_BLOCK = "#ANNO ---->"


class InfoFileNotUpdatableException(Exception):
    def __init__(self, filepath: str):
        super().__init__(f"File {filepath} not updatable")


def _check_info_file(file_data: str, filepath: str):
    if not (START_BLOCK in file_data and END_BLOCK in file_data):
        raise InfoFileNotUpdatableException(filepath)


def _append_filedata(existing_filedata: str, new_filedata: str, filepath: str) -> str:
    _check_info_file(existing_filedata, filepath)
    return "\n".join(
        (
            existing_filedata[: existing_filedata.index(END_BLOCK)],
            new_filedata,
            existing_filedata[existing_filedata.index(END_BLOCK) :],
        )
    )


def append_to_info_file(filepath: str, filedata_part: str, settings: Dict[str, str]):
    populated_filepath = populate_setting_values(filepath, settings)
    with open(populated_filepath, "r") as reader:
        file_data = reader.read()
    with open(populated_filepath, "w") as writer:
        writer.write(_append_filedata(file_data, filedata_part, populated_filepath))
