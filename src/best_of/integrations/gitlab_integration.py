import logging
from typing import Tuple

import requests
from addict import Dict
from dateutil.parser import parse

from best_of import utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)

query = """
query($fullPath: ID!) {
  project(fullPath: $fullPath) {
    name
    forksCount
    starCount
    issueStatusCounts {
      all
      closed
      opened
    }
    description
    createdAt
    lastActivityAt
    mergeRequests {
      count
    }
    webUrl
    httpUrlToRepo
    statistics {
      commitCount
    }
    releases(first: 100, sort: CREATED_DESC) {
      edges {
        node {
          createdAt
          name
          releasedAt
          tagName
          tagPath
          upcomingRelease
        }
      }
    }
  }
}
"""

GITLAB_DEFAULT_API = "https://gitlab.com/api/graphql"


class GitLabIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "gitlab"

    def get_api_url(self, gitlab_id: str) -> Tuple[str, str]:
        """If `gitlab_id` is in the format "<API_ENDPOINT>::org/repo", it returns a tuple "<API_ENDPOINT>, org/repo", otherwise it returns "<GITLAB_DEFAULT_API>, org/repo".

        Args:
            gitlab_id (str): A string in the format "org/repo" for GitLab projects
            or "<API_ENDPOINT>::org/repo" for GitLab API compatible endpoints.

        Returns:
            tuple[str, str]: API endpoint, org/repo
        """

        if "::" in gitlab_id:
            id_parts = tuple(gitlab_id.split("::"))
            return id_parts[0], id_parts[1]
        else:
            return GITLAB_DEFAULT_API, gitlab_id

    def update_project_info(self, project_info: Dict) -> None:

        # project_info:
        # gitlab_url, homepage, name, gitlab_id, license, created_at
        # updated_at, last_commit_pushed_at, fork_count, open_issue_count
        # closed_issue_count, star_count, commit_count,
        # latest_stable_release_published_at, latest_stable_release_number
        # github_release_downloads, monthly_downloads, release_count
        # description, dependent_project_count, contributor_count
        if not project_info.gitlab_id:
            return

        api_url, project_id = self.get_api_url(project_info.gitlab_id)
        variables = {"fullPath": project_id}
        try:
            request = requests.post(
                api_url,
                json={"query": query, "variables": variables},
            )

            if request.status_code != 200:
                log.info(
                    f"Unable to find the repo {project_info.gitlab_id} on {api_url}. Statuscode: {request.status_code}"
                )
                return

            repo_info = Dict(request.json()["data"]["project"])

            if not repo_info:
                log.info(
                    f"Unable to find the repo {project_info.gitlab_id} on {api_url}. No data returned."
                )
                return
        except Exception as ex:
            log.info(
                f"Failed to request the repo {project_id} on API {api_url} ",
                exc_info=ex,
            )
            return

        if not project_info.gitlab_url:
            project_info.gitlab_url = repo_info.webUrl

        if not project_info.homepage:
            project_info.homepage = repo_info.webUrl

        if not project_info.name and repo_info.name:
            project_info.name = repo_info.name

        if repo_info.createdAt:
            try:
                created_at = parse(repo_info.createdAt, ignoretz=True)
                if not project_info.created_at or project_info.created_at > created_at:
                    project_info.created_at = created_at
            except Exception as ex:
                log.warning(
                    f"Failed to parse timestamp: {repo_info.createdAt}", exc_info=ex
                )

        if repo_info.lastActivity:
            try:
                last_activity_at = parse(repo_info.lastActivityAt, ignoretz=True)
                if (
                    not project_info.updated_at
                    or project_info.updated_at < last_activity_at
                ):
                    project_info.updated_at = last_activity_at
            except Exception as ex:
                log.warning(
                    f"Failed to parse timestamp: {repo_info.lastActivityAt}",
                    exc_info=ex,
                )

        forks_count = int(repo_info.forksCount) if repo_info.forksCount else 0
        if not project_info.fork_count or int(project_info.fork_count) < forks_count:
            project_info.fork_count = forks_count

        issue_status_counts = repo_info.issueStatusCounts
        if issue_status_counts:
            if issue_status_counts.opened:
                open_issues_count = int(issue_status_counts.opened)
                if (
                    not project_info.open_issue_count
                    or int(project_info.open_issue_count) < open_issues_count
                ):
                    project_info.open_issue_count = open_issues_count

            if issue_status_counts.closed:
                closed_issue_count = int(issue_status_counts.closed)
                if (
                    not project_info.closed_issue_count
                    or int(project_info.closed_issue_count) < closed_issue_count
                ):
                    project_info.closed_issue_count = closed_issue_count

        if repo_info.starCount:
            stars_count = int(repo_info.starCount)
            if not project_info.star_count or project_info.star_count < stars_count:
                project_info.star_count = stars_count

        if repo_info.releases:
            release_count = len(repo_info.releases.edges)
            if (
                not project_info.release_count
                or int(project_info.release_count) < release_count
            ):
                project_info.release_count = release_count

        if repo_info.description and (
            not project_info.description
            or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
        ):
            project_info.description = repo_info.description

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        # reuse generate_github_details?
        # contributor_count
        # fork_count
        # gitlab_release_downloads
        # gitlab_dependent_project_count
        # open_issue count + closed_issue_count
        # last_commit_pushed_at
        # gitlab_url

        # Only show if gitlab url is set
        if not project.gitlab_id or not project.gitlab_url:
            return ""

        metrics_md = ""
        if project.fork_count >= 0:
            if metrics_md:
                metrics_md += " · "
            metrics_md += f"🔀 {utils.simplify_number(project.fork_count)}"

        if project.open_issue_count and project.closed_issue_count:
            if metrics_md:
                metrics_md += " · "
            total_issues = project.closed_issue_count + project.open_issue_count
            metrics_md += f"📋 {utils.simplify_number(total_issues)} - {int((project.open_issue_count / total_issues) * 100)}% open"

        if project.updated_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += f"⏱️ {project.updated_at.strftime('%d.%m.%Y')}"

        if metrics_md:
            metrics_md = f"({metrics_md})"

        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = f"- [GitLab]({project.gitlab_url}) {metrics_md}{separator}\n"

        if configuration.generate_install_hints:
            details_md += f"\n\t```\n\tgit clone {project.gitlab_url}\n\t```\n"

        return details_md
