import json
import logging
import math
import os
import re
from collections import OrderedDict
from datetime import datetime
from typing import Optional
from urllib.parse import quote, urlparse

import numpy as np
import pypistats
import requests
from addict import Dict
from bs4 import BeautifulSoup
from dateutil.parser import parse
from tqdm import tqdm

from best_of import utils
from best_of.license import get_license

log = logging.getLogger(__name__)

MIN_PROJECT_DESC_LENGTH = 10
DEFAULT_OTHERS_CATEGORY_ID = "others"
# Official Regex: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_VALIDATION = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def update_package_via_libio(
    project_info: Dict, package_info: Dict, package_manager: str
) -> None:
    if not project_info or not package_info:
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
            updated_at = parse(str(package_info.latest_release_published_at))
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
            updated_at = parse(str(package_info.versions[0].published_at))
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
                str(package_info.latest_stable_release_published_at)
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

    if package_info.rank:
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


def update_via_conda(project_info: Dict) -> None:
    if not project_info.conda_id:
        return

    if "/" in project_info.conda_id:
        # Package from different conda channel (not anaconda)
        # Cannot be requested by libraries.io
        project_info.conda_url = "https://anaconda.org/" + project_info.conda_id
        return

    from pybraries.search import Search

    search = Search()
    conda_info = search.project(
        platforms="conda", name=quote(project_info.conda_id, safe="")
    )

    if not conda_info:
        return

    conda_info = Dict(conda_info)

    if not project_info.conda_url:
        project_info.conda_url = (
            "https://anaconda.org/anaconda/" + project_info.conda_id
        )

    update_package_via_libio(project_info, conda_info, "conda")


def update_via_npm(project_info: Dict) -> None:
    if not project_info.npm_id:
        return

    from pybraries.search import Search

    search = Search()
    npm_info = search.project(platforms="npm", name=quote(project_info.npm_id, safe=""))

    if not npm_info:
        log.info("Unable to find npm package: " + project_info.npm_id)
        return

    npm_info = Dict(npm_info)

    if not project_info.npm_url:
        project_info.npm_url = "https://www.npmjs.com/package/" + project_info.npm_id

    update_package_via_libio(project_info, npm_info, "npm")

    # Get monthly downloads
    try:
        request = requests.get(
            "https://api.npmjs.org/downloads/point/last-month/"
            + quote(project_info.npm_id, safe="")
        )
        request.text
        if request.status_code != 200:
            log.info(
                "Unable to find package via npm api: "
                + project_info.npm_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return
        npm_download_info = Dict(request.json())
        if npm_download_info.downloads:
            project_info.npm_monthly_downloads = int(npm_download_info.downloads)

            if not project_info.monthly_downloads:
                project_info.monthly_downloads = 0

            project_info.monthly_downloads += project_info.npm_monthly_downloads

    except Exception as ex:
        log.info(
            "Failed to request package via npm api: " + project_info.npm_id, exc_info=ex
        )
        return

    # TODO use npms-api to get additional details:
    # https://api-docs.npms.io/#api-Package-GetMultiPackageInfo


def update_via_dockerhub(project_info: Dict) -> None:
    if not project_info.dockerhub_id:
        return

    if not project_info.dockerhub_url:
        dockerhub_url_id = project_info.dockerhub_id
        if "/" not in dockerhub_url_id:
            # if official image, it needs a _/ appended to the id to be requested via url
            dockerhub_url_id = "_/" + dockerhub_url_id

        project_info.dockerhub_url = "https://hub.docker.com/r/" + dockerhub_url_id

    try:
        dockerhub_url_id = project_info.dockerhub_id
        if "/" not in dockerhub_url_id:
            # if official image, it needs a library/ appended to the id to be requested via url
            dockerhub_url_id = "library/" + dockerhub_url_id

        request = requests.get(
            "https://hub.docker.com/v2/repositories/" + dockerhub_url_id
        )
        if request.status_code != 200:
            log.info(
                "Unable to find image via dockerhub api: "
                + project_info.dockerhub_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return
        dockerhub_info = Dict(request.json())
    except Exception as ex:
        log.info(
            "Failed to request docker image via dockerhub api: "
            + project_info.dockerhub_id,
            exc_info=ex,
        )
        return

    if not dockerhub_info.name:
        # Check if name exist -> if not, request most likely failed
        log.info(
            "Failed to request docker image via dockerhub api: "
            + project_info.dockerhub_id
        )
        return

    if dockerhub_info.last_updated:
        try:
            updated_at = parse(str(dockerhub_info.last_updated))
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at

            project_info.dockerhub_latest_release_published_at = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(project_info.last_updated),
                exc_info=ex,
            )

    if dockerhub_info.star_count:
        project_info.dockerhub_stars = dockerhub_info.star_count
        if not project_info.star_count:
            project_info.star_count = 0
        # Add dockerhub stars to total star count
        project_info.star_count += dockerhub_info.star_count

    if dockerhub_info.pull_count:
        project_info.dockerhub_pulls = int(dockerhub_info.pull_count)
        if project_info.created_at:
            # Add to monthly downloads
            if not project_info.monthly_downloads:
                project_info.monthly_downloads = 0

            # monthly downloads = total downloads to total month
            project_info.monthly_downloads += int(
                project_info.dockerhub_pulls
                / max(1, int(utils.diff_month(datetime.now(), project_info.created_at)))
            )

    if (
        not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ) and dockerhub_info.description:
        project_info.description = dockerhub_info.description


def update_via_pypi(project_info: Dict) -> None:
    if not project_info.pypi_id:
        return

    from pybraries.search import Search

    search = Search()
    pypi_info = search.project(
        platforms="pypi", name=quote(project_info.pypi_id, safe="")
    )

    if not pypi_info:
        log.info("Unable to find pypi package: " + project_info.pypi_id)
        return

    pypi_info = Dict(pypi_info)

    if not project_info.pypi_url:
        project_info.pypi_url = "https://pypi.org/project/" + project_info.pypi_id

    update_package_via_libio(project_info, pypi_info, "pypi")

    try:
        # get download count from pypi stats
        project_info.pypi_monthly_downloads = int(
            json.loads(pypistats.recent(project_info.pypi_id, "month", format="json"))[
                "data"
            ]["last_month"]
        )

        if not project_info.monthly_downloads:
            project_info.monthly_downloads = 0

        project_info.monthly_downloads += int(project_info.pypi_monthly_downloads)
    except Exception:
        pass


def update_via_maven(project_info: Dict) -> None:
    if not project_info.maven_id:
        return

    from pybraries.search import Search

    search = Search()
    maven_info = search.project(
        platforms="maven", name=quote(project_info.maven_id, safe="")
    )

    if not maven_info:
        log.info("Unable to find maven package: " + project_info.maven_id)
        return

    maven_info = Dict(maven_info)

    if not project_info.maven_url:
        project_info.maven_url = (
            "https://search.maven.org/artifact/"
            + project_info.maven_id.replace(":", "/")
        )

    update_package_via_libio(project_info, maven_info, "maven")


def get_repo_deps_via_github(github_id: str) -> int:
    try:
        request = requests.get(
            "https://github.com/" + github_id + "/network/dependents"
        )
        if request.status_code != 200:
            log.info(
                "Unable to find repo dependets via github api: "
                + github_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return 0
        repo_deps = 0
        soup = BeautifulSoup(request.text, "html.parser")
        repo_deps_str = soup.find(string=re.compile(r"[0-9,]+\s+Repositories"))
        if repo_deps_str:
            count_search = re.search("([0-9,]+)", repo_deps_str, re.IGNORECASE)
            if count_search:
                repo_deps += int(count_search.group(1).replace(",", ""))
        pkg_deps_str = soup.find(string=re.compile(r"[0-9,]+\s+Packages"))
        if pkg_deps_str:
            count_search = re.search("([0-9,]+)", pkg_deps_str, re.IGNORECASE)
            if count_search:
                repo_deps += int(count_search.group(1).replace(",", ""))
        return repo_deps
    except Exception as ex:
        log.info(
            "Unable to find repo dependets via github api: " + github_id, exc_info=ex
        )
        return 0


def get_contributors_via_github_api(
    github_id: str, github_api_token: str
) -> Optional[int]:
    if not github_id or not github_api_token:
        return None

    try:
        request = requests.get(
            "https://api.github.com/repos/"
            + github_id
            + "/contributors?page=1&per_page=1&anon=True",
            headers={"Authorization": "token " + github_api_token},
        )
        if request.status_code != 200:
            log.info(
                "Unable to find repo contributors via github api: "
                + github_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return None

        if "Link" not in request.headers or not request.headers["Link"]:
            return None

        link_header = request.headers["Link"]

        contributor_count = 0
        for found_group in re.findall(r"\?page=([0-9]+)", link_header, re.IGNORECASE):
            if contributor_count < int(found_group):
                contributor_count = int(found_group)
        return contributor_count
    except Exception as ex:
        log.info(
            "Unable to find repo dependets via github api: " + github_id, exc_info=ex
        )
        return None


def update_via_github_api(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    github_api_token = os.getenv("GITHUB_API_KEY")
    if not github_api_token:
        return

    if "/" not in project_info.github_id:
        log.info("The github project id is not valid: " + project_info.github_id)
        return

    owner = project_info.github_id.split("/")[0]
    repo = project_info.github_id.split("/")[1]

    # TODO: parse github dependents: https://github.com/badgen/badgen.net/blob/master/endpoints/github.ts#L406
    # TODO: Github assets download: https://github.com/badgen/badgen.net/blob/master/endpoints/github.ts#L125
    # TODO: latest stable release, PR...

    # GraphQL query
    # https://github.com/badgen/badgen.net/blob/master/endpoints/github.ts#L214
    query = """
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    name
    description
    url
    homepageUrl
    createdAt
    updatedAt
    pushedAt
    diskUsage
    primaryLanguage {
      name
    }
    licenseInfo {
      spdxId
    }
    stargazers {
      totalCount
    }
    pullRequests {
      totalCount
    }
    forks {
      totalCount
    }
    watchers {
      totalCount
    }
    pullRequests {
      totalCount
    }
    masterCommit: defaultBranchRef {
        target {
          ... on Commit {
            committedDate
          }
        }
    }
    repositoryTopics(first: 100) {
      nodes {
        topic {
          name
        }
      }
    }
    openIssues: issues(states: OPEN) {
      totalCount
    }
    closedIssues: issues(states: CLOSED) {
      totalCount
    }
    commits: object(expression:"master") {
      ... on Commit {
        history {
          totalCount
        }
      }
    }
    releases(first: 100, orderBy: {field:CREATED_AT, direction:DESC}) {
      nodes {
        createdAt
        publishedAt
        tagName
        isDraft
        isPrerelease
        releaseAssets(first: 100) {
          nodes {
            downloadCount
          }
        }
      }
    }
  }
}
"""

    headers = {"Authorization": "token " + github_api_token}
    variables = {"owner": owner, "repo": repo}

    try:
        request = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if request.status_code != 200:
            log.info(
                "Unable to find github repo via github api: "
                + project_info.github_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return
        github_info = Dict(request.json()["data"]["repository"])
    except Exception as ex:
        log.info(
            "Failed to request github repo via github api: " + project_info.github_id,
            exc_info=ex,
        )
        return

    if not project_info.github_url and github_info.url:
        project_info.github_url = github_info.url

    if not project_info.homepage:
        project_info.homepage = project_info.github_url

    if (
        not project_info.license
        and github_info.licenseInfo
        and github_info.licenseInfo.spdxId
    ):
        # if licenses is noassertion, then it is not provided
        if github_info.licenseInfo.spdxId.lower() != "noassertion":
            project_info.license = github_info.licenseInfo.spdxId

    if github_info.createdAt:
        try:
            created_at = parse(str(github_info.createdAt))
            if not project_info.created_at:
                project_info.created_at = created_at
            elif project_info.created_at > created_at:
                # always use the oldest available date
                project_info.created_at = created_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.createdAt), exc_info=ex
            )

    # pushed_at is the last github push, updated_at is the last sync?
    if github_info.pushedAt:
        try:
            updated_at = parse(str(github_info.pushedAt))
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.pushedAt), exc_info=ex
            )

    if (
        github_info.masterCommit
        and github_info.masterCommit.target
        and github_info.masterCommit.target.committedDate
    ):
        try:
            last_commit_pushed_at = parse(
                str(github_info.masterCommit.target.committedDate)
            )
            if not project_info.last_commit_pushed_at:
                project_info.last_commit_pushed_at = last_commit_pushed_at
            elif project_info.last_commit_pushed_at < last_commit_pushed_at:
                # always use the latest available date
                project_info.last_commit_pushed_at = last_commit_pushed_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.target.committedDate),
                exc_info=ex,
            )

    if github_info.forks and github_info.forks.totalCount:
        fork_count = int(github_info.forks.totalCount)
        if not project_info.fork_count:
            project_info.fork_count = fork_count
        elif int(project_info.fork_count) < fork_count:
            # always use the highest number
            project_info.fork_count = fork_count

    if github_info.openIssues and github_info.openIssues.totalCount:
        open_issue_count = int(github_info.openIssues.totalCount)
        if not project_info.open_issue_count:
            project_info.open_issue_count = open_issue_count
        elif int(project_info.open_issue_count) < open_issue_count:
            # always use the highest number
            project_info.open_issue_count = open_issue_count

    if github_info.closedIssues and github_info.closedIssues.totalCount:
        closed_issue_count = int(github_info.closedIssues.totalCount)
        if not project_info.closed_issue_count:
            project_info.closed_issue_count = closed_issue_count
        elif int(project_info.closed_issue_count) < closed_issue_count:
            # always use the highest number
            project_info.closed_issue_count = closed_issue_count

    if github_info.stargazers and github_info.stargazers.totalCount:
        star_count = int(github_info.stargazers.totalCount)
        if not project_info.star_count:
            project_info.star_count = star_count
        elif int(project_info.star_count) < star_count:
            # always use the highest number
            project_info.star_count = star_count

    if (
        github_info.commits
        and github_info.commits.history
        and github_info.commits.history.totalCount
    ):
        project_info.commit_count = int(github_info.commits.history.totalCount)

    if github_info.releases and github_info.releases.nodes:
        release_count = 0
        first_release_date = None
        total_downloads = 0
        for release in github_info.releases.nodes:
            try:
                release_count += 1
                is_stable = True
                if release.isDraft or release.isPrerelease:
                    is_stable = False

                if release.publishedAt:
                    release_date = parse(str(release.publishedAt))
                    if not first_release_date:
                        first_release_date = release_date
                    if first_release_date > release_date:
                        first_release_date = release_date

                    if is_stable and release.tagName:
                        if (
                            not project_info.latest_stable_release_published_at
                            or project_info.latest_stable_release_published_at
                            < release_date
                        ):
                            project_info.latest_stable_release_published_at = (
                                release_date
                            )
                            version = str(release.tagName)
                            if version.startswith("v"):
                                # TODO also replace next letter if not a number?
                                version = version.replace("v", "").strip()
                            project_info.latest_stable_release_number = version

                if release.releaseAssets and release.releaseAssets.nodes:
                    for release_artifact in release.releaseAssets.nodes:
                        if release_artifact.downloadCount:
                            total_downloads += int(release_artifact.downloadCount)
            except Exception as ex:
                log.warning("Failed to parse github release info.", exc_info=ex)

        if total_downloads:
            project_info.github_release_downloads = total_downloads

            # Add to monthly downloads
            if not project_info.monthly_downloads:
                project_info.monthly_downloads = 0

            if first_release_date:
                # monthly downloads = total downloads to total month
                project_info.monthly_downloads += int(
                    total_downloads
                    / max(1, int(utils.diff_month(datetime.now(), first_release_date)))
                )

        if release_count:
            if not project_info.release_count:
                project_info.release_count = release_count
            elif int(project_info.release_count) < release_count:
                # always use the highest number
                project_info.release_count = release_count

    if (
        not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ) and github_info.description:
        project_info.description = github_info.description

    # Get dependets count
    dependent_project_count = get_repo_deps_via_github(project_info.github_id)
    if dependent_project_count:
        if not project_info.dependent_project_count:
            project_info.dependent_project_count = 0

        # TODO: really add this or use the highest dependents count
        project_info.dependent_project_count += dependent_project_count
        project_info.github_dependent_project_count = dependent_project_count

    # Get contributor count via github api 3
    contributor_count = get_contributors_via_github_api(
        project_info.github_id, github_api_token
    )
    if contributor_count:
        if not project_info.contributor_count:
            project_info.contributor_count = contributor_count
        elif int(project_info.contributor_count) < contributor_count:
            # always use the highest number
            project_info.contributor_count = contributor_count


def update_repo_via_libio(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    if "/" not in project_info.github_id:
        log.info("The github project id is not valid: " + project_info.github_id)
        return

    owner = project_info.github_id.split("/")[0]
    repo = project_info.github_id.split("/")[1]

    from pybraries.search import Search

    search = Search()
    github_info = search.repository(host="github", owner=owner, repo=repo)

    if not github_info:
        log.info(
            "Unable to find github repo via libraries.io: " + project_info.github_id
        )
        return

    github_info = Dict(github_info)

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
            created_at = parse(str(github_info.created_at))
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
            updated_at = parse(str(github_info.pushed_at))
            if not project_info.updated_at:
                project_info.updated_at = updated_at
            elif project_info.updated_at < updated_at:
                # always use the latest available date
                project_info.updated_at = updated_at
        except Exception as ex:
            log.warning(
                "Failed to parse timestamp: " + str(github_info.pushed_at), exc_info=ex
            )

    if github_info.rank:
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


def update_via_github(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    update_via_github_api(project_info)
    update_repo_via_libio(project_info)


def calc_projectrank(project_info: Dict) -> int:
    projectrank = 0

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
        if not project.category or not project.projectrank:
            continue

        if project.category not in projectrank_placing:
            projectrank_placing[project.category] = []

        projectrank_placing[project.category].append(int(project.projectrank))

    # Calculate projectrank placing
    for project in projects:
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
        if (
            not project.description
            or len(project.description) < MIN_PROJECT_DESC_LENGTH
        ):
            # project desc should also be longer than 10 chars
            log.info(
                "A project description is required with atleast "
                + str(MIN_PROJECT_DESC_LENGTH)
                + " chars. Ignoring project: "
                + project.name
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
        project_info.category = DEFAULT_OTHERS_CATEGORY_ID

    if project_info.category not in categories:
        log.info(
            "Category "
            + project_info.category
            + " is not listed in the categories configuration."
        )
        project_info.category = DEFAULT_OTHERS_CATEGORY_ID


def prepare_categories(input_categories: dict) -> OrderedDict:
    categories = OrderedDict()
    for category in input_categories:
        categories[category["category"]] = Dict(category)

    if DEFAULT_OTHERS_CATEGORY_ID not in categories:
        # Add others category at the last position
        categories[DEFAULT_OTHERS_CATEGORY_ID] = Dict({"title": "Others"})
    return categories


def prepare_configuration(cfg: dict) -> Dict:
    config = Dict(cfg)

    if "project_inactive_months" not in config:
        config.project_inactive_months = 6

    if "project_dead_months" not in config:
        config.project_dead_months = 12

    if "project_new_months" not in config:
        config.project_new_months = 6

    if "min_projectrank" not in config:
        config.min_projectrank = 10

    if "min_stars" not in config:
        config.min_stars = 100

    if "require_license" not in config:
        config.require_license = True

    if "require_pypi" not in config:
        config.require_pypi = False

    if "require_github" not in config:
        config.require_github = False

    if "require_npm" not in config:
        config.require_npm = False

    if "require_conda" not in config:
        config.require_conda = False

    if "markdown_output_file" not in config:
        config.markdown_output_file = "README.md"

    if "generate_badges" not in config:
        config.generate_badges = False

    if "generate_install_hints" not in config:
        config.generate_install_hints = True

    if "generate_toc" not in config:
        config.generate_toc = True

    if "generate_link_shortcuts" not in config:
        config.generate_link_shortcuts = False

    if "generate_legend" not in config:
        config.generate_legend = True

    if "sort_by" not in config:
        config.sort_by = "projectrank"

    if "allowed_licenses" not in config:
        config.allowed_licenses = []
        from best_of.license import LICENSES

        for license in LICENSES:
            config.allowed_licenses.append(license["spdx_id"])

    return config


def sort_projects(projects: list, configuration: Dict) -> list:
    def sort_project_list(project):  # type: ignore
        project = Dict(project)
        projectrank = 0
        star_count = 0

        if project.projectrank:
            projectrank = int(project.projectrank)

        if project.star_count:
            star_count = int(project.star_count)

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
    if (
        not project_info.name
        or not project_info.homepage
        or not project_info.description
        or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
    ):
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
    if configuration.require_pypi and not project_info.pypi_url:
        project_info.show = False

    if configuration.require_github and not project_info.github_url:
        project_info.show = False

    if configuration.require_npm and not project_info.npm_url:
        project_info.show = False

    if configuration.require_conda and not project_info.conda_url:
        project_info.show = False

    if configuration.require_dockerhub and not project_info.dockerhub_url:
        project_info.show = False

    # Do not show if license was not found
    if not project_info.license and configuration.require_license:
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

        if project_license not in set(allowed_licenses):
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

        update_via_github(project_info)
        update_via_pypi(project_info)
        update_via_conda(project_info)
        update_via_npm(project_info)
        update_via_maven(project_info)
        update_via_dockerhub(project_info)

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
