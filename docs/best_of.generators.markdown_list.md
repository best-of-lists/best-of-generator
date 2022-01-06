<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.generators.markdown_list`





---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_metrics_info`

```python
generate_metrics_info(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_label_info`

```python
get_label_info(label: str, labels: list) → Dict
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_labels`

```python
generate_project_labels(project: Dict, labels: list) → Tuple[str, int]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_license_info`

```python
generate_license_info(project: Dict, configuration: Dict) → Tuple[str, int]
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_body`

```python
generate_project_body(project: Dict, configuration: Dict, labels: list) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_md`

```python
generate_project_md(
    project: Dict,
    configuration: Dict,
    labels: list,
    generate_body: bool = True
) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L323"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_category_md`

```python
generate_category_md(
    category: Dict,
    config: Dict,
    labels: list,
    title_md_prefix: str = '##'
) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L373"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_changes_md`

```python
generate_changes_md(projects: list, config: Dict, labels: list) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L426"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_legend`

```python
generate_legend(
    configuration: Dict,
    labels: list,
    title_md_prefix: str = '##'
) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L475"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_md_link`

```python
process_md_link(text: str) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L480"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_toc`

```python
generate_toc(categories: OrderedDict, config: Dict) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L508"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_md`

```python
generate_md(categories: OrderedDict, config: Dict, labels: list) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L581"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MarkdownListGenerator`





---

#### <kbd>property</kbd> name







---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_list.py#L586"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_output`

```python
write_output(
    categories: OrderedDict,
    projects: List[Dict],
    config: Dict,
    labels: list
) → None
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
