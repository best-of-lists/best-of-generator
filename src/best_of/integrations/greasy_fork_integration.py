import logging

import requests
from addict import Dict
from dateutil.parser import parse

from best_of import utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class GreasyForkIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "greasy_fork"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.greasy_fork_id:
            return

        if not project_info.greasy_fork_url:
            project_info.greasy_fork_url = (
                f"https://greasyfork.org/scripts/{project_info.greasy_fork_id}"
            )

        try:
            params = Dict()

            response = requests.get(
                f"{project_info.greasy_fork_url}.json",
                params=params,
            )
            response.raise_for_status()

            greasy_fork_info = Dict(response.json())
        except Exception as ex:
            log.info(
                f"Failed to request {project_info.greasy_fork_id} via Greasy Fork ",
                exc_info=ex,
            )
            return

        # Greasy Fork takes precedence over GitHub.
        # A GitHub repository may contain multiple scripts on Greasy Fork,
        # therefore Greasy Fork gives more specific metadata.
        if (
            not project_info.homepage
            or project_info.homepage == project_info.github_url
        ):
            project_info.homepage = greasy_fork_info.url

        # Greasy Fork takes precedence for the same reason.
        if greasy_fork_info.description:
            project_info.description = greasy_fork_info.description

        if not project_info.license:
            project_info.license = greasy_fork_info.license

        if greasy_fork_info.code_url:
            project_info.greasy_fork_code_url = greasy_fork_info.code_url

        if greasy_fork_info.created_at:
            try:
                created_at = parse(greasy_fork_info.created_at, ignoretz=True)
                if not project_info.created_at or project_info.created_at > created_at:
                    project_info.created_at = created_at
            except Exception as ex:
                log.warning(
                    f"Failed to parse timestamp: {greasy_fork_info.created_at}",
                    exc_info=ex,
                )

        if greasy_fork_info.code_updated_at:
            try:
                updated_at = parse(greasy_fork_info.code_updated_at, ignoretz=True)
                if not project_info.updated_at or project_info.updated_at > updated_at:
                    project_info.updated_at = updated_at
            except Exception as ex:
                log.warning(
                    f"Failed to parse timestamp: {greasy_fork_info.code_updated_at}",
                    exc_info=ex,
                )

        if greasy_fork_info.total_installs:
            # Greasy Fork provides only daily installs and total installs.
            # The former is too unstable, so we only take the latter.
            project_info.greasy_fork_total_installs = int(
                greasy_fork_info.total_installs
            )

        if greasy_fork_info.fan_score:
            # Fan score = favorites + good ratings - bad ratings
            # https://github.com/JasonBarnabe/greasyfork/issues/218
            project_info.greasy_fork_fan_score = float(greasy_fork_info.fan_score)

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        greasy_fork_id = project.greasy_fork_id
        if not greasy_fork_id:
            return ""

        metrics_md = ""
        if project.greasy_fork_total_installs:
            if metrics_md:
                metrics_md += " · "
            metrics_md += (
                "📥 "
                + str(utils.simplify_number(project.greasy_fork_total_installs))
                + " (total)"
            )

        if project.greasy_fork_fan_score:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "🌟 " + str(
                utils.simplify_number(project.greasy_fork_fan_score)
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = (
            f"- [Greasy Fork]({project.greasy_fork_url}) {metrics_md}{separator}\n"
        )

        if configuration.generate_install_hints:
            details_md += f"\t[{greasy_fork_id}]({project.greasy_fork_code_url})\n"

        return details_md
