import logging
import os
import re
import urllib.parse
from collections import OrderedDict
from datetime import datetime
from typing import List, Tuple

from addict import Dict

from best_of import default_config, integrations, utils
from best_of.generators.base_generator import BaseGenerator
from best_of.integrations import github_integration
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


def generate_project_labels(project: Dict, labels: list) -> Tuple[str, int]:
    IMAGE_LABEL_LENGTH = 2
    LABEL_SPACING_LENGTH = 2

    labels_md = ""
    labels_text_length = 0

    if not project.labels:
        return "", 0

    for label in project.labels:
        label_info = get_label_info(label, labels)

        if label_info.ignore:
            # Label should not be displayed
            continue

        if not label_info.image and not label_info.name:
            # no image or name is given, do not add the label
            # this should not happen
            continue

        label_md = ""
        if label_info.image and label_info.name:
            labels_text_length += len(label_info.name) + IMAGE_LABEL_LENGTH

            label_md = '<code><img src="{image}" style="display:inline;" width="13" height="13">{name}</code>'.format(
                image=label_info.image, name=label_info.name
            )
        elif label_info.image:
            labels_text_length += IMAGE_LABEL_LENGTH

            label_md = '<code><img src="{image}" style="display:inline;" width="13" height="13"></code>'.format(
                image=label_info.image
            )
        elif label_info.name:
            labels_text_length += len(label_info.name)
            label_md = "<code>{name}</code>".format(name=label_info.name)

        if label_info.url:
            # Add link to label
            # target="_blank"?
            label_md = '<a href="' + label_info.url + '">' + label_md + "</a>"

        if label_md:
            # Add a single space in front of label:
            labels_md += " " + label_md.strip()
            labels_text_length += LABEL_SPACING_LENGTH

    return (labels_md, labels_text_length)


def generate_license_info(project: Dict, configuration: Dict) -> Tuple[str, int]:
    if configuration.hide_project_license or project.resource:
        return "", 0

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

        if licenses_warning and not configuration.hide_license_risk:
            licenses_name = "❗️" + licenses_name

        license_length = len(licenses_name)
        # target="_blank"
        license_template = ' <code><a href="{url}">{text}</a></code>'
        license_md += license_template.format(url=licenses_url, text=licenses_name)
    else:
        if configuration.hide_license_risk:
            license_md += " <code>Unlicensed</code>"
        else:
            license_md += " <code>❗Unlicensed</code>"
    return license_md, license_length


def generate_project_body(project: Dict, configuration: Dict) -> str:
    body_md = ""

    if project.github_id:
        body_md += github_integration.generate_github_details(project, configuration)

    for package_manager in integrations.AVAILABLE_PACKAGE_MANAGER:
        package_manager_id = package_manager.name.lower().strip() + "_id"
        if package_manager_id in project and project[package_manager_id]:
            body_md += package_manager.generate_md_details(project, configuration)

    if not body_md:
        # show message if no information is available
        body_md = "- _No project information available._"

    body_md = "\n\n" + body_md
    return body_md


def generate_project_md(
    project: Dict, configuration: Dict, labels: list, generate_body: bool = True
) -> str:

    if project.ignore:
        return ""

    project_md = ""
    metrics_md = generate_metrics_info(project, configuration)
    license_md, license_len = generate_license_info(project, configuration)
    labels_md, labels_lenght = generate_project_labels(project, labels)

    # TODO: use labels_lenght

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

    if license_len:
        # Add spacing to length
        license_len += 2

    desc_length = int(
        round(
            max(
                55,
                105
                - (len(project.name) * 1.3)
                - len(metrics_md)
                - license_len
                - (label_count * 5),
            )
        )
    )
    description = utils.process_description(project.description, desc_length)

    # target="_blank"
    if project.resource:
        if description:
            description = f"- {description}"
        project_md = '🔗&nbsp;<b><a href="{homepage}">{name}</a></b> {metrics} {description}{metadata}\n'.format(
            homepage=project.homepage,
            name=project.name,
            description=description,
            metrics=metrics_md,
            metadata=metadata_md,
        )
    elif generate_body:
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
    category: Dict, config: Dict, labels: list, title_md_prefix: str = "##"
) -> str:
    if category.ignore:
        return ""

    if (
        (
            config.hide_empty_categories
            or category.category == default_config.DEFAULT_OTHERS_CATEGORY_ID
        )
        and not category.projects
        and not category.hidden_projects
    ):
        # Do not show category
        return ""

    category_md: str = ""
    category_md += title_md_prefix + " " + category.title + "\n\n"
    back_to_top_anchor = "#contents"
    if not config.generate_toc:
        # Use # anchor to get back to top of repo
        back_to_top_anchor = "#"

    category_md += f'<a href="{back_to_top_anchor}"><img align="right" width="15" height="15" src="{default_config.UP_ARROW_IMAGE}" alt="Back to top"></a>\n\n'

    if category.subtitle:
        category_md += "_" + category.subtitle.strip() + "_\n\n"

    if category.projects:
        for project in category.projects:
            project_md = generate_project_md(project, config, labels)
            category_md += project_md + "\n"

    if category.hidden_projects:
        category_md += (
            "<details><summary>Show "
            + str(len(category.hidden_projects))
            + " hidden projects...</summary>\n\n"
        )
        for project in category.hidden_projects:
            project_md = generate_project_md(
                project, config, labels, generate_body=False
            )
            category_md += project_md + "\n"
        category_md += "</details>\n"

    return "<br>\n\n" + category_md


def generate_changes_md(projects: list, config: Dict, labels: list) -> str:
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

    if trending_up_projects:
        markdown += "## 📈 Trending Up\n\n"
        markdown += "_Projects that have a higher project-quality score compared to the last update. There might be a variety of reasons, such as increased downloads or code activity._\n\n"
        for project in trending_up_projects:
            project_md = generate_project_md(
                project, config, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if trending_down_projects:
        markdown += "## 📉 Trending Down\n\n"
        markdown += "_Projects that have a lower project-quality score compared to the last update. There might be a variety of reasons such as decreased downloads or code activity._\n\n"
        for project in trending_down_projects:
            project_md = generate_project_md(
                project, config, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if added_projects:
        markdown += "## ➕ Added Projects\n\n"
        markdown += "_Projects that were recently added to this best-of list._\n\n"
        for project in added_projects:
            project_md = generate_project_md(
                project, config, labels, generate_body=False
            )
            markdown += project_md + "\n"
        markdown += "\n"

    if not markdown:
        markdown = "Nothing changed from last update."

    return markdown


def generate_legend(
    configuration: Dict, labels: list, title_md_prefix: str = "##"
) -> str:
    legend_md = title_md_prefix + " Explanation\n"
    # Score that various project-quality metrics
    # score for a package based on a number of metrics
    legend_md += "- 🥇🥈🥉&nbsp; Combined project-quality score\n"
    legend_md += "- ⭐️&nbsp; Star count from GitHub\n"
    legend_md += (
        "- 🐣&nbsp; New project _(less than "
        + str(configuration.project_new_months)
        + " months old)_\n"
    )
    legend_md += (
        "- 💤&nbsp; Inactive project _("
        + str(configuration.project_inactive_months)
        + " months no activity)_\n"
    )
    legend_md += (
        "- 💀&nbsp; Dead project _("
        + str(configuration.project_dead_months)
        + " months no activity)_\n"
    )
    legend_md += "- 📈📉&nbsp; Project is trending up or down\n"
    legend_md += "- ➕&nbsp; Project was recently added\n"
    if not configuration.hide_project_license and not configuration.hide_license_risk:
        legend_md += "- ❗️&nbsp; Warning _(e.g. missing/risky license)_\n"
    legend_md += "- 👨‍💻&nbsp; Contributors count from GitHub\n"
    legend_md += "- 🔀&nbsp; Fork count from GitHub\n"
    legend_md += "- 📋&nbsp; Issue count from GitHub\n"
    legend_md += "- ⏱️&nbsp; Last update timestamp on package manager\n"
    legend_md += "- 📥&nbsp; Download count from package manager\n"
    legend_md += "- 📦&nbsp; Number of dependent projects\n"
    # legend_md += "- 💲&nbsp; Commercial project\n"

    if configuration.show_labels_in_legend:
        for label in labels:
            label_info = Dict(label)
            if label_info.ignore:
                continue
            # Add image labels to explanations
            if label_info.image and label_info.description:
                legend_md += '- <img src="{image}" style="display:inline;" width="13" height="13">&nbsp; {description}\n'.format(
                    image=label_info.image, description=label_info.description
                )

    return legend_md + "\n"


def process_md_link(text: str) -> str:
    text = text.lower().replace(" ", "-")
    return re.compile(r"[^a-zA-Z0-9-]").sub("", text)


def generate_toc(categories: OrderedDict, config: Dict) -> str:
    toc_md = "## Contents\n\n"
    for category in categories:
        category_info = Dict(categories[category])
        if category_info.ignore:
            continue

        url = "#" + process_md_link(category_info.title)

        project_count = 0
        if category_info.projects:
            project_count += len(category_info.projects)
        if category_info.hidden_projects:
            project_count += len(category_info.hidden_projects)

        if not project_count and (
            config.hide_empty_categories
            or category == default_config.DEFAULT_OTHERS_CATEGORY_ID
        ):
            # only add if more than 0 projects
            continue

        toc_md += "- [{title}]({url}) _{project_count} projects_\n".format(
            title=category_info.title, url=url, project_count=project_count
        )
    return toc_md + "\n"


def generate_md(categories: OrderedDict, config: Dict, labels: list) -> str:
    full_markdown = ""

    project_count = 0
    category_count = 0
    stars_count = 0

    for category_name in categories:
        category = categories[category_name]
        if not config.hide_empty_categories or (
            category.projects or category.hidden_projects
        ):
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

    if category_count > 0:
        # do not count others as category
        category_count -= 1

    if config.markdown_header_file:
        if os.path.exists(config.markdown_header_file):
            with open(config.markdown_header_file, "r") as f:
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
                + os.path.abspath(config.markdown_header_file)
            )

    if config.generate_toc:
        full_markdown += generate_toc(categories, config)

    if config.generate_legend:
        full_markdown += generate_legend(config, labels)

    for category in categories:
        category_info = categories[category]
        full_markdown += generate_category_md(category_info, config, labels)

    if config.markdown_footer_file:
        if os.path.exists(config.markdown_footer_file):
            with open(config.markdown_footer_file, "r") as f:
                full_markdown += str(f.read()).format(
                    project_count=utils.simplify_number(project_count),
                    category_count=utils.simplify_number(category_count),
                    stars_count=utils.simplify_number(stars_count),
                )
        else:
            log.warning(
                "The markdown footer file does not exist: "
                + os.path.abspath(config.markdown_footer_file)
            )
    return full_markdown


class MarkdownListGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "markdown-list"

    def write_output(
        self, categories: OrderedDict, projects: List[Dict], config: Dict, labels: list
    ) -> None:
        markdown = generate_md(categories=categories, config=config, labels=labels)

        changes_md = generate_changes_md(projects, config, labels)

        if config.projects_history_folder:
            changes_md_file_name = datetime.today().strftime("%Y-%m-%d") + "_changes.md"
            # write to history folder
            with open(
                os.path.join(config.projects_history_folder, changes_md_file_name), "w"
            ) as f:
                f.write(changes_md)

        # write changes to working directory
        with open(
            os.path.join(
                os.path.dirname(config.output_file), default_config.LATEST_CHANGES_FILE
            ),
            "w",
        ) as f:
            f.write(changes_md)

        # Write markdown to file
        with open(config.output_file, "w") as f:
            f.write(markdown)
