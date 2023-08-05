import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Union
from uuid import uuid4

import yaml

from hathor.project.information.project import Project
from hathor.serve.models import ChangeListEntry, Package, PackageTakeout

CLIENTS = dict()
THREAD_INTERVAL = 2

ActiveProject = Union[None, Project]
active_project: ActiveProject = None


def by_id(client_id: str):
    return CLIENTS.get(client_id, None)


class OnClientAdded:
    _listener: callable
    _listeners: List[callable] = []

    def __init__(self, listener: callable):
        self._listener = listener
        self._listeners.append(listener)

    def disconnect(self):
        self._listeners.remove(self._listener)

    @classmethod
    def fire(cls, client):
        for listener in cls._listeners:
            listener(client)


class OnClientRemoved:
    _listener: callable
    _listeners: List[callable] = []

    def __init__(self, listener: callable):
        self._listener = listener
        self._listeners.append(listener)

    def disconnect(self):
        self._listeners.remove(self._listener)

    @classmethod
    def fire(cls, client):
        for listener in cls._listeners:
            listener(client)


def _generate_client_id() -> str:
    return str(uuid4())


class Client:
    _id: str
    _name: str
    _changes: Dict[str, ChangeListEntry]
    _packages: Dict[str, Package]
    _active_project: ActiveProject = None

    def __init__(self, name):
        self._id = _generate_client_id()
        self._name = name
        self._active_project = active_project

        self._changes = dict()
        self._packages = dict()

        CLIENTS[self._id] = self
        OnClientAdded.fire(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self):
        return self._name

    def add_changes(self, changes: List[ChangeListEntry]):
        for change in changes:
            self._changes[change.id] = change

    def remove(self):
        CLIENTS.pop(self._id)
        OnClientRemoved.fire(self)

    @property
    def changes(self) -> List[ChangeListEntry]:
        return list(self._changes.values())

    @property
    def active_project(self):
        return self._active_project

    def delete_changes(self, changes: List[str]):
        for change in changes:
            if change in self._changes:
                self._changes.pop(change)

    def create_package(self, change_ids: List[str]) -> Package:
        package = Package(
            id=str(uuid4()),
            changes=list(
                map(lambda t: t[1],
                    filter(lambda t: t[0] in change_ids,
                           self._changes.items()
                           )
                    )
            )
        )

        self._packages[package.id] = package

        return package

    def create_takeout(self, package_id: str) -> PackageTakeout:
        package = self._packages[package_id]

        takeout = PackageTakeout(dict())

        for change in package.changes:
            if not takeout.add_change(change):
                break

            if change.id in self._changes:
                self._changes.pop(change.id)

        return takeout

    def delete_package(self, package_id):
        if package_id in self._packages:
            self._packages.pop(package_id)

    def save_instance(self, instance_path: str, instance_json):
        instance_data = json.loads(instance_json) \
            if isinstance(instance_json, str) else instance_json

        for instance in instance_data:
            for prop_name, prop_value in instance["Properties"].items():
                if len(prop_value) == 1:
                    instance["Properties"][prop_name] = prop_value[0]

                elif len(prop_value) == 0:
                    instance["Properties"][prop_name] = None

        instance_data = {
            "Version": 1,
            "SaveDateTime": datetime.now().isoformat(),
            "Instances": instance_data
        }

        instance_path_split = instance_path.split(".")
        instance_name = instance_path_split[-1]

        if len(instance_path_split) <= 1:
            instance_directory = instance_path_split

        else:
            instance_directory = instance_path_split[:-1]

        fs_instance_path_rel = Path(*instance_directory, f"{instance_name}.instance.yml")
        fs_instance_path = self.active_project.save_instance_root / fs_instance_path_rel
        os.makedirs(fs_instance_path.parent, exist_ok=True)

        with fs_instance_path.open("w+") as fp:
            yaml.dump(instance_data, stream=fp, Dumper=yaml.Dumper)


def iter_clients():
    for client in CLIENTS.values():
        yield client


def set_active_project(project: Project):
    global active_project

    active_project = project
    for client in iter_clients():
        client.active_project = project
