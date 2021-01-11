import glob
import logging
import os
from collections import OrderedDict
from datetime import datetime
from typing import Tuple

import pandas as pd
import yaml
from addict import Dict

from best_of import default_config

log = logging.getLogger(__name__)


def parse_projects_yaml(
    projects_yaml_path: str,
) -> Tuple[Dict, list, OrderedDict, list]:

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

    if not projects:
        projects = []

    config = default_config.prepare_configuration(
        parsed_yaml["configuration"] if "configuration" in parsed_yaml else {}
    )

    if not config:
        config = {}

    categories = default_config.prepare_categories(
        parsed_yaml["categories"] if "categories" in parsed_yaml else []
    )

    if not categories:
        categories = OrderedDict()

    labels = parsed_yaml["labels"] if "labels" in parsed_yaml else []

    if not labels:
        labels = []

    return config, projects, categories, labels


def load_extension_script(extension_script_path: str) -> None:
    if not os.path.exists(extension_script_path):
        log.warn("Extension script does not exist " + extension_script_path)
        return

    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "module.name", extension_script_path
        )
        loaded_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded_module)  # type: ignore
    except Exception as ex:
        log.warn(
            "Failed to load extension script: " + extension_script_path, exc_info=ex
        )


def generate_markdown(
    projects_yaml_path: str, libraries_api_key: str = None, github_api_key: str = None
) -> None:
    try:
        # Set libraries api key
        if libraries_api_key:
            os.environ[default_config.ENV_LIBRARIES_API_KEY] = libraries_api_key
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

        config, projects, categories, labels = parse_projects_yaml(projects_yaml_path)

        if config.extension_script:
            load_extension_script(config.extension_script)

        # Needs to be imported without setting environment variable
        from best_of import projects_collection

        projects = projects_collection.collect_projects_info(
            projects, categories, config
        )

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
                    projects, sorted(history_files, reverse=True)[0]
                )

                projects_collection.apply_projects_changes(
                    projects,
                    added_projects,
                    trending_projects,
                    max_trends=config.max_trending_projects,
                )

        projects_collection.categorize_projects(projects, categories)

        if config.projects_history_folder:
            # Save projects collection to history folder
            os.makedirs(config.projects_history_folder, exist_ok=True)
            projects_file_name = datetime.today().strftime("%Y-%m-%d") + "_projects.csv"
            projects_history_file = os.path.join(
                config.projects_history_folder, projects_file_name
            )
            pd.DataFrame(projects).to_csv(projects_history_file, sep=",")

        from best_of.generators import get_generator

        output_generator = get_generator(config.output_generator)
        if not output_generator:
            log.error("No output generator registered for " + config.output_generator)
            return

        output_generator.write_output(categories, projects, config, labels)
    except Exception as ex:
        log.error("Failed to generate markdown.", exc_info=ex)
