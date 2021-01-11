import logging
from urllib.parse import quote

import requests
from addict import Dict

from best_of import utils
from best_of.integrations import libio_integration
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class NpmIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "npm"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.npm_id:
            return

        if not project_info.npm_url:
            project_info.npm_url = (
                "https://www.npmjs.com/package/" + project_info.npm_id
            )

        if libio_integration.is_activated():
            libio_integration.update_package_via_libio("npm", project_info)

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
                "Failed to request package via npm api: " + project_info.npm_id,
                exc_info=ex,
            )
            return

        # TODO use npms-api to get additional details:
        # https://api-docs.npms.io/#api-Package-GetMultiPackageInfo

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        npm_id = project.npm_id
        if not npm_id:
            return ""

        metrics_md = ""
        if project.npm_monthly_downloads:
            if metrics_md:
                metrics_md += " · "
            metrics_md += (
                "📥 "
                + str(utils.simplify_number(project.npm_monthly_downloads))
                + " / month"
            )

        if project.npm_dependent_project_count:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📦 " + str(
                utils.simplify_number(project.npm_dependent_project_count)
            )

        if project.npm_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.npm_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        npm_url = ""
        if project.npm_url:
            npm_url = project.npm_url

        # only show : if details are available
        seperator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = "- [NPM](" + npm_url + ")" + metrics_md + seperator + "\n"

        if configuration.generate_install_hints:
            details_md += "\t```\n\tnpm install {npm_id}\n\t```\n"
        return details_md.format(npm_id=npm_id)
