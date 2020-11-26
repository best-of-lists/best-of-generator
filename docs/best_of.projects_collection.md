<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.projects_collection`




**Global Variables**
---------------
- **MIN_PROJECT_DESC_LENGTH**
- **DEFAULT_OTHERS_CATEGORY_ID**
- **SEMVER_VALIDATION**

---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_package_via_libio`

```python
update_package_via_libio(
    project_info: Dict,
    package_info: Dict,
    package_manager: str
) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_conda`

```python
update_via_conda(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_npm`

```python
update_via_npm(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L280"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_dockerhub`

```python
update_via_dockerhub(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L370"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_pypi`

```python
update_via_pypi(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L408"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_maven`

```python
update_via_maven(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L434"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_repo_deps_via_github`

```python
get_repo_deps_via_github(github_id: str)
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L468"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_contributors_via_github_api`

```python
get_contributors_via_github_api(
    github_id: str,
    github_api_token: str
) → Union[int, NoneType]
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L508"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_github_api`

```python
update_via_github_api(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L822"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_repo_via_libio`

```python
update_repo_via_libio(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L933"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_github`

```python
update_via_github(project_info: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L941"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank`

```python
calc_projectrank(project_info: Dict)
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1041"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank_placing`

```python
calc_projectrank_placing(projects: list) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1079"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `categorize_projects`

```python
categorize_projects(projects: list, categories: OrderedDict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_project_category`

```python
update_project_category(project_info: Dict, categories: OrderedDict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_categories`

```python
prepare_categories(input_categories: dict) → OrderedDict
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_configuration`

```python
prepare_configuration(cfg: dict) → Dict
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sort_projects`

```python
sort_projects(projects: list, configuration: Dict) → list
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_filters`

```python
apply_filters(project_info: Dict, configuration: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L1310"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `collect_projects_info`

```python
collect_projects_info(
    projects: list,
    categories: OrderedDict,
    config: Dict
) → list
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
