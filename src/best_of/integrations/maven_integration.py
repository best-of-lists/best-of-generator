import logging

from addict import Dict

from best_of import utils
from best_of.integrations import libio_integration
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class MavenIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "maven"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.maven_id:
            return

        if not project_info.maven_url:
            project_info.maven_url = (
                "https://search.maven.org/artifact/"
                + project_info.maven_id.replace(":", "/")
            )

        if libio_integration.is_activated():
            libio_integration.update_package_via_libio("maven", project_info)

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        maven_id = project.maven_id
        if not maven_id or ":" not in maven_id:
            return ""

        metrics_md = ""
        if project.maven_dependent_project_count:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📦 " + str(
                utils.simplify_number(project.maven_dependent_project_count)
            )

        if project.maven_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.maven_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        maven_url = ""
        if project.maven_url:
            maven_url = project.maven_url

        # only show : if details are available
        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = "- [Maven](" + maven_url + ")" + metrics_md + separator + "\n"

        if configuration.generate_install_hints:
            details_md += "\t```\n\t<dependency>\n\t\t<groupId>{maven_group_id}</groupId>\n\t\t<artifactId>{maven_artifact_id}</artifactId>\n\t\t<version>[VERSION]</version>\n\t</dependency>\n\t```\n"
        maven_group_id = maven_id.split(":")[0]
        maven_artifact_id = maven_id.split(":")[1]
        return details_md.format(
            maven_group_id=maven_group_id, maven_artifact_id=maven_artifact_id
        )
