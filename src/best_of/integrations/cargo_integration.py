import logging
from urllib.parse import quote

import requests
from addict import Dict

from best_of import utils
from best_of.default_config import MIN_PROJECT_DESC_LENGTH
from best_of.integrations import libio_integration
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class CargoIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "cargo"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.cargo_id:
            return

        if not project_info.cargo_url:
            project_info.cargo_url = "https://crates.io/crates/" + project_info.cargo_id

        if libio_integration.is_activated():
            libio_integration.update_package_via_libio("cargo", project_info)

        # Get monthly downloads
        try:
            request = requests.get(
                "https://crates.io/api/v1/crates/"
                + quote(project_info.cargo_id, safe="")
            )
            request.text
            if request.status_code != 200:
                log.info(
                    "Unable to find package via cargo api: "
                    + project_info.cargo_id
                    + " ("
                    + str(request.status_code)
                    + ")"
                )
                return
            cargo_packaged_details = Dict(request.json())
            if not cargo_packaged_details or not cargo_packaged_details.crate:
                log.info(
                    "Unable to get package info via cargo api: " + project_info.cargo_id
                )
                return

            if cargo_packaged_details.crate.recent_downloads:
                # recent downloads == downloads of last 90 days
                project_info.cargo_monthly_downloads = (
                    int(cargo_packaged_details.crate.recent_downloads) / 3
                )

                if not project_info.monthly_downloads:
                    project_info.monthly_downloads = 0

                project_info.monthly_downloads += project_info.cargo_monthly_downloads

            if cargo_packaged_details.crate.downloads:
                project_info.cargo_total_downloads = int(
                    cargo_packaged_details.crate.downloads
                )

            if (
                not project_info.description
                or len(project_info.description) < MIN_PROJECT_DESC_LENGTH
            ) and cargo_packaged_details.crate.description:
                project_info.description = cargo_packaged_details.crate.description

            # TODO: use other info like created_at, updated_at, homepage, newest_version, license

        except Exception as ex:
            log.info(
                "Failed to request package via cargo api: " + project_info.cargo_id,
                exc_info=ex,
            )
            return

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        cargo_id = project.cargo_id
        if not cargo_id:
            return ""

        metrics_md = ""
        if project.cargo_monthly_downloads:
            if metrics_md:
                metrics_md += " · "
            metrics_md += (
                "📥 "
                + str(utils.simplify_number(project.cargo_monthly_downloads))
                + " / month"
            )

        if project.cargo_dependent_project_count:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📦 " + str(
                utils.simplify_number(project.cargo_dependent_project_count)
            )

        if project.cargo_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.cargo_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        cargo_url = project.cargo_url or ""
        # only show : if details are available
        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = "- [Cargo](" + cargo_url + ")" + metrics_md + separator + "\n"

        if configuration.generate_install_hints:
            # TODO: Cargo install only works for binary packages
            details_md += "\t```\n\tcargo install {cargo_id}\n\t```\n"
        return details_md.format(cargo_id=cargo_id)
