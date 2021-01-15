import logging

import requests
from addict import Dict
from dateutil.parser import parse

from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)

query = """
query($fullPath: ID!) {
  project(fullPath: "gitlab-org/gitlab") {
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

    def update_project_info(self, project_info: Dict) -> None:

        # project_info:
        # gitlab_url, homepage, name, gitlab_id, license, created_at
        # updated_at, last_commit_pushed_at, fork_count, open_issue_count
        # closed_issue_count, star_count, commit_count,
        # latest_stable_release_published_at, latest_stable_release_number
        # github_release_downloads, monthly_downloads, release_count
        # description, dependent_project_count, contributor_count

        api_url = project_info.api_url or GITLAB_DEFAULT_API
        variables = {"fullPath": project_info.gitlab_id}
        try:
            request = requests.post(
                api_url, json={"query": query, "variables": variables}
            )

            if request.status_code != 200:
                log.info(
                    f"Unable to find the repo {project_info.gitlab_id}. Statuscode: {request.status_code}"
                )
                return

            repo_info = Dict(request.json()["data"]["project"])
        except Exception as ex:
            log.info(
                f"Failed to request the repo {project_info.gitlab_id} on API {api_url} ",
                exc_info=ex,
            )
            return

        if not project_info.gitlab_url and repo_info.httpUrlToRepo:
            project_info.gitlab_url = repo_info.httpUrlToRepo

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
                last_ativity_at = parse(repo_info.lastActivityAt, ignoretz=True)
                if (
                    not project_info.lastActivityAt
                    or project_info.lastActivityAt < created_at
                ):
                    project_info.lastActivityAt = last_ativity_at
            except Exception as ex:
                log.warning(
                    f"Failed to parse timestamp: {repo_info.lastActivityAt}",
                    exc_info=ex,
                )

        if repo_info.forksCount:
            forks_count = int(repo_info.forksCount)
            if (
                not project_info.fork_count
                or int(project_info.fork_count) < forks_count
            ):
                project_info = forks_count

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

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        # reuse generate_github_details?
        # contributor_count
        # fork_count
        # gitlab_release_downloads
        # gitlab_dependent_project_count
        # open_issue count + closed_issue_count
        # last_commit_pushed_at
        # gitlab_url

        return super().generate_md_details(project, configuration)
