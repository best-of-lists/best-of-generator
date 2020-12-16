import json
import logging
import time

import pypistats
from addict import Dict

from best_of import utils
from best_of.integrations import libio_integration

log = logging.getLogger(__name__)


def update_via_pypi(project_info: Dict) -> None:
    if not project_info.pypi_id:
        return

    if not project_info.pypi_url:
        project_info.pypi_url = "https://pypi.org/project/" + project_info.pypi_id

    if libio_integration.is_activated():
        libio_integration.update_package_via_libio("pypi", project_info)

    try:
        # pypi stats limit is 30 per minute: https://github.com/crflynn/pypistats.org/issues/28#issuecomment-598417650
        time.sleep(1.5)

        # get download count from pypi stats
        project_info.pypi_monthly_downloads = int(
            json.loads(pypistats.recent(project_info.pypi_id, "month", format="json"))[
                "data"
            ]["last_month"]
        )

        if not project_info.monthly_downloads:
            project_info.monthly_downloads = 0

        project_info.monthly_downloads += int(project_info.pypi_monthly_downloads)
    except Exception as ex:
        log.info(
            "Unable to request statistics from pypi: " + project_info.pypi_id,
            exc_info=ex,
        )


def generate_pypi_details(project: Dict, configuration: Dict) -> str:
    pypi_id = project.pypi_id
    if not pypi_id:
        return ""

    metrics_md = ""
    if project.pypi_monthly_downloads:
        if metrics_md:
            metrics_md += " · "
        metrics_md += (
            "📥 "
            + str(utils.simplify_number(project.pypi_monthly_downloads))
            + " / month"
        )

    if project.pypi_dependent_project_count:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "📦 " + str(
            utils.simplify_number(project.pypi_dependent_project_count)
        )

    if project.pypi_latest_release_published_at:
        if metrics_md:
            metrics_md += " · "
        metrics_md += "⏱️ " + str(
            project.pypi_latest_release_published_at.strftime("%d.%m.%Y")
        )

    if metrics_md:
        metrics_md = " (" + metrics_md + ")"

    pypi_url = ""
    if project.pypi_url:
        pypi_url = project.pypi_url

    # https://badgen.net/#pypi

    # only show : if details are available
    seperator = (
        ""
        if not configuration.generate_badges
        and not configuration.generate_install_hints
        else ":"
    )

    details_md = "- [PyPi](" + pypi_url + ")" + metrics_md + seperator + "\n"

    if configuration.generate_install_hints:
        details_md += "\n\t```\n\tpip install {pypi_id}\n\t```\n"
    return details_md.format(pypi_id=pypi_id)
