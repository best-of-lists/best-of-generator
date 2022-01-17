<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.projects_collection`




**Global Variables**
---------------
- **SEMVER_VALIDATION**

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank`

```python
calc_projectrank(project_info: Dict) → int
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_projectrank_placing`

```python
calc_projectrank_placing(projects: list) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `group_projects`

```python
group_projects(projects: list) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `categorize_projects`

```python
categorize_projects(projects: list, categories: OrderedDict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_project_category`

```python
update_project_category(project_info: Dict, categories: OrderedDict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_projects_changes`

```python
get_projects_changes(
    projects: List[Dict],
    history_file_path: str
) → Tuple[List[str], Dict]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_projects_changes`

```python
apply_projects_changes(
    projects: List[Dict],
    added_projects: List[str],
    trending_projects: Dict,
    configuration: Dict
) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L361"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sort_projects`

```python
sort_projects(projects: list, configuration: Dict) → list
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L388"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_filters`

```python
apply_filters(project_info: Dict, configuration: Dict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L486"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `calc_grouped_metrics`

```python
calc_grouped_metrics(projects: list, config: Dict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/projects_collection.py#L640"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
