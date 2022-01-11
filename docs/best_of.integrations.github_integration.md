<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.integrations.github_integration`




**Global Variables**
---------------
- **MIN_PROJECT_DESC_LENGTH**

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_repo_deps_via_github`

```python
get_repo_deps_via_github(github_id: str) → int
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_contributors_via_github_api`

```python
get_contributors_via_github_api(
    github_id: str,
    github_api_token: str
) → Union[int, NoneType]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `request_metadata_from_github_api`

```python
request_metadata_from_github_api(
    github_api_token: str,
    github_id: str,
    recent_activity_date: datetime
) → Union[Dict, NoneType]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_github_api`

```python
update_via_github_api(project_info: Dict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L485"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_via_github`

```python
update_via_github(project_info: Dict) → None
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/github_integration.py#L498"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_github_details`

```python
generate_github_details(project: Dict, configuration: Dict) → str
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
