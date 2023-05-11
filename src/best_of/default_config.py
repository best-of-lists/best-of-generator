from collections import OrderedDict

from addict import Dict

DEFAULT_OTHERS_CATEGORY_ID = "others"
MIN_PROJECT_DESC_LENGTH = 10
RECENT_ACTIVITY_DAYS = 90
UP_ARROW_IMAGE = "https://git.io/JtehR"
LATEST_CHANGES_FILE = "latest-changes.md"
ENV_LIBRARIES_API_KEY = "LIBRARIES_API_KEY"
ENV_GITEE_API_KEY = "GITEE_API_KEY"


def prepare_configuration(cfg: dict) -> Dict:
    config = Dict(cfg)

    if "project_inactive_months" not in config:
        config.project_inactive_months = 6

    if "project_dead_months" not in config:
        config.project_dead_months = 12

    if "project_new_months" not in config:
        config.project_new_months = 6

    if "min_projectrank" not in config:
        config.min_projectrank = 10

    if "min_stars" not in config:
        config.min_stars = 100

    if "require_license" not in config:
        config.require_license = True

    if "require_repo" not in config:
        config.require_repo = False

    if "output_file" not in config:
        config.output_file = "README.md"

    if "projects_history_folder" not in config:
        config.projects_history_folder = "history"

    if "generate_install_hints" not in config:
        config.generate_install_hints = True

    if "generate_toc" not in config:
        config.generate_toc = True

    if "category_heading" not in config:
        config.category_heading = "simple"

    if "generate_legend" not in config:
        config.generate_legend = True

    if "sort_by" not in config:
        config.sort_by = "projectrank"

    if "max_trending_projects" not in config:
        config.max_trending_projects = 5

    if "hide_empty_categories" not in config:
        config.hide_empty_categories = False

    if "max_description_length" not in config:
        config.max_description_length = 55

    if "min_description_length" not in config:
        config.min_description_length = MIN_PROJECT_DESC_LENGTH

    if "ascii_description" not in config:
        config.ascii_description = True

    if "hide_project_license" not in config:
        config.hide_project_license = False

    if "show_labels_in_legend" not in config:
        config.show_labels_in_legend = True

    if "hide_license_risk" not in config:
        config.hide_license_risk = False

    if "extension_script" not in config:
        config.extension_script = None

    if "output_generator" not in config:
        config.output_generator = "markdown-list"

    if "allowed_licenses" not in config:
        config.allowed_licenses = []
        from best_of.license import LICENSES

        for license in LICENSES:
            config.allowed_licenses.append(license["spdx_id"])

    return config


def prepare_categories(input_categories: dict) -> OrderedDict:
    categories = OrderedDict()

    if input_categories:
        for category in input_categories:
            categories[category["category"]] = Dict(category)

    if DEFAULT_OTHERS_CATEGORY_ID not in categories:
        # Add others category at the last position
        categories[DEFAULT_OTHERS_CATEGORY_ID] = Dict(
            {"category": DEFAULT_OTHERS_CATEGORY_ID, "title": "Others"}
        )
    return categories
