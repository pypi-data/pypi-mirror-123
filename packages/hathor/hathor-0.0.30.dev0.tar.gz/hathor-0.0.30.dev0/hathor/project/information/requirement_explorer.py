from dataclasses import dataclass
from typing import Dict, List

from hathor.project.information.project import Project
from hathor.project.information.source_file import SourceFile


@dataclass
class RequireLink:
    file: SourceFile
    requirements: List[SourceFile]


class RequirementNotFound(RuntimeError):
    pass


class RequirementExplorer:
    _project: Project
    _entry_point: SourceFile
    _links: List[RequireLink]

    def __init__(self, project: Project, entry_point: SourceFile):
        self._project = project
        self._entry_point = entry_point
        self._links = []

        self._build()

    def _build(self):
        reference: Dict[str, SourceFile] = \
            dict(zip(map(lambda f: f.require_alias, self._project.source_files), self._project.source_files))

        def _process_file(file: SourceFile):
            requirements: List[SourceFile] = []

            for require_def in file.requires:
                if required_file := reference.get(require_def.require, None):
                    requirements.append(required_file)

                else:
                    raise RequirementNotFound(str(require_def))

            self._links.append(RequireLink(file, requirements))

            for requirement in requirements:
                _process_file(requirement)

        _process_file(self._entry_point)

    @property
    def links(self) -> List[RequireLink]:
        return list(self._links)
