<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    Best-of Generator
</h1>

<p align="center">
    <strong>🏆&nbsp; Generates a ranked markdown list of awesome libraries and tools.</strong>
</p>

<p align="center">
    <a href="https://best-of.org" title="Best-of Badge"><img src="http://bit.ly/3o3EHNN"></a>
    <a href="https://pypi.org/project/best-of/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/best-of?color=green&style=flat"></a>
    <a href="https://github.com/best-of-lists/best-of-generator/actions?query=workflow%3Abuild-pipeline" title="Build status"><img src="https://img.shields.io/github/workflow/status/best-of-lists/best-of-generator/build-pipeline?style=flat"></a>
    <a href="https://gitter.im/ml-tooling/best-of" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/best-of.svg"></a>
    <a href="https://bestoflists.substack.com/subscribe" title="Subscribe for updates"><img src="http://bit.ly/2Md9rxM"></a>
    <a href="https://twitter.com/best_of_lists" title="Best-of on Twitter"><img src="https://img.shields.io/twitter/follow/best_of_lists.svg?style=social&label=Follow"></a>
</p>

<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support--feedback">Support</a> •
  <a href="https://github.com/best-of-lists/best-of-generator/issues/new?labels=bug&template=01_bug-report.md">Report a Bug</a> •
  <a href="#contribution">Contribution</a> •
  <a href="https://github.com/best-of-lists/best-of-generator/releases">Changelog</a>
</p>

The best-of-generator is a CLI tool to generate a markdown page of ranked open-source projects based on a list of projects defined in a `yaml` file. It is integrated with different package managers - such as PyPI, NPM, Conda, and DockerHub - to automatically collect a variety of project metadata and calculate project-quality scores. It also comes with a Github Action workflow for a fully automized update process.

## Highlights

- 📇&nbsp; Generates a beautiful markdown page from a `yaml` list.
- 🔌&nbsp; Integrates various package managers (npm, pypi, conda ...).
- 🔄&nbsp; Github Action workflow for automated weekly updates.
- 📈&nbsp; Identify trending projects based on collected metrics.

## Getting Started

### Run via Github Action

### Run via CLI

## Support & Feedback

This project is maintained by [Benjamin Räthlein](https://twitter.com/raethlein), [Lukas Masuch](https://twitter.com/LukasMasuch), and [Jan Kalkan](https://www.linkedin.com/in/jan-kalkan-b5390284/). Please understand that we won't be able to provide individual support via email. We also believe that help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                     | Channel                                              |
| ------------------------ | ------------------------------------------------------ |
| 🚨&nbsp; **Bug Reports**       | <a href="https://github.com/best-of-lists/best-of-generator/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3Abug+sort%3Areactions-%2B1-desc+" title="Open Bug Report"><img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/bug.svg?label=bug"></a>                                 |
| 🎁&nbsp; **Feature Requests**  | <a href="https://github.com/best-of-lists/best-of-generator/issues?q=is%3Aopen+is%3Aissue+label%3Afeature+sort%3Areactions-%2B1-desc" title="Open Feature Request"><img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/feature.svg?label=feature%20request"></a>                                 |
| 👩‍💻&nbsp; **Usage Questions**   |  <a href="https://github.com/best-of-lists/best-of-generator/issues?q=is%3Aopen+is%3Aissue+label%3Asupport+sort%3Areactions-%2B1-desc" title="Open Support Request"> <img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/support.svg?label=support%20request"></a> <a href="https://gitter.im/ml-tooling/best-of" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/best-of.svg"></a> |
| 📢&nbsp; **Announcements** | <a href="https://gitter.im/ml-tooling/best-of" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/best-of.svg"></a> <a href="https://bestoflists.substack.com/subscribe" title="Subscribe for updates"><img src="http://bit.ly/2Md9rxM"></a> <a href="https://twitter.com/best_of_lists" title="Best-of on Twitter"><img src="https://img.shields.io/twitter/follow/best_of_lists.svg?style=social&label=Follow"> |
| ❓&nbsp; **Other Requests** | <a href="mailto:best-of@mltooling.org" title="Email best-of team"><img src="https://img.shields.io/badge/email-best of-green?logo=mail.ru&logoColor=white"></a> |

## Documentation

<p align="center">
  <a href="#">YAML Structure</a> •
  <a href="#">Projects</a> •
  <a href="#">Categories</a> •
  <a href="#">Labels</a> •
  <a href="#">Configuration</a> •
  <a href="#">Trending Projects</a> •
  <a href="#">Project Quality Score</a> •
  <a href="#">Generator CLI</a> •
  <a href="#">Github Action</a>
</p>

The best-of generator is a CLI tool to generate a markdown page from list of projects configured in a `yaml` file. The documentation sections below will provide information on the [`projects.yaml` structure](), on its different sections ([projects](), [labels](), [categories]() & [configuration]()), on some of the best-of features ([project-quality score]() & [trending projects]()) and instructions on how to run the markdown generation [via the command-line interface]() or [via Github Actions]().


### `projects.yaml` Structure

The `projects.yaml` file has the following structure:

- `configurations` (optional): Can be used to overwrite the default configuration of the best-of list. More information in the [configuration section]().
- `categories` (required): All used categories should be listed here with at least a descriptive title. More information in the [categories section]().
- `labels` (optional): Used labels can be added here to extend the label with additional aspects (e.g. URL, image, description). More information in the [labels section]().
- `projects` (required): All projects should be shown in the generated markdown page should be listed here. Should contain at least one project. More information in the [projects section]().

The following `yaml` shows a small example:

```yaml
# Optional: change the default configuration
configuration:
    markdown_header_file: "config/header.md"
    markdown_footer_file: "config/footer.md"

# Optional: add categories
categories:
  - category: "data-engineering"
    title: "Machine Learning & Data Engineering"
    subtitle: "Best-of lists about machine learning, data engieering, data science, or other topics related to big data."

# Optional: add labels
labels:
  - label: "python"
    image: "https://www.python.org/static/favicon.ico"
    description: "Best-of list with Python projects"

# Required: list of all projects
projects:
  - name: "best-of-ml-python"
    github_id: "ml-tooling/best-of-ml-python"
    labels: ["python"]
    category: "data-engineering"
```

### Projects

#### Project Properties

<table>
    <tr>
        <th>Property</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>name</code></td>
        <td>Name of the project.</td>
    </tr>
    <tr>
        <td colspan="2"><b>Optional Properties:</b></td>
    </tr>
    <tr>
        <td><code>github_id</code></td>
        <td>Github ID of the project based on user or organization  and the repository name (e.g. <code>best-of-lists/best-of-generator</code>).</td>
    </tr>
    <tr>
        <td><code>category</code></td>
        <td>Category that this project is most related to. You can find all available category IDs in the <code>projects.yaml</code> file. The project will be sorted into the <code>Others</code> category if no category is provided.</td>
    </tr>
    <tr>
        <td><code>license</code></td>
        <td>License of the project. If set, license information from Github or package managers will be overwritten.</td>
    </tr>
    <tr>
        <td><code>labels</code></td>
        <td>List of labels that this project is related to. You can find all available label IDs in the projects.yaml file.</td>
    </tr>
    <tr>
        <td><code>description</code></td>
        <td>Short description of the project. If set, the description from Github or package managers will be overwritten.</td>
    </tr>
    <tr>
        <td><code>homepage</code></td>
        <td>Hompage URL of the project. Only use this property if the project homepage is different from the Github URL.</td>
    </tr>
    <tr>
        <td><code>docs_url</code></td>
        <td>Documentation URL of the project. Only use this property if the project documentation site is different from the Github URL.</td>
    </tr>
    <tr>
        <td><code>resource</code></td>
        <td>If `True`, the project will be marked as a resource. Resources are not ranked and will always be shown on top of the category. You can use this to link to another best-of list section or website that contains additional projects.</td>
    </tr>
    <tr>
        <td colspan="2"><b>Supported Package Managers:</b></td>
    </tr>
    <tr>
        <td><code>pypi_id</code></td>
        <td>Project ID on the python package index (pypi.org).</td>
    </tr>
    <tr>
        <td><code>conda_id</code></td>
        <td>Project ID on the conda package manager (anaconda.org). If the main package is provided on a different channel, prefix the ID with the given channel: e.g. <code>conda-forge/tensorflow</code></td>
    </tr>
    <tr>
        <td><code>npm_id</code></td>
        <td>Project ID on the Node package manager (npmjs.com).</td>
    </tr>
    <tr>
        <td><code>dockerhub_id</code></td>
        <td>Project ID on the Dockerhub container registry (hub.docker.com). </td>
    </tr>
</table>

### Categories

A category allows to add additional structure to the best-of list by grouping related projects into a shared category. Thereby, every project is grouped into exactly one category. If no category is provided with the project metadata, the project will be categorized into `others`.

#### Category Example

```yaml
categories:
  - category: "data-engineering"
    title: "Machine Learning & Data Engineering"
    subtitle: "Best-of lists about machine learning, data engieering, data science, or other topics related to big data."

projects:
  - name: "best-of-ml-python"
    github_id: "ml-tooling/best-of-ml-python"
    category: "data-engineering"
```

The example above will be rendered as shown below:

![Category Example](./docs/images/best-of-category-example.png)

#### Category Properties

<table>
    <tr>
        <th>Property</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>category</code></td>
        <td>ID of the category. This ID should also be used for adding a project to this category.</td>
    </tr>
    <tr>
        <td><code>title</code></td>
        <td>Category name used as the header of the category section.</td>
    </tr>
    <tr>
        <td colspan="2"><b>Optional Properties:</b></td>
    </tr>
    <tr>
        <td><code>subtitle</code></td>
        <td>Short description about the category shown under the title.</td>
    </tr>
</table>

### Labels

A label allows to highlight similarities or special features shared between projects. Compared to categories, a project can have any number of labels. The labels are shown as badges attached to the project description. It can have only an image (favicons are recommended), only a name, or both. We recommend to use image labels (or only very short labels) since the usage of labels will shorten the visible description text of a project.

#### Label Example

```yaml
labels:
  - label: "python"
    image: "https://www.python.org/static/favicon.ico"
    description: "Best-of list with Python projects"
  - label: "libraries"
    name: "libraries"

projects:
  - name: "best-of-ml-python"
    github_id: "ml-tooling/best-of-ml-python"
    labels: ["libraries", "python"]
    category: "data-engineering"
```

The example above will be rendered as shown below:

![Label Example](./docs/images/best-of-label-example.png)

#### Label Properties

<table>
    <tr>
        <th>Property</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>label</code></td>
        <td>ID of the label. This ID should also be used for adding the label to a project.</td>
    </tr>
    <tr>
        <td colspan="2"><b>Optional Properties:</b></td>
    </tr>
    <tr>
        <td><code>image</code></td>
        <td>URL to an image. If a valid URL is provided, the image will be shown wherever the label is used.</td>
    </tr>
    <tr>
        <td><code>name</code></td>
        <td>Name of the label. If a name is provided, the name will be shown wherever the label is used.</td>
    </tr>
    <tr>
        <td><code>description</code></td>
        <td>Short description of the label. If <code>show_labels_in_legend</code> configuration is <code>True</code> and an <code>image</code> is set, this description will also be shown in the legend (explanations).</td>
    </tr>
    <tr>
        <td><code>url</code></td>
        <td>If <code>url</code> is set, the label will be a rendered as a link wherever it is used.</td>
    </tr>
</table>

### Configuration

Many aspects of the best-of list can be configured. Since most default values are selected to support the widest range of different lists, changing the default configuration is not required for most cases.

#### Configuration Example

```yaml
configuration:
  min_stars: 0
  min_projectrank: 0
  require_github: True
  allowed_licenses: ["all"]
  markdown_header_file: "config/header.md"
  markdown_footer_file: "config/footer.md"
```

The configuration example above changes the default configuration to show all projects regardless of star count (via `min_stars`), projectrank (via `min_projectrank`), or license (via `allows_licenses`). It also configures a header (via `markdown_header_file`) and footer (via `markdown_footer_file`) markdown files that will be attached to the generated content. In addition, all projects are required to provide at-least a `github_id` (via `require_github`).

#### Configuration Options

<table>
    <tr>
        <th>Config</th>
        <th>Description</th>
        <th>Default</th>
    </tr>
    <tr>
        <td><code>markdown_output_file</code></td>
        <td>The markdown output file.</td>
        <td><code>./README.md</code></td>
    </tr>
    <tr>
        <td><code>markdown_header_file</code></td>
        <td>Path to a markdown file that will be attached above the generated content.</td>
        <td></td>
    </tr>
    <tr>
        <td><code>markdown_footer_file</code></td>
        <td>Path to a markdown file that will be attached below the generated content.</td>
        <td></td>
    </tr>
    <tr>
        <td><code>project_inactive_months</code></td>
        <td>Number of month without activity until a project is marked as inactive.</td>
        <td><code>6</code></td>
    </tr>
    <tr>
        <td><code>project_dead_months</code></td>
        <td>Number of month without activity until a project is marked as dead.</td>
        <td><code>12</code></td>
    </tr>
    <tr>
        <td><code>project_new_months</code></td>
        <td>Number of month since creation to mark a project as newcomer.</td>
        <td><code>6</code></td>
    </tr>
    <tr>
        <td><code>min_projectrank</code></td>
        <td>Project will be hidden if it has a smaller projectrank (quality score).</td>
        <td><code>10</code></td>
    </tr>
    <tr>
        <td><code>min_stars</code></td>
        <td>Project will be hidden if it has a less stars on GitHub.</td>
        <td><code>100</code></td>
    </tr>
    <tr>
        <td><code>require_license</code></td>
        <td>If <code>True</code>, all projects without a detected license will be hidden.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>require_github</code></td>
        <td>If <code>True</code>, all projects without a <code>github_id</code> will be hidden.</td>
        <td><code>False</code></td>
    </tr>
    <tr>
        <td><code>projects_history_folder</code></td>
        <td>The folder used for storing history files (<code>csv</code> files with project metadata). If <code>null</code>, no history files will be created.</td>
        <td><code>./history</code></td>
    </tr>
    <tr>
        <td><code>generate_install_hints</code></td>
        <td>If <code>False</code>, the install hint code block for the package managers will not be shown.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>generate_toc</code></td>
        <td>If <code>True</code>, generate a table of content with all categories.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>generate_legend</code></td>
        <td>If <code>True</code>, generate a legend containing explanations for the used emojis.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>sort_by</code></td>
        <td>The project property used to sort the projects within a category.</td>
        <td><code>projectrank</code></td>
    </tr>
    <tr>
        <td><code>max_trending_projects</code></td>
        <td>The number of trending projects to show for trending up as well as down.</td>
        <td><code>5</code></td>
    </tr>
    <tr>
        <td><code>hide_empty_categories</code></td>
        <td>If <code>True</code>, empty categories will not be shown.</td>
        <td><code>False</code></td>
    </tr>
    <tr>
        <td><code>hide_project_license</code></td>
        <td>If <code>True</code>, the project license badge will not be shown.</td>
        <td><code>False</code></td>
    </tr>
    <tr>
        <td><code>show_labels_in_legend</code></td>
        <td>If <code>True</code>, image labels will be listed in the legend (explanation) if they also have a description.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>allowed_licenses</code></td>
        <td>List of allowed licenses (spdx format). A project with a different license will be hidden. Use <code>["all"]</code> to allow all licenses.</td>
        <td>selection of common open-source licenses</td>
    </tr>
</table>

### Trending Projects

_TODO_

### Project Quality Score

_TODO_

### Generator CLI

_TODO_

## Known Issues

<details>
<summary><b>The generated README file is not displayed completely </b> (click to expand...)</summary>

Github only renders the first 512 kb of the main `README.md` file and will cut of the rendered version as soon as it has processed the first 512 kb of the raw markdown content. The rendering is only cut off when viewing the readme on the main repo page, if you directly select the `README.md` file, it will render in its entirety. To mitigate this issue, we optimized the markdown generation to require the minimum amount of characters. However, if you have a very large list of projects (more than 800), you might reach the 512 kb limit (check the file size of the generated `README.md` file). In this case, we suggest to extract some of the categories or projects into smaller best-of lists.

</details>

## Contribution

- Pull requests are encouraged and always welcome. Read our [contribution guidelines](https://github.com/best-of-lists/best-of-generator/tree/main/CONTRIBUTING.md) and check out [help-wanted](https://github.com/best-of-lists/best-of-generator/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3A"help+wanted"+sort%3Areactions-%2B1-desc+) issues.
- Submit Github issues for any [feature request and enhancement](https://github.com/best-of-lists/best-of-generator/issues/new?assignees=&labels=feature&template=02_feature-request.md&title=), [bugs](https://github.com/best-of-lists/best-of-generator/issues/new?assignees=&labels=bug&template=01_bug-report.md&title=), or [documentation](https://github.com/best-of-lists/best-of-generator/issues/new?assignees=&labels=documentation&template=03_documentation.md&title=) problems.
- By participating in this project, you agree to abide by its [Code of Conduct](https://github.com/best-of-lists/best-of-generator/blob/main/.github/CODE_OF_CONDUCT.md).
- The [development section](#development) below contains information on how to build and test the project after you have implemented some changes.

## Development

> _**Requirements**: [Docker](https://docs.docker.com/get-docker/) and [Act](https://github.com/nektos/act#installation) are required to be installed on your machine to execute the containerized build process._

To simplify the process of building this project from scratch, we provide build-scripts - based on [universal-build](https://github.com/ml-tooling/universal-build) - that run all necessary steps (build, check, test, and release) within a containerized environment. To build and test your changes, execute the following command in the project root folder:

```bash
act -b -j build
```

Refer to our [contribution guides](https://github.com/best-of-lists/best-of-generator/blob/main/CONTRIBUTING.md#development-instructions) for more detailed information on our build scripts and development process.

---

Licensed **MIT**. Created and maintained with ❤️&nbsp; by developers from Berlin.
