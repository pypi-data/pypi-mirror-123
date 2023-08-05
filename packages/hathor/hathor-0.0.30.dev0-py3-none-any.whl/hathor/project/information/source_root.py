from typing import List, Dict

from fs.base import FS

from hathor.project.information.source_file import SourceFile
from hathor.project.source_processors.processors import source_processors


class SourceRoot:
    _fs: FS
    _properties: Dict
    _source_files: List[SourceFile]

    def __init__(self, fs: FS, properties: Dict):
        self._fs = fs
        self._properties = properties
        self._source_files = []

        self._scan()

    def _scan(self):
        for processor in source_processors():
            self._source_files.extend(
                map(
                    lambda gm: SourceFile(self._fs, gm.path),
                    self._fs.glob(f"**/*.{processor.extension()}")
                )
            )

    @property
    def source_files(self) -> List[SourceFile]:
        return list(self._source_files)

    @property
    def path(self):
        return self._fs.root_path

    @property
    def fs(self):
        return self._fs
