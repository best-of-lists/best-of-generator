"""Gallery view for a best-of list.

For each project, it shows an image (or takes a screenshot of the homepage) and some
information. Note that only a selected subset of project information is shown
(compared to MarkdownListGenerator).
See the example at: https://github.com/jrieke/best-of-streamlit

Gallery view allows for some additional configuration args, see README.md.
"""

import asyncio
import logging
import os
import time
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Generator, List

import pyppeteer
from addict import Dict

from best_of import default_config, utils
from best_of.generators import markdown_list
from best_of.generators.base_generator import BaseGenerator

log = logging.getLogger(__name__)


# This is used if no image is given at all.
DUMMY_IMAGE = "https://dummyimage.com/1024x768/ffffff/000000.jpg&text=No+image+found+:("


def chunker(seq: list, size: int) -> Generator:
    """Iterates over a sequence in chunks."""
    # From https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def shorten(s: str, max_len: int) -> str:
    """Shorten a string by appending ... if it's too long."""
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


async def save_screenshot(
    url: str, img_path: str, sleep: int = 5, width: int = 1024, height: int = 576
) -> None:
    """Loads url in headless browser and saves screenshot to file (.jpg or .png)."""
    browser = await pyppeteer.launch({"args": ["--no-sandbox"]})
    page = await browser.newPage()
    await page.goto(url, {"timeout": 6000})  # increase timeout to 60 s for heroku apps
    await page.emulate({"viewport": {"width": width, "height": height}})
    time.sleep(sleep)
    # Type (PNG or JPEG) will be inferred from file ending.
    await page.screenshot({"path": img_path})
    await browser.close()


def generate_project_html(
    project: Dict, configuration: Dict, labels: Dict = None
) -> str:
    """Generates the content of a table cell for a project."""

    project_md = ""

    if project.image:
        img_path = project.image
    else:
        # Retrieve default image and any existing screenshot.
        default_img_path = configuration.get("default_image", DUMMY_IMAGE)
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        img_filename = "".join([c for c in project.name if c.isalpha()]) + ".png"
        img_path = screenshot_dir / img_filename

        if configuration.skip_screenshots:
            # Use existing screenshot or default img if doesn't exist.
            if not img_path.exists():
                img_path = default_img_path
        elif not (configuration.skip_existing_screenshots and img_path.exists()):
            if (
                configuration.ignore_github_screenshot
                and project.homepage == project.github_url
            ):
                # If no dedicated homepage is given (other than the github site),
                # use the default img.
                img_path = default_img_path
            else:
                # Try to take a screenshot of the website and use default img if that
                # fails.
                try:
                    # TODO: Could make this in parallel, but not really required right
                    #   now.
                    print(
                        f"Taking screenshot for {project.name} (from {project.homepage})"
                    )
                    sleep = configuration.get("wait_before_screenshot", 10)
                    asyncio.run(  # type: ignore
                        save_screenshot(project.homepage, img_path, sleep=sleep)
                    )
                    print(f"Success! Saved in: {img_path}")
                except pyppeteer.errors.TimeoutError:
                    print(f"Timeout when loading: {project.homepage}")
                    img_path = default_img_path

    # Add image and project name to md.
    project_md += f'<br><a href="{project.homepage}"><img width="256" height="144" src="{img_path}"></a><br>'
    project_md += f'<h3><a href="{project.homepage}">{project.name}</a></h3>'

    # Add metrics to md.
    metrics = []
    if project.created_at:
        project_total_month = utils.diff_month(datetime.now(), project.created_at)
        if (
            configuration.project_new_months
            and int(configuration.project_new_months) >= project_total_month
        ):
            metrics.append("🐣 New")
    if project.star_count:
        metrics.append(f"⭐ {str(utils.simplify_number(project.star_count))}")
    if project.github_url:
        metrics.append(f'<a href="{project.github_url}">:octocat: Code</a>')
    if metrics:
        metrics_str = " · ".join(metrics)
        project_md += f"<p>{metrics_str}</p>"

    # Shorten description and add to md.
    description = project.description
    if description[-1] == ".":  # descriptions returned by best-of end with .
        description = description[:-1]
    description = shorten(description, 90)
    project_md += f"<p>{description}</p>"

    # Add project author (=Github repo owner) to md.
    if project.github_id:
        author = project.github_id.split("/")[0]
        project_md += (
            f'<p><sup>by <a href="https://github.com/{author}">@{author}</a></sup></p>'
        )

    return project_md


def generate_table_html(projects: list, config: Dict, labels: Dict) -> str:
    """Generates a table containing several projects."""
    table_html = '<table width="100%">'
    print("Creating table...")
    for project_row in chunker(projects, config.get("projects_per_row", 3)):
        print("New row:")
        table_html += '<tr align="center">'
        for project in project_row:
            print("- " + project.name)
            project_md = generate_project_html(project, config, labels)
            table_html += f'<td valign="top" width="33.3%">{project_md}</td>'
        table_html += "</tr>"
    table_html += "</table>"
    print()
    return table_html


def generate_category_gallery_md(
    category: Dict, config: Dict, labels: list, title_md_prefix: str = "##"
) -> str:
    """Generates markdown gallery for a category, containing tables with projects."""
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

    # Set up category header.
    category_md = ""
    category_md += title_md_prefix + " " + category.title + "\n\n"
    back_to_top_anchor = "#contents"
    if not config.generate_toc or config.short_toc:
        # Use # anchor to get back to top of repo
        back_to_top_anchor = "#"

    category_md += f'<a href="{back_to_top_anchor}"><img align="right" width="15" height="15" src="{default_config.UP_ARROW_IMAGE}" alt="Back to top"></a>\n\n'

    if category.subtitle:
        category_md += "_" + category.subtitle.strip() + "_\n\n"

    if category.projects:
        # Show top projects directly (in a html table).
        num_shown = config.get("projects_per_category", 6)
        table_html = generate_table_html(category.projects[:num_shown], config, labels)
        category_md += table_html + "\n\n"

        # Hide other projects in an expander.
        if len(category.projects) > num_shown:
            hidden_table_html = generate_table_html(
                category.projects[num_shown:], config, labels
            )
            category_md += f'<br><details align="center"><summary><b>Show {len(category.projects) - num_shown} more for "{category.title}"</b></summary><br>{hidden_table_html}</details>\n\n'

    # TODO: Hidden projects are not adjusted to the gallery view so far.
    if category.hidden_projects:
        category_md += (
            "<details><summary>Show "
            + str(len(category.hidden_projects))
            + " hidden projects...</summary>\n\n"
        )
        for project in category.hidden_projects:
            project_md = markdown_list.generate_project_md(
                project, config, labels, generate_body=False
            )
            category_md += project_md + "\n"
        category_md += "</details>\n"

    return "<br>\n\n" + category_md


def generate_short_toc(categories: OrderedDict, config: Dict) -> str:
    """Generate a short TOC, which is just all category names in one line."""
    # TODO: Maybe port this to markdown_list.
    toc_md = ""
    toc_points = []
    for category in categories:
        category_info = Dict(categories[category])
        if category_info.ignore:
            continue

        url = "#" + markdown_list.process_md_link(category_info.title)

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

        toc_points.append(f"[{category_info.title}]({url})")
    toc_md += " | ".join(toc_points) + "\n\n"
    return toc_md


def generate_md(categories: OrderedDict, config: Dict, labels: list) -> str:
    """Generate the markdown text.

    This is a near-complete copy of the same method in markdown_list but it uses the
    functions in this file.
    """
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
        if config.short_toc:
            full_markdown += generate_short_toc(categories, config)
        else:
            full_markdown += markdown_list.generate_toc(categories, config)

    if config.generate_legend:
        full_markdown += markdown_list.generate_legend(config, labels)

    for category in categories:
        category_info = categories[category]
        full_markdown += generate_category_gallery_md(category_info, config, labels)

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


class MarkdownGalleryGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "markdown-gallery"

    def write_output(
        self, categories: OrderedDict, projects: List[Dict], config: Dict, labels: list
    ) -> None:
        markdown = generate_md(categories=categories, config=config, labels=labels)

        changes_md = markdown_list.generate_changes_md(projects, config, labels)

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

        # Create mobile version with 1 column.
        if config.mobile_version:
            mobile_config = Dict(config)
            mobile_config.output_file = config.get(
                "mobile_output_file", "README-mobile.md"
            )
            mobile_config.projects_per_row = 1
            if "mobile_markdown_header_file" in config:
                mobile_config.markdown_header_file = config.mobile_markdown_header_file
            if "mobile_markdown_footer_file" in config:
                mobile_config.markdown_footer_file = config.mobile_markdown_footer_file

            mobile_markdown = generate_md(
                categories=categories, config=mobile_config, labels=labels
            )

            # Write mobile markdown to file
            with open(mobile_config.output_file, "w") as f:
                f.write(mobile_markdown)
