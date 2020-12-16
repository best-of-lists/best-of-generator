import re

import requirements
import yaml
from addict import Dict
from tqdm import tqdm

from best_of.integrations import github_integration, pypi_integration


def extract_github_projects_to_yaml(input_str: str, yaml_output_path: str) -> None:
    # extract github project urls
    projects = []
    for github_match in tqdm(
        re.findall(
            r"(^|[^#])https:\/\/github\.com\/(.*?)(\s|$)", input_str, re.MULTILINE
        )
    ):
        if len(github_match) <= 1:
            continue

        github_id = github_match[1].rstrip("/").strip()
        if not github_id:
            continue

        project = Dict()
        project.github_id = github_id
        github_integration.update_via_github(project)
        projects.append(project)

    output_yaml = []
    for project in projects:
        project_output = {}

        if project.name:
            project_output["name"] = project.name

        if project.github_id:
            if not project.name:
                project_output["name"] = project.github_id.split("/")[1]
            project_output["github_id"] = project.github_id

        output_yaml.append(project_output)

    with open(yaml_output_path, "w") as f:
        yaml.dump(output_yaml, f, default_flow_style=False, sort_keys=False)


def requirements_to_yaml(requirements_path: str, yaml_output_path: str) -> None:
    requirements_projects = []
    with open(requirements_path, "r") as fd:
        for req in tqdm(requirements.parse(fd)):
            project = Dict()
            project.pypi_id = req.name
            pypi_integration.update_via_pypi(project)
            requirements_projects.append(project)

    output_yaml = []
    for project in requirements_projects:
        project_output = {}

        if project.name:
            project_output["name"] = project.name

        if project.pypi_id:
            if not project.name:
                project_output["name"] = project.pypi_id
            project_output["pypi_id"] = project.pypi_id

        if project.github_id:
            project_output["github_id"] = project.github_id

        output_yaml.append(project_output)

    # define a custom representer for strings
    # def quoted_presenter(dumper, data):
    #    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

    # yaml.add_representer(str, quoted_presenter)

    with open(yaml_output_path, "w") as f:
        yaml.dump(output_yaml, f, default_flow_style=False, sort_keys=False)
