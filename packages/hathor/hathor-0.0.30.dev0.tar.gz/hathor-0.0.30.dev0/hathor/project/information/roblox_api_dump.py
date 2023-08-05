from functools import lru_cache
from typing import Dict, Union

import requests

_api_dump = None


def version_qt_studio() -> str:
    response = requests.get("https://setup.rbxcdn.com/versionQTStudio")
    response.raise_for_status()

    return response.text.strip()


def current_api_dump() -> Dict:
    response = requests.get(f"https://setup.rbxcdn.com/{version_qt_studio()}-API-Dump.json")
    response.raise_for_status()

    return response.json()


@lru_cache()
def api_dump() -> Dict:
    return current_api_dump()


@lru_cache()
def api_dump_by_class_name() -> Dict[str, Dict]:
    d = dict()

    for class_specification in api_dump()["Classes"]:
        d[class_specification["Name"]] = class_specification

    return d


@lru_cache()
def query_property(class_name: str, property_name: str, superclass_name: Union[None, str] = None):
    query_class_name = superclass_name or class_name

    class_specification = api_dump_by_class_name()[query_class_name]
    for class_member in class_specification["Members"]:
        if class_member["MemberType"] == "Property" and class_member["Name"] == property_name:
            return class_member

    superclass = class_specification["Superclass"]
    if superclass == "<<<ROOT>>>":
        return None

    return query_property(class_name, property_name, superclass)


@lru_cache()
def has_tag(class_name: str, tag: str):
    class_specification = api_dump_by_class_name()[class_name]
    tags = class_specification.get("Tags", [])

    return tag.lower() in list(map(str.lower, map(str.strip, tags)))


@lru_cache()
def is_a(class_name: str, ancestor_name: str):
    if class_name == ancestor_name:
        return True

    ancestry_tree = [class_name]
    class_specification = api_dump_by_class_name()[class_name]

    while class_specification["Superclass"] != "<<<ROOT>>>":
        class_specification = api_dump_by_class_name()[class_specification["Superclass"]]
        ancestry_tree.append(class_specification["Name"])

    return ancestor_name in ancestry_tree


@lru_cache()
def has_property(class_name: str, property_name: str) -> bool:
    class_specification = api_dump_by_class_name()[class_name]
    for member_specification in class_specification["Members"]:
        if member_specification["MemberType"] == "Property" and member_specification["Name"] == property_name:
            return True

    superclass = class_specification["Superclass"]
    if superclass == "<<<ROOT>>>":
        return False

    return has_property(superclass, property_name)
