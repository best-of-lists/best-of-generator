<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.yaml_generation`





---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_projects_from_org`

```python
get_projects_from_org(organization: str, min_stars: int = 30) → List[str]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `collect_github_projects`

```python
collect_github_projects(
    repos: List[str],
    excluded_github_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None,
    group: Optional[str] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_github_projects`

```python
extract_github_projects(
    input: Union[str, List[str]],
    excluded_github_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_pypi_projects`

```python
extract_pypi_projects(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_pypi_projects_from_requirements`

```python
extract_pypi_projects_from_requirements(
    input: Union[str, List[str]],
    excluded_pypi_ids: Optional[List[str]] = None,
    existing_projects: Optional[List[Dict]] = None
) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L406"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `auto_extend_via_libio`

```python
auto_extend_via_libio(projects: list) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/yaml_generation.py#L486"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
