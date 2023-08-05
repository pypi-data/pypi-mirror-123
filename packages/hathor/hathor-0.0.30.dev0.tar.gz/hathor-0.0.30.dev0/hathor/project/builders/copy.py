import os

from fs.base import FS

from hathor.project.information.project import Project


def build_copy(project: Project, build_root: FS):
    build_root.makedirs("/", recreate=True)

    for source_file in project.source_files:
        build_root.makedirs(os.path.dirname(source_file.path), recreate=True)

        with build_root.open(source_file.path, "w+") as fp:
            fp.write(source_file.read())
