from addict import Dict

from best_of.integrations.base_integration import BaseIntegration


def _get_as_list(mapping, key):
    names = mapping.get(key, ())
    if isinstance(names, str):
        names = (names,)
    return names


class MkDocsIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "mkdocs"

    def update_project_info(self, project_info: Dict) -> None:
        pass

    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        if not configuration.generate_install_hints:
            return ""

        themes = _get_as_list(project, "mkdocs_theme")
        plugins = _get_as_list(project, "mkdocs_plugin")
        extensions = _get_as_list(project, "markdown_extension")

        config_keys = []
        yml = yml_main = []
        yml_extra = []
        if themes:
            config_keys.append("theme")
            yml += [f"theme: {x}" for x in themes]
            yml = yml_extra
        if plugins:
            config_keys.append("plugins")
            theme_prefix = f"{themes[0]}/" if themes else ""
            yml += ["plugins:"] + [
                f"  - {x.removeprefix(theme_prefix)}" for x in plugins
            ]
        if extensions:
            config_keys.append("markdown_extensions")
            yml += ["markdown_extensions:"] + [f"  - {x}" for x in extensions]

        if not config_keys:
            return ""
        url = f"https://www.mkdocs.org/user-guide/configuration/#{config_keys[0]}"

        lines = [
            f"Add to [mkdocs.yml]({url}):",
            "```yaml",
            *yml_main,
            "```",
        ]
        if yml_extra:
            lines += [
                "Extras:",
                "```yaml",
                *yml_extra,
                "```",
            ]
        return "- " + "".join(f"   {line}\n" for line in lines).lstrip()
