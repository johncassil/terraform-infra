#! /usr/bin/python3

from argparse import ArgumentParser
import os
from typing import Tuple


MAIN_CONTENTS = """
resource "RESOURCE_TYPE_HERE" "RESOURCE_NAME_HERE" {
    blah=blippy
}
"""

OUTPUTS_CONTENTS = """
output "SOME_OUTPUT_NAME" {
  value = SOME_RESOURCE_TYPE.SOME_RESOURCE.name
}
"""

VARIABLES_CONTENTS = """
variable "env" {
  type        = string
  description = "The name of the environment associated resources will be deployed in."
}

variable "system" {
  type        = string
  description = "The name of the system"
  default     = "MODULE_REPLACE"
}

variable "stewarded_by" {
  type        = string
  description = "The team that stewards the system"
  default     = "platform-team"
}
"""

LOCALS_CONTENTS = """
locals {
  common_labels = {
    env          = var.env
    system       = var.system
    stewarded-by = var.stewarded_by
  }
  force_destroy_buckets = var.env == "stg" || var.env == "prd" ? false : true
}
"""

TEST_MAIN_CONTENTS = """
provider "google" {
  region = "us-central1"
  project = "dev-sixrs-platform-team"
}

variable "yourname" {
  type = string
  description = "your name, plz"
}

module "MODULE_REPLACE" {
    source = "../"
    env = "dev-${var.yourname}"
    system = "MODULE_REPLACE"
    stewarded_by = "stubby-mcstubbins"
}
"""

FILES_AND_CONTENTS = {
    "test/main.tf": TEST_MAIN_CONTENTS,
    "main.tf": MAIN_CONTENTS,
    "variables.tf": VARIABLES_CONTENTS,
    "locals.tf": LOCALS_CONTENTS,
    "outputs.tf": OUTPUTS_CONTENTS,
}


def create_module(module_name: str) -> None:
    module_directory = module_name
    module_test_directory = f"{module_directory}/test"
    os.mkdir(module_directory)
    os.mkdir(module_test_directory)

    for tf_path, file_contents in FILES_AND_CONTENTS.items():
        module_tf_path = f"{module_name}/{tf_path}"
        replaced_file_contents = file_contents.replace("MODULE_REPLACE", module_name)
        print(f"Creating {module_tf_path}...")
        with open(module_tf_path, "w+") as f:
            f.write(replaced_file_contents)


def create_module_if_nonexistent(module_name: str) -> None:
    if not os.path.exists(module_name):
        print(f"Creating {module_name} tf module...")
        create_module(module_name)
    else:
        print(f"The {module_name} module already exists. Not creating...")


if __name__ == "__main__":
    parser = ArgumentParser(prog="TfModule-ater")
    parser.add_argument(
        "--name",
        "-n",
        dest="name",
        required=True,
        help="The name of the module to create.",
    )
    args = parser.parse_args()
    create_module_if_nonexistent(args.name)
