<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/base_integration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.integrations.base_integration`






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/base_integration.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BaseIntegration`





---

#### <kbd>property</kbd> name

Returns the name of the integration. 



---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/base_integration.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_md_details`

```python
generate_md_details(project: Dict, configuration: Dict) → str
```

Generates markdown details for the given project. 



**Args:**
 
 - <b>`project`</b> (Dict):  Collected project metadata. 
 - <b>`configuration`</b> (Dict):  Best-of configuration. 



**Returns:**
 
 - <b>`str`</b>:  Generated markdown. 

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/integrations/base_integration.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_project_info`

```python
update_project_info(project_info: Dict) → None
```

Updates the project metadata by fetching information from the package manager. 



**Args:**
 
 - <b>`project_info`</b> (Dict):  Collected project metadata. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
