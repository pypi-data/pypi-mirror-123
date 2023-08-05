import io
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import List, Union, Dict, Tuple

import yaml

from hathor.project.information import roblox_api_dump
from hathor.project.information.source_file import SourceFile
from hathor.project.source_processors.lua_value_encoders import value_encoder, attribute_encoder
from hathor.project.source_processors.source_processor import SourceProcessor, ProcessingResult

IGNORED_PROPERTIES = (
    ["BasePart",
     [
         "Position",
         "Rotation"
     ]],
    ["Attachment",
     [
         "Position",
         "Orientation",
         "WorldPosition",
         "WorldOrientation",
         "WorldSecondaryAxis",
         "Axis",
         "SecondaryAxis"
     ]],
)


@lru_cache()
def is_property_ignored(class_name: str, property_name: str) -> bool:
    for ignored_class_name, ignored_properties in IGNORED_PROPERTIES:
        if roblox_api_dump.is_a(class_name, ignored_class_name):
            return property_name in ignored_properties

    return False


@dataclass
class InstanceRef:
    id: str
    parent: Union[None, str]
    instance: Dict
    children: List = field(default_factory=list)


Refs = Dict[str, InstanceRef]


def build_refs(data_root) -> Refs:
    refs = {}

    for instance in data_root["Instances"]:
        parent = None

        not_creatable = roblox_api_dump.has_tag(instance["ClassName"], "NotCreatable")
        if not_creatable:
            continue

        for name, value in instance["Properties"].items():
            if name == "Parent":
                parent = value

        refs[instance["Id"]] = InstanceRef(
            id=instance["Id"],
            parent=parent,
            instance=instance
        )

    for ref in refs.values():
        if ref.parent:
            refs[ref.parent].children.append(ref)

    return refs


def find_root_ref(refs: Refs) -> InstanceRef:
    root_refs = list(filter(lambda ref: not ref.parent, refs.values()))
    assert len(root_refs) == 1, "The number of root references must be 1"

    return root_refs[0]


class PropertyNotFound(RuntimeError):
    pass


def get_property(instance, property_name: str):
    for name, value in instance["Properties"].items():
        if name == property_name:
            return value

    raise PropertyNotFound(property_name)


LuaNames = Dict[str, str]


def create_lua_names(refs: Refs) -> LuaNames:
    provisional_names = dict()

    for ref in refs.values():
        provisional_names.setdefault(get_property(ref.instance, "Name"), []).append(ref.id)

    lua_names = dict()

    for name, ref_list in provisional_names.items():
        n = len(ref_list)

        for i, ref_id in enumerate(ref_list):
            ref_name = name
            ref_name = re.sub(r"\s", "_", ref_name)

            if name[0].isnumeric():
                ref_name = "_" + name

            if n > 1:
                ref_name = ref_name + str(i)

            lua_names[ref_id] = ref_name

    return lua_names


LinePriorityType = int


class LinePriority:
    normal: LinePriorityType = 0
    properties_closure = 850
    instance_reference: LinePriorityType = 800
    new_line: LinePriorityType = 900


def encode_value(lua_names, value, class_member) -> Tuple[str, LinePriorityType]:
    value_type = class_member["ValueType"]
    type_category = value_type["Category"]

    if type_category == "Enum":
        return value, LinePriority.normal

    elif type_category == "Class":
        return f"instances[\"{lua_names[value]}\"]", LinePriority.instance_reference

    encoder = value_encoder(type_category, value_type["Name"])

    return encoder(value), LinePriority.normal


def encode_attribute(attribute: Dict):
    attribute_type = attribute["Type"]
    attribute_value = attribute["Value"]

    encoder = attribute_encoder(attribute_type)

    return encoder(attribute_value)


@dataclass
class GeneratorSession:
    refs: Refs
    root_ref: InstanceRef
    lua_names: LuaNames
    lua_lines: List[str]
    withheld_lua_lines: List[str]


def generate_instancing_source(session: GeneratorSession):
    ref_stack = [session.root_ref]
    while len(ref_stack) > 0:
        ref = ref_stack.pop(0)
        ref_stack.extend(ref.children)

        lua_name = session.lua_names[ref.id]
        class_name = ref.instance["ClassName"]

        instance_lua_lines: List[Tuple[str, LinePriorityType]] = [
            (f"instances[\"{lua_name}\"] = createInstance(\"{class_name}\", " + "{", LinePriority.normal)
        ]

        for property_name, value in ref.instance["Properties"].items():
            if value is None:
                continue

            if is_property_ignored(class_name, property_name):
                continue

            class_member = roblox_api_dump.query_property(class_name, property_name)
            lua_value, priority = encode_value(session.lua_names, value, class_member)
            line = f"    {property_name} = {lua_value},"

            if priority == LinePriority.instance_reference:
                session.withheld_lua_lines.append(f"instances[\"{lua_name}\"].{property_name} = " + lua_value)

            else:
                instance_lua_lines.append((line, priority))

        last_line_no = len(instance_lua_lines) - 1
        instance_lua_lines[last_line_no] = (
            instance_lua_lines[last_line_no][0].rstrip(","),
            instance_lua_lines[last_line_no][1],
        )

        instance_lua_lines.append(("})", LinePriority.properties_closure))
        instance_lua_lines.append(("", LinePriority.new_line))

        session.lua_lines.extend(list(map(lambda t: t[0], sorted(instance_lua_lines, key=lambda t: t[1]))))


def generate_attributes_source(session: GeneratorSession):
    local_lua_lines = ["""
local function setAttributes(instanceRef, attributes)
    local instance = instances[instanceRef]

    for k, v in pairs(attributes) do
        instance:SetAttribute(k, v)
    end
end
    """]

    did_attribute = 0

    for ref in session.refs.values():
        if "Attributes" in ref.instance:
            attribute_lines = []

            for attribute_name, attribute in ref.instance["Attributes"].items():
                encoded_attribute = encode_attribute(attribute)
                attribute_lines.append(f"    [\"{attribute_name}\"] = {encoded_attribute}")

            template = Template("""setAttributes("$instance_ref", {
$attribute_lines
})
            """)

            local_lua_lines.append(
                template.safe_substitute({
                    "instance_ref": session.lua_names[ref.id],
                    "attribute_lines": ",\n".join(attribute_lines)
                })
            )

            did_attribute += 1

    if did_attribute > 0:
        session.lua_lines.extend(local_lua_lines)


def yaml_instance_to_lua(yaml_source: str) -> str:
    if not yaml_source.strip():
        return "error(\"Could not process instance!\")"

    with io.TextIOWrapper(io.BytesIO(yaml_source.encode())) as fp:
        data_root = yaml.load(fp, Loader=yaml.Loader)

    refs = build_refs(data_root)
    root_ref = find_root_ref(refs)
    lua_names = create_lua_names(refs)
    lua_lines = ["local instances = {}", """
local function createInstance(className, properties)
    local instance = Instance.new(className)

    for k, v in pairs(properties) do
        instance[k] = v
    end

    return instance
end
    """]
    withheld_lua_lines = []

    session = GeneratorSession(
        refs,
        root_ref,
        lua_names,
        lua_lines,
        withheld_lua_lines
    )

    generate_instancing_source(session)
    generate_attributes_source(session)

    lua_lines.extend(withheld_lua_lines)
    lua_lines.append("")
    lua_lines.append(f"return instances[\"{lua_names[root_ref.id]}\"]")

    return "\n".join(lua_lines)


class InstanceYamlProcessor(SourceProcessor):
    @staticmethod
    def extension():
        return "instance.yml"

    @classmethod
    def _is_candidate(cls, path: Path) -> bool:
        return path.name.lower().endswith(f".{cls.extension().lower()}")

    def process(self, source_file: SourceFile) -> ProcessingResult:
        lua_source = yaml_instance_to_lua(source_file.read())

        return ProcessingResult(
            Path(source_file.path + ".lua").name,
            lua_source
        )
