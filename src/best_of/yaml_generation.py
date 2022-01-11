import copy
import logging
import os
import re
import urllib.request
from typing import List, Optional, Union

import requests
import requirements
from addict import Dict
from tqdm import tqdm

from best_of import projects_collection, utils
from best_of.integrations import (
    conda_integration,
    github_integration,
    npm_integration,
    pypi_integration,
)

log = logging.getLogger(__name__)


def get_projects_from_org(organization: str, min_stars: int = 30) -> List[str]:
    query = """
query($organization: String!) {
      organization(login: $organization) {
        repositories(first: 100) {
          nodes {
            nameWithOwner
            stargazerCount
          }
        }
      }
 }
    """

    headers = {"Authorization": "token " + os.environ["GITHUB_API_KEY"]}
    variables = {"organization": organization}

    try:
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if response.status_code != 200:
            print(
                "Unable to find GitHub org via GitHub api: "
                + organization
                + " ("
                + str(response.status_code)
                + ")"
            )
            return []
        response_data = response.json()
        if "data" not in response_data:
            print(f"Failed to get Github org data for {organization}", response_data)
            return []
        github_org_info = Dict(response_data["data"]["organization"])
    except Exception as ex:
        log.info(
            "Failed to request GitHub org via GitHub api: " + organization,
            exc_info=ex,
        )
        return []

    return [
        repo.nameWithOwner
        for repo in github_org_info.repositories.nodes
        if repo.stargazerCount > min_stars
    ]


def collect_github_projects(
    repos: List[str],
    excluded_github_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None,
    group: Optional[str] = None,
) -> list:

    projects: List = []

    if not excluded_github_ids:
        excluded_github_ids = []

    if existing_projects:
        # Add projects to the overall project list
        projects.extend(existing_projects)
        for project in existing_projects:
            if "github_id" in project and project["github_id"]:
                # ignore all based on github_id
                excluded_github_ids.append(project["github_id"])

    excluded_projects = set()
    added_projects = set()

    if excluded_github_ids:
        for excluded_project in excluded_github_ids:
            excluded_projects.add(utils.simplify_str(excluded_project))

    # extract github project urls
    for github_id in tqdm(repos):
        if utils.simplify_str(github_id) in added_projects:
            # project already added
            continue

        if utils.simplify_str(github_id) in excluded_projects:
            # skip excluded projects
            continue

        project = Dict()
        project.github_id = github_id
        github_integration.update_via_github(project)

        if not project.github_url or not project.name:
            # did not fetch any data from github, do not add project
            continue

        if project.updated_github_id:
            if utils.simplify_str(project.updated_github_id) in excluded_projects:
                # project is added with updated id
                continue

            # Apply updated github id:
            project.github_id = project.updated_github_id
            added_projects.add(utils.simplify_str(project.updated_github_id))

        project.projectrank = projects_collection.calc_projectrank(project)
        if group:
            project.group_id = group
        added_projects.add(utils.simplify_str(github_id))
        projects.append(project.to_dict())

    return projects


def extract_github_projects(
    input: Union[str, List[str]],
    excluded_github_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None,
) -> list:

    projects: List = []

    if not excluded_github_ids:
        excluded_github_ids = []

    if existing_projects:
        # Add projects to the overall project list
        projects.extend(existing_projects)
        for project in existing_projects:
            if "github_id" in project and project["github_id"]:
                # ignore all based on github_id
                excluded_github_ids.append(project["github_id"])

    # If input is a list, iterate instead and combine all input lists
    if not isinstance(input, str):
        for input_str in input:
            extracted_projects = extract_github_projects(input_str, excluded_github_ids)
            projects.extend(extracted_projects)
            for project in extracted_projects:
                if (
                    "github_id" in project
                    and project["github_id"] not in excluded_github_ids
                ):
                    excluded_github_ids.append(project["github_id"])
                else:
                    print("No github id found.")
        return projects

    excluded_projects = set()
    added_projects = set()

    if excluded_github_ids:
        for excluded_project in excluded_github_ids:
            excluded_projects.add(utils.simplify_str(excluded_project))

    input_str = input
    if os.path.isfile(input):
        # If input is a valid file path, read as file
        with open(input, "r") as f:
            input_str = f.read()
    elif utils.is_valid_url(input):
        # if input is a valid url, open and read from url
        filedata = urllib.request.urlopen(input)
        input_str = filedata.read().decode("utf-8")

    # extract github project urls
    for github_match in tqdm(
        re.findall(
            r"(^|[^#])https:\/\/github\.com\/([a-zA-Z0-9-_.]*\/[a-zA-Z0-9-_.]*)",
            input_str,
            re.MULTILINE,
        )
    ):
        if len(github_match) <= 1:
            continue

        github_id = github_match[1].strip().rstrip("/").rstrip(".")
        if not github_id:
            continue

        if utils.simplify_str(github_id) in added_projects:
            # project already added
            continue

        if utils.simplify_str(github_id) in excluded_projects:
            # skip excluded projects
            continue

        project = Dict()
        project.github_id = github_id
        github_integration.update_via_github(project)

        if not project.github_url or not project.name:
            # did not fetch any data from github, do not add project
            continue

        if project.updated_github_id:
            if utils.simplify_str(project.updated_github_id) in excluded_projects:
                # project is added with updated id
                continue

            # Apply updated github id:
            project.github_id = project.updated_github_id
            added_projects.add(utils.simplify_str(project.updated_github_id))

        project.projectrank = projects_collection.calc_projectrank(project)

        added_projects.add(utils.simplify_str(github_id))
        projects.append(project.to_dict())

    return projects


def extract_pypi_projects(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None,
) -> list:
    projects: List = []

    if not excluded_pypi_ids:
        excluded_pypi_ids = []

    if existing_projects:
        # Add projects to the overall project list
        projects.extend(existing_projects)
        for project in existing_projects:
            if "pypi_id" in project and project["pypi_id"]:
                # ignore all based on pypi_id
                excluded_pypi_ids.append(project["pypi_id"])

    # If input is a list, iterate instead and combine all input lists
    if not isinstance(input, str):
        for input_str in input:
            extracted_projects = extract_pypi_projects(input_str, excluded_pypi_ids)
            projects.extend(extracted_projects)
            for project in extracted_projects:
                if "pypi_id" in project and project["pypi_id"] not in excluded_pypi_ids:
                    excluded_pypi_ids.append(project["pypi_id"])
                else:
                    print("No pypi_id found.")
        return projects

    excluded_projects = set()
    added_projects = set()

    if excluded_pypi_ids:
        for excluded_project in excluded_pypi_ids:
            excluded_projects.add(utils.simplify_str(excluded_project))

    input_str = input
    if os.path.isfile(input):
        # If input is a valid file path, read as file
        with open(input, "r") as f:
            input_str = f.read()
    elif utils.is_valid_url(input):
        # if input is a valid url, open and read from url
        filedata = urllib.request.urlopen(input)
        input_str = filedata.read().decode("utf-8")

    # extract pypi project urls
    for pypi_match in tqdm(
        re.findall(
            r"(^|[^#])https:\/\/pypi\.org\/project\/([a-zA-Z0-9-_.]*)",
            input_str,
            re.MULTILINE,
        )
    ):
        if len(pypi_match) <= 1:
            continue

        pypi_id = pypi_match[1].strip().rstrip("/").rstrip(".")
        if not pypi_id:
            continue

        if utils.simplify_str(pypi_id) in added_projects:
            # project already added
            continue

        if utils.simplify_str(pypi_id) in excluded_projects:
            # skip excluded projects
            continue

        project = Dict()
        project.pypi_id = pypi_id
        pypi_integration.PypiIntegration().update_project_info(project)
        if not project.monthly_downloads:
            # did not fetch any data from github, do not add project
            continue

        if project.github_id:
            # Update metadata again via twitter
            github_integration.update_via_github(project)
            if project.updated_github_id:
                project.github_id = project.updated_github_id

        project.projectrank = projects_collection.calc_projectrank(project)
        added_projects.add(utils.simplify_str(pypi_id))
        projects.append(project.to_dict())

    return projects


def extract_pypi_projects_from_requirements(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None,
) -> list:
    projects = []
    # libraries.io should be configured

    if not excluded_pypi_ids:
        excluded_pypi_ids = []

    if existing_projects:
        # Add projects to the overall project list
        projects.extend(existing_projects)
        for project in existing_projects:
            if "pypi_id" in project and project["pypi_id"]:
                # ignore all based on pypi_id
                excluded_pypi_ids.append(project["pypi_id"])

    # If input is a list, iterate instead and combine all input lists
    if not isinstance(input, str):
        for input_str in input:
            extracted_projects = extract_pypi_projects_from_requirements(
                input_str, excluded_pypi_ids
            )
            projects.extend(extracted_projects)
            for project in extracted_projects:
                if "pypi_id" in project and project["pypi_id"] not in excluded_pypi_ids:
                    excluded_pypi_ids.append(project["pypi_id"])
                else:
                    print("No pypi_id found.")
        return projects

    excluded_projects = set()
    added_projects = set()

    if excluded_pypi_ids:
        for excluded_project in excluded_pypi_ids:
            excluded_projects.add(utils.simplify_str(excluded_project))

    input_str = input
    if os.path.isfile(input):
        # If input is a valid file path, read as file
        with open(input, "r") as f:
            input_str = f.read()
    elif utils.is_valid_url(input):
        # if input is a valid url, open and read from url
        filedata = urllib.request.urlopen(input)
        input_str = filedata.read().decode("utf-8")

    for req in tqdm(requirements.parse(input_str)):
        pypi_id = req.name.strip().lower()

        if utils.simplify_str(pypi_id) in added_projects:
            # project already added
            continue

        if utils.simplify_str(pypi_id) in excluded_projects:
            # skip excluded projects
            continue

        project = Dict()
        project.pypi_id = pypi_id
        pypi_integration.PypiIntegration().update_project_info(project)

        if not project.monthly_downloads:
            # did not fetch any data from github, do not add project
            continue

        if project.github_id:
            # Update metadata again via twitter
            github_integration.update_via_github(project)
            if project.updated_github_id:
                project.github_id = project.updated_github_id

        project.projectrank = projects_collection.calc_projectrank(project)
        added_projects.add(utils.simplify_str(pypi_id))
        projects.append(project.to_dict())

    return projects


def auto_extend_via_libio(
    projects: list, selected_package_manager: Optional[List[str]] = None
) -> list:
    from pybraries.search import Search

    updated_projects = []
    for project in tqdm(projects):
        project = copy.deepcopy(project)
        if "github_id" in project:
            search = Search()
            related_projects = search.repository_projects(
                host="github",
                owner=project["github_id"].split("/")[0],
                repo=project["github_id"].split("/")[1],
            )
            selected_platform_dep_rank: dict = {}
            if related_projects is not None:
                for related_project in related_projects:
                    platform = related_project["platform"].lower()
                    if platform in selected_platform_dep_rank and (
                        selected_platform_dep_rank[platform] >= related_project["rank"]
                    ):
                        # Project with same platform and higher rank already added
                        continue

                    project_id = None
                    id_property = None

                    if (
                        selected_package_manager
                        and platform not in selected_package_manager
                    ):
                        # Skip project
                        print(f"Platform {platform} is not selected -> Ignore.")
                        continue

                    if platform == "pypi":
                        id_property = "pypi_id"
                        project_id = related_project["name"]
                    elif platform == "npm":
                        id_property = "npm_id"
                        project_id = related_project["name"]
                    elif platform == "maven":
                        id_property = "maven_id"
                        project_id = related_project["name"]
                    elif platform == "conda":
                        id_property = "conda_id"
                        project_id = related_project["package_manager_url"].replace(
                            "https://anaconda.org/", ""
                        )
                    elif platform == "go":
                        id_property = "go_id"
                        project_id = related_project["name"]
                    elif platform == "cargo":
                        id_property = "cargo_id"
                        project_id = related_project["name"]
                    elif platform == "nuget":
                        # TODO: not supported yet
                        id_property = "nuget_id"
                        project_id = related_project["name"]
                    elif platform == "homebrew":
                        # TODO: not supported yet
                        id_property = "brew_id"
                        project_id = related_project["name"]
                    else:
                        print(f"Platform {platform} not supported")
                        continue

                    if not project_id or not id_property:
                        print(f"Platform {platform} not supported")
                        continue

                    if (
                        platform not in selected_platform_dep_rank
                        and id_property in project
                    ):
                        # dependency already added manually
                        continue

                    # TODO: Perform download check: min 50 downloads

                    project[id_property] = project_id
                    selected_platform_dep_rank[platform] = related_project["rank"]
            else:
                print("Failed to get projects for " + project["github_id"])

            updated_projects.append(project)
    return updated_projects


def auto_extend_package_manager(
    projects: list, pypi: bool = False, conda: bool = False, npm: bool = False
) -> list:
    updated_projects = []
    for project in tqdm(projects):
        project = Dict(project)
        project_name = ""
        if not project.name:
            if project.pypi_id:
                # fallback: use pypi_id as name
                project.name = project.pypi_id
            else:
                # skip project
                continue

        project_name = project.name.lower().strip().replace(" ", "-")

        if pypi and not project.pypi_id:
            project_cloned = copy.deepcopy(project)
            project_cloned.pypi_id = project_name
            pypi_integration.PypiIntegration().update_project_info(project_cloned)
            if (
                project_cloned.pypi_monthly_downloads
                and project_cloned.pypi_monthly_downloads > 250
            ):
                # only use this package if monthly downloads over X -> to prevent errors
                log.info(
                    f"Detected pypi package: {project_cloned.pypi_id} for project {project_cloned.name}."
                )
                project = project_cloned

        if conda and not project.conda_id:
            project_cloned = copy.deepcopy(project)
            project_cloned.conda_id = "conda-forge/" + project_name
            conda_integration.CondaIntegration().update_project_info(project_cloned)
            if (
                project_cloned.conda_total_downloads
                and project_cloned.conda_total_downloads > 2500
            ):
                # only use this package if total downloads over X -> to prevent errors
                log.info(
                    f"Detected conda package: {project_cloned.conda_id} for project {project_cloned.name}."
                )
                project = project_cloned
            elif not project_cloned.conda_total_downloads and project.pypi_id:
                # Try again with pypi_id
                project_cloned.conda_id = "conda-forge/" + project.pypi_id
                conda_integration.CondaIntegration().update_project_info(project_cloned)
                if (
                    project_cloned.conda_total_downloads
                    and project_cloned.conda_total_downloads > 2500
                ):
                    # only use this package if total downloads over X -> to prevent errors
                    log.info(
                        f"Detected conda package: {project_cloned.conda_id} for project {project_cloned.name}."
                    )
                    project = project_cloned
        if npm and not project.npm_id:
            project_cloned = copy.deepcopy(project)

            project_cloned.npm_id = project_name
            npm_integration.NpmIntegration().update_project_info(project_cloned)
            if (
                project_cloned.npm_monthly_downloads
                and project_cloned.npm_monthly_downloads > 500
            ):
                # only use this package if monthly downloads over X -> to prevent errors
                log.info(
                    f"Detected npm package: {project_cloned.npm_id} for project {project_cloned.name}."
                )
                project = project_cloned
        # recalculated projectrank
        project.projectrank = projects_collection.calc_projectrank(project)
        updated_projects.append(project)
    return [project.to_dict() for project in updated_projects]
