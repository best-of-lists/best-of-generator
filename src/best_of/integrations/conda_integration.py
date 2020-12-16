import logging

from addict import Dict

from best_of import utils
from best_of.integrations import libio_integration

log = logging.getLogger(__name__)


def update_via_conda(project_info: Dict) -> None:
    if not project_info.conda_id:
        return

    if "/" in project_info.conda_id:
        # Package from different conda channel (not anaconda)
        # Cannot be requested by libraries.io
        project_info.conda_url = "https://anaconda.org/" + project_info.conda_id
        return

    if not project_info.conda_url:
        project_info.conda_url = (
            "https://anaconda.org/anaconda/" + project_info.conda_id
        )

    if libio_integration.is_activated():
        libio_integration.update_package_via_libio("conda", project_info)


def generate_conda_details(project: Dict, configuration: Dict) -> str:
    conda_id = project.conda_id
    if not conda_id:
        return ""

    metrics_md = ""
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
            "\n\t```\n\tconda install -c {conda_channel} {conda_package}\n\t```\n"
        )
    return details_md.format(conda_channel=conda_channel, conda_package=conda_package)
