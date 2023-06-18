import logging
from datetime import datetime

import requests
from addict import Dict
from dateutil.parser import parse

from best_of import utils
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class DockerhubIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "dockerhub"

    def update_project_info(self, project_info: Dict) -> None:
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
                updated_at = parse(str(dockerhub_info.last_updated), ignoretz=True)
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
                    / max(
                        1,
                        int(utils.diff_month(datetime.now(), project_info.created_at)),
                    )
                )

        if (
            not project_info.description or len(project_info.description) < 10
        ) and dockerhub_info.description:
            project_info.description = dockerhub_info.description

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        dockerhub_id = project.dockerhub_id
        if not dockerhub_id:
            return ""

        metrics_md = ""
        if project.dockerhub_pulls:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📥 " + str(utils.simplify_number(project.dockerhub_pulls))

        if project.dockerhub_stars:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⭐ " + str(utils.simplify_number(project.dockerhub_stars))

        if project.dockerhub_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.dockerhub_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        dockerhub_url = ""
        if project.dockerhub_url:
            dockerhub_url = project.dockerhub_url

        # only show : if details are available
        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = (
            "- [Docker Hub](" + dockerhub_url + ")" + metrics_md + separator + "\n"
        )

        if configuration.generate_install_hints:
            details_md += "\t```\n\tdocker pull {dockerhub_id}\n\t```\n"
        return details_md.format(dockerhub_id=dockerhub_id)
