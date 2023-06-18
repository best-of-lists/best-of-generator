<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/base_generator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.generators.base_generator`






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/base_generator.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BaseGenerator`





---

#### <kbd>property</kbd> name

Returns the name of the generator. 



---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/base_generator.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_output`

```python
write_output(
    categories: OrderedDict,
    projects: List[Dict],
    config: Dict,
    labels: list
) → None
```

Generates the markdown output and writes into files. 



**Args:**
 
 - <b>`categories`</b> (OrderedDict):  Projects categorized into configured categories. 
 - <b>`projects`</b> (list):  List of projects. 
 - <b>`config`</b> (Dict):  Best-of configuration. 
 - <b>`labels`</b> (list):  List of available labels. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
