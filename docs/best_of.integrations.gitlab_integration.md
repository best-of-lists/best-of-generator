<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/gitlab_integration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.integrations.gitlab_integration`




**Global Variables**
---------------
- **MIN_PROJECT_DESC_LENGTH**
- **query**
- **GITLAB_DEFAULT_API**


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/gitlab_integration.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GitLabIntegration`





---

#### <kbd>property</kbd> name







---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/gitlab_integration.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_md_details`

```python
generate_md_details(project: Dict, configuration: Dict) → str
```





---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/gitlab_integration.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_api_url`

```python
get_api_url(gitlab_id: str) → Tuple[str, str]
```

If `gitlab_id` is in the format "<API_ENDPOINT>::org/repo", it returns a tuple "<API_ENDPOINT>, org/repo", otherwise it returns "<GITLAB_DEFAULT_API>, org/repo". 



**Args:**
 
 - <b>`gitlab_id`</b> (str):  A string in the format "org/repo" for GitLab projects 
 - <b>`or "<API_ENDPOINT>`</b>: :org/repo" for GitLab API compatible endpoints. 



**Returns:**
 
 - <b>`tuple[str, str]`</b>:  API endpoint, org/repo 

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/gitlab_integration.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_project_info`

```python
update_project_info(project_info: Dict) → None
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
