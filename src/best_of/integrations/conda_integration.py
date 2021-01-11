import logging
from datetime import datetime

import requests
from addict import Dict
from dateutil.parser import parse

from best_of import utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations import libio_integration
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class CondaIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "conda"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.conda_id:
            return

        if not project_info.conda_url:
            if "/" in project_info.conda_id:
                # Package from different conda channel (not anaconda)
                # Cannot be requested by libraries.io
                project_info.conda_url = "https://anaconda.org/" + project_info.conda_id
            else:
                project_info.conda_url = (
                    "https://anaconda.org/anaconda/" + project_info.conda_id
                )

        if libio_integration.is_activated() and "/" not in project_info.conda_id:
            # libraries.io can currently only parse conda packages from default channel (anaconda)
            libio_integration.update_package_via_libio("conda", project_info)

        self.update_via_conda_api(project_info)

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        conda_id = project.conda_id
        if not conda_id:
            return ""

        metrics_md = ""

        if project.conda_total_downloads:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📥 " + str(
                utils.simplify_number(project.conda_total_downloads)
            )

        if project.conda_dependent_project_count:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📦 " + str(
                utils.simplify_number(project.conda_dependent_project_count)
            )

        if project.conda_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.conda_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        conda_url = ""
        if project.conda_url:
            conda_url = project.conda_url

        conda_package = project.conda_id
        conda_channel = "anaconda"
        if "/" in project.conda_id:
            # different channel
            conda_channel = project.conda_id.split("/")[0]
            conda_package = project.conda_id.split("/")[1]

        # only show : if details are available
        seperator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = "- [Conda](" + conda_url + ")" + metrics_md + seperator + "\n"

        if configuration.generate_install_hints:
            details_md += (
                "\t```\n\tconda install -c {conda_channel} {conda_package}\n\t```\n"
            )
        return details_md.format(
            conda_channel=conda_channel, conda_package=conda_package
        )

    def update_via_conda_api(self, project_info: Dict) -> None:
        try:
            conda_package = project_info.conda_id
            if "/" not in conda_package:
                # Add anaconda as default channel, if channel not provided
                conda_package = "anaconda/" + project_info.conda_id

            request = requests.get("https://api.anaconda.org/package/" + conda_package)
            request.text
            if request.status_code != 200:
                log.info(
                    "Unable to find package via conda api: "
                    + project_info.conda_id
                    + " ("
                    + str(request.status_code)
                    + ")"
                )
                return
            conda_info = Dict(request.json())

            created_at = None
            if conda_info.created_at:
                try:
                    created_at = parse(str(conda_info.created_at), ignoretz=True)
                    if (
                        not project_info.created_at
                        or project_info.created_at > created_at
                    ):
                        project_info.created_at = created_at
                except Exception as ex:
                    log.warning(
                        "Failed to parse timestamp: " + str(conda_info.created_at),
                        exc_info=ex,
                    )

            if conda_info.modified_at:
                try:
                    updated_at = parse(str(conda_info.modified_at), ignoretz=True)
                    # Set as latest release publish date
                    project_info.conda_latest_release_published_at = updated_at
                    # Update update date from project
                    if (
                        not project_info.updated_at
                        or project_info.updated_at < updated_at
                    ):
                        project_info.updated_at = updated_at
                except Exception as ex:
                    log.warning(
                        "Failed to parse timestamp: " + str(conda_info.modified_at),
                        exc_info=ex,
                    )

            total_downloads = 0
            if conda_info.files:
                for package_file in conda_info.files:
                    total_downloads += int(package_file.ndownloads)

            if total_downloads:
                project_info.conda_total_downloads = total_downloads

                # Add to monthly downloads
                if not project_info.monthly_downloads:
                    project_info.monthly_downloads = 0

                if created_at:
                    # monthly downloads = total downloads to total month
                    project_info.monthly_downloads += int(
                        total_downloads
                        / max(1, int(utils.diff_month(datetime.now(), created_at)))
                    )

            if conda_info.versions:
                version_count = len(conda_info.versions)
                if (
                    not project_info.release_count
                    or int(project_info.release_count) < version_count
                ):
                    project_info.release_count = version_count

            # TODO set docs or project url based on metadata
            # TODO set latest stable release based on latest_version
            # TODO: set licenses if provided

            if (
                not project_info.description
                or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
            ) and conda_info.summary:
                project_info.description = conda_info.summary

        except Exception as ex:
            log.info(
                "Failed to request package via conda api: " + project_info.conda_id,
                exc_info=ex,
            )
            return
