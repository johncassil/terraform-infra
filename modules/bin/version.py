#! /usr/bin/python3

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import date
from subprocess import run


VERSION_FILE = ".VERSION"
CHANGELOG_FILE = ".CHANGELOG"
CHECK = "check"
BUMP = "bump"
TAG = "reftag"
MAJOR = "major"
MINOR = "minor"
PATCH = "patch"


@dataclass
class ModuleVersion:
    major: int
    minor: int
    patch: int

    @property
    def version(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def get_version_from_file(version_file: str) -> ModuleVersion:
    """Parse the local version file and return major/minor/patch via a ModuleVersion dataclass."""
    with open(version_file, "r+") as f:
        contents = f.read()
    split_contents = contents.split(".")
    return ModuleVersion(
        major=int(split_contents[0]),
        minor=int(split_contents[1]),
        patch=int(split_contents[2]),
    )

def get_version_description_from_file(changelog_file):
    """Parse the local changelog file and return last version description."""
    with open(changelog_file, "r+") as f:
        for line in f:
            pass
        last_line = line
    return last_line.split("*")[1].lstrip()

def set_version(version_file: str, module_version: ModuleVersion) -> None:
    """Set a specific version number to the versions file."""
    version_description = input("Please provide a description for this version: ")
    with open(version_file, "w+") as v_file:
        v_file.write(module_version.version)
        with open(CHANGELOG_FILE, "a") as c_file:
            c_file.write(
                f"\n\n[v{module_version.version}] - {date.today().isoformat()}\n    * {version_description}"
            )


def push_reftag(module_version: ModuleVersion, tag_description: str) -> None:
    """Set a git reftag using the locally-defined version."""
    run(["git", "tag", "-a", "-m", f"{tag_description}", f"v{module_version.version}"])
    run(["git", "push", "origin", "--tags"])


def version(cmd, version_type=None):
    module_version = get_version_from_file(VERSION_FILE)
    version_description = get_version_description_from_file(CHANGELOG_FILE)
    if cmd == CHECK:
        if not version_type:
            print(module_version.version)
        elif version_type == MAJOR:
            print(module_version.major)
        elif version_type == MINOR:
            print(module_version.minor)
        elif version_type == PATCH:
            print(module_version.patch)
    elif cmd == BUMP:
        if version_type == MAJOR:
            module_version.major += 1
        elif version_type == MINOR:
            module_version.minor += 1
        else:
            module_version.patch += 1
        set_version(VERSION_FILE, module_version)
    elif cmd == TAG:
        push_reftag(module_version, version_description)


if __name__ == "__main__":
    parser = ArgumentParser(prog="TFModules Versioner")
    parser.add_argument(
        "--command",
        "-c",
        dest="command",
        required=True,
        choices=[CHECK, BUMP, TAG],
        help="The command to run.",
    )
    parser.add_argument(
        "--version_type",
        "-t",
        dest="version_type",
        required=False,
        choices=[MAJOR, MINOR, PATCH],
        help="Which version type to increment or check. Ignored when using the `reftag` command.",
    )
    args = parser.parse_args()
    version(args.command, args.version_type)
