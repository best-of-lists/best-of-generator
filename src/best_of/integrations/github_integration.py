import logging
import os
import re
from datetime import datetime
from typing import Optional

import requests
from addict import Dict
from bs4 import BeautifulSoup
from dateutil.parser import parse

from best_of import utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations import libio_integration

log = logging.getLogger(__name__)


def get_repo_deps_via_github(github_id: str) -> int:
    try:
        request = requests.get(
            "https://github.com/" + github_id + "/network/dependents"
        )
        if request.status_code != 200:
            log.info(
                "Unable to find repo dependents via GitHub api: "
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
            "Unable to find repo dependents via GitHub api: " + github_id, exc_info=ex
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
                "Unable to find repo contributors via GitHub api: "
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
            contributor_count = max(contributor_count, int(found_group))
        return contributor_count
    except Exception as ex:
        log.info(
            "Unable to find repo dependents via GitHub api: " + github_id,
            exc_info=ex,
        )

        return None


def update_via_github_api(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    github_api_token = os.getenv("GITHUB_API_KEY")
    if not github_api_token:
        return

    if "/" not in project_info.github_id:
        log.info("The GitHub project id is not valid: " + project_info.github_id)
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
    nameWithOwner
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
                "Unable to find GitHub repo via GitHub api: "
                + project_info.github_id
                + " ("
                + str(request.status_code)
                + ")"
            )
            return
        github_info = Dict(request.json()["data"]["repository"])
    except Exception as ex:
        log.info(
            "Failed to request GitHub repo via GitHub api: " + project_info.github_id,
            exc_info=ex,
        )
        return

    if not project_info.github_url and github_info.url:
        project_info.github_url = github_info.url

    if not project_info.homepage:
        project_info.homepage = project_info.github_url

    if not project_info.name and github_info.name:
        project_info.name = github_info.name

    if github_info.nameWithOwner and utils.simplify_str(
        project_info.github_id
    ) != utils.simplify_str(github_info.nameWithOwner):
        log.info(
            f"The GitHub repo name has changed from {project_info.github_id} to {github_info.nameWithOwner}"
        )
        project_info.updated_github_id = github_info.nameWithOwner

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
            created_at = parse(str(github_info.createdAt), ignoretz=True)
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
            updated_at = parse(str(github_info.pushedAt), ignoretz=True)
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
                str(github_info.masterCommit.target.committedDate), ignoretz=True
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
                    release_date = parse(str(release.publishedAt), ignoretz=True)
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
                log.warning("Failed to parse GitHub release info.", exc_info=ex)

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

    # Get dependents count
    dependent_project_count = get_repo_deps_via_github(project_info.github_id)
    if dependent_project_count:
        if not project_info.dependent_project_count:
            project_info.dependent_project_count = 0

        # TODO: really add this or use the highest dependents count
        project_info.dependent_project_count += dependent_project_count
        project_info.github_dependent_project_count = dependent_project_count

    # Get contributor count via GitHub api 3
    contributor_count = get_contributors_via_github_api(
        project_info.github_id, github_api_token
    )
    if contributor_count:
        if not project_info.contributor_count:
            project_info.contributor_count = contributor_count
        elif int(project_info.contributor_count) < contributor_count:
            # always use the highest number
            project_info.contributor_count = contributor_count


def update_via_github(project_info: Dict) -> None:
    if not project_info.github_id:
        return

    update_via_github_api(project_info)

    if not project_info.github_url or (
        project_info.star_count and project_info.star_count > 20
    ):
        # small projects cannot be found on liberies.io often
        libio_integration.update_repo_via_libio(project_info)


def generate_github_details(project: Dict, configuration: Dict) -> str:
    github_id = project.github_id
    if not github_id:
        return ""

    metrics_md = ""
    if project.contributor_count:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "👨‍💻 " + str(utils.simplify_number(project.contributor_count))

    if project.fork_count:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "🔀 " + str(utils.simplify_number(project.fork_count))

    if project.github_release_downloads:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "📥 " + str(
            utils.simplify_number(project.github_release_downloads)
        )

    if project.github_dependent_project_count:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "📦 " + str(
            utils.simplify_number(project.github_dependent_project_count)
        )

    if project.open_issue_count and project.closed_issue_count:
        if metrics_md:
            metrics_md += " · "
        total_issues = project.closed_issue_count + project.open_issue_count

        metrics_md += (
            "📋 "
            + str(utils.simplify_number(total_issues))
            + " - "
            + str(
                int(
                    (
                        project.open_issue_count
                        / (project.closed_issue_count + project.open_issue_count)
                    )
                    * 100
                )
            )
            + "% open"
        )

    if project.last_commit_pushed_at:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "⏱️ " + str(project.last_commit_pushed_at.strftime("%d.%m.%Y"))

    if metrics_md:
        metrics_md = " (" + metrics_md + ")"

    github_url = ""
    if project.github_url:
        github_url = project.github_url

    # https://badgen.net/#github

    # only show : if details are available
    seperator = (
        ""
        if not configuration.generate_badges
        and not configuration.generate_install_hints
        else ":"
    )

    details_md = "- [GitHub](" + github_url + ")" + metrics_md + seperator + "\n"

    if configuration.generate_install_hints:
        details_md += "\n\t```\n\tgit clone https://github.com/{github_id}\n\t```\n"
    return details_md.format(github_id=github_id)
