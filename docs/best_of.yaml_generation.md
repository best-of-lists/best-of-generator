<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.yaml_generation`





---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_github_projects`

```python
extract_github_projects(
    input: Union[str, List[str]],
    excluded_github_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_pypi_projects`

```python
extract_pypi_projects(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_pypi_projects_from_requirements`

```python
extract_pypi_projects_from_requirements(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L294"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `auto_extend_package_manager`

```python
auto_extend_package_manager(
    projects: list,
    pypi: bool = False,
    conda: bool = False,
    npm: bool = False
) → list
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
