from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Union

from hathor.project.information.source_file import SourceFile


@dataclass
class ProcessingResult:
    file_name: str
    file_content: str


class SourceProcessor(ABC):
    @staticmethod
    @abstractmethod
    def extension():
        pass

    @classmethod
    @abstractmethod
    def _is_candidate(cls, path: Path) -> bool:
        pass

    @classmethod
    def is_candidate(cls, path: Union[str, PathLike]) -> bool:
        if isinstance(path, str):
            path = Path(path)

        else:
            path = str(path)

        return cls._is_candidate(path)

    @abstractmethod
    def process(self, source_file: SourceFile) -> ProcessingResult:
        pass
