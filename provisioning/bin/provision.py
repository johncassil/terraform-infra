#! /usr/bin/python3

from argparse import ArgumentParser
import os
from pathlib import Path
from typing import List


GROUP_CHOICES = ["platform-team", "devops-team"]
ENV_CHOICES = ["dev", "stg", "prd"]


MAIN_TEMPLATE_CONTENTS = """terraform {
  backend "gcs" {
    bucket = "platform-team-terraform-state"
    prefix = "GROUP_REPLACE/ENV_REPLACE/SYSTEM_REPLACE/tfstate.json"
  }
}

provider "google" {
  project = "ENV_REPLACE-GROUP_REPLACE"
  region  = "us-central1"
  zone    = "us-central1-b"
}

module "SYSTEM_REPLACE" {
    source          = "git@github.com:johncassil/terraform-infra.git//modules/SYSTEM_REPLACE?ref=1.0.2" # FIXME! Use appropriate version
    env             = "ENV_REPLACE"
    system          = "SYSTEM_REPLACE"
    stewarded_by    = "platform-team"
    # FIXME! Add additional module variables here.
}
"""

OUTPUTS_TEMPLATE_CONTENTS = """output "FIXME_OUTPUT_HERE" {
    value = module.SYSTEM_REPLACE.SOME_OUTPUT_HERE
}
"""

def provision_permutation(group: str, env: str, system: str) -> None:
    print(f"Setting up group={group} env={env} system={system}")
    provision_path = Path(group, env, system)
    provision_path.mkdir(parents=True, exist_ok=True)
    main_file_path = Path(provision_path, "main.tf")
    outputs_file_path = Path(provision_path, "outputs.tf")
    if not main_file_path.exists():
        print(f"{main_file_path} doesn't exist. Creating...")
        with open(main_file_path, "w+") as f:
            # NOTE! Str formatting via .replace() isn't particularly beautiful.
            # Typical str formatting cannot be used since {}, so it's either this or
            # a bunch of escape chars in MAIN_TEMPLATE_CONTENTS.
            contents = MAIN_TEMPLATE_CONTENTS.replace("GROUP_REPLACE", group)
            contents = contents.replace("ENV_REPLACE", env)
            contents = contents.replace("SYSTEM_REPLACE", system)
            f.write(contents)
    else:
        print(f"{main_file_path} already exists. Not creating...")
    if not outputs_file_path.exists():
        print(f"{outputs_file_path} doesn't exist. Creating...")
        with open(outputs_file_path, "w+") as f:
            o_contents = OUTPUTS_TEMPLATE_CONTENTS.replace("SYSTEM_REPLACE", system)
            f.write(o_contents)
    else:
        print(f"{outputs_file_path} already exists. Not creating...")


def provision(groups: List[str], envs: List[str], systems: List[str]) -> None:
    for group in groups:
        for env in envs:
            for system in systems:
                provision_permutation(group, env, system)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--groups",
        "-g",
        dest="groups",
        nargs="+",
        required=True,
        help="The groups in which to provision modules",
        choices=GROUP_CHOICES,
    )
    parser.add_argument(
        "--envs",
        "-e",
        nargs="+",
        required=True,
        help="The envs in which to provision modules",
        choices=ENV_CHOICES,
    )
    parser.add_argument(
        "--systems",
        "-s",
        dest="systems",
        nargs="+",
        required=True,
        help="The terraform modules to provision",
    )
    args = parser.parse_args()
    provision(args.groups, args.envs, args.systems)
