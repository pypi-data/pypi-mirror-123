import json
from enum import Enum
from typing import List


def stringify_arg_list(arg_list):
    return list(map(str, arg_list))


def roblox_userdata(userdata_name: str, arg_list: List[str]):
    arg_list_str = ", ".join(arg_list)
    return f"{userdata_name}.new({arg_list_str})"


def roblox_userdata_str_args(userdata_name: str, arg_list: List):
    return roblox_userdata(userdata_name, stringify_arg_list(arg_list))


def vector3(arg_list):
    return roblox_userdata_str_args("Vector3", arg_list)


def brick_color(arg_list):
    arg_list_str = ", ".join(stringify_arg_list(arg_list[-3:]))

    return f"BrickColor.new({arg_list_str})"


def c_frame(arg_list):
    return roblox_userdata_str_args("CFrame", arg_list)


def color_3(arg_list):
    return roblox_userdata_str_args("Color3", arg_list)


def string(v):
    v = str(v)

    if "\n" in v:
        return f"[[==[[{str(v)}]]==]]"

    else:
        return f"\"{str(v)}\""


def vector2(arg_list):
    return roblox_userdata_str_args("Vector2", arg_list)


def color_sequence_keypoint(arg_list):
    time = arg_list[0]
    color = color_3(arg_list[1])

    return f"ColorSequenceKeypoint.new({time}, {color})"


def color_sequence(arg_list):
    arg_list = ", ".join(stringify_arg_list(map(color_sequence_keypoint, arg_list)))
    return "ColorSequence.new { " + arg_list + " }"


def number_sequence_keypoint(arg_list):
    return roblox_userdata_str_args("NumberSequenceKeypoint", arg_list)


def number_sequence(arg_list):
    arg_list = ", ".join(stringify_arg_list(map(number_sequence_keypoint, arg_list)))
    return "NumberSequence.new { " + arg_list + " }"


class DataTypeCategory(Enum):
    Primitive = 0
    DataType = 1


ROBLOX_DATA_TYPES = {
    "string": DataTypeCategory.Primitive,
    "boolean": DataTypeCategory.Primitive,
    "bool": DataTypeCategory.Primitive,
    "number": DataTypeCategory.Primitive,
    "UDim2": DataTypeCategory.DataType,
    "UDim": DataTypeCategory.DataType,
    "BrickColor": DataTypeCategory.DataType,
    "Color3": DataTypeCategory.DataType,
    "Vector2": DataTypeCategory.DataType,
    "Vector3": DataTypeCategory.DataType,
    "NumberSequence": DataTypeCategory.DataType,
    "ColorSequence": DataTypeCategory.DataType,
    "NumberRange": DataTypeCategory.DataType,
    "Rect": DataTypeCategory.DataType
}

VALUE_ENCODERS = {
    "Primitive": {
        "bool": lambda v: "true" if v else "false",
        "boolean": lambda v: "true" if v else "false",
        "string": string,
        "number": str
    },
    "DataType": {
        "BrickColor": brick_color,
        "Content": string,
        "ColorSequenceKeypoint": color_sequence_keypoint,
        "ColorSequence": color_sequence,
        "NumberSequenceKeypoint": number_sequence_keypoint,
        "NumberSequence": number_sequence
    }
}


class NoEncoder(RuntimeError):
    def __init__(self, value_type):
        super().__init__(json.dumps(value_type, indent=2))


def value_encoder(category: str, type_name: str):
    try:
        return VALUE_ENCODERS[category][type_name]

    except KeyError:
        if category == "DataType":
            return lambda v: roblox_userdata_str_args(type_name, v)

        elif category == "Primitive":
            return str

        raise NoEncoder({
            "Category": category,
            "Name": type_name
        })


def attribute_encoder(attribute_type: str):
    attribute_type = attribute_type.strip()
    attribute_type_lower = attribute_type.lower()

    for encoders in VALUE_ENCODERS.values():
        for encodes_for, encoder in encoders.items():
            if encodes_for.lower() == attribute_type_lower:
                return encoder

    if attribute_type in ROBLOX_DATA_TYPES:
        roblox_data_category = ROBLOX_DATA_TYPES[attribute_type]

        if roblox_data_category is DataTypeCategory.Primitive:
            return str

        else:
            return lambda v: roblox_userdata_str_args(attribute_type, v)

    raise NoEncoder({
        "Category": "Attribute",
        "AttributeType": attribute_type
    })
