import json
import os
from enum import Enum
from typing import Dict

from component_files.component import COMPONENT_FILES
from component_files.consumer import CONSUMER_FILES
from component_files.service import SERVICE_FILES
from helpers import populate_setting_values, create_folder_for_filepath
from info_file import append_to_info_file

SETTINGS_FILENAME = ".anno.json"


class ComponentType(Enum):
    COMPONENT = "component"
    SERVICE = "service"
    CONSUMER = "consumer"


COMPONENT_FILESTRUCTURE = {
    ComponentType.COMPONENT: COMPONENT_FILES,
    ComponentType.SERVICE: SERVICE_FILES,
    ComponentType.CONSUMER: CONSUMER_FILES,
}


def generate_component(component_type: ComponentType, component_name: str, main_component_name: str):
    settings = load_settings_from_file()
    settings[f"{component_type.value}Name"] = component_name
    settings[f"{ComponentType.COMPONENT.value}Name"] = main_component_name
    generate(main_component_name, COMPONENT_FILESTRUCTURE[component_type], settings)


def generate(component_name: str, structure: Dict[str, str], settings: Dict[str, str]):
    for filepath, filedata in structure.items():
        if filepath.startswith("+"):
            filepath = f"{component_name}/{filepath[1:]}"
            append_to_info_file(filepath, filedata, settings)
        else:
            filepath = f"component/{filepath}"
            generate_file(filepath, filedata, settings)


def generate_file(filepath: str, filedata: str, settings: Dict[str, str]):
    populated_filepath = populate_setting_values(filepath, settings)
    create_folder_for_filepath(populated_filepath)

    if os.path.exists(populated_filepath):
        raise FileExistsError
    with open(populated_filepath, "w") as file:
        file.write(populate_setting_values(filedata, settings))


def load_settings_from_file(settings_filename: str = SETTINGS_FILENAME) -> Dict[str, str]:
    with open(settings_filename, "r") as file:
        return json.load(file)
