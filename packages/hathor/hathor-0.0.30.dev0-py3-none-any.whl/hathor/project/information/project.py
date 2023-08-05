import os
import re
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Union

import yaml
from fs.base import FS
from fs.osfs import OSFS

from hathor.project.information.source_file import SourceFile
from hathor.project.information.source_root import SourceRoot


@dataclass()
class BuildProfile:
    directory: str = "./build"
    builder: str = "copy"


class Project:
    _root_directory: Path
    _config_path: Path
    _config: Dict = None
    _sources_root: List[SourceRoot]
    _build_profiles: Dict[str, BuildProfile]
    _active_profile: str = "default"

    def __init__(self, config_file: Path):
        self._config_path = config_file
        self._root_directory = self._config_path.parent
        self._sources_root = []

        self._build_profiles = dict()
        self._parse_build_profiles()
        self._scan()

    @property
    def config(self) -> Dict:
        if self._config is None:
            with self._config_path.open("r") as fp:
                self._config = yaml.load(fp, yaml.FullLoader)

        return self._config

    @property
    def build_config(self) -> Dict:
        return self.config.get("build", {})

    def build_profile(self, profile: str = None) -> BuildProfile:
        return self._build_profiles[profile or self._active_profile]

    @property
    def active_profile(self):
        return self._active_profile

    @active_profile.setter
    def active_profile(self, v: str):
        assert v in self._build_profiles, f"{v} is not a valid build profile"
        self._active_profile = v

    @property
    def serve_config(self):
        return self.config.get("serve", {})

    @property
    def save_instance_config(self) -> Dict:
        return self.config.get("save_instance", {})

    @property
    def save_instance_root(self) -> Path:
        path_string = self.save_instance_config.get("root_directory", self._sources_root[0].path)
        return Path(path_string)

    def resolve_user_path(self, path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            # *nix to host os
            if "/" in path:
                path = os.path.sep.join(path.split("/"))

        path = Path(path)
        if not path.is_absolute():
            path = self._root_directory.joinpath(path)

        return path

    def _parse_build_profiles(self):
        profiles = self.build_config.get("profiles", {})

        if "default" in profiles:
            default_profile = profiles["default"]

        else:
            default_profile = {}

            for k, v in typing.get_type_hints(BuildProfile).items():
                default_profile[k] = self.build_config.get(k)

        for profile_name, profile_object in {**profiles, "default": default_profile}.items():
            self._build_profiles[profile_name] = BuildProfile(**profile_object)

    def _scan(self):
        for source_path, properties in self.config["sources"].items():
            if not properties.get("enabled", False):
                continue

            path = self.resolve_user_path(source_path)
            self._sources_root.append(SourceRoot(OSFS(str(path.resolve())), properties))

    def rescan(self):
        self._sources_root = []

        self._scan()

    @property
    def source_files(self) -> List[SourceFile]:
        files = []

        for root in self._sources_root:
            files.extend(root.source_files)

        return files

    @property
    def entry_points(self) -> List[SourceFile]:
        return list(filter(lambda f: f.is_entry_point, self.source_files))

    @property
    def name(self):
        return self.config["name"]

    @property
    def path_compatible_name(self):
        return re.subn(r"\W", "_", self.name.lower())[0]

    @property
    def build_directory(self) -> Path:
        return self.resolve_user_path(self.build_profile().directory)

    @property
    def source_file_systems(self) -> List[FS]:
        return list(map(lambda r: r.fs, self._sources_root))

    @property
    def root_directory(self) -> Path:
        return self._root_directory

    @property
    def scripts(self) -> Dict[str, str]:
        return self.config.get("scripts", {})


def find_projects(search_root: Path = None) -> List[Project]:
    search_root = search_root or Path(os.getcwd()).resolve()
    projects = []

    for project_config in search_root.rglob("hathor.project.yml"):
        projects.append(Project(project_config))

    return projects
