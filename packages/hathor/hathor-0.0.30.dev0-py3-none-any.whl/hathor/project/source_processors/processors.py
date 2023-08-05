from os import PathLike
from typing import List, Type, Union

from hathor.project.source_processors.instance_yaml_processor import InstanceYamlProcessor
from hathor.project.source_processors.lua_processor import LuaProcessor
from hathor.project.source_processors.source_processor import SourceProcessor


def source_processors() -> List[Type[SourceProcessor]]:
    return [
        LuaProcessor,
        InstanceYamlProcessor
    ]


def get_processor_by_path(path: Union[str, PathLike]) -> SourceProcessor:
    for processor_class in source_processors():
        if processor_class.is_candidate(path):
            return processor_class()
