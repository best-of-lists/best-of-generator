<!-- markdownlint-disable -->

# API Overview

## Modules

- [`best_of.default_config`](./best_of.default_config.md#module-best_ofdefault_config)
- [`best_of.generator`](./best_of.generator.md#module-best_ofgenerator)
- [`best_of.generators`](./best_of.generators.md#module-best_ofgenerators)
- [`best_of.generators.base_generator`](./best_of.generators.base_generator.md#module-best_ofgeneratorsbase_generator)
- [`best_of.generators.markdown_gallery`](./best_of.generators.markdown_gallery.md#module-best_ofgeneratorsmarkdown_gallery): Gallery view for a best-of list.
- [`best_of.generators.markdown_list`](./best_of.generators.markdown_list.md#module-best_ofgeneratorsmarkdown_list)
- [`best_of.integrations`](./best_of.integrations.md#module-best_ofintegrations)
- [`best_of.integrations.base_integration`](./best_of.integrations.base_integration.md#module-best_ofintegrationsbase_integration)
- [`best_of.integrations.cargo_integration`](./best_of.integrations.cargo_integration.md#module-best_ofintegrationscargo_integration)
- [`best_of.integrations.conda_integration`](./best_of.integrations.conda_integration.md#module-best_ofintegrationsconda_integration)
- [`best_of.integrations.dockerhub_integration`](./best_of.integrations.dockerhub_integration.md#module-best_ofintegrationsdockerhub_integration)
- [`best_of.integrations.github_integration`](./best_of.integrations.github_integration.md#module-best_ofintegrationsgithub_integration)
- [`best_of.integrations.gitlab_integration`](./best_of.integrations.gitlab_integration.md#module-best_ofintegrationsgitlab_integration)
- [`best_of.integrations.go_integration`](./best_of.integrations.go_integration.md#module-best_ofintegrationsgo_integration)
- [`best_of.integrations.libio_integration`](./best_of.integrations.libio_integration.md#module-best_ofintegrationslibio_integration)
- [`best_of.integrations.maven_integration`](./best_of.integrations.maven_integration.md#module-best_ofintegrationsmaven_integration)
- [`best_of.integrations.npm_integration`](./best_of.integrations.npm_integration.md#module-best_ofintegrationsnpm_integration)
- [`best_of.integrations.pypi_integration`](./best_of.integrations.pypi_integration.md#module-best_ofintegrationspypi_integration)
- [`best_of.license`](./best_of.license.md#module-best_oflicense)
- [`best_of.projects_collection`](./best_of.projects_collection.md#module-best_ofprojects_collection)
- [`best_of.utils`](./best_of.utils.md#module-best_ofutils)
- [`best_of.yaml_generation`](./best_of.yaml_generation.md#module-best_ofyaml_generation)

## Classes

- [`base_generator.BaseGenerator`](./best_of.generators.base_generator.md#class-basegenerator)
- [`markdown_gallery.MarkdownGalleryGenerator`](./best_of.generators.markdown_gallery.md#class-markdowngallerygenerator)
- [`markdown_list.MarkdownListGenerator`](./best_of.generators.markdown_list.md#class-markdownlistgenerator)
- [`base_integration.BaseIntegration`](./best_of.integrations.base_integration.md#class-baseintegration)
- [`cargo_integration.CargoIntegration`](./best_of.integrations.cargo_integration.md#class-cargointegration)
- [`conda_integration.CondaIntegration`](./best_of.integrations.conda_integration.md#class-condaintegration)
- [`dockerhub_integration.DockerhubIntegration`](./best_of.integrations.dockerhub_integration.md#class-dockerhubintegration)
- [`gitlab_integration.GitLabIntegration`](./best_of.integrations.gitlab_integration.md#class-gitlabintegration)
- [`go_integration.GoIntegration`](./best_of.integrations.go_integration.md#class-gointegration)
- [`maven_integration.MavenIntegration`](./best_of.integrations.maven_integration.md#class-mavenintegration)
- [`npm_integration.NpmIntegration`](./best_of.integrations.npm_integration.md#class-npmintegration)
- [`pypi_integration.PypiIntegration`](./best_of.integrations.pypi_integration.md#class-pypiintegration)

## Functions

- [`default_config.prepare_categories`](./best_of.default_config.md#function-prepare_categories)
- [`default_config.prepare_configuration`](./best_of.default_config.md#function-prepare_configuration)
- [`generator.generate_markdown`](./best_of.generator.md#function-generate_markdown)
- [`generator.load_extension_script`](./best_of.generator.md#function-load_extension_script)
- [`generator.parse_projects_yaml`](./best_of.generator.md#function-parse_projects_yaml)
- [`generators.get_generator`](./best_of.generators.md#function-get_generator)
- [`markdown_gallery.chunker`](./best_of.generators.markdown_gallery.md#function-chunker): Iterates over a sequence in chunks.
- [`markdown_gallery.generate_category_gallery_md`](./best_of.generators.markdown_gallery.md#function-generate_category_gallery_md): Generates markdown gallery for a category, containing tables with projects.
- [`markdown_gallery.generate_md`](./best_of.generators.markdown_gallery.md#function-generate_md): Generate the markdown text.
- [`markdown_gallery.generate_project_html`](./best_of.generators.markdown_gallery.md#function-generate_project_html): Generates the content of a table cell for a project.
- [`markdown_gallery.generate_short_toc`](./best_of.generators.markdown_gallery.md#function-generate_short_toc): Generate a short TOC, which is just all category names in one line.
- [`markdown_gallery.generate_table_html`](./best_of.generators.markdown_gallery.md#function-generate_table_html): Generates a table containing several projects.
- [`markdown_gallery.save_screenshot`](./best_of.generators.markdown_gallery.md#function-save_screenshot): Loads url in headless browser and saves screenshot to file (.jpg or .png).
- [`markdown_gallery.shorten`](./best_of.generators.markdown_gallery.md#function-shorten): Shorten a string by appending ... if it's too long.
- [`markdown_list.generate_category_md`](./best_of.generators.markdown_list.md#function-generate_category_md)
- [`markdown_list.generate_changes_md`](./best_of.generators.markdown_list.md#function-generate_changes_md)
- [`markdown_list.generate_legend`](./best_of.generators.markdown_list.md#function-generate_legend)
- [`markdown_list.generate_license_info`](./best_of.generators.markdown_list.md#function-generate_license_info)
- [`markdown_list.generate_md`](./best_of.generators.markdown_list.md#function-generate_md)
- [`markdown_list.generate_metrics_info`](./best_of.generators.markdown_list.md#function-generate_metrics_info)
- [`markdown_list.generate_project_body`](./best_of.generators.markdown_list.md#function-generate_project_body)
- [`markdown_list.generate_project_labels`](./best_of.generators.markdown_list.md#function-generate_project_labels)
- [`markdown_list.generate_project_md`](./best_of.generators.markdown_list.md#function-generate_project_md)
- [`markdown_list.generate_toc`](./best_of.generators.markdown_list.md#function-generate_toc)
- [`markdown_list.get_label_info`](./best_of.generators.markdown_list.md#function-get_label_info)
- [`markdown_list.process_md_link`](./best_of.generators.markdown_list.md#function-process_md_link)
- [`github_integration.generate_github_details`](./best_of.integrations.github_integration.md#function-generate_github_details)
- [`github_integration.get_contributors_via_github_api`](./best_of.integrations.github_integration.md#function-get_contributors_via_github_api)
- [`github_integration.get_repo_deps_via_github`](./best_of.integrations.github_integration.md#function-get_repo_deps_via_github)
- [`github_integration.update_via_github`](./best_of.integrations.github_integration.md#function-update_via_github)
- [`github_integration.update_via_github_api`](./best_of.integrations.github_integration.md#function-update_via_github_api)
- [`libio_integration.is_activated`](./best_of.integrations.libio_integration.md#function-is_activated)
- [`libio_integration.update_package_via_libio`](./best_of.integrations.libio_integration.md#function-update_package_via_libio)
- [`libio_integration.update_repo_via_libio`](./best_of.integrations.libio_integration.md#function-update_repo_via_libio)
- [`license.get_license`](./best_of.license.md#function-get_license)
- [`projects_collection.apply_filters`](./best_of.projects_collection.md#function-apply_filters)
- [`projects_collection.apply_projects_changes`](./best_of.projects_collection.md#function-apply_projects_changes)
- [`projects_collection.calc_grouped_metrics`](./best_of.projects_collection.md#function-calc_grouped_metrics)
- [`projects_collection.calc_projectrank`](./best_of.projects_collection.md#function-calc_projectrank)
- [`projects_collection.calc_projectrank_placing`](./best_of.projects_collection.md#function-calc_projectrank_placing)
- [`projects_collection.categorize_projects`](./best_of.projects_collection.md#function-categorize_projects)
- [`projects_collection.collect_projects_info`](./best_of.projects_collection.md#function-collect_projects_info)
- [`projects_collection.get_projects_changes`](./best_of.projects_collection.md#function-get_projects_changes)
- [`projects_collection.group_projects`](./best_of.projects_collection.md#function-group_projects)
- [`projects_collection.sort_projects`](./best_of.projects_collection.md#function-sort_projects)
- [`projects_collection.update_project_category`](./best_of.projects_collection.md#function-update_project_category)
- [`utils.clean_whitespaces`](./best_of.utils.md#function-clean_whitespaces)
- [`utils.diff_month`](./best_of.utils.md#function-diff_month)
- [`utils.exit_process`](./best_of.utils.md#function-exit_process): Exit the process with exit code.
- [`utils.is_valid_url`](./best_of.utils.md#function-is_valid_url)
- [`utils.process_description`](./best_of.utils.md#function-process_description)
- [`utils.remove_special_chars`](./best_of.utils.md#function-remove_special_chars)
- [`utils.simplify_number`](./best_of.utils.md#function-simplify_number)
- [`utils.simplify_str`](./best_of.utils.md#function-simplify_str)
- [`yaml_generation.auto_extend_package_manager`](./best_of.yaml_generation.md#function-auto_extend_package_manager)
- [`yaml_generation.auto_extend_via_libio`](./best_of.yaml_generation.md#function-auto_extend_via_libio)
- [`yaml_generation.collect_github_projects`](./best_of.yaml_generation.md#function-collect_github_projects)
- [`yaml_generation.extract_github_projects`](./best_of.yaml_generation.md#function-extract_github_projects)
- [`yaml_generation.extract_pypi_projects`](./best_of.yaml_generation.md#function-extract_pypi_projects)
- [`yaml_generation.extract_pypi_projects_from_requirements`](./best_of.yaml_generation.md#function-extract_pypi_projects_from_requirements)
- [`yaml_generation.get_projects_from_org`](./best_of.yaml_generation.md#function-get_projects_from_org)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
