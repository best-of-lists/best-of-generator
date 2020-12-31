<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.projects_collection`




**Global Variables**
---------------
- **SEMVER_VALIDATION**

---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank`

```python
calc_projectrank(project_info: Dict)
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank_placing`

```python
calc_projectrank_placing(projects: list) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `categorize_projects`

```python
categorize_projects(projects: list, categories: OrderedDict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_project_category`

```python
update_project_category(project_info: Dict, categories: OrderedDict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L220"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_categories`

```python
prepare_categories(input_categories: dict) → OrderedDict
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_projects_changes`

```python
get_projects_changes(
    projects: List[Dict],
    history_file_path: str
) → Tuple[List[str], Dict]
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_projects_changes`

```python
apply_projects_changes(
    projects: List[Dict],
    added_projects: List[str],
    trending_projects: Dict,
    max_trends: int = 5
) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L299"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_configuration`

```python
prepare_configuration(cfg: dict) → Dict
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L360"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sort_projects`

```python
sort_projects(projects: list, configuration: Dict) → list
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_filters`

```python
apply_filters(project_info: Dict, configuration: Dict) → None
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/projects_collection.py#L461"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
