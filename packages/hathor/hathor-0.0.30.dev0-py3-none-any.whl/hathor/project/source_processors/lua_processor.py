from pathlib import Path

from hathor import resources
from hathor.project.information.source_file import SourceFile, module_returns
from hathor.project.information.source_ptns import *
from hathor.project.source_processors.source_processor import SourceProcessor, ProcessingResult


class LuaProcessor(SourceProcessor):
    def process(self, source_file: SourceFile) -> ProcessingResult:
        contents = source_file.read()
        contents = resources.hathor_stub() + "\n" + contents

        processed_lines = []

        for line in contents.splitlines():
            if match := REQUIRE_PTN.search(line):
                proc_line = REQUIRE_PTN.sub(f"__require(\"{match.group(1)}\")", line)
                processed_lines.append(proc_line)

                continue

            processed_lines.append(line)

        if source_file.is_entry_point and not module_returns(processed_lines):
            processed_lines.append("\n")
            processed_lines.append("return true")

        contents = "\n".join(processed_lines)

        return ProcessingResult(
            Path(source_file.path).name,
            contents
        )

    @classmethod
    def _is_candidate(cls, path: Path) -> bool:
        return path.name.lower().endswith(f".{cls.extension().lower()}")

    @staticmethod
    def extension():
        return "lua"
