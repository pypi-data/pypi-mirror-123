import os
from typing import Dict


def populate_setting_values(string: str, settings: Dict[str, str]) -> str:
    for key, val in settings.items():
        string = string.replace(f"${{{key}}}", val)
    return string


def create_folder_for_filepath(filepath: str):
    try:
        folderpath = filepath[: filepath.rindex("/")]
        os.makedirs(folderpath)
    except (ValueError, FileExistsError):
        pass
