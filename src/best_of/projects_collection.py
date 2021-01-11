import logging
import math
import re
from collections import OrderedDict
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
from addict import Dict
from tqdm import tqdm

from best_of import default_config, integrations, utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations import github_integration
from best_of.license import get_license

log = logging.getLogger(__name__)

# Official Regex: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_VALIDATION = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def calc_projectrank(project_info: Dict) -> int:
    projectrank = 0

    if project_info.resource:
        return 0

    # Basic info present?
    if project_info.homepage and project_info.description:
        # TODO: check for keywords
        # TODO: check hasX from libio
        projectrank += 1

    # Source repository present?
    if project_info.github_url:
        # For now only check for github
        projectrank += 1

    # TODO: Readme present?

    # License present?
    if project_info.license:
        projectrank += 1
        # Custom addition: Permissive & common license
        project_license_metadata = get_license(project_info.license)
        if (
            project_license_metadata
            and "warning" in project_license_metadata
            and project_license_metadata["warning"] is False
        ):
            projectrank += 1

    # Has multiple versions?
    if project_info.release_count and project_info.release_count > 1:
        projectrank += 1

    # Follows SemVer?
    if project_info.latest_stable_release_number and SEMVER_VALIDATION.match(
        project_info.latest_stable_release_number
    ):
        projectrank += 1

    # Recent release? within 6 month
    if project_info.latest_stable_release_published_at:
        month_since_latest_release = utils.diff_month(
            datetime.now(), project_info.latest_stable_release_published_at
        )
        if month_since_latest_release < 6:
            projectrank += 1

    # Custom addition: Check if repo was updated within the last 3 month
    if project_info.updated_at:
        project_inactive_month = utils.diff_month(
            datetime.now(), project_info.updated_at
        )
        if project_inactive_month < 3:
            projectrank += 1

    # Not brand new?
    if project_info.created_at:
        project_age = utils.diff_month(datetime.now(), project_info.created_at)
        if project_age >= 6:
            projectrank += 1

    # 1.0.0 or greater? - Ignored for now
    # TODO save last version number and last version date

    if project_info.dependent_project_count:
        # TODO: Difference between repos and packages?
        projectrank += round(math.log(project_info.dependent_project_count) / 1.5)

    # Stars  - Logarithmic scale
    if project_info.star_count:
        projectrank += round(math.log(project_info.star_count) / 2)

    # Contributors - Logarithmic scale
    if project_info.contributor_count:
        projectrank += round(math.log(project_info.contributor_count) / 2) - 1

    # Custom addition: Forks - Logarithmic scale
    if project_info.fork_count:
        projectrank += round(math.log(project_info.fork_count) / 2)

    # Custom addition: Monthly downloads - Logarithmic scale
    if project_info.monthly_downloads:
        projectrank += round(math.log(project_info.monthly_downloads) / 2) - 1

    # Custom addition: Commit count - Logarithmic scale
    if project_info.commit_count:
        projectrank += round(math.log(project_info.commit_count) / 2) - 1

    # Minus if issues not activated or repo archived

    # TODO: Closed/Open Issue count, e.g. https://isitmaintained.com/project/ml-tooling/ml-workspace

    # TODO: from github api:
    # isArchived: -1
    # isDisabled: -1
    # hasIssuesEnabled: -1
    # TODO: pullRequests

    return projectrank


def calc_projectrank_placing(projects: list) -> None:
    projectrank_placing: dict = {}
    # Collet all projectranks
    for project in projects:
        project = Dict(project)
        if not project.category or not project.projectrank or project.resource:
            continue

        if project.category not in projectrank_placing:
            projectrank_placing[project.category] = []

        projectrank_placing[project.category].append(int(project.projectrank))

    # Calculate projectrank placing
    for project in projects:
        if "resource" in project and project["resource"]:
            continue

        if "projectrank" not in project or not project["projectrank"]:
            continue

        if "category" not in project or not project["category"]:
            continue

        category = project["category"]
        if category in projectrank_placing:
            placing_1 = np.percentile(
                np.sort(np.array(projectrank_placing[category]))[::-1], 90
            )
            placing_2 = np.percentile(
                np.sort(np.array(projectrank_placing[category]))[::-1], 60
            )

            if project["projectrank"] >= placing_1:
                project["projectrank_placing"] = 1
            elif project["projectrank"] >= placing_2:
                project["projectrank_placing"] = 2
            else:
                project["projectrank_placing"] = 3


def categorize_projects(projects: list, categories: OrderedDict) -> None:
    for project in projects:
        project = Dict(project)

        if not project.name:
            log.info("A project name is required. Ignoring project.")
            continue

        if not project.homepage:
            log.info(
                "A project homepage is required. Ignoring project: " + project.name
            )
            continue

        if project.show:
            if not categories[project.category].projects:
                categories[project.category].projects = []
            categories[project.category].projects.append(project)
        else:
            if not categories[project.category].hidden_projects:
                categories[project.category].hidden_projects = []
            categories[project.category].hidden_projects.append(project)


def update_project_category(project_info: Dict, categories: OrderedDict) -> None:
    if not project_info.category:
        # if category is not provided, put into others category
        project_info.category = default_config.DEFAULT_OTHERS_CATEGORY_ID

    if project_info.category not in categories:
        log.info(
            "Category "
            + project_info.category
            + " is not listed in the categories configuration."
        )
        project_info.category = default_config.DEFAULT_OTHERS_CATEGORY_ID


def get_projects_changes(
    projects: List[Dict], history_file_path: str
) -> Tuple[List[str], Dict]:
    print(history_file_path)
    # get project scores from history file
    projects_history_df = pd.read_csv(history_file_path, sep=",", index_col=0)
    project_scores_history = {}

    for project in projects_history_df.to_dict("records"):
        project_scores_history[project["name"]] = int(project["projectrank"])

    added_projects = []
    trending_projects = {}

    for project in projects:
        if "resource" in project and project["resource"]:
            # Ignore resource projects
            continue

        score_difference = 0
        project_name = project["name"]
        project_score = project["projectrank"]

        if project_name not in project_scores_history:
            added_projects.append(project_name)
            continue
        else:
            score_difference = project_score - project_scores_history[project_name]

        if score_difference == 0:
            # did not change
            continue
        trending_projects[project_name] = score_difference
    return added_projects, trending_projects


def apply_projects_changes(
    projects: List[Dict],
    added_projects: List[str],
    trending_projects: Dict,
    max_trends: int = 5,
) -> None:
    trending_up: dict = {}
    for project in sorted(trending_projects.items(), key=lambda x: x[1], reverse=True):
        project_name = project[0]
        project_score = trending_projects[project[0]]
        if project_score < 0:
            break
        if len(trending_up) < max_trends:
            trending_up[project_name] = project_score

    trending_down: dict = {}
    for project in sorted(trending_projects.items(), key=lambda x: x[1], reverse=False):
        project_name = project[0]
        project_score = trending_projects[project[0]]
        if project_score > 0:
            break
        if len(trending_down) < max_trends:
            trending_down[project_name] = project_score

    for project in projects:
        project_name = project["name"]
        if project_name in trending_up:
            project["trending"] = trending_up[project_name]
        elif project_name in trending_down:
            project["trending"] = trending_down[project_name]

        if project_name in added_projects:
            project["new_addition"] = True


def sort_projects(projects: list, configuration: Dict) -> list:
    def sort_project_list(project):  # type: ignore
        project = Dict(project)
        projectrank = 0
        star_count = 0

        if project.projectrank:
            projectrank = int(project.projectrank)

        if project.star_count:
            star_count = int(project.star_count)

        if project.resource:
            # resources should always be on top
            projectrank = 999999999
            star_count = 999999999

        if not configuration.sort_by or configuration.sort_by == "projectrank":
            # this is also the default if nothing is set
            return (projectrank, star_count)
        elif configuration.sort_by == "star_count":
            return (star_count, projectrank)
        return (projectrank, star_count)

    return sorted(projects, key=sort_project_list, reverse=True)


def apply_filters(project_info: Dict, configuration: Dict) -> None:
    project_info.show = True

    # Project should have atleast name, homepage, and an description longer than a few chars
    if not project_info.name:
        log.info("Could not find a valid name" + str(project_info))
        project_info.show = False
        return

    if not project_info.homepage:
        log.info(f"Could not find a valid homepage for {project_info.name}")
        project_info.show = False

    if project_info.resource:
        project_info.show = True
        return

    if (
        not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ):
        log.info(
            f"A project description is required with atleast {MIN_PROJECT_DESC_LENGTH} chars. The project {project_info.name} will be hidden."
        )
        project_info.show = False

    # Do not show if project projectrank less than min_projectrank
    if (
        configuration.min_projectrank
        and project_info.projectrank
        and int(project_info.projectrank) < int(configuration.min_projectrank)
    ):
        project_info.show = False

    # Do not show if project stars less than min_stars
    if (
        configuration.min_stars
        and project_info.star_count
        and int(project_info.star_count) < int(configuration.min_stars)
    ):
        project_info.show = False

    # Check platform requires
    if configuration.require_github and not project_info.github_url:
        log.info(f"{project_info.name} requires github, but no github repo found .")
        project_info.show = False

    # TODO: also support other package managers as requirement
    # if configuration.require_pypi and not project_info.pypi_url:
    #    project_info.show = False

    # Do not show if license was not found
    if not project_info.license and configuration.require_license:
        log.info(f"Unable to detect a licenses for {project_info.name}")
        project_info.show = False

    # Do not show if license is not in allowed_licenses
    if configuration.allowed_licenses and project_info.license:
        project_license = utils.simplify_str(project_info.license)
        project_license_metadata = get_license(project_info.license)
        if project_license_metadata:
            project_license = utils.simplify_str(project_license_metadata["spdx_id"])

        allowed_licenses = [
            utils.simplify_str(license) for license in configuration.allowed_licenses
        ]
        for license in configuration.allowed_licenses:
            license_metadata = get_license(license)
            if license_metadata:
                allowed_licenses.append(utils.simplify_str(license_metadata["spdx_id"]))

        if project_license not in set(allowed_licenses) and "all" not in set(
            allowed_licenses
        ):
            project_info.show = False

    # Do not show if project is dead
    project_inactive_month = None
    if project_info.last_commit_pushed_at:
        project_inactive_month = utils.diff_month(
            datetime.now(), project_info.last_commit_pushed_at
        )
    elif project_info.updated_at:
        project_inactive_month = utils.diff_month(
            datetime.now(), project_info.updated_at
        )

    if (
        project_inactive_month
        and configuration.project_dead_months
        and int(configuration.project_dead_months) < project_inactive_month
    ):
        project_info.show = False


def collect_projects_info(
    projects: list, categories: OrderedDict, config: Dict
) -> list:
    projects_processed = []
    unique_projects = set()
    for project in tqdm(projects):
        project_info = Dict(project)

        if project_info.name.lower() in unique_projects:
            log.info("Project " + project_info.name + " is duplicated.")
            continue
        unique_projects.add(project_info.name.lower())

        github_integration.update_via_github(project_info)

        for package_manager in integrations.AVAILABLE_PACKAGE_MANAGER:
            package_manager.update_project_info(project_info)

        if not project_info.updated_at and project_info.created_at:
            # set update at if created at is available
            project_info.updated_at = project_info.created_at

        # Calculate an improved project rank metric
        adapted_projectrank = calc_projectrank(project_info)
        if (
            not project_info.projectrank
            or project_info.projectrank < adapted_projectrank
        ):
            # Use the rank that is higher
            project_info.projectrank = adapted_projectrank

        # set the show flag for every project, if not shown it will be moved to the More section
        apply_filters(project_info, config)

        # make sure that all defined values (but not category) are guaranteed to be used
        project_info.update(project)

        if project_info.description:
            # Process description
            project_info.description = utils.process_description(
                project_info.description, 120
            )

        # Check and update the project category
        update_project_category(project_info, categories)

        projects_processed.append(project_info.to_dict())

    projects_processed = sort_projects(projects_processed, config)
    calc_projectrank_placing(projects_processed)

    return projects_processed
