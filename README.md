<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    Best-of Generator
</h1>

<p align="center">
    <strong>🏆 Generates a ranked list of awesome libraries and tools.</strong>
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
  <a href="#features">Features</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support--feedback">Support</a> •
  <a href="https://github.com/best-of-lists/best-of-generator/issues/new?labels=bug&template=01_bug-report.md">Report a Bug</a> •
  <a href="#contribution">Contribution</a> •
  <a href="https://github.com/best-of-lists/best-of-generator/releases">Changelog</a>
</p>

_TODO_

## Highlights

- 📄&nbsp; _TODO_

## Getting Started

_TODO_
## Support & Feedback

This project is maintained by [Benjamin Räthlein](https://twitter.com/raethlein), [Lukas Masuch](https://twitter.com/LukasMasuch), and [Jan Kalkan](https://www.linkedin.com/in/jan-kalkan-b5390284/). Please understand that we won't be able to provide individual support via email. We also believe that help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                     | Channel                                              |
| ------------------------ | ------------------------------------------------------ |
| 🚨&nbsp; **Bug Reports**       | <a href="https://github.com/best-of-lists/best-of-generator/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3Abug+sort%3Areactions-%2B1-desc+" title="Open Bug Report"><img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/bug.svg?label=bug"></a>                                 |
| 🎁&nbsp; **Feature Requests**  | <a href="https://github.com/best-of-lists/best-of-generator/issues?q=is%3Aopen+is%3Aissue+label%3Afeature+sort%3Areactions-%2B1-desc" title="Open Feature Request"><img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/feature.svg?label=feature%20request"></a>                                 |
| 👩‍💻&nbsp; **Usage Questions**   |  <a href="https://github.com/best-of-lists/best-of-generator/issues?q=is%3Aopen+is%3Aissue+label%3Asupport+sort%3Areactions-%2B1-desc" title="Open Support Request"> <img src="https://img.shields.io/github/issues/best-of-lists/best-of-generator/support.svg?label=support%20request"></a> <a href="https://gitter.im/ml-tooling/best-of" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/best-of.svg"></a> |
| 🗯&nbsp; **General Discussion** | <a href="https://gitter.im/ml-tooling/best-of" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/best-of.svg"></a> <a href="https://twitter.com/best_of_lists" title="Best-of on Twitter"><img src="https://img.shields.io/twitter/follow/best_of_lists.svg?style=social&label=Follow"> |
| ❓&nbsp; **Other Requests** | <a href="mailto:best-of@mltooling.org" title="Email best-of team"><img src="https://img.shields.io/badge/email-best of-green?logo=mail.ru&logoColor=white"></a> |

## Features

_TODO_

## Documentation

_TODO_

### Generator CLI

_TODO_

### Configuration

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
