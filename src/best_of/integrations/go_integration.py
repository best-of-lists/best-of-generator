import logging

from addict import Dict

from best_of import utils
from best_of.integrations import libio_integration
from best_of.integrations.base_integration import BaseIntegration

log = logging.getLogger(__name__)


class GoIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "go"

    def update_project_info(self, project_info: Dict) -> None:
        if not project_info.go_id:
            return

        if not project_info.go_url:
            project_info.go_url = "https://pkg.go.dev/" + project_info.go_id

        if libio_integration.is_activated():
            libio_integration.update_package_via_libio("go", project_info)

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        go_id = project.go_id
        if not go_id:
            return ""

        metrics_md = ""
        if project.go_dependent_project_count:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "📦 " + str(
                utils.simplify_number(project.go_dependent_project_count)
            )

        if project.go_latest_release_published_at:
            if metrics_md:
                metrics_md += " · "
            metrics_md += "⏱️ " + str(
                project.go_latest_release_published_at.strftime("%d.%m.%Y")
            )

        if metrics_md:
            metrics_md = " (" + metrics_md + ")"

        go_url = project.go_url or ""
        # only show : if details are available
        separator = (
            ""
            if not configuration.generate_badges
            and not configuration.generate_install_hints
            else ":"
        )

        details_md = "- [Go](" + go_url + ")" + metrics_md + separator + "\n"

        if configuration.generate_install_hints:
            details_md += "\t```\n\tgo install {go_id}\n\t```\n"

        return details_md.format(go_id=go_id)
