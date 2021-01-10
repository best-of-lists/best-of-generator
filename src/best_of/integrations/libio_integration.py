import logging
import os
from urllib.parse import quote, urlparse

from addict import Dict
from dateutil.parser import parse

from best_of.default_config import ENV_LIBRARIES_API_KEY, MIN_PROJECT_DESC_LENGTH

log = logging.getLogger(__name__)


def is_activated() -> bool:
    return os.getenv(ENV_LIBRARIES_API_KEY) is not None


def update_package_via_libio(
    package_manager: str, project_info: Dict, package_info: Dict = None
) -> None:
    if not project_info:
        return

    if not package_info:
        package_id = package_manager + "_id"
        try:
            from pybraries.search import Search

            search = Search()
            package_info = search.project(
                platforms=package_manager, name=quote(project_info[package_id], safe="")
            )

            if not package_info:
                log.info(
                    "Unable to find "
                    + package_manager
                    + " package: "
                    + project_info[package_id]
                )
                return

            package_info = Dict(package_info)
        except Exception as ex:
            log.info(
                "Unable to request "
                + package_manager
                + " info from libraries.io: "
                + project_info[package_id],
                exc_info=ex,
            )
            return

    if not project_info.homepage:
        if package_info.homepage and package_info.homepage.lower() != "unknown":
            project_info.homepage = package_info.homepage
        elif (
            package_info.repository_url
            and package_info.repository_url.lower() != "unknown"
        ):
            project_info.homepage = package_info.repository_url
        elif (
            package_info.package_manager_url
            and package_info.package_manager_url.lower() != "unknown"
        ):
            project_info.homepage = package_info.package_manager_url

    if not project_info.name and package_info.name:
        project_info.name = package_info.name

    if not project_info.github_id and package_info.repository_url:
        if (
            "github" in package_info.repository_url
            and urlparse(package_info.repository_url).path
        ):
            project_info.github_id = urlparse(package_info.repository_url).path.strip(
                "/"
            )
            project_info.github_url = package_info.repository_url

    if not project_info.license and package_info.normalized_licenses:
        if len(package_info.normalized_licenses) > 1:
            log.info("Package " + package_info.name + " has more than one license.")
        # Always take the first license
        project_info.license = package_info.normalized_licenses[0]
        if project_info.license.lower() == "other":
            # if licenses is other, set to None
            project_info.license = None

    if package_info.latest_release_published_at:
        try:
            updated_at = parse(
                str(package_info.latest_release_published_at), ignoretz=True
            )
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at

            # Set package manager specific publish date
            release_key = package_manager + "_latest_release_published_at"
            if (
                release_key not in project_info
                or project_info[release_key] < updated_at
            ):
                # always use the latest available date
                project_info[release_key] = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: "
                + str(package_info.latest_release_published_at),
                exc_info=ex,
            )

    if package_info.versions and len(package_info.versions) > 0:
        try:
            updated_at = parse(
                str(package_info.versions[0].published_at), ignoretz=True
            )
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: "
                + str(package_info.versions[0].published_at),
                exc_info=ex,
            )

    if package_info.latest_stable_release_published_at:
        try:
            latest_stable_release_published_at = parse(
                str(package_info.latest_stable_release_published_at), ignoretz=True
            )
            if (
                not project_info.latest_stable_release_published_at
                or project_info.latest_stable_release_published_at
                < latest_stable_release_published_at
            ):
                # always use the latest available date
                project_info.latest_stable_release_published_at = (
                    latest_stable_release_published_at
                )
                project_info.latest_stable_release_number = str(
                    package_info.latest_stable_release_number
                )
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: "
                + str(package_info.latest_stable_release_published_at),
                exc_info=ex,
            )

    if package_info.versions:
        # Number of released versions
        release_count = int(len(package_info.versions))
        if not project_info.release_count:
            project_info.release_count = release_count
        elif int(project_info.release_count) < release_count:
            # always use the highest number
            project_info.release_count = release_count

    if package_info.stars:
        star_count = int(package_info.stars)
        if not project_info.star_count:
            project_info.star_count = star_count
        elif int(project_info.star_count) < star_count:
            # always use the highest number
            project_info.star_count = star_count

    if package_info.forks:
        fork_count = int(package_info.forks)
        if not project_info.fork_count:
            project_info.fork_count = fork_count
        elif int(project_info.fork_count) < fork_count:
            # always use the highest number
            project_info.fork_count = fork_count

    if package_info.rank and not project_info.resource:
        projectrank = int(package_info.rank)
        if not project_info.projectrank:
            project_info.projectrank = projectrank
        elif int(project_info.projectrank) < projectrank:
            # always use the highest number
            project_info.projectrank = projectrank

    if package_info.dependent_repos_count or package_info.dependents_count:
        dependent_project_count = 0

        if package_info.dependent_repos_count:
            dependent_project_count += int(package_info.dependent_repos_count)

        if package_info.dependents_count:
            dependent_project_count += int(package_info.dependent_repos_count)

        if not project_info.dependent_project_count:
            project_info.dependent_project_count = 0
        project_info.dependent_project_count += dependent_project_count

        # Add for project manager
        project_info[
            package_manager + "_dependent_project_count"
        ] = dependent_project_count

    if (
        not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ) and package_info.description:
        project_info.description = package_info.description


def update_repo_via_libio(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    if "/" not in project_info.github_id:
        log.info("The GitHub project id is not valid: " + project_info.github_id)
        return

    if not is_activated():
        # Libraries.io not activated
        return

    owner = project_info.github_id.split("/")[0]
    repo = project_info.github_id.split("/")[1]

    try:
        from pybraries.search import Search

        search = Search()
        github_info = search.repository(host="github", owner=owner, repo=repo)

        if not github_info:
            log.info(
                "Unable to find GitHub repo via libraries.io: "
                + project_info.github_id
                + ". This might also happen if the repo is quite new, was recently renamed, or has very few stars."
            )
            return

        github_info = Dict(github_info)
    except Exception as ex:
        log.info(
            "Unable to request GitHub repo info from libraries.io: "
            + project_info.github_id,
            exc_info=ex,
        )
        return

    if not project_info.github_url:
        project_info.github_url = "https://github.com/" + project_info.github_id

    if not project_info.homepage:
        project_info.homepage = project_info.github_url

    if (
        not project_info.license
        and github_info.license
        and github_info.license.lower() != "other"
    ):
        # some unknown licenses are returned as other
        project_info.license = github_info.license

    if github_info.created_at:
        try:
            created_at = parse(str(github_info.created_at), ignoretz=True)
            if not project_info.created_at:
                project_info.created_at = created_at
            elif project_info.created_at > created_at:
                # always use the oldest available date
                project_info.created_at = created_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.created_at), exc_info=ex
            )
    # pushed_at is the last github push, updated_at is the last sync?
    if github_info.pushed_at:
        try:
            updated_at = parse(str(github_info.pushed_at), ignoretz=True)
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.pushed_at), exc_info=ex
            )

    if github_info.rank and not project_info.resource:
        projectrank = int(github_info.rank)
        if not project_info.projectrank:
            project_info.projectrank = projectrank
        elif int(project_info.projectrank) < projectrank:
            # always use the highest number
            project_info.projectrank = projectrank

    if github_info.forks_count:
        fork_count = int(github_info.forks_count)
        if not project_info.fork_count:
            project_info.fork_count = fork_count
        elif int(project_info.fork_count) < fork_count:
            # always use the highest number
            project_info.fork_count = fork_count

    if github_info.contributions_count:
        contributor_count = int(github_info.contributions_count)
        if not project_info.contributor_count:
            project_info.contributor_count = contributor_count
        elif int(project_info.contributor_count) < contributor_count:
            # always use the highest number
            project_info.contributor_count = contributor_count

    if github_info.open_issues_count:
        open_issue_count = int(github_info.open_issues_count)
        if not project_info.open_issue_count:
            project_info.open_issue_count = open_issue_count
        elif int(project_info.open_issue_count) < open_issue_count:
            # always use the highest number
            project_info.open_issue_count = open_issue_count

    if github_info.stargazers_count:
        star_count = int(github_info.stargazers_count)
        if not project_info.star_count:
            project_info.star_count = star_count
        elif int(project_info.star_count) < star_count:
            # always use the highest number
            project_info.star_count = star_count

    if (
        not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ) and github_info.description:
        project_info.description = github_info.description
