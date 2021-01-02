from addict import Dict

DEFAULT_OTHERS_CATEGORY_ID = "others"
MIN_PROJECT_DESC_LENGTH = 10
UP_ARROW_IMAGE = "https://bit.ly/382Vmvi"
LATEST_CHANGES_FILE = "latest-changes.md"


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

    if "require_github" not in config:
        config.require_github = False

    if "markdown_output_file" not in config:
        config.markdown_output_file = "README.md"

    if "projects_history_folder" not in config:
        config.projects_history_folder = "history"

    if "generate_badges" not in config:
        config.generate_badges = False

    if "generate_install_hints" not in config:
        config.generate_install_hints = True

    if "generate_toc" not in config:
        config.generate_toc = True

    if "generate_legend" not in config:
        config.generate_legend = True

    if "sort_by" not in config:
        config.sort_by = "projectrank"

    if "max_trending_projects" not in config:
        config.max_trending_projects = 5

    if "hide_empty_categories" not in config:
        config.hide_empty_categories = False

    if "show_labels_in_legend" not in config:
        config.show_labels_in_legend = True

    if "allowed_licenses" not in config:
        config.allowed_licenses = []
        from best_of.license import LICENSES

        for license in LICENSES:
            config.allowed_licenses.append(license["spdx_id"])

    return config
