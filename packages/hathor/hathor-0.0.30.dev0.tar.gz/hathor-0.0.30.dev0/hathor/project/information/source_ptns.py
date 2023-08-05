import re

ENTRY_POINT_PTN = re.compile(r"---\s*@entrypoint\s+(\w+)\s+([\w\d.]+)")
REQUIRE_PTN = re.compile(r"require\([\"\']([\w\d\.]+)[\'\"]\)")
QUOTES = "'" + '"'
