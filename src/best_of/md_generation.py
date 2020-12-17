import logging
import os
import re
import urllib.parse
from collections import OrderedDict
from datetime import datetime
from typing import Tuple

from addict import Dict

from best_of import utils
from best_of.integrations import (
    conda_integration,
    dockerhub_integration,
    github_integration,
    maven_integration,
    npm_integration,
    pypi_integration,
)
from best_of.license import get_license

log = logging.getLogger(__name__)


def generate_metrics_info(project: Dict, configuration: Dict) -> str:
    metrics_md = ""

    if project.projectrank:
        placing_emoji = "🥉"
        if project.projectrank_placing:
            if project.projectrank_placing == 1:
                placing_emoji = "🥇"
            elif project.projectrank_placing == 2:
                placing_emoji = "🥈"

        # TODO: add spacing? " " ?
        metrics_md += placing_emoji + str(project.projectrank)

    if project.star_count:
        if metrics_md:
            metrics_md += " · "
        metrics_md += " ⭐ " + str(utils.simplify_number(project.star_count))

    status_md = ""
    project_total_month = None
    if project.created_at:
        project_total_month = utils.diff_month(datetime.now(), project.created_at)

    project_inactive_month = None
    if project.last_commit_pushed_at:
        project_inactive_month = utils.diff_month(
            datetime.now(), project.last_commit_pushed_at
        )
    elif project.updated_at:
        project_inactive_month = utils.diff_month(datetime.now(), project.updated_at)

    if (
        project_inactive_month
        and configuration.project_dead_months
        and int(configuration.project_dead_months) < project_inactive_month
    ):
        status_md = "💀"
    elif (
        project_inactive_month
        and configuration.project_inactive_months
        and int(configuration.project_inactive_months) < project_inactive_month
    ):
        status_md = "💤"
    elif (
        project_total_month
        and configuration.project_new_months
        and int(configuration.project_new_months) >= project_total_month
    ):
        status_md = "🐣"
    elif project.commercial:
        status_md = "💲"
    elif project.trending:
        if project.trending > 0:
            status_md = "📈"
        elif project.trending < 0:
            status_md = "📉"
    elif project.new_addition:
        status_md = "➕"

    if status_md and metrics_md:
        metrics_md = metrics_md + " · " + status_md
    elif status_md:
        # TODO: add spacing? " "
        metrics_md = status_md

    if metrics_md:
        # add divider if metrics are available
        metrics_md = "(" + metrics_md + ")"
        # remove unneccesary whitespaces
        utils.clean_whitespaces(metrics_md)
        # Add whitespace
        metrics_md = metrics_md + " "

    return metrics_md


def get_label_info(label: str, labels: list) -> Dict:
    labels_map = {}
    for label_info in labels:
        label_info = Dict(label_info)
        if not label_info.label:
            continue
        labels_map[utils.simplify_str(label_info.label)] = label_info

    label_query = utils.simplify_str(label)
    if label_query not in labels_map:
        return Dict({"name": label})

    return labels_map[label_query]


def generate_project_labels(project: Dict, labels: list) -> str:
    labels_md = ""

    if not project.labels:
        return labels_md

    for label in project.labels:
        label_info = get_label_info(label, labels)

        if not label_info.image and not label_info.name:
            # no image or name is given, do not add the label
            # this should not happen
            continue

        label_md = ""
        if label_info.image and label_info.name:
            label_md = '<code><img src="{image}" style="display:inline;" width="13" height="13">{name}</code>'.format(
                image=label_info.image, name=label_info.name
            )
        elif label_info.image:
            # TODO: try code blocks?
            label_md = '<code><img src="{image}" style="display:inline;" width="13" height="13"></code>'.format(
                image=label_info.image
            )
        elif label_info.name:
            label_md = "<code>{name}</code>".format(name=label_info.name)

        if label_info.url:
            # Add link to label
            # target="_blank"?
            label_md = '<a href="' + label_info.url + '">' + label_md + "</a>"

        if label_md:
            # Add a single space in front of label:
            labels_md += " " + label_md.strip()

    return labels_md


def generate_license_info(project: Dict, configuration: Dict) -> Tuple[str, int]:
    license_length = 12
    license_md = ""
    if project.license:
        licenses_name = project.license
        licenses_warning = True
        licenses_url = "https://tldrlegal.com/search?q=" + urllib.parse.quote(
            project.license
        )
        license_metadata = get_license(licenses_name)

        if license_metadata:
            if license_metadata.name:
                licenses_name = license_metadata.name
            if license_metadata.url:
                licenses_url = license_metadata.url
            if "warning" in license_metadata:
                licenses_warning = license_metadata.warning

        if licenses_warning:
            licenses_name = "❗️" + licenses_name

        license_length = len(licenses_name)
        # target="_blank"
        license_template = ' <code><a href="{url}">{text}</a></code>'
        license_md += license_template.format(url=licenses_url, text=licenses_name)
    else:
        license_md += " <code>❗️Unlicensed</code>"
    return license_md, license_length


def generate_project_body(project: Dict, configuration: Dict) -> str:
    body_md = ""

    if project.github_id:
        body_md += github_integration.generate_github_details(project, configuration)

    if project.pypi_id:
        body_md += pypi_integration.generate_pypi_details(project, configuration)

    if project.npm_id:
        body_md += npm_integration.generate_npm_details(project, configuration)

    if project.conda_id:
        body_md += conda_integration.generate_conda_details(project, configuration)

    if project.dockerhub_id:
        body_md += dockerhub_integration.generate_dockerhub_details(
            project, configuration
        )

    if project.maven_id:
        body_md += maven_integration.generate_maven_details(project, configuration)

    if not body_md:
        # show message if no information is available
        body_md = "- _No project information available._"

    body_md = "\n\n" + body_md
    return body_md


def generate_project_md(
    project: Dict, configuration: Dict, labels: list, generate_body: bool = True
) -> str:

    project_md = ""
    metrics_md = generate_metrics_info(project, configuration)
    license_md, license_len = generate_license_info(project, configuration)
    labels_md = generate_project_labels(project, labels)

    metadata_md = ""
    if license_md and labels_md:
        # TODO: add " · " in between?
        metadata_md = license_md + labels_md
    elif license_md:
        metadata_md = license_md
    elif labels_md:
        metadata_md = labels_md

    if generate_body:
        body_md = generate_project_body(project, configuration)
    else:
        body_md = ""

    # Dynamically calculate the max length of the description.
    # The goal is that it fits into one row in most cases.
    label_count = 0
    if project.labels:
        label_count = len(project.labels)
    desc_length = int(
        round(
            max(
                60,
                100
                - (len(project.name) * 1.1)
                - len(metrics_md)
                - license_len
                - (label_count * 4),
            )
        )
    )
    description = utils.process_description(project.description, desc_length)
    # target="_blank"
    if generate_body:
        project_md = '<details><summary><b><a href="{homepage}">{name}</a></b> {metrics}- {description}{metadata}</summary>{body}</details>'.format(
            homepage=project.homepage,
            name=project.name,
            description=description,
            metrics=metrics_md,
            metadata=metadata_md,
            body=body_md,
        )
    else:
        # don't use details format
        project_md = '- <b><a href="{homepage}">{name}</a></b> {metrics}- {description}{metadata}'.format(
            homepage=project.homepage,
            name=project.name,
            description=description,
            metrics=metrics_md,
            metadata=metadata_md,
        )

    return project_md


def generate_category_md(
    category: Dict, configuration: Dict, labels: list, title_md_prefix: str = "##"
) -> str:
    category_md = ""

    if not category.projects and not category.hidden_projects:
        # Do not show category
        return category_md

    category_md += title_md_prefix + " " + category.title + "\n\n"
    category_md += '<a href="#contents"><img align="right" width="15" height="15" src="https://i.ibb.co/2PS8bhR/up-arrow.png" alt="Back to top"></a>\n\n'

    if category.subtitle:
        category_md += "_" + category.subtitle.strip() + "_\n\n"

    if category.projects:
        for project in category.projects:
            project_md = generate_project_md(project, configuration, labels)
            category_md += project_md + "\n"

    if category.hidden_projects:
        category_md += (
            "<details><summary>Show "
            + str(len(category.hidden_projects))
            + " hidden projects...</summary>\n<br>"
        )
        for project in category.hidden_projects:
            project_md = generate_project_md(project, configuration, labels)
            category_md += project_md + "\n"
        category_md += "</details>\n"

    return "<br>\n\n" + category_md


def generate_changes_md(projects: list, configuration: Dict, labels: list) -> str:
    added_projects = []
    trending_up_projects = []
    trending_down_projects = []

    for project in projects:
        project = Dict(project)
        if project.trending:
            if project.trending > 0:
                trending_up_projects.append(project)
            elif project.trending < 0:
                trending_down_projects.append(project)
        elif project.new_addition:
            added_projects.append(project)

    markdown = ""

    if added_projects:
        markdown += "## ➕ Added Projects\n\n"
        markdown += "_Projects that were recently added to this best-of list._\n\n"
        for project in added_projects:
            project_md = generate_project_md(
                project, configuration, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if trending_up_projects:
        markdown += "## 📈 Trending Up\n\n"
        markdown += "_Projects that have a higher project-quality score compared to the last update. There might be a variety of reasons, such as increased downloads or code activity._\n\n"
        for project in trending_up_projects:
            project_md = generate_project_md(
                project, configuration, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if trending_down_projects:
        markdown += "## 📉 Trending Down\n\n"
        markdown += "_Projects that have a lower project-quality score compared to the last update. There might be a variety of reasons such as decreased downloads or code activity._\n\n"
        for project in trending_down_projects:
            project_md = generate_project_md(
                project, configuration, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if not markdown:
        markdown = "Nothing changed from last update."

    return markdown


def generate_legend(configuration: Dict, title_md_prefix: str = "##") -> str:
    legend_md = title_md_prefix + " Explanation\n"
    # Score that various project-quality metrics
    # score for a package based on a number of metrics
    legend_md += "- 🥇🥈🥉&nbsp; Combined project-quality score\n"
    legend_md += "- ⭐️&nbsp; Star count from Github\n"
    legend_md += (
        "- 🐣&nbsp; New project _(less than "
        + str(configuration.project_new_months)
        + " month old)_\n"
    )
    legend_md += (
        "- 💤&nbsp; Inactive project _("
        + str(configuration.project_inactive_months)
        + " month no activity)_\n"
    )
    legend_md += (
        "- 💀&nbsp; Dead project _("
        + str(configuration.project_dead_months)
        + " month no activity)_\n"
    )
    legend_md += "- 📈📉&nbsp; Project is trending up or down\n"
    legend_md += "- ➕&nbsp; Project was recently added\n"
    legend_md += "- ❗️&nbsp; Warning _(e.g. missing/risky license)_\n"
    legend_md += "- 👨‍💻&nbsp; Contributors count from Github\n"
    legend_md += "- 🔀&nbsp; Fork count from Github\n"
    legend_md += "- 📋&nbsp; Issue count from Github\n"
    legend_md += "- ⏱️&nbsp; Last update timestamp on package manager\n"
    legend_md += "- 📥&nbsp; Download count from package manager\n"
    legend_md += "- 📦&nbsp; Number of dependent projects\n"

    # legend_md += "- 💲&nbsp; Commercial project\n"
    return legend_md + "\n"


def process_md_link(text: str) -> str:
    text = text.lower().replace(" ", "-")
    return re.compile(r"[^a-zA-Z0-9-]").sub("", text)


def generate_toc(categories: OrderedDict) -> str:
    toc_md = "## Contents\n\n"
    for category in categories:
        title = categories[category]["title"]
        url = "#" + process_md_link(title)

        project_count = 0
        if "projects" in categories[category] and categories[category]["projects"]:
            project_count += len(categories[category]["projects"])
        if (
            "hidden_projects" in categories[category]
            and categories[category]["hidden_projects"]
        ):
            project_count += len(categories[category]["hidden_projects"])

        if not project_count:
            # only add if more than 0 projects
            continue

        toc_md += "- [{title}]({url}) _{project_count} projects_\n".format(
            title=categories[category]["title"], url=url, project_count=project_count
        )
    return toc_md + "\n"


def generate_md(categories: OrderedDict, configuration: Dict, labels: list) -> str:
    full_markdown = ""

    project_count = 0
    category_count = 0
    stars_count = 0

    for category_name in categories:
        category = categories[category_name]
        if category.projects or category.hidden_projects:
            category_count += 1

        if category.projects:
            for project in category.projects:
                project_count += 1
                if project.star_count:
                    stars_count += project.star_count

        if category.hidden_projects:
            for project in category.hidden_projects:
                project_count += 1
                if project.star_count:
                    stars_count += project.star_count

    if configuration.markdown_header_file:
        if os.path.exists(configuration.markdown_header_file):
            with open(configuration.markdown_header_file, "r") as f:
                full_markdown += (
                    str(f.read()).format(
                        project_count=utils.simplify_number(project_count),
                        category_count=utils.simplify_number(category_count),
                        stars_count=utils.simplify_number(stars_count),
                    )
                    + "\n"
                )
        else:
            log.warning(
                "The markdown header file does not exist: "
                + os.path.abspath(configuration.markdown_header_file)
            )

    if configuration.generate_toc:
        full_markdown += generate_toc(categories)

    if configuration.generate_legend:
        full_markdown += generate_legend(configuration)

    for category in categories:
        full_markdown += generate_category_md(
            categories[category], configuration, labels
        )

    if configuration.markdown_footer_file:
        if os.path.exists(configuration.markdown_footer_file):
            with open(configuration.markdown_footer_file, "r") as f:
                full_markdown += str(f.read()).format(
                    project_count=utils.simplify_number(project_count),
                    category_count=utils.simplify_number(category_count),
                    stars_count=utils.simplify_number(stars_count),
                )
        else:
            log.warning(
                "The markdown footer file does not exist: "
                + os.path.abspath(configuration.markdown_footer_file)
            )
    return full_markdown
