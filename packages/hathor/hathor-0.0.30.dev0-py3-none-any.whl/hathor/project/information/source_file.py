import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from fs.base import FS

from hathor.project.information.source_ptns import *


class EntryPointType:
    script = "Script"
    local_script = "LocalScript"


@dataclass
class EntryPointDefinition:
    line: str
    type: str
    game_location: str

    @property
    def name(self):
        return self.game_location.split(".")[-1]


@dataclass
class RequireDefinition:
    line: str
    require: str

    def __str__(self):
        return self.require


def module_returns(lines: List[str]) -> bool:
    for line in lines[-3:]:
        if line.strip().startswith("return"):
            return True

    return False


class SourceFile:
    _entry_point: Union[None, EntryPointDefinition] = None
    _requires: List[RequireDefinition]
    _root_fs: FS
    _path: str

    def __init__(self, root_fs: FS, path: str):
        self._root_fs = root_fs
        self._path = path
        self._requires = []
        self._scan()

    def _scan(self):
        with self._root_fs.open(self._path) as fp:
            for line in fp.readlines():
                if match := ENTRY_POINT_PTN.match(line):
                    self._entry_point = EntryPointDefinition(
                        line,
                        match.group(1).strip(),
                        match.group(2).strip()
                    )

                if match := REQUIRE_PTN.search(line.strip()):
                    self._requires.append(RequireDefinition(
                        line,
                        match.group(1).strip()
                    ))

    @property
    def is_entry_point(self):
        return self._entry_point is not None

    @property
    def require_alias(self) -> str:
        path_split = self._path.lstrip(os.path.sep).split(os.path.sep)
        last = len(path_split) - 1
        file_name_split = path_split[last].split(".")

        if path_split[last].lower().endswith(".lua"):
            path_split[last] = ".".join(file_name_split[:-1])

        return ".".join(path_split)

    @property
    def requires(self) -> List[RequireDefinition]:
        return list(self._requires)

    @property
    def name(self):
        return ".".join(os.path.basename(self._path).split('.')[:-1])

    @property
    def entry_point_path(self) -> Path:
        assert self.is_entry_point, "File must be an entry point"

        return Path(*self._entry_point.game_location.split("."))

    @property
    def entry_point_definition(self) -> EntryPointDefinition:
        assert self.is_entry_point and self._entry_point, "This source file is not an entry point!"
        return self._entry_point

    @property
    def path(self) -> str:
        return self._path

    def read(self):
        with self._root_fs.open(self._path, "r") as fp:
            contents = fp.read()

        return contents

    def __str__(self):
        return self.require_alias
