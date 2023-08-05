import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import click
import requests
import yaml
from click_spinner import spinner
from fs.osfs import OSFS

from hathor import resources
from hathor.project import builders


@click.group()
def cli():
    pass


@cli.command()
@click.option('-p', '--profile', default="default")
def build(profile):
    from hathor.project.information.project import find_projects

    projects = find_projects()
    for project in projects:
        project.active_profile = profile

        build_root = project.build_directory.joinpath(project.path_compatible_name)
        if build_root.exists():
            shutil.rmtree(build_root)

        os.makedirs(build_root, exist_ok=True)

        build_profile = project.build_profile()
        builder = builders.get_builder(build_profile.builder)

        builder(project, OSFS(str(build_root.resolve())))


@cli.command()
def init():
    project_file = Path("hathor.project.yml").resolve()

    if project_file.exists():
        if not click.confirm("The project file will be overwritten if you continue, proceed?"):
            return

    def query_builder():
        b = list(builders.BUILDERS.keys())
        builders_list = "\n".join(b)

        msg = f"Which builder would you like to use for this profile?\n" \
              f"The available builders are:\n\n{builders_list}\n"

        choice = "_"
        while choice not in b:
            click.echo(msg)
            choice = click.prompt("? ", builders.DEFAULT_BUILDER)
            if choice not in b:
                click.echo(f"The builder '{choice}' is not a valid choice!")

        return choice

    def query_build_profile(name: str):
        click.echo(f"Configuring build profile '{name}'")

        profile = {
            "directory": click.prompt("Build directory", "./build"),
            "builder": query_builder()
        }

        return profile

    project = {
        "name": click.prompt("Project name"),
        "metadata": {
            "author": click.prompt("Author"),
            "author_email": click.prompt("Author email")
        },
        "build": query_build_profile("default"),
        "serve": {
            "host": "127.0.01",
            "port": 8080,
        },
        "sources": {
            click.prompt("Default source path", "./src"): {
                "enabled": True
            }
        }
    }

    while click.confirm("Add more sources?"):
        project["sources"][click.prompt("Source directory")] = {
            "enabled": True
        }

    while click.confirm("Add another build profile?"):
        profiles = project["build"].get("profiles", {})
        name = click.prompt("What is the name for this new profile?")

        if not name.strip():
            click.echo("That name is invalid, please try again")
            continue

        profiles[name] = query_build_profile(name)

        project["build"]["profiles"] = profiles

    if "profiles" in project["build"]:
        available_profiles = ["default", *project["build"]["profiles"].keys()]

    else:
        available_profiles = ["default"]

    available_profiles = "\n".join(available_profiles)
    click.echo(f"Currently available build profiles:\n{available_profiles}")

    project["serve"]["build_profile"] = \
        click.prompt("Which build profile would you like to use for serving?", "default")

    with project_file.open("w+") as fp:
        yaml.dump(project, fp, yaml.Dumper, sort_keys=False)

    for source_dir in project["sources"].keys():
        if not source_dir.strip():
            continue

        path = Path(source_dir).resolve()
        os.makedirs(path, exist_ok=True)

    gitignore_path = project_file.parent.joinpath(".gitignore")

    if click.confirm("Add a .gitignore file? This uses the gitignore.io service"):
        ignore_categories = [
            "lua",
            "windows",
            "linux",
            "macos",
            "archive"
        ]

        if click.confirm("Add ignores for IntelliJ?"):
            ignore_categories.append("intellij+all")

        if click.confirm("Add ignores for VSCode?"):
            ignore_categories.append("code")

        click.echo("Downloading gitignore")
        query_string = ",".join(ignore_categories)
        with spinner():
            response = requests.get(f"https://www.toptal.com/developers/gitignore/api/{query_string}")
            if response.status_code > 299:
                click.echo("Gitignore download failed, it will not be appended to the file")
                click.echo(f"{response.request.url}\n{response.status_code} {response.reason}:\n{response.text}")
                response = None

        with gitignore_path.open("w+") as fp:
            fp.write(resources.gitignore_base())

            if response is not None:
                fp.write(response.text)

        click.echo("Gitignore written")

    editorconfig_path = project_file.parent.joinpath(".editorconfig")

    if click.confirm("Add a .editorconfig file?"):
        editorconfig = resources.editorconfig_template({
            "charset": click.prompt("Charset", "utf-8"),
            "end_of_line": click.prompt("End of line", "lf"),
            "indent_size": click.prompt("Indent size", "4"),
            "indent_style": click.prompt("Indent style", "tab"),
            "insert_final_newline": "true" if click.confirm("Insert final newline", True) else "false",
            "max_line_length": click.prompt("Maximum line length", "100"),
            "tab_width": click.prompt("Tab width", "4")
        })

        with editorconfig_path.open("w+") as fp:
            fp.write(editorconfig + "\n")

        click.echo("Editorconfig written")


@cli.command()
def serve():
    from hathor import hacks

    hacks.patch_restx()

    from hathor.serve import app
    from hathor.project.information.project import find_projects

    projects = find_projects()
    assert len(projects), f"Only one project can be served at a time, found {len(projects)}"

    app.run(projects[0])


@cli.command()
@click.argument("script_name")
def run(script_name):
    from hathor.project.information.project import find_projects
    scripts = dict()

    projects = find_projects()

    if len(projects) <= 0:
        print("No projects found!", file=sys.stderr)
        return sys.exit(1)

    for project in projects:
        for k, v in project.scripts.items():
            scripts[k] = {
                "project": project,
                "command": v
            }

    try:
        the_script = scripts[script_name.strip()]

    except KeyError:
        print(f"Script {script_name} not found", file=sys.stderr)
        return sys.exit(1)

    print(f"Running script {script_name} in project {the_script['project'].name}")
    os.chdir(the_script["project"].root_directory)

    if lua_version_match := re.search(r"^Lua (\d+)\.(\d+).*", subprocess.check_output(["lua", "-v"]).decode()):
        lua_version_string = f"{lua_version_match.group(1)}.{lua_version_match.group(2)}"

    else:
        print("Could not determine lua version", file=sys.stderr)
        return sys.exit(1)

    luarocks_env = dict()
    for line in subprocess.check_output(["luarocks", "path"]).decode().split("\n"):
        line = line.replace("\r", "").strip()
        if export_match := re.search(r"^export (\w)+='(.+)'", line):
            luarocks_env[export_match.group(1)] = export_match.group(2)

    lua_modules = the_script["project"].root_directory / "lua_modules"
    assert lua_modules.exists() and lua_modules.is_dir()

    luarocks_env["LUA_PATH"] = ";".join([
        str(lua_modules / "share" / "lua" / lua_version_string / "?.lua"),
        str(lua_modules / "share" / "lua" / lua_version_string / "?" / "init.lua"),
        *luarocks_env.get("LUA_PATH", "").split(";")
    ])

    luarocks_env["LUA_CPATH"] = ";".join([
        str(lua_modules / "lib" / "lua" / lua_version_string / "?.so"),
        *luarocks_env.get("LUA_CPATH", "").split(";")
    ])

    luarocks_env["PATH"] = os.pathsep.join([
        str(lua_modules / "bin"),
        *luarocks_env.get("PATH", "").split(os.pathsep),
        *os.environ.get("PATH", "").split(os.pathsep)
    ])

    for k, v in luarocks_env.items():
        os.environ[k] = v

    subprocess.call([
        *re.split(r"\s+", the_script["command"])
    ])


def define_rocks():
    @cli.group()
    def rocks():
        pass

    @rocks.command()
    @click.argument("packages", nargs=-1)
    def install(packages):
        from hathor.project.information.project import find_projects
        from whichcraft import which

        lua_rocks = which("luarocks")
        assert not not lua_rocks, "This command depends on LuaRocks, please install it"

        projects = find_projects()
        if len(projects) <= 0:
            print("No projects found!", file=sys.stderr)
            return sys.exit(1)

        for project in projects:
            lua_modules = project.root_directory.resolve() / "lua_modules"
            lua_modules.mkdir(parents=True, exist_ok=True)

            subprocess.check_call([
                lua_rocks,
                "install", "--tree", str(lua_modules),
                *packages
            ])


define_rocks()

if __name__ == '__main__':
    cli()
