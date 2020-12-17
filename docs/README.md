<!-- markdownlint-disable -->

# API Overview

## Modules

- [`best_of.generator`](./best_of.generator.md#module-best_ofgenerator)
- [`best_of.integrations`](./best_of.integrations.md#module-best_ofintegrations)
- [`best_of.integrations.conda_integration`](./best_of.integrations.conda_integration.md#module-best_ofintegrationsconda_integration)
- [`best_of.integrations.dockerhub_integration`](./best_of.integrations.dockerhub_integration.md#module-best_ofintegrationsdockerhub_integration)
- [`best_of.integrations.github_integration`](./best_of.integrations.github_integration.md#module-best_ofintegrationsgithub_integration)
- [`best_of.integrations.libio_integration`](./best_of.integrations.libio_integration.md#module-best_ofintegrationslibio_integration)
- [`best_of.integrations.maven_integration`](./best_of.integrations.maven_integration.md#module-best_ofintegrationsmaven_integration)
- [`best_of.integrations.npm_integration`](./best_of.integrations.npm_integration.md#module-best_ofintegrationsnpm_integration)
- [`best_of.integrations.pypi_integration`](./best_of.integrations.pypi_integration.md#module-best_ofintegrationspypi_integration)
- [`best_of.license`](./best_of.license.md#module-best_oflicense)
- [`best_of.md_generation`](./best_of.md_generation.md#module-best_ofmd_generation)
- [`best_of.projects_collection`](./best_of.projects_collection.md#module-best_ofprojects_collection)
- [`best_of.utils`](./best_of.utils.md#module-best_ofutils)
- [`best_of.yaml_generation`](./best_of.yaml_generation.md#module-best_ofyaml_generation)

## Classes

- No classes

## Functions

- [`generator.generate_markdown`](./best_of.generator.md#function-generate_markdown)
- [`generator.parse_projects_yaml`](./best_of.generator.md#function-parse_projects_yaml)
- [`conda_integration.generate_conda_details`](./best_of.integrations.conda_integration.md#function-generate_conda_details)
- [`conda_integration.update_via_conda`](./best_of.integrations.conda_integration.md#function-update_via_conda)
- [`dockerhub_integration.generate_dockerhub_details`](./best_of.integrations.dockerhub_integration.md#function-generate_dockerhub_details)
- [`dockerhub_integration.update_via_dockerhub`](./best_of.integrations.dockerhub_integration.md#function-update_via_dockerhub)
- [`github_integration.generate_github_details`](./best_of.integrations.github_integration.md#function-generate_github_details)
- [`github_integration.get_contributors_via_github_api`](./best_of.integrations.github_integration.md#function-get_contributors_via_github_api)
- [`github_integration.get_repo_deps_via_github`](./best_of.integrations.github_integration.md#function-get_repo_deps_via_github)
- [`github_integration.update_via_github`](./best_of.integrations.github_integration.md#function-update_via_github)
- [`github_integration.update_via_github_api`](./best_of.integrations.github_integration.md#function-update_via_github_api)
- [`libio_integration.is_activated`](./best_of.integrations.libio_integration.md#function-is_activated)
- [`libio_integration.update_package_via_libio`](./best_of.integrations.libio_integration.md#function-update_package_via_libio)
- [`libio_integration.update_repo_via_libio`](./best_of.integrations.libio_integration.md#function-update_repo_via_libio)
- [`maven_integration.generate_maven_details`](./best_of.integrations.maven_integration.md#function-generate_maven_details)
- [`maven_integration.update_via_maven`](./best_of.integrations.maven_integration.md#function-update_via_maven)
- [`npm_integration.generate_npm_details`](./best_of.integrations.npm_integration.md#function-generate_npm_details)
- [`npm_integration.update_via_npm`](./best_of.integrations.npm_integration.md#function-update_via_npm)
- [`pypi_integration.generate_pypi_details`](./best_of.integrations.pypi_integration.md#function-generate_pypi_details)
- [`pypi_integration.update_via_pypi`](./best_of.integrations.pypi_integration.md#function-update_via_pypi)
- [`pypi_integration.update_via_pypistats`](./best_of.integrations.pypi_integration.md#function-update_via_pypistats)
- [`license.get_license`](./best_of.license.md#function-get_license)
- [`md_generation.generate_category_md`](./best_of.md_generation.md#function-generate_category_md)
- [`md_generation.generate_changes_md`](./best_of.md_generation.md#function-generate_changes_md)
- [`md_generation.generate_legend`](./best_of.md_generation.md#function-generate_legend)
- [`md_generation.generate_license_info`](./best_of.md_generation.md#function-generate_license_info)
- [`md_generation.generate_md`](./best_of.md_generation.md#function-generate_md)
- [`md_generation.generate_metrics_info`](./best_of.md_generation.md#function-generate_metrics_info)
- [`md_generation.generate_project_body`](./best_of.md_generation.md#function-generate_project_body)
- [`md_generation.generate_project_labels`](./best_of.md_generation.md#function-generate_project_labels)
- [`md_generation.generate_project_md`](./best_of.md_generation.md#function-generate_project_md)
- [`md_generation.generate_toc`](./best_of.md_generation.md#function-generate_toc)
- [`md_generation.get_label_info`](./best_of.md_generation.md#function-get_label_info)
- [`md_generation.process_md_link`](./best_of.md_generation.md#function-process_md_link)
- [`projects_collection.apply_filters`](./best_of.projects_collection.md#function-apply_filters)
- [`projects_collection.apply_projects_changes`](./best_of.projects_collection.md#function-apply_projects_changes)
- [`projects_collection.calc_projectrank`](./best_of.projects_collection.md#function-calc_projectrank)
- [`projects_collection.calc_projectrank_placing`](./best_of.projects_collection.md#function-calc_projectrank_placing)
- [`projects_collection.categorize_projects`](./best_of.projects_collection.md#function-categorize_projects)
- [`projects_collection.collect_projects_info`](./best_of.projects_collection.md#function-collect_projects_info)
- [`projects_collection.get_projects_changes`](./best_of.projects_collection.md#function-get_projects_changes)
- [`projects_collection.prepare_categories`](./best_of.projects_collection.md#function-prepare_categories)
- [`projects_collection.prepare_configuration`](./best_of.projects_collection.md#function-prepare_configuration)
- [`projects_collection.sort_projects`](./best_of.projects_collection.md#function-sort_projects)
- [`projects_collection.update_project_category`](./best_of.projects_collection.md#function-update_project_category)
- [`utils.clean_whitespaces`](./best_of.utils.md#function-clean_whitespaces)
- [`utils.diff_month`](./best_of.utils.md#function-diff_month)
- [`utils.process_description`](./best_of.utils.md#function-process_description)
- [`utils.remove_special_chars`](./best_of.utils.md#function-remove_special_chars)
- [`utils.simplify_number`](./best_of.utils.md#function-simplify_number)
- [`utils.simplify_str`](./best_of.utils.md#function-simplify_str)
- [`yaml_generation.extract_github_projects_to_yaml`](./best_of.yaml_generation.md#function-extract_github_projects_to_yaml)
- [`yaml_generation.requirements_to_yaml`](./best_of.yaml_generation.md#function-requirements_to_yaml)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
