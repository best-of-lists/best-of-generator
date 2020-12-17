import glob
import logging
import os
from collections import OrderedDict
from datetime import datetime
from typing import Tuple

import pandas as pd
import yaml
from addict import Dict

from best_of.integrations import libio_integration

log = logging.getLogger(__name__)


def parse_projects_yaml(
    projects_yaml_path: str,
) -> Tuple[Dict, list, OrderedDict, list]:
    from best_of import projects_collection

    parsed_yaml = {}

    # https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html
    # https://github.com/Animosity/CraftIRC/wiki/Complete-idiot%27s-introduction-to-yaml

    if not os.path.exists(projects_yaml_path):
        raise Exception(
            "Projects yaml file does not exist: " + os.path.abspath(projects_yaml_path)
        )
    with open(projects_yaml_path, "r") as stream:
        parsed_yaml = yaml.safe_load(stream)

    projects = parsed_yaml["projects"]

    config = projects_collection.prepare_configuration(
        parsed_yaml["configuration"] if "configuration" in parsed_yaml else {}
    )

    categories = projects_collection.prepare_categories(
        parsed_yaml["categories"] if "categories" in parsed_yaml else []
    )

    labels = parsed_yaml["labels"] if "labels" in parsed_yaml else []

    return config, projects, categories, labels


def generate_markdown(
    projects_yaml_path: str, libraries_api_key: str = None, github_api_key: str = None
) -> None:
    try:
        # Set libraries api key
        if libraries_api_key:
            os.environ[libio_integration.ENV_LIBRARIES_API_KEY] = libraries_api_key
        else:
            log.warning(
                "No Libraries.io API key provided. "
                "We recommend to activate the libraries.io integration by providing a valid API key from https://libraries.io/api"
            )

        if github_api_key:
            os.environ["GITHUB_API_KEY"] = github_api_key
        else:
            log.warning(
                "No Github API key provided. We recommend to activate the Github integration by providing a valid API key from https://github.com/settings/tokens"
            )

        # Needs to be imported without setting environment variable
        from best_of import md_generation, projects_collection

        config, projects, categories, labels = parse_projects_yaml(projects_yaml_path)

        projects = projects_collection.collect_projects_info(
            projects, categories, config
        )

        LATEST_CHANGES_FILE = "latest_changes.md"

        if config.projects_history_folder:
            # generate trending information from most recent

            history_files = glob.glob(
                os.path.join(config.projects_history_folder, "*_projects.csv")
            )

            if history_files:
                (
                    added_projects,
                    trending_projects,
                ) = projects_collection.get_projects_changes(
                    projects, sorted(history_files, reverse=True)[1]
                )

                projects_collection.apply_projects_changes(
                    projects, added_projects, trending_projects
                )

                changes_md = md_generation.generate_changes_md(projects, config, labels)
                changes_md_file_name = (
                    datetime.today().strftime("%Y-%m-%d") + "_changes.md"
                )

                # write to history file
                with open(
                    os.path.join(config.projects_history_folder, changes_md_file_name),
                    "w",
                ) as f:
                    f.write(changes_md)

                # write to working directory
                with open(LATEST_CHANGES_FILE, "w") as f:
                    f.write(changes_md)

        projects_collection.categorize_projects(projects, categories)

        if config.projects_history_folder:
            # Save projects collection to history folder
            os.makedirs(config.projects_history_folder, exist_ok=True)
            projects_file_name = datetime.today().strftime("%Y-%m-%d") + "_projects.csv"
            projects_history_file = os.path.join(
                config.projects_history_folder, projects_file_name
            )
            pd.DataFrame(projects).to_csv(projects_history_file, sep=",")

            # Load most recent

        markdown = md_generation.generate_md(categories, config, labels)

        # Write markdown to file
        if not config.output_markdown_file:
            # Default output markdown file
            config.output_markdown_file = "README.md"

        if not os.path.exists(LATEST_CHANGES_FILE):
            with open(LATEST_CHANGES_FILE, "w") as f:
                f.write("Nothing changed from last update.")

        with open(config.output_markdown_file, "w") as f:
            f.write(markdown)
    except Exception as ex:
        log.error("Failed to generate markdown.", exc_info=ex)
